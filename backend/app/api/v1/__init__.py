"""V1 API 路由注册"""
from fastapi import APIRouter
from app.api.v1 import documents, query, graph, tasks, config

# 创建 v1 路由
router = APIRouter()

# 注册各个子路由
router.include_router(
    documents.router,
    prefix="/documents",
    tags=["V1 - Documents"]
)

router.include_router(
    query.router,
    prefix="/query",
    tags=["V1 - Query"]
)

router.include_router(
    graph.router,
    prefix="/graph",
    tags=["V1 - Knowledge Graph"]
)

router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["V1 - Tasks"]
)

router.include_router(
    config.router,
    tags=["V1 - Config & Health"]
)
