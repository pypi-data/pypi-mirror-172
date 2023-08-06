from typing import Any, Optional, TypeAlias, Union

from pydantic import Field

from mui.v5.grid.base import GridBaseModel

ColumnField: TypeAlias = str
Id: TypeAlias = Optional[Union[int, str]]
OperatorValue: TypeAlias = Optional[str]
Value: TypeAlias = Optional[Any]


class GridFilterItem(GridBaseModel):
    """A grid filter item.

    Documentation:
        https://mui.com/x/api/data-grid/grid-filter-item/

    Attributes:
        column_field (str): The column from which we want to filter the rows.
            - Alias: columnField
        id (str | int | not set): Must be unique. Only useful when the model contains
            several items.
        operator_value (str | None | not set): The name of the operator we want to
            apply. Will become required on @mui/x-data-grid@6.X.
            - Alias: operatorValue
        value: (Any | None | not set): The filtering value.
            The operator filtering function will decide for each row if the row values
            is correct compared to this value.
    """

    column_field: ColumnField = Field(
        default=...,
        title="Column Field",
        description="The column from which we want to filter the rows.",
        alias="columnField",
    )
    id: Id = Field(
        default=None,
        title="Identifier",
        description="A unique identifier if a model contains several items",
    )
    operator_value: OperatorValue = Field(
        default=None,
        title="Operator Value",
        description="The name of the operator we want to apply.",
        alias="operatorValue",
    )
    value: Value = Field(default=None, title="Value", description="The filtering value")

    _optional_keys = {
        # be careful, this is a tuple because of the trailing comma
        ("id",),
        ("operatorValue", "operator_value"),
        # be careful, this is a tuple because of the trailing comma
        ("value",),
    }
