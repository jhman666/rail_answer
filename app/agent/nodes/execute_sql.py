# app/agent/nodes/execute_sql.py

from app.agent.state import RailwayAgentState


def execute_sql(
    state: RailwayAgentState,
    mysql_repository,
) -> dict:
    """
    执行最终 SQL。
    """

    sql = state.get(
        "sql",
        ""
    ).strip()

    if not sql:
        return {
            "result": [],
            "error": "SQL 为空",
        }

    try:

        result = (
            mysql_repository
            .execute_query(sql)
        )

        return {
            "result": result,
            "error": "",
        }

    except Exception as e:

        return {
            "result": [],
            "error": str(e),
        }