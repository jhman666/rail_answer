# app/agent/nodes/recall_value.py

from app.agent.state import RailwayAgentState
from app.models.es.dimension_value import DimensionValue


def recall_value(
    state: RailwayAgentState,
    es_repository,
) -> dict:
    """
    根据关键词从 Elasticsearch 中召回字段真实取值。
    """

    keywords = state["keywords"]

    retrieved_values: dict[str, DimensionValue] = {}

    for keyword in keywords:
        values = es_repository.search_values(
            keyword=keyword
        )

        for value in values:
            # 用 表名 + 字段名 + 字段值 作为唯一标识
            key = (
                f"{value.table_name}."
                f"{value.column_name}."
                f"{value.value}"
            )

            retrieved_values[key] = value

    return {
        "retrieved_values": list(
            retrieved_values.values()
        )
    }