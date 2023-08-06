from datetime import datetime
from typing import Any, Dict, TypeVar

import numpy as np
import sqlalchemy as sa

# To be used as a type annotation on columns that should be used to create a hypertable partition.
HypertablePartition = TypeVar("HypertablePartition")

# To be used as a type annotation on the columns that should not be used in the generation of row data IDs.
DataIDIgnore = TypeVar("DataIDIgnore")


type_value_generators = {
    int: np.int64,
    float: np.float64,
    str: np.unicode_,
    bool: np.bool_,
    datetime: "datetime64[s]",
}


def table_np_types(table: sa.Table) -> Dict[str, Any]:
    col_np_types = {}
    for column in table.columns:
        col_t = getattr(column.type, "python_type", type(column.type))
        if col_t not in type_value_generators:
            raise RuntimeError(f"Unknown sqlalchemy type: {column.type}")
        col_np_types[column.name] = type_value_generators[col_t]
    return col_np_types
