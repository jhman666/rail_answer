# app/agent/nodes/check_intent.py

from app.agent.state import RailwayAgentState


def check_intent(state: RailwayAgentState) -> dict:
    query = state["query"]

    write_keywords = [
        "修改",
        "改为",
        "更新",
        "删除",
        "新增",
        "添加",
        "插入",
        "清空",
        "移除",
    ]

    for keyword in write_keywords:
        if keyword in query:
            return {
                "error": "当前系统仅支持数据查询，不支持新增、修改或删除操作。",
                "is_query": False,
            }

    return {
        "error": "",
        "is_query": True,
    }


def route_after_intent(state: RailwayAgentState) -> str:
    if state.get("is_query"):
        return "extract_keywords"

    return "end"