import json

from app.agent.state import RailwayAgentState
from app.core.prompt_loader import load_prompt


def validate_sql(
    state: RailwayAgentState,
    mysql_repository,
    llm,
) -> dict:

    query = state.get("query", "")
    sql = state.get("sql", "")

    # =========================================================
    # 1. SQL 不能为空
    # =========================================================

    if not sql:
        return {
            "error": "SQL 为空，请重新生成 SQL。"
        }

    sql = sql.strip()
    normalized_sql = sql.lower()

    # =========================================================
    # 2. 只允许 SELECT / WITH
    # =========================================================

    if not (
        normalized_sql.startswith("select")
        or normalized_sql.startswith("with")
    ):
        return {
            "error": (
                "当前系统只允许 SELECT 或 WITH 查询语句，"
                "请重新生成只读查询 SQL。"
            )
        }

    # =========================================================
    # 3. 危险 SQL 检查
    # =========================================================

    dangerous_keywords = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "truncate ",
        "create ",
        "replace ",
    ]

    for keyword in dangerous_keywords:

        if keyword in normalized_sql:

            return {
                "error": (
                    f"检测到禁止的 SQL 操作："
                    f"{keyword.strip()}，"
                    "当前系统仅允许查询操作。"
                )
            }

    # =========================================================
    # 4. MySQL EXPLAIN
    #    判断 SQL 在数据库层面是否有效
    # =========================================================

    try:

        mysql_repository.execute_query(
            f"EXPLAIN {sql}"
        )

    except Exception as e:

        return {
            "error": (
                "SQL 数据库校验失败："
                f"{str(e)}"
            )
        }

    # =========================================================
    # 5. 大模型进行一次语义核验
    #
    #    判断：
    #    SQL 虽然可以执行，
    #    但是否真正回答了用户的问题
    # =========================================================

    try:

        prompt_template = load_prompt(
            "validate_sql"
        )

        prompt = prompt_template.format(
            query=query,
            sql=sql,
        )

        response = llm.invoke(
            prompt
        )

        content = response.content

        if not isinstance(content, str):
            content = str(content)

        content = content.strip()

        # -----------------------------------------------------
        # 兼容模型返回：
        #
        # ```json
        # {...}
        # ```
        # -----------------------------------------------------

        if content.startswith("```"):

            content = (
                content
                .replace("```json", "")
                .replace("```JSON", "")
                .replace("```", "")
                .strip()
            )

        # -----------------------------------------------------
        # 如果模型前后夹带少量文字，
        # 尝试截取 JSON 对象
        # -----------------------------------------------------

        start_index = content.find("{")
        end_index = content.rfind("}")

        if (
            start_index != -1
            and end_index != -1
            and end_index >= start_index
        ):
            content = content[
                start_index:end_index + 1
            ]

        review = json.loads(
            content
        )

        # -----------------------------------------------------
        # 获取审核结果
        # -----------------------------------------------------

        valid = review.get(
            "valid",
            False,
        )

        # 兼容模型偶尔返回 "true" / "false"
        if isinstance(valid, str):

            valid = (
                valid.strip().lower()
                == "true"
            )

        suggestion = review.get(
            "suggestion",
            "",
        )

        # =====================================================
        # 6. 语义核验不通过
        #
        #    直接把修改建议写进现有 error
        #
        #    这样你原来的 route_after_validate()
        #    会自动走 correct_sql
        # =====================================================

        if valid is not True:

            if not suggestion:

                suggestion = (
                    "当前 SQL 与用户问题的语义不完全一致，"
                    "请重新结合用户原始问题生成 SQL。"
                )

            return {
                "error": (
                    "SQL 语义核验未通过。"
                    f"修改建议：{suggestion}"
                )
            }

    except Exception as e:

        # =====================================================
        # 大模型审核本身失败
        #
        # 不把它当作 SQL 正确，
        # 而是交给 correct_sql 再生成一次
        # =====================================================

        return {
            "error": (
                "SQL 语义核验失败，"
                "无法确认当前 SQL 是否准确回答用户问题。"
                f"核验异常：{str(e)}"
            )
        }

    # =========================================================
    # 7. SQL 数据库校验 + 语义核验全部通过
    # =========================================================

    return {
        "error": ""
    }


def route_after_validate(
    state: RailwayAgentState,
) -> str:

    # 有任何错误：
    # 1. SQL 本身错误
    # 2. SQL 语义错误
    #
    # 都进入原来的 correct_sql

    if state.get("error"):
        return "correct_sql"

    # 没有错误直接执行

    return "execute_sql"