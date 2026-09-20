# app/agent/nodes/generate_sql.py

import json

from app.agent.state import RailwayAgentState
from app.core.prompt_loader import load_prompt


def generate_sql(
    state: RailwayAgentState,
    llm,
) -> dict:
    """
    根据前面整理好的上下文生成 SQL。
    """

    query = state["query"]

    table_infos = state.get(
        "table_infos",
        []
    )

    column_infos = state.get(
        "column_infos",
        []
    )

    metric_infos = state.get(
        "metric_infos",
        []
    )

    value_infos = state.get(
        "value_infos",
        []
    )

    extra_context = state.get(
        "extra_context",
        {}
    )

    # =========================
    # 1. 整理表信息
    # =========================

    tables = []

    for item in table_infos:

        table = item["table"]

        tables.append(
            {
                "table_name": item["table_name"],
                "name": table.name,
                "description": table.description,
                "business_domain": table.business_domain,
                "primary_key": table.primary_key,
            }
        )

    # =========================
    # 2. 整理字段
    # =========================

    columns = [
        column.model_dump()
        for column in column_infos
    ]

    # =========================
    # 3. 整理指标
    # =========================

    metrics = [
        metric.model_dump()
        for metric in metric_infos
    ]

    values = [
        value.model_dump()
        for value in value_infos
    ]

    # =========================
    # 4. 加载 Prompt
    # =========================

    prompt_template = load_prompt(
        "generate_sql"
    )

    prompt = prompt_template.format(
        query=query,

        table_infos=json.dumps(
            tables,
            ensure_ascii=False,
            indent=2,
        ),

        column_infos=json.dumps(
            columns,
            ensure_ascii=False,
            indent=2,
        ),

        metric_infos=json.dumps(
            metrics,
            ensure_ascii=False,
            indent=2,
        ),

        value_infos=json.dumps(
            values,
            ensure_ascii=False,
            indent=2,
        ),

        extra_context=json.dumps(
            extra_context,
            ensure_ascii=False,
            indent=2,
        ),
    )

    # =========================
    # 5. 调用 LLM
    # =========================

    response = llm.invoke(prompt)

    sql = response.content.strip()

    # 防止模型还是返回 markdown
    sql = sql.replace(
        "```sql",
        ""
    ).replace(
        "```SQL",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    return {
        "sql": sql
    }