"""FastAPI 主应用"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from app.api import routes
from app.api.v1 import router as v1_router
from app.config import settings
from app.middleware.response import wrap_response, ErrorCode
from app.storage import get_storage_manager, close_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await get_storage_manager()  # Initialize storage
    yield
    # Shutdown
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
        {"name": "upload", "description": "旧版上传 API (deprecated)"},
        {"name": "documents", "description": "旧版文档 API (deprecated)"},
        {"name": "query", "description": "旧版查询 API (deprecated)"},
        {"name": "graph", "description": "旧版图谱 API (deprecated)"},
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

# 注册旧版 API 路由（向后兼容，标记为 deprecated）
app.include_router(routes.router, prefix="/api", deprecated=True)


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
