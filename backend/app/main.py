"""FastAPI 主应用"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from app.api.v1 import router as v1_router
from app.config import settings
from app.middleware.response import wrap_response, ErrorCode
from app.storage import get_storage_manager, close_storage
from app.dependencies import check_storage_health

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management

    Handles startup health checks and graceful shutdown
    """
    # Startup
    backend = os.getenv("STORAGE_BACKEND", "local")
    logger.info(f"Starting with STORAGE_BACKEND={backend}")

    if backend == "qdrant_neo4j":
        health = await check_storage_health(backend, settings)

        if not all(health.values()):
            failed = [k for k, v in health.items() if not v]
            logger.error(
                f"⚠️  Storage health check failed: {failed}\n"
                f"   RAG instance will NOT be initialized.\n"
                f"   API endpoints will return 503 Service Unavailable.\n"
                f"   Please check Docker services: docker-compose up -d"
            )
        else:
            logger.info("✓ Storage backends healthy")
    else:
        logger.info("Using local storage (development mode)")

    # Initialize storage
    await get_storage_manager()

    yield

    # Shutdown
    logger.info("Application shutdown complete")
    await close_storage()


# 创建 FastAPI 应用
app = FastAPI(
    title="Knowledge Graph RAG System",
    version="1.0.0",
    description="基于 RAGAnything 的多模态知识图谱 RAG 系统，支持企业级 API 集成",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "V1 - Documents", "description": "文档管理 API"},
        {"name": "V1 - Query", "description": "智能问答 API"},
        {"name": "V1 - Knowledge Graph", "description": "知识图谱 API"},
        {"name": "V1 - Tasks", "description": "任务管理 API"},
        {"name": "V1 - Config & Health", "description": "配置和健康检查"},
    ]
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content=wrap_response(
            code=ErrorCode.INTERNAL_ERROR,
            message=f"Internal server error: {str(exc)}"
        )
    )


# 挂载静态文件
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# 注册 V1 API 路由
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    frontend_index = Path(__file__).parent.parent.parent / "frontend" / "index.html"
    if frontend_index.exists():
        return FileResponse(str(frontend_index))
    return {
        "message": "Knowledge Graph RAG System",
        "version": "1.0.0",
        "docs": "/docs",
        "frontend": "/static/index.html"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
