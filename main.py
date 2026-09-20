from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent.graph import graph

from app.conf.sync_metadata_to_qdrant import (
    sync_metadata_to_qdrant,
)


# ============================================================
# FastAPI 生命周期
# ============================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    # --------------------------------------------------------
    # 后端启动时自动同步 metadata.yaml -> Qdrant
    # --------------------------------------------------------

    print(
        "\n正在自动同步 metadata.yaml -> Qdrant..."
    )

    try:

        sync_metadata_to_qdrant()

        print(
            "metadata.yaml -> Qdrant 同步成功"
        )

    except Exception as e:

        print(
            f"metadata.yaml -> Qdrant 同步失败: {e}"
        )

        # 同步失败时直接阻止后端启动
        raise

    # --------------------------------------------------------
    # FastAPI 正式运行
    # --------------------------------------------------------

    yield

    # --------------------------------------------------------
    # 后端关闭
    # --------------------------------------------------------

    print(
        "Railway Agent API 已关闭"
    )


# ============================================================
# 创建 FastAPI
# ============================================================

app = FastAPI(
    title="Railway Text-to-SQL API",
    lifespan=lifespan,
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# 请求参数
# ============================================================

class QueryRequest(
    BaseModel
):
    query: str


# ============================================================
# 首页
# ============================================================

@app.get("/")
def root():

    return {
        "message":
            "Railway Agent API is running"
    }


# ============================================================
# Text-to-SQL
# ============================================================

@app.post(
    "/api/query"
)
def query_agent(
    request: QueryRequest,
):

    try:

        result = graph.invoke(
            {
                "query":
                    request.query
            }
        )

        return {

            "sql":
                result.get(
                    "sql",
                    "",
                ),

            "result":
                result.get(
                    "result",
                    [],
                ),

            "error":
                result.get(
                    "error",
                    "",
                ),
        }

    except Exception as e:

        return {

            "sql":
                "",

            "result":
                [],

            "error":
                str(e),
        }


# ============================================================
# Python 直接启动
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )