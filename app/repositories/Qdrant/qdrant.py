from qdrant_client import QdrantClient

from app.core.app_config import AppConfig


def create_qdrant_client(
    config: AppConfig
) -> QdrantClient:

    return QdrantClient(
        host=config.qdrant.host,
        port=config.qdrant.port,
        api_key=config.qdrant.api_key,
        https=config.qdrant.https,
    )