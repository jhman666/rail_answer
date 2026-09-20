from pprint import pprint

from app.agent.graph import graph


def main():
    # 先用最简单的问题测试
    query = "查询各线路的车辆数量，并按车辆数量从高到低排序"

    print("=" * 60)
    print("用户问题：")
    print(query)
    print("=" * 60)

    try:
        result = graph.invoke({
            "query": query
        })

    except Exception as e:
        print("\nAgent 执行失败：")
        print(type(e).__name__)
        print(e)
        return

    print("\n【关键词】")
    pprint(
        result.get("keywords")
    )

    print("\n【字段召回】")
    pprint(
        result.get("retrieved_columns")
    )

    print("\n【指标召回】")
    pprint(
        result.get("retrieved_metrics")
    )

    print("\n【字段值召回】")
    pprint(
        result.get("retrieved_values")
    )

    print("\n【表信息】")
    pprint(
        result.get("table_infos")
    )

    print("\n【过滤后的字段】")
    pprint(
        result.get("column_infos")
    )

    print("\n【过滤后的指标】")
    pprint(
        result.get("metric_infos")
    )

    print("\n【额外上下文】")
    pprint(
        result.get("extra_context")
    )

    print("\n【最终 SQL】")
    print(
        result.get("sql")
    )

    print("\n【SQL 错误】")
    print(
        result.get("error")
    )

    print("\n【查询结果】")
    pprint(
        result.get("result")
    )


if __name__ == "__main__":
    main()