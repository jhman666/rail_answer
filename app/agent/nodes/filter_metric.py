# app/agent/nodes/filter_metric.py

import json

from app.agent.state import RailwayAgentState
from app.core.prompt_loader import load_prompt


def filter_metric(
    state: RailwayAgentState,
    llm,
) -> dict:
    """
    根据用户问题过滤无关指标。
    """

    query = state["query"]

    metric_infos = state.get(
        "metric_infos",
        []
    )

    # 没有召回指标
    if not metric_infos:
        return {
            "metric_infos": []
        }

    # 只有一个指标，暂时直接保留
    if len(metric_infos) == 1:
        return {
            "metric_infos": metric_infos
        }

    # =========================
    # 1. 整理指标信息
    # =========================

    candidate_metrics = []

    for metric in metric_infos:

        candidate_metrics.append(
            {
                "name": metric.name,
                "description": metric.description,
                "formula": metric.formula,
                "conditions": metric.conditions,
                "related_tables": metric.related_tables,
                "related_columns": metric.related_columns,
                "unit": metric.unit,
            }
        )

    # =========================
    # 2. 加载 Prompt
    # =========================

    prompt_template = load_prompt(
        "filter_metric"
    )

    prompt = prompt_template.format(
        query=query,
        metric_infos=json.dumps(
            candidate_metrics,
            ensure_ascii=False,
            indent=2,
        ),
    )

    # =========================
    # 3. 调用 LLM
    # =========================

    response = llm.invoke(prompt)

    content = response.content.strip()

    # =========================
    # 4. 解析结果
    # =========================

    try:
        selected_metrics = json.loads(
            content
        )

    except json.JSONDecodeError:
        # 格式错误时先不删
        return {
            "metric_infos": metric_infos
        }

    selected_metric_names = set(
        selected_metrics
    )

    # =========================
    # 5. 过滤指标
    # =========================

    filtered_metrics = [
        metric
        for metric in metric_infos
        if metric.name in selected_metric_names
    ]

    return {
        "metric_infos": filtered_metrics
    }