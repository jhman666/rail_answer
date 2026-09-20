from typing import TypedDict


class RailwayAgentState(TypedDict, total=False):

    # 用户输入
    query: str

    # 关键词
    keywords: list[str]

    # 三路原始召回结果
    retrieved_columns: list
    retrieved_metrics: list
    retrieved_values: list

    # merge 之后
    table_infos: list
    column_infos: list
    metric_infos: list
    value_infos: list

    # 额外上下文
    extra_context: dict

    # SQL
    sql: str
    error: str

    is_query: bool
    # 查询结果
    result: list