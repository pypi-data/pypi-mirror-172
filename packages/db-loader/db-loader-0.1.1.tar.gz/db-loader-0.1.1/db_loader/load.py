from collections import defaultdict, deque
from datetime import datetime
from functools import lru_cache
from typing import Any, Callable, Dict, List, Optional, Union

import sqlalchemy as sa
from cytoolz.itertoolz import partition_all

# from sqlalchemy.dialects.postgresql import insert as pg_insert
# from sqlalchemy.dialects.sqlite import insert as sq_insert
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql.dml import Insert
from sqlalchemy.exc import CompileError, IntegrityError
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .create import async_create_table
from .utils import (
    create_column_name_filter,
    create_row_id_generator,
    engine_from_env,
    get_logger,
    groupby_columns,
    to_table,
)


class DbLoader:
    def __init__(
        self,
        table: Union[sa.Table, DeclarativeMeta],
        on_duplicate_key_update: Optional[Union[bool, List[str]]] = True,
        row_batch_size: int = 1500,
        remove_duplicate_keys: bool = True,
        drop_rows_missing_key: bool = True,
        group_by_columns_present: bool = True,
        drop_columns: Optional[List[str]] = None,
        field_to_column: Optional[Dict[str, str]] = None,
        column_names_converter: Callable[[str], str] = None,
        column_name_converters: Optional[Dict[str, Callable[[str], str]]] = None,
        value_to_value: Optional[Dict[Any, Any]] = None,
        column_to_value: Optional[Dict[str, Any]] = None,
        value_converter: Optional[Callable[[Any], Any]] = None,
        column_value_converters: Optional[Dict[str, Callable[[Any], Any]]] = None,
        drop_values: Optional[List[str]] = None,
        column_drop_values: Optional[Dict[str, List[str]]] = None,
        drop_on_type_conversion_fail: bool = True,
        engine: Optional[AsyncEngine] = None,
    ) -> None:
        """Load data rows to a postgresql database.
        Name converters are the first thing applied,
        so arguments mapping from name should use the name in converted form.

        Args:
            table (Union[sa.Table, DeclarativeMeta]): The SQLAlchemy table or entity corresponding to the database table that rows will be loaded to.
            remove_duplicate_keys (bool, optional): Remove duplicates from upsert batches. Defaults to True.
            group_by_columns_present (bool, optional): Group rows by columns present and execute upsert statement for each group. Defaults to True.
            on_duplicate_key_update (Union[bool, List[str]], optional): List of columns that should be updated when primary key exists, or True for all columns, False for no columns, None if duplicates should not be checked (i.e. a normal INSERT). Defaults to True.
            engine (Optional[AsyncEngine], optional): The engine to use to execute sql statements. Defaults to None.
            row_batch_size (int): The maximum number of rows to upsert at once.
            field_to_column (Optional[Dict[str, str]], optional): Map column name to desired column name. Defaults to None.
            column_names_converter (Callable, optional): A formatting function to apply to every name. Defaults to None.
            column_name_converters (Optional[Dict[str, Callable]], optional): Map column name to formatting function. Defaults to None.
            drop_columns (Optional[List[str]], optional): Names of columns that should be filtered from rows. Defaults to None.
            value_to_value (Optional[Dict[Any, Any]], optional): Map value to desired value. Defaults to None.
            column_to_value: (Optional[Dict[str, Any]], optional): Map column name to desired column value. Defaults to None.
            value_converter (Optional[Callable], optional): A conversion function to apply to every value. Defaults to None.
            column_value_converters (Optional[Dict[str, Callable]], optional): Map column name to column value conversion function. Defaults to None.
            drop_values (Optional[List[str]], optional): Values where columns should be dropped if they are that value. (e.g ['null', None, 'Na']). Defaults to None.
            drop_on_type_conversion_fail (bool, optional): Remove column from row if conversion fails. Defaults to False.
            kwargs: keyword arguments for initializing ColumnNameFilter and ColumnValueFilter.
        """
        self.table = to_table(table)
        self._engine = engine or engine_from_env()
        self._row_batch_size = row_batch_size
        self._on_duplicate_key_update = on_duplicate_key_update
        self._logger = get_logger(f"{self.table.name}-loader")
        self._load_sources = False
        self._row_buffer = []
        # If doing non-deterministic column dropping, we need to group by columns present.
        self._group_by_columns_present = group_by_columns_present or any(
            (drop_values, column_drop_values, drop_on_type_conversion_fail)
        )
        self._primary_key_column_names = {
            c.name for c in self.table.primary_key.columns
        }
        if not self._primary_key_column_names:
            # not applicable because there are no keys.
            drop_rows_missing_key = False
            self._on_duplicate_key_update = None
            remove_duplicate_keys = False

        # determine what should be updated when there is an existing primary key.
        if self._on_duplicate_key_update == True:
            # update all columns that aren't primary key.
            self._on_duplicate_key_update = [
                col_name
                for col_name, col in self.table.columns.items()
                if not col.primary_key
            ]
        if self._on_duplicate_key_update:
            self._build_statement = self._upsert_update_statement
        elif self._on_duplicate_key_update == False:
            self._build_statement = self._upsert_ignore_statement
        elif self._on_duplicate_key_update is None:
            self._build_statement = self._insert_statement
        else:
            raise ValueError(
                f"Invalid argument for on_duplicate_key_update: {self._on_duplicate_key_update}"
            )

        self._filters = {}
        # do column name filtering first, so other functions will use the filtered names.
        if column_name_filter := create_column_name_filter(
            field_to_column, column_names_converter, column_name_converters
        ):
            self._filters["column-name-filter"] = column_name_filter

        drop_columns = drop_columns or []
        column_names_to_load = {
            str(c) for c in self.table.columns.keys() if c not in drop_columns
        }
        self._filters["remove-unwanted-columns"] = lambda rows: [
            {c: row[c] for c in column_names_to_load if c in row} for row in rows
        ]
        if drop_rows_missing_key:
            self._filters["drop-rows-missing-key"] = lambda rows: [
                row
                for row in rows
                if all(c in row for c in self._primary_key_column_names)
            ]

        if remove_duplicate_keys:
            self._filters["remove-duplicate-keys"] = self._remove_duplicate_keys

        if value_to_value:
            self._filters["map-value-to-value"] = lambda rows: [
                {k: value_to_value.get(v, v) for k, v in row.items()} for row in rows
            ]
        if drop_values:
            if not isinstance(drop_values, (list, tuple, set)):
                drop_values = [drop_values]
            self._filters["drop-values"] = lambda rows: [
                {k: v for k, v in row.items() if v not in drop_values} for row in rows
            ]
        if column_drop_values:
            self._filters["drop-column-values"] = lambda rows: [
                {k: v for k, v in row.items() if column_drop_values.get(k) != v}
                for row in rows
            ]
        if column_to_value:
            self._filters["set-column-value"] = lambda rows: [
                {k: column_to_value.get(k, v) for k, v in row.items()} for row in rows
            ]

        col_val_cvts = defaultdict(list)
        if value_converter:
            for c in column_names_to_load:
                col_val_cvts[c].append(value_converter)
        if column_value_converters:
            for k, v in column_value_converters.items():
                col_val_cvts[k].append(v)
        if col_val_cvts:

            def convert_column_values(rows):
                converted_rows = []
                for row in rows:
                    to_remove = set()
                    for col, val_cvts in col_val_cvts.items():
                        if col in row:
                            for vc in val_cvts:
                                try:
                                    row[col] = vc(row[col])
                                except Exception as e:
                                    msg = f"Error converting column '{col}' value {row[col]}: {e}"
                                    if drop_on_type_conversion_fail:
                                        self._logger.error(msg)
                                        to_remove.add(col)
                                    else:
                                        raise type(e)(msg)
                    for col in to_remove:
                        del row[col]
                    converted_rows.append(row)
                return converted_rows

            self._filters["convert_column_values"] = convert_column_values

        self._logger.info(
            f"{len(self._filters)} filters will be applied before loading rows: {list(self._filters.keys())}"
        )

    @classmethod
    async def create(cls, *args, **kwargs):
        """Initialize and create table if it does not already exist."""
        self = cls(*args, **kwargs)
        # create table if it doesn't already exist.
        async with self._engine.begin() as conn:
            await async_create_table(conn, self.table)
        return self

    @classmethod
    async def source_loader(
        cls,
        source: str,
        row_id_column: str = "data_id",
        generate_row_id: bool = True,
        *args,
        **kwargs,
    ):
        """Upsert rows to a table and also upsert source metadata to the corresponding sources table.

        Args:
            source (str): Where the data is from.
            row_id_column (str): The column that should be used to join to the data table to the sources table.
            generate_row_id (bool): Assign a data-generated ID to `row_id_column` for each row.
            kwargs: If `db_loader` argument is not provided, DbLoader kwargs may be provided and a new `DbLoader` will be initialized.

        Raises:
            RuntimeError: If the loader's table does not contain column `row_id_column`.
        """
        self = await cls.create(*args, **kwargs)
        self.source = source
        self.row_id_column = row_id_column
        self._load_sources = True
        self._generate_row_id = generate_row_id
        if self.row_id_column not in self.table.columns:
            raise RuntimeError(
                f"Table {self.table.name} must contain column `{self.row_id_column}` to be linked to a sources table."
            )
        self._row_id_generator = (
            create_row_id_generator(self.table, self.row_id_column)
            if generate_row_id
            else None
        )
        self._sources_table = self.get_sources_table(self.table, self.row_id_column)
        async with self._engine.begin() as conn:
            await conn.run_sync(self._sources_table.create, checkfirst=True)
        return self

    async def add(self, row: Dict[str, Any]):
        self._row_buffer.append(row)
        if len(self._row_buffer) >= self._row_batch_size:
            await self.load()

    async def extend(self, rows: List[Dict[str, Any]]):
        self._row_buffer.extend(rows)
        if len(self._row_buffer) >= self._row_batch_size:
            await self.load()

    async def load(self, rows: Optional[List[Dict[str, Any]]] = None):
        """Load rows to the database.

        Args:
            rows (Optional[List[Dict[str, Any]]]): Rows to that should be loaded in addition to all rows that were added with `add` and `extend`.
        """
        if rows:
            self._row_buffer.extend(rows)
        # take all rows in the buffer.
        if not (rows := self._row_buffer):
            return []
        # start a new buffer.
        self._row_buffer = []

        if self._load_sources and self._generate_row_id:
            for row in rows:
                row[self.row_id_column] = self._row_id_generator(row)

        if not (rows := self.filter_rows(rows)):
            return []

        row_groups = groupby_columns(rows) if self._group_by_columns_present else [rows]
        batches = deque()
        # split rows into smaller batches if there are too many to insert at once.
        for rows in row_groups:
            for batch in partition_all(self._row_batch_size, rows):
                batches.append(batch)
        # upsert all batches.
        self._logger.info(
            f"Loading {len(rows)} rows ({len(batches)} batches) to the database."
        )
        async with self._engine.begin() as conn:
            while len(batches):
                rows = batches.popleft()
                self._logger.info(f"Loading {len(rows)} rows to {self.table}")
                try:
                    await conn.execute(self._build_statement(rows))
                    if self._load_sources:
                        await conn.execute(self._upsert_sources_statement(rows))
                except IntegrityError as ie:
                    if (
                        not self._remove_duplicate_keys
                        and "duplicate key value violates unique constraint"
                        in ie._message()
                    ):
                        batches.append(self._remove_duplicate_keys(rows))
                    else:
                        raise ie

                except CompileError as ce:
                    if (
                        not self._group_by_columns_present
                        and "is explicitly rendered as a boundparameter in the VALUES clause"
                        in ce._message()
                    ):
                        for rows in groupby_columns(rows):
                            batches.append(rows)
                    else:
                        raise ce

    def filter_rows(
        self, rows: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """Apply all filter functions to rows.

        Args:
            rows (Optional[List[Dict[str, Any]]], optional): The rows to filter in addition to rows buffered with `add` and `extend`. Defaults to None.

        Returns:
            List[Dict[str, Any]]: The filtered rows.
        """
        rows = rows + self._row_buffer if rows else self._row_buffer
        for filter_name, filter_func in self._filters.items():
            if not (rows := filter_func(rows)):
                self._logger.warning(
                    f"No rows remain after applying filter function: {filter_name}"
                )
                return
        return rows

    def _remove_duplicate_keys(
        self, rows: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Remove rows that repeat a primary key.
        Multiple row in the same upsert statement can not have the same primary key.

        Args:
            rows (List[Dict[str, Any]]): Data row, possibly containing duplicates.

        Returns:
            List[Dict[str, Any]]: Duplicate-free data rows.
        """
        unique_key_rows = {
            tuple([row[c] for c in self._primary_key_column_names]): row for row in rows
        }
        unique_key_rows = list(unique_key_rows.values())
        if (unique_count := len(unique_key_rows)) < (row_count := len(rows)):
            self._logger.warning(
                f"{row_count - unique_count}/{row_count} rows had a duplicate primary key and will not be loaded."
            )
        return unique_key_rows

    def _insert_statement(self, rows: List[Dict[str, Any]]) -> Insert:
        """Construct a statement to insert `rows`.

        Args:
            rows (List[Dict[str,Any]]): The rows that will be loaded.

        Returns:
            Insert: An insert statement.
        """
        return postgresql.insert(self.table).values(rows)

    def _upsert_update_statement(self, rows: List[Dict[str, Any]]) -> Insert:
        """Construct a statement to load `rows`.

        Args:
            rows (List[Dict[str,Any]]): The rows that will be loaded.

        Returns:
            Insert: An upsert statement.
        """

        # check column of first row (all rows should have same columns)
        on_duplicate_key_update = [
            c for c in self._on_duplicate_key_update if c in rows[0]
        ]
        if len(on_duplicate_key_update):
            statement = postgresql.insert(self.table).values(rows)
            return statement.on_conflict_do_update(
                index_elements=self._primary_key_column_names,
                set_={k: statement.excluded[k] for k in on_duplicate_key_update},
            )
        return self._build_upsert_ignore_statement(rows)

    def _upsert_ignore_statement(self, rows: List[Dict[str, Any]]) -> Insert:
        """Construct a statement to load `rows`.

        Args:
            rows (List[Dict[str,Any]]): The rows that will be loaded.

        Returns:
            Insert: An upsert statement.
        """
        return (
            postgresql.insert(self.table)
            .values(rows)
            .on_conflict_do_nothing(index_elements=self._primary_key_column_names)
        )

    def _upsert_sources_statement(self, rows: List[Dict[str, Any]]) -> Insert:
        """Construct an upsert statement to load source metadata for each row.

        Args:
            rows (List[Dict[str,Any]]): The rows to load source metadata for.

        Returns:
            Insert: An upsert statement.
        """
        statement = (
            postgresql.insert(self._sources_table)
            .values(
                [
                    {self.row_id_column: row[self.row_id_column], "source": self.source}
                    for row in rows
                ]
            )
            .on_conflict_do_update(
                index_elements=[self.row_id_column, "source"],
                set_={
                    "last_seen": datetime.utcnow(),
                    "times_seen": sa.text(
                        f'{self._sources_table.schema}."{self._sources_table.name}".times_seen + 1'
                    ),
                },
            )
        )
        return statement

    @staticmethod
    @lru_cache(maxsize=None)
    def get_sources_table(
        table: Union[sa.Table, DeclarativeMeta], row_id_column: str
    ) -> sa.Table:
        """Create a table to contain all sources of unique rows in a table.

        Args:
            table (Union[DbLoader, sa.Table, DeclarativeMeta]): The entity to make the sources table for.

        Returns:
            sa.Table: The sources table.
        """
        table = to_table(table)
        sources_table = sa.Table(
            f"{table.name}_sources",
            sa.MetaData(schema=table.schema),
            sa.Column(
                row_id_column,
                sa.VARCHAR,
                sa.ForeignKey(getattr(table.c, row_id_column), ondelete="CASCADE"),
                primary_key=True,
            ),
            sa.Column("source", sa.VARCHAR, primary_key=True),
            sa.Column(
                "created",
                sa.DateTime(timezone=False),
                default=datetime.utcnow,
                nullable=False,
            ),
            sa.Column(
                "last_seen",
                sa.DateTime(timezone=False),
                default=datetime.utcnow,
                nullable=False,
            ),
            sa.Column("times_seen", sa.Integer, default=1, nullable=False),
        )
        return sources_table
