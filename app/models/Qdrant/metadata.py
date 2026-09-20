from pydantic import BaseModel, Field


class TableMetadata(BaseModel):
    name: str
    description: str
    business_domain: str | None = None
    primary_key: str | None = None
    active: bool = True


class ColumnMetadata(BaseModel):
    table_name: str
    column_name: str
    name: str
    type: str
    description: str

    primary_key: bool = False
    foreign_key: bool = False

    references_table: str | None = None
    references_column: str | None = None

    active: bool = True


class MetricMetadata(BaseModel):
    name: str
    description: str
    formula: str

    conditions: list[str] = Field(
        default_factory=list
    )

    related_tables: list[str] = Field(
        default_factory=list
    )

    related_columns: list[str] = Field(
        default_factory=list
    )

    unit: str | None = None

    active: bool = True