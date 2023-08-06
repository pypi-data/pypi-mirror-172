import re
from functools import lru_cache
from hashlib import md5
from operator import itemgetter
from typing import Any, Callable, Dict, List, Sequence, Union, get_type_hints
from uuid import uuid4

import sqlalchemy as sa
from cytoolz.itertoolz import groupby
from pydantic import BaseSettings, PostgresDsn
from ready_logger import get_logger
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .types import DataIDIgnore

logger = get_logger("db-loader")


class PgURL(BaseSettings):
    url: PostgresDsn

    class Config:
        env_prefix = "postgres_async_"


@lru_cache(maxsize=None)
def engine_from_env() -> AsyncEngine:
    """Create an async SQLAlchemy engine and cache it so we only create it once.

    Returns:
        AsyncEngine: The SQLAlchemy engine.
    """
    return create_async_engine(PgURL().url)


def to_table(table: Union[sa.Table, DeclarativeMeta]) -> sa.Table:
    """Extract the SQLAlchemy table from an entity, or return the passed argument if argument is already a table.

    Args:
        table (Union[sa.Table, DeclarativeMeta]): An entity or table object.

    Raises:
        ValueError: If argument is not an entity or table object.

    Returns:
        sa.Table: The table corresponding to the passed argument.
    """
    if isinstance(table, sa.Table):
        return table
    elif hasattr(table, "__table__"):
        return table.__table__
    raise ValueError(
        f"Object {table} is not an entity or table! Can not extract table."
    )


def get_typed_columns(
    of_type: Any, table: Union[sa.Table, DeclarativeMeta]
) -> List[str]:
    """Find columns that are tagged as being of type `of_type` via querying type annotations and comments.

    Args:
        of_type (Any): The type who's type annotation should be searched for.
        table (Union[sa.Table, DeclarativeMeta]): The table or entity to query.

    Returns:
        List[str]: Names of columns that are of type `of_type`.
    """
    table = to_table(table)

    # extract type labels from column comments.
    type_columns = {
        col_name
        for col_name, col in table.columns.items()
        if col.comment == of_type.__name__
    }
    if not isinstance(table, sa.Table):
        # extract type labels from column type annotations.
        type_columns.update(
            {
                col_name
                for col_name, hint in get_type_hints(table).items()
                if hint is of_type
            }
        )
    return list(type_columns)


def to_safe_snake_case(name: str) -> str:
    """Convert `name` to snake case and also add a leading underscore to variables starting with a digit.

    Args:
        name (str): The name to convert.

    Returns:
        str: The converted name.
    """
    # remove trailing space.
    name = name.strip()
    # convert space to underscores.
    name = re.sub(r"\s+", "_", name)
    # convert camel case to underscores.
    if not name.isupper():
        name = re.sub(
            r"([a-z0-8])([A-Z])", lambda m: f"{m.group(1)}_{m.group(2)}", name
        )
    # variable names can't start with number, so add leading underscore.
    if re.match(r"^\d", name):
        name = f"_{name}"
    # make name lowercase.
    return name.lower()


def groupby_columns(rows: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    """Group rows by column names present.
    We can not have rows with different columns in the same statement.

    Args:
        rows (List[Dict[str,Any]]): The rows to group.

    Returns:
        List[List[Dict[str, Any]]]: The grouped rows.
    """
    return groupby(lambda r: tuple(r.keys()), rows).values()


def column_type_casts(
    table: Union[sa.Table, DeclarativeMeta],
    type_casts: Union[Dict[str, Any], Sequence[Any]] = (int, float, str),
) -> Dict[str, Any]:
    """Find functions to cast column values to the appropriate Python type.
    This is needed before inserting data into the database.

    Args:
        table (Union[sa.Table, DeclarativeMeta]): Table or entity that needs type casting.
        type_casts (Sequence[Any]): Types that we are interested in casted.

    Returns:
        Dict[str, Any]: Map column name to cast function.
    """
    table = to_table(table)
    column_casts = {}
    for column in table.columns:
        if (
            col_t := getattr(column.type, "python_type", type(column.type))
        ) in type_casts:
            column_casts[column.name] = (
                type_casts[col_t] if isinstance(type_casts, dict) else col_t
            )
    return column_casts


def create_column_name_filter(
    field_to_column, column_names_converter, column_name_converters
) -> Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]:
    """Filter columns and convert to match database column names.

    Args:
        field_to_column (Optional[Dict[str, str]], optional): Map column name to desired column name. Defaults to None.
        column_names_converter (Callable, optional): A formatting function to apply to every name. Defaults to None.
        column_name_converters (Optional[Dict[str, Callable]], optional): Map column name to formatting function. Defaults to None.

    Returns:
        Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]: The filter function.
    """

    converters = []
    if column_names_converter:
        converters.append(column_names_converter)
    if column_name_converters:
        converters.append(
            lambda name: column_name_converters[name](name)
            if name in column_name_converters
            else name
        )
    if field_to_column:
        converters.append(lambda name: field_to_column.get(name, name))
    if not converters:
        return

    converted_column_names: Dict[str, str] = {}

    def _convert_name(name: str) -> str:
        """Convert `name` to a table column name.

        Args:
            name (str): The Name that should be converted.

        Returns:
            str: The converted name.
        """
        orig_name = name
        for func in converters:
            name = func(name)
        converted_column_names[orig_name] = name
        return name

    def _filter_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter unwanted columns from `row` and convert names to database column names.

        Args:
            row (Dict[str, Any]): The row to be filtered.

        Returns:
            Dict[str, Any]: The filtered row.
        """
        rows = [
            {
                converted_column_names.get(c) or _convert_name(c): v
                for c, v in row.items()
            }
            for row in rows
        ]
        return rows

    return _filter_rows


def create_row_id_generator(
    table: Union[sa.Table, DeclarativeMeta],
    row_id_column: str,
) -> Callable[[Dict[str, Any]], str]:
    """Generate an ID based on a hash of `row`'s data.

    Args:
        row (Dict[str, Any]): row with data that we should generate an ID for.

    Returns:
        str: The row's ID.
    """
    table = to_table(table)
    _non_id_columns = {
        *get_typed_columns(DataIDIgnore, table),
        row_id_column,
    }
    _data_id_columns = [c.name for c in table.columns if c.name not in _non_id_columns]
    if not len(_data_id_columns):
        raise ValueError(
            f"{table} does not have any ID columns. Can not create data ID generator."
        )

    def _create_row_data_id(row: Dict[str, Any]) -> str:
        data_id_members = {k: v for k, v in row.items() if k in _data_id_columns}
        if not len(data_id_members):
            _id = str(uuid4())
            logger.warning(
                "Row does not contain any fields that can be used to generate a data ID. Random ID '%s' will be used. (Data ID columns: %s. Row: %s)",
                _id,
                _data_id_columns,
                row,
            )
            return _id
        # sort values by key so key ordering will not effect generated hash.
        data_id_members = [
            str(v).strip()
            for _, v in sorted(data_id_members.items(), key=itemgetter(0))
        ]
        return md5("".join(data_id_members).encode()).hexdigest()

    return _create_row_data_id
