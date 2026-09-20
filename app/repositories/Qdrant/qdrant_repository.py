from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)

from app.core.app_config import AppConfig
from app.core.metadata import (
    TableMetadata,
    ColumnMetadata,
    MetricMetadata,
)


class QdrantRepository:

    def __init__(
        self,
        client: QdrantClient,
        embedding: OllamaEmbeddings,
        config: AppConfig,
    ):
        self.client = client
        self.embedding = embedding
        self.config = config

    def search_tables(
        self,
        query: str,
        limit: int = 5,
    ) -> list[TableMetadata]:

        vector = self.embedding.embed_query(query)

        result = self.client.query_points(
            collection_name=self.config.qdrant.collections.tables,
            query=vector,
            query_filter=self._active_filter(),
            limit=limit,
            with_payload=True,
        )

        return [
            TableMetadata.model_validate(point.payload)
            for point in result.points
        ]

    def search_columns(
        self,
        query: str,
        limit: int = 15,
    ) -> list[ColumnMetadata]:

        vector = self.embedding.embed_query(query)

        result = self.client.query_points(
            collection_name=self.config.qdrant.collections.columns,
            query=vector,
            query_filter=self._active_filter(),
            limit=limit,
            with_payload=True,
        )

        return [
            ColumnMetadata.model_validate(point.payload)
            for point in result.points
        ]

    def search_metrics(
        self,
        query: str,
        limit: int = 10,
    ) -> list[MetricMetadata]:

        vector = self.embedding.embed_query(query)

        result = self.client.query_points(
            collection_name=self.config.qdrant.collections.metrics,
            query=vector,
            query_filter=self._active_filter(),
            limit=limit,
            with_payload=True,
        )

        return [
            MetricMetadata.model_validate(point.payload)
            for point in result.points
        ]

    @staticmethod
    def _active_filter() -> Filter:
        return Filter(
            must=[
                FieldCondition(
                    key="active",
                    match=MatchValue(value=True),
                )
            ]
        )