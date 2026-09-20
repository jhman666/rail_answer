"""
metadata.yaml -> Qdrant 自动同步

同步规则：
1. metadata.yaml 中存在的数据：
   - 重新生成 embedding
   - upsert 到 Qdrant
   - active=true

2. Qdrant 中存在、但 metadata.yaml 中已不存在的数据：
   - 不删除
   - active=false

3. 三类元数据分别同步：
   tables  -> railway_tables
   columns -> railway_columns
   metrics -> railway_metrics

4. 提供 sync_metadata_to_qdrant() 方法，
   供 FastAPI 启动时自动调用。
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.app_config import (
    AppConfig,
    load_app_config,
)

from app.core.metadata import (
    ColumnMetadata,
    MetadataConfig,
    MetricMetadata,
    TableMetadata,
    load_metadata,
)


# ============================================================
# 基础配置
# ============================================================

BATCH_SIZE = 64

SECTIONS = (
    "tables",
    "columns",
    "metrics",
)
from typing import Any, Union

from app.core.metadata import (
    ColumnMetadata,
    MetadataConfig,
    MetricMetadata,
    TableMetadata,
    load_metadata,
)


MetadataItem = Union[
    TableMetadata,
    ColumnMetadata,
    MetricMetadata,
]



# ============================================================
# 创建 Qdrant Client
# ============================================================

def get_qdrant_client(
    config: AppConfig,
) -> QdrantClient:

    cfg = config.qdrant

    return QdrantClient(
        host=cfg.host,
        port=cfg.port,
        api_key=cfg.api_key,
        https=cfg.https,
    )


# ============================================================
# 创建 Embedding
# ============================================================

def get_embedding_model(
    config: AppConfig,
) -> OllamaEmbeddings:

    cfg = config.embedding

    if cfg.provider.lower() != "ollama":
        raise ValueError(
            f"当前同步脚本只支持 Ollama Embedding，"
            f"但 provider={cfg.provider}"
        )

    return OllamaEmbeddings(
        model=cfg.model,
        base_url=(
            cfg.base_url
            or "http://localhost:11434"
        ),
    )


# ============================================================
# 生成固定 Point ID
# ============================================================

def make_point_id(
    section: str,
    metadata_key: str,
) -> str:

    source = (
        f"railway-metadata:"
        f"{section}:"
        f"{metadata_key}"
    )

    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            source,
        )
    )


# ============================================================
# 构建 Table Embedding 文本
# ============================================================

def build_table_text(
    key: str,
    data: TableMetadata,
) -> str:

    return "\n".join(
        [
            f"表名：{key}",
            f"中文名称：{data.name}",
            f"业务领域：{data.business_domain or ''}",
            f"主键：{data.primary_key or ''}",
            f"描述：{data.description}",
        ]
    )


# ============================================================
# 构建 Column Embedding 文本
# ============================================================

def build_column_text(
    key: str,
    data: ColumnMetadata,
) -> str:

    lines = [
        f"字段：{key}",
        f"所属表：{data.table_name}",
        f"字段名：{data.column_name}",
        f"中文名称：{data.name}",
        f"数据类型：{data.type}",
        f"描述：{data.description}",
    ]

    if data.primary_key:
        lines.append(
            "该字段是主键。"
        )

    if data.foreign_key:
        lines.append(
            f"该字段是外键，关联 "
            f"{data.references_table or ''}."
            f"{data.references_column or ''}。"
        )

    return "\n".join(
        lines
    )


# ============================================================
# 构建 Metric Embedding 文本
# ============================================================

def build_metric_text(
    key: str,
    data: MetricMetadata,
) -> str:

    return "\n".join(
        [
            f"指标编码：{key}",
            f"指标名称：{data.name}",
            f"描述：{data.description}",
            f"计算公式：{data.formula}",
            f"固定条件：{'；'.join(data.conditions)}",
            f"相关表：{', '.join(data.related_tables)}",
            f"相关字段：{', '.join(data.related_columns)}",
            f"单位：{data.unit or ''}",
        ]
    )


# ============================================================
# 根据类型生成 Embedding 文本
# ============================================================

def build_embedding_text(
    section: str,
    key: str,
    data: MetadataItem,
) -> str:

    if section == "tables":

        if not isinstance(
            data,
            TableMetadata,
        ):
            raise TypeError(
                f"{key} 不是 TableMetadata"
            )

        return build_table_text(
            key,
            data,
        )

    if section == "columns":

        if not isinstance(
            data,
            ColumnMetadata,
        ):
            raise TypeError(
                f"{key} 不是 ColumnMetadata"
            )

        return build_column_text(
            key,
            data,
        )

    if section == "metrics":

        if not isinstance(
            data,
            MetricMetadata,
        ):
            raise TypeError(
                f"{key} 不是 MetricMetadata"
            )

        return build_metric_text(
            key,
            data,
        )

    raise ValueError(
        f"未知 section: {section}"
    )


# ============================================================
# 确保 Collection 存在
# ============================================================

def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int,
) -> None:

    if not client.collection_exists(
        collection_name
    ):

        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

        print(
            f"  创建 Collection: "
            f"{collection_name}, "
            f"vector_size={vector_size}"
        )

        return

    info = client.get_collection(
        collection_name
    )

    vectors_config = (
        info.config.params.vectors
    )

    old_size = getattr(
        vectors_config,
        "size",
        None,
    )

    if (
        old_size is not None
        and old_size != vector_size
    ):

        raise ValueError(
            f"{collection_name} 已存在，"
            f"向量维度={old_size}，"
            f"当前 Embedding 模型维度="
            f"{vector_size}。\n"
            f"说明 Embedding 模型发生了变化，"
            f"请删除旧 Collection 后重新同步。"
        )

    print(
        f"  Collection 已存在: "
        f"{collection_name}"
    )


# ============================================================
# 获取 Qdrant 中已有 Point
# ============================================================

def get_existing_ids(
    client: QdrantClient,
    collection_name: str,
) -> set[str]:

    ids: set[str] = set()

    offset = None

    while True:

        points, next_offset = client.scroll(
            collection_name=collection_name,
            limit=256,
            offset=offset,
            with_payload=False,
            with_vectors=False,
        )

        for point in points:
            ids.add(
                str(point.id)
            )

        if next_offset is None:
            break

        offset = next_offset

    return ids


# ============================================================
# 批量 Embedding
# ============================================================

def embed_texts(
    embedding_model: OllamaEmbeddings,
    texts: list[str],
) -> list[list[float]]:

    vectors: list[list[float]] = []

    for start in range(
        0,
        len(texts),
        BATCH_SIZE,
    ):

        batch = texts[
            start:start + BATCH_SIZE
        ]

        batch_vectors = (
            embedding_model.embed_documents(
                batch
            )
        )

        vectors.extend(
            batch_vectors
        )

        print(
            f"  Embedding: "
            f"{min(start + BATCH_SIZE, len(texts))}"
            f"/"
            f"{len(texts)}"
        )

    return vectors


# ============================================================
# 同步一个 Collection
# ============================================================

def sync_collection(
    client: QdrantClient,
    embedding_model: OllamaEmbeddings,
    section: str,
    collection_name: str,
    metadata_data: dict[
        str,
        MetadataItem,
    ],
) -> None:

    print(
        f"\n同步 "
        f"{section} "
        f"-> "
        f"{collection_name}"
    )

    if not metadata_data:

        print(
            "  metadata.yaml 中无数据"
        )

        return

    point_ids: list[str] = []
    texts: list[str] = []
    payloads: list[
        dict[str, Any]
    ] = []

    # --------------------------------------------------------
    # 构建数据
    # --------------------------------------------------------

    for (
        metadata_key,
        item,
    ) in metadata_data.items():

        point_id = make_point_id(
            section,
            metadata_key,
        )

        embedding_text = (
            build_embedding_text(
                section,
                metadata_key,
                item,
            )
        )

        data = item.model_dump()

        payload = {
            **data,
            "metadata_key": metadata_key,
            "metadata_type": section,
            "embedding_text": embedding_text,
            "active": True,
        }

        point_ids.append(
            point_id
        )

        texts.append(
            embedding_text
        )

        payloads.append(
            payload
        )

    # --------------------------------------------------------
    # Embedding
    # --------------------------------------------------------

    vectors = embed_texts(
        embedding_model,
        texts,
    )

    if not vectors:

        print(
            "  未生成向量"
        )

        return

    vector_size = len(
        vectors[0]
    )

    if any(
        len(vector) != vector_size
        for vector in vectors
    ):

        raise ValueError(
            "Embedding 返回的向量维度不一致"
        )

    # --------------------------------------------------------
    # Collection
    # --------------------------------------------------------

    ensure_collection(
        client=client,
        collection_name=collection_name,
        vector_size=vector_size,
    )

    # --------------------------------------------------------
    # 原来的 Point
    # --------------------------------------------------------

    existing_ids = get_existing_ids(
        client=client,
        collection_name=collection_name,
    )

    # --------------------------------------------------------
    # 构造 Qdrant Point
    # --------------------------------------------------------

    points = [
        PointStruct(
            id=point_id,
            vector=vector,
            payload=payload,
        )
        for (
            point_id,
            vector,
            payload,
        ) in zip(
            point_ids,
            vectors,
            payloads,
        )
    ]

    # --------------------------------------------------------
    # Upsert
    # --------------------------------------------------------

    for start in range(
        0,
        len(points),
        BATCH_SIZE,
    ):

        batch = points[
            start:start + BATCH_SIZE
        ]

        client.upsert(
            collection_name=collection_name,
            points=batch,
            wait=True,
        )

        print(
            f"  Upsert: "
            f"{min(start + BATCH_SIZE, len(points))}"
            f"/"
            f"{len(points)}"
        )

    # --------------------------------------------------------
    # metadata.yaml 中已经删除的数据
    # 标记 inactive
    # --------------------------------------------------------

    current_ids = set(
        point_ids
    )

    missing_ids = (
        existing_ids
        - current_ids
    )

    if missing_ids:

        missing_list = list(
            missing_ids
        )

        for start in range(
            0,
            len(missing_list),
            BATCH_SIZE,
        ):

            batch = missing_list[
                start:start + BATCH_SIZE
            ]

            client.set_payload(
                collection_name=collection_name,
                payload={
                    "active": False
                },
                points=batch,
                wait=True,
            )

        print(
            f"  标记 inactive: "
            f"{len(missing_ids)} 条"
        )

    else:

        print(
            "  无需要标记 inactive 的旧数据"
        )

    # --------------------------------------------------------
    # 统计
    # --------------------------------------------------------

    total = client.count(
        collection_name=collection_name,
        exact=True,
    ).count

    print(
        f"  完成: "
        f"{collection_name}, "
        f"当前总 Point 数="
        f"{total}"
    )


# ============================================================
# 获取配置文件路径
# ============================================================

def get_paths() -> tuple[
    Path,
    Path,
]:

    """
    project/
    ├── conf/
    │   ├── app_config.yaml
    │   └── metadata.yaml
    │
    └── app/
        └── conf/
            └── sync_metadata_to_qdrant.py
    """

    script_dir = (
        Path(__file__)
        .resolve()
        .parent
    )

    project_root = (
        script_dir
        .parent
        .parent
    )

    config_path = (
        project_root
        / "conf"
        / "app_config.yaml"
    )

    metadata_path = (
        project_root
        / "conf"
        / "metadata.yaml"
    )

    return (
        config_path,
        metadata_path,
    )


# ============================================================
# 自动同步方法
# ============================================================

def sync_metadata_to_qdrant() -> None:

    print(
        "=" * 60
    )

    print(
        "Railway Metadata -> Qdrant"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # 路径
    # --------------------------------------------------------

    (
        config_path,
        metadata_path,
    ) = get_paths()

    print(
        f"app_config: "
        f"{config_path}"
    )

    print(
        f"metadata:   "
        f"{metadata_path}"
    )

    # --------------------------------------------------------
    # 加载 app_config.yaml
    # --------------------------------------------------------

    print(
        "\n加载并校验 app_config.yaml..."
    )

    config: AppConfig = (
        load_app_config(
            config_path
        )
    )

    # --------------------------------------------------------
    # 加载 metadata.yaml
    # --------------------------------------------------------

    print(
        "加载并校验 metadata.yaml..."
    )

    metadata: MetadataConfig = (
        load_metadata(
            metadata_path
        )
    )

    # --------------------------------------------------------
    # Qdrant
    # --------------------------------------------------------

    print(
        "\n连接 Qdrant..."
    )

    client = get_qdrant_client(
        config
    )

    result = (
        client.get_collections()
    )

    print(
        f"Qdrant 连接成功，"
        f"当前 Collection 数量="
        f"{len(result.collections)}"
    )

    # --------------------------------------------------------
    # Embedding
    # --------------------------------------------------------

    print(
        "\n初始化 Ollama Embedding..."
    )

    embedding_model = (
        get_embedding_model(
            config
        )
    )

    # --------------------------------------------------------
    # Collection 名称
    # --------------------------------------------------------

    collections_cfg = (
        config.qdrant.collections
    )

    section_collection_names = {

        "tables":
            collections_cfg.tables,

        "columns":
            collections_cfg.columns,

        "metrics":
            collections_cfg.metrics,
    }

    # --------------------------------------------------------
    # metadata 数据
    # --------------------------------------------------------

    section_metadata = {

        "tables":
            metadata.tables,

        "columns":
            metadata.columns,

        "metrics":
            metadata.metrics,
    }

    # --------------------------------------------------------
    # 开始同步
    # --------------------------------------------------------

    for section in SECTIONS:

        sync_collection(
            client=client,
            embedding_model=embedding_model,
            section=section,
            collection_name=(
                section_collection_names[
                    section
                ]
            ),
            metadata_data=(
                section_metadata[
                    section
                ]
            ),
        )

    print(
        "\n" + "=" * 60
    )

    print(
        "全部元数据自动同步完成"
    )

    print(
        "=" * 60
    )


# ============================================================
# 保留手动运行能力
# ============================================================

def main() -> None:

    sync_metadata_to_qdrant()


if __name__ == "__main__":
    main()