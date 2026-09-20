from pathlib import Path

import yaml
from pydantic import BaseModel, Field


# ============================================================
# Table Metadata
# ============================================================

class TableMetadata(BaseModel):
    name: str

    description: str

    business_domain: str | None = None

    primary_key: str | None = None

    active: bool = True


# ============================================================
# Column Metadata
# ============================================================

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


# ============================================================
# Metric Metadata
# ============================================================

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


# ============================================================
# metadata.yaml 总结构
# ============================================================

class MetadataConfig(BaseModel):

    tables: dict[
        str,
        TableMetadata
    ] = Field(
        default_factory=dict
    )

    columns: dict[
        str,
        ColumnMetadata
    ] = Field(
        default_factory=dict
    )

    metrics: dict[
        str,
        MetricMetadata
    ] = Field(
        default_factory=dict
    )


# ============================================================
# 加载 metadata.yaml
# ============================================================

def load_metadata(
    path: str | Path
) -> MetadataConfig:

    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8"
    ) as f:
        raw_data = yaml.safe_load(f)

    return MetadataConfig.model_validate(
        raw_data
    )