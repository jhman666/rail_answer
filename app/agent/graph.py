from functools import partial
from pathlib import Path

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaEmbeddings

from app.agent.state import RailwayAgentState

# =========================
# Agent Nodes
# =========================

from app.agent.nodes.check_intent import (
    check_intent,
    route_after_intent,
)

from app.agent.nodes.extract_keywords import extract_keywords
from app.agent.nodes.recall_column import recall_column
from app.agent.nodes.recall_metric import recall_metric
from app.agent.nodes.recall_value import recall_value
from app.agent.nodes.merge_retrieved_info import merge_retrieved_info
from app.agent.nodes.filter_table import filter_table
from app.agent.nodes.filter_metric import filter_metric
from app.agent.nodes.add_extra_context import add_extra_context
from app.agent.nodes.generate_sql import generate_sql

from app.agent.nodes.validate_sql import (
    validate_sql,
    route_after_validate,
)

from app.agent.nodes.correct_sql import correct_sql
from app.agent.nodes.execute_sql import execute_sql


# =========================
# Config
# =========================

from app.core.app_config import load_app_config


# =========================
# Qdrant
# =========================

from app.repositories.Qdrant.qdrant import (
    create_qdrant_client,
)

from app.repositories.Qdrant.qdrant_repository import (
    QdrantRepository,
)


# =========================
# Elasticsearch
# =========================

from app.repositories.es.elasticsearch import (
    create_elasticsearch_client,
)

from app.repositories.es.elasticsearch_repository import (
    ElasticsearchRepository,
)


# =========================
# MySQL
# =========================

from app.repositories.db.mysql import (
    create_mysql_engine,
    create_session_factory,
)

from app.repositories.db.mysql_repository import (
    MySQLRepository,
)


def build_graph():

    # =========================================================
    # 1. 加载应用配置
    # =========================================================
    #
    # 注意：
    # 这里读取的是 app_config.yaml
    # 只用于读取：
    #
    # LLM
    # Embedding
    # Qdrant
    # Elasticsearch
    # MySQL
    #
    # 不是 metadata.yaml

    project_root = (
        Path(__file__).resolve().parents[2]
    )

    config_path = (
        project_root
        / "conf"
        / "app_config.yaml"
    )

    config = load_app_config(
        config_path
    )

    # =========================================================
    # 2. 创建 LLM
    # =========================================================
    #
    # 当前使用 Qwen 的 OpenAI Compatible API，
    # 所以继续使用 ChatOpenAI。

    llm = ChatOpenAI(
        model=config.llm.model,
        api_key=config.llm.api_key,
        base_url=config.llm.base_url,
        temperature=config.llm.temperature,
    )

    # =========================================================
    # 3. 创建 Embedding
    # =========================================================

    embedding = OllamaEmbeddings(
        model=config.embedding.model,
        base_url=config.embedding.base_url,
    )

    # =========================================================
    # 4. Qdrant
    # =========================================================

    qdrant_client = create_qdrant_client(
        config
    )

    qdrant_repository = QdrantRepository(
        client=qdrant_client,
        embedding=embedding,
        config=config,
    )

    # =========================================================
    # 5. Elasticsearch
    # =========================================================

    es_client = create_elasticsearch_client(
        config
    )

    es_repository = ElasticsearchRepository(
        client=es_client,
        config=config,
    )

    # =========================================================
    # 6. MySQL
    # =========================================================

    mysql_engine = create_mysql_engine(
        config
    )

    session_factory = create_session_factory(
        mysql_engine
    )

    session = session_factory()

    mysql_repository = MySQLRepository(
        session=session
    )

    # =========================================================
    # 7. 创建 LangGraph
    # =========================================================

    builder = StateGraph(
        RailwayAgentState
    )

    # =========================================================
    # 8. 注册节点
    # =========================================================

    # ---------- 意图检查 ----------

    builder.add_node(
        "check_intent",
        check_intent,
    )

    # ---------- 关键词 ----------

    builder.add_node(
        "extract_keywords",
        extract_keywords,
    )

    # ---------- 三路召回 ----------

    builder.add_node(
        "recall_column",
        partial(
            recall_column,
            qdrant_repository=qdrant_repository,
        ),
    )

    builder.add_node(
        "recall_metric",
        partial(
            recall_metric,
            qdrant_repository=qdrant_repository,
        ),
    )

    builder.add_node(
        "recall_value",
        partial(
            recall_value,
            es_repository=es_repository,
        ),
    )

    # ---------- 合并召回 ----------

    builder.add_node(
        "merge_retrieved_info",
        partial(
            merge_retrieved_info,
            qdrant_repository=qdrant_repository,
        ),
    )

    # ---------- 过滤 ----------

    builder.add_node(
        "filter_table",
        partial(
            filter_table,
            llm=llm,
        ),
    )

    builder.add_node(
        "filter_metric",
        partial(
            filter_metric,
            llm=llm,
        ),
    )

    # ---------- 上下文 ----------

    builder.add_node(
        "add_extra_context",
        add_extra_context,
    )

    # ---------- SQL 生成 ----------

    builder.add_node(
        "generate_sql",
        partial(
            generate_sql,
            llm=llm,
        ),
    )

    # ---------- SQL 校验 ----------

    builder.add_node(
        "validate_sql",
        partial(
            validate_sql,
            mysql_repository=mysql_repository,
            llm=llm,
        ),
    )

    # ---------- SQL 修正 ----------

    builder.add_node(
        "correct_sql",
        partial(
            correct_sql,
            llm=llm,
        ),
    )

    # ---------- SQL 执行 ----------

    builder.add_node(
        "execute_sql",
        partial(
            execute_sql,
            mysql_repository=mysql_repository,
        ),
    )

    # =========================================================
    # 9. START
    # =========================================================

    builder.add_edge(
        START,
        "check_intent",
    )

    # =========================================================
    # 10. 意图判断
    # =========================================================
    #
    # 查询：
    # check_intent
    #     ↓
    # extract_keywords
    #
    # 修改 / 删除 / 新增：
    # check_intent
    #     ↓
    # END

    builder.add_conditional_edges(
        "check_intent",
        route_after_intent,
        {
            "extract_keywords": "extract_keywords",
            "end": END,
        },
    )

    # =========================================================
    # 11. 三路并行召回
    # =========================================================

    builder.add_edge(
        "extract_keywords",
        "recall_column",
    )

    builder.add_edge(
        "extract_keywords",
        "recall_metric",
    )

    builder.add_edge(
        "extract_keywords",
        "recall_value",
    )

    # 三路完成后统一进入 merge
    builder.add_edge(
        [
            "recall_column",
            "recall_metric",
            "recall_value",
        ],
        "merge_retrieved_info",
    )

    # =========================================================
    # 12. 两路并行过滤
    # =========================================================

    builder.add_edge(
        "merge_retrieved_info",
        "filter_table",
    )

    builder.add_edge(
        "merge_retrieved_info",
        "filter_metric",
    )

    # 两个过滤完成以后继续
    builder.add_edge(
        [
            "filter_table",
            "filter_metric",
        ],
        "add_extra_context",
    )

    # =========================================================
    # 13. SQL 生成
    # =========================================================

    builder.add_edge(
        "add_extra_context",
        "generate_sql",
    )

    # =========================================================
    # 14. SQL 校验
    # =========================================================

    builder.add_edge(
        "generate_sql",
        "validate_sql",
    )

    # =========================================================
    # 15. SQL 校验后的条件路由
    # =========================================================

    builder.add_conditional_edges(
        "validate_sql",
        route_after_validate,
        {
            "correct_sql": "correct_sql",
            "execute_sql": "execute_sql",

        },
    )

    # =========================================================
    # 16. SQL 修正后执行
    # =========================================================

    builder.add_edge(
        "correct_sql",
        "execute_sql",
    )

    # =========================================================
    # 17. END
    # =========================================================

    builder.add_edge(
        "execute_sql",
        END,
    )

    # =========================================================
    # 18. 编译
    # =========================================================

    return builder.compile()


graph = build_graph()