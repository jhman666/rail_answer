from elasticsearch import Elasticsearch

from app.core.app_config import AppConfig


def create_elasticsearch_client(
    config: AppConfig,
) -> Elasticsearch:

    return Elasticsearch(
        config.elasticsearch.url
    )