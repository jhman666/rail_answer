# app/agent/nodes/add_extra_context.py

from datetime import datetime

from app.agent.state import RailwayAgentState


def add_extra_context(
    state: RailwayAgentState,
) -> dict:
    """
    为 SQL 生成补充额外上下文信息。
    """

    now = datetime.now()

    extra_context = {
        "current_date": now.strftime("%Y-%m-%d"),
        "current_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "database_type": "MySQL",
    }

    return {
        "extra_context": extra_context
    }