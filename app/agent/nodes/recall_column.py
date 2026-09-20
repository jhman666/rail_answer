# app/agent/nodes/recall_column.py

from app.agent.state import RailwayAgentState


def recall_column(
    state: RailwayAgentState,
    qdrant_repository,
) -> dict:
    """
    根据关键词召回相关字段。
    """

    keywords = state["keywords"]

    retrieved_columns = {}

    for keyword in keywords:
        columns = qdrant_repository.search_columns(
            query=keyword
        )

        for column in columns:
            key = f"{column.table_name}.{column.column_name}"

            retrieved_columns[key] = column

    return {
        "retrieved_columns": list(
            retrieved_columns.values()
        )
    }