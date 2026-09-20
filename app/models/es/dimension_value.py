from pydantic import BaseModel


class DimensionValue(BaseModel):
    """
    Elasticsearch 字段取值模型
    """

    table_name: str
    column_name: str
    value: str
    active: bool = True