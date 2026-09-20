from app.agent.state import RailwayAgentState
from app.core.metadata import MetricMetadata


def recall_metric(
    state: RailwayAgentState,
    qdrant_repository,
) -> dict:
    """
    根据关键词从 Qdrant 中召回相关指标。
    """

    keywords = state["keywords"]

    # key: 指标名称
    # value: MetricMetadata
    retrieved_metrics: dict[str, MetricMetadata] = {}

    for keyword in keywords:
        metrics = qdrant_repository.search_metrics(
            query=keyword
        )

        for metric in metrics:
            # 指标名称作为唯一标识，避免不同关键词召回出重复指标
            retrieved_metrics[metric.name] = metric

    return {
        "retrieved_metrics": list(
            retrieved_metrics.values()
        )
    }