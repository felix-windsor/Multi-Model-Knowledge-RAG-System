"""API 路由注册"""
from fastapi import APIRouter
from app.api import upload, documents, query, graph

# 创建主路由
router = APIRouter()

# 注册各个子路由
router.include_router(upload.router, tags=["upload"])
router.include_router(documents.router, prefix="/documents", tags=["documents"])
router.include_router(query.router, prefix="/query", tags=["query"])
router.include_router(graph.router, prefix="/graph", tags=["graph"])
