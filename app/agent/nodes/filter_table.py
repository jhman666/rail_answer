import json

from app.agent.state import RailwayAgentState
from app.core.prompt_loader import load_prompt


def filter_table(
    state: RailwayAgentState,
    llm,
) -> dict:

    query = state["query"]

    table_infos = state.get(
        "table_infos",
        []
    )

    column_infos = state.get(
        "column_infos",
        []
    )

    # =========================
    # 没有候选表
    # =========================

    if not table_infos:
        return {
            "table_infos": [],
            "column_infos": [],
        }

    # =========================
    # 只有一张表
    # 直接保留该表，并过滤字段
    # =========================

    if len(table_infos) == 1:

        table_name = table_infos[0]["table_name"]

        filtered_columns = [
            column
            for column in column_infos
            if column.table_name == table_name
        ]

        return {
            "table_infos": table_infos,
            "column_infos": filtered_columns,
        }

    # =========================
    # 整理候选表信息
    # =========================

    candidate_tables = []

    for item in table_infos:

        table_name = item["table_name"]
        table = item["table"]

        candidate_tables.append(
            {
                "table_name": table_name,
                "name": table.name,
                "description": table.description,
                "business_domain": table.business_domain,
                "primary_key": table.primary_key,
            }
        )

    # =========================
    # 加载 Prompt
    # =========================

    prompt_template = load_prompt(
        "filter_table"
    )

    prompt = prompt_template.format(
        query=query,
        table_infos=json.dumps(
            candidate_tables,
            ensure_ascii=False,
            indent=2,
        ),
    )

    # =========================
    # 调用 LLM
    # =========================

    response = llm.invoke(prompt)

    content = response.content.strip()

    # =========================
    # 解析结果
    # =========================

    try:
        selected_tables = json.loads(
            content
        )

    except json.JSONDecodeError:

        # LLM 格式异常，不过滤
        return {
            "table_infos": table_infos,
            "column_infos": column_infos,
        }

    selected_table_names = set(
        selected_tables
    )

    # =========================
    # 过滤表
    # =========================

    filtered_tables = [
        item
        for item in table_infos
        if item["table_name"]
        in selected_table_names
    ]

    # 防止 LLM 把所有表误删
    if not filtered_tables:
        return {
            "table_infos": table_infos,
            "column_infos": column_infos,
        }

    # =========================
    # 根据最终表过滤字段
    # =========================

    final_table_names = {
        item["table_name"]
        for item in filtered_tables
    }

    filtered_columns = [
        column
        for column in column_infos
        if column.table_name
        in final_table_names
    ]

    return {
        "table_infos": filtered_tables,
        "column_infos": filtered_columns,
    }