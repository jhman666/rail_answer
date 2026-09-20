from elasticsearch import Elasticsearch

from app.core.app_config import AppConfig
from app.models.es.dimension_value import DimensionValue


class ElasticsearchRepository:

    def __init__(
        self,
        client: Elasticsearch,
        config: AppConfig,
    ):
        self.client = client
        self.index_name = (
            config.elasticsearch.index.dimension_values
        )

    def search_values(
        self,
        keyword: str,
        limit: int = 5,
    ) -> list[DimensionValue]:

        response = self.client.search(
            index=self.index_name,
            query={
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": keyword,
                                "fields": [
                                    "value^2",
                                    "aliases",
                                ],
                            }
                        }
                    ],
                    "filter": [
                        {
                            "term": {
                                "active": True
                            }
                        }
                    ],
                }
            },
            size=limit,
        )

        return [
            DimensionValue.model_validate(
                hit["_source"]
            )
            for hit in response["hits"]["hits"]
        ]