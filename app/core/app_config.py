from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# MySQL
# ============================================================

class MySQLConfig(BaseModel):
    host: str = "localhost"
    port: int = 3306

    username: str
    password: str
    database: str

    charset: str = "utf8mb4"


# ============================================================
# Qdrant
# ============================================================

class QdrantCollectionsConfig(BaseModel):
    tables: str
    columns: str
    metrics: str


class QdrantConfig(BaseModel):
    host: str = "localhost"
    port: int = 6333

    collections: QdrantCollectionsConfig

    api_key: str | None = None
    https: bool = False


# ============================================================
# Elasticsearch
# ============================================================

class ElasticsearchIndexConfig(BaseModel):
    dimension_values: str


class ElasticsearchConfig(BaseModel):
    url: str = "http://localhost:9200"

    index: ElasticsearchIndexConfig


# ============================================================
# LLM
# ============================================================

class LLMConfig(BaseModel):
    provider: str
    model: str

    base_url: str | None = None
    api_key: str | None = None

    temperature: float = 0

    # 后续不同模型提供商有额外参数时也允许存在
    model_config = ConfigDict(
        extra="allow"
    )


# ============================================================
# Embedding
# ============================================================

class EmbeddingConfig(BaseModel):
    provider: str
    model: str

    base_url: str | None = None
    api_key: str | None = None

    dimensions: int | None = None

    model_config = ConfigDict(
        extra="allow"
    )


# ============================================================
# 整个 app_config.yaml
# ============================================================

class AppConfig(BaseModel):
    mysql: MySQLConfig
    qdrant: QdrantConfig
    elasticsearch: ElasticsearchConfig
    llm: LLMConfig
    embedding: EmbeddingConfig


# ============================================================
# 加载
# ============================================================

def load_app_config(
    path: str | Path
) -> AppConfig:

    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8"
    ) as f:
        raw_data = yaml.safe_load(f)

    return AppConfig.model_validate(
        raw_data
    )