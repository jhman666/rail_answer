from app.agent.state import RailwayAgentState


def merge_retrieved_info(
    state: RailwayAgentState,
    qdrant_repository,
) -> dict:

    retrieved_columns = state.get(
        "retrieved_columns",
        []
    )

    retrieved_metrics = state.get(
        "retrieved_metrics",
        []
    )

    retrieved_values = state.get(
        "retrieved_values",
        []
    )

    # =========================
    # 1. 找涉及的表
    # =========================

    table_names = set()

    # 字段
    for column in retrieved_columns:
        table_names.add(
            column.table_name
        )

    # 指标
    for metric in retrieved_metrics:
        for table_name in metric.related_tables:
            table_names.add(table_name)

    # ES 取值
    for value in retrieved_values:
        table_names.add(
            value.table_name
        )

    # =========================
    # 2. 搜表信息
    # =========================

    table_infos = []

    for table_name in table_names:

        tables = qdrant_repository.search_tables(
            query=table_name,
            limit=1,
        )

        if not tables:
            continue

        table_infos.append(
            {
                "table_name": table_name,
                "table": tables[0],
            }
        )

    # =========================
    # 3. 返回
    # =========================

    return {
        "table_infos": table_infos,
        "column_infos": retrieved_columns,
        "metric_infos": retrieved_metrics,
        "value_infos": retrieved_values,
    }