"""FastAPI 主应用"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.api import routes
from app.config import settings

# 创建 FastAPI 应用
app = FastAPI(
    title="Knowledge Graph RAG System",
    version="1.0.0",
    description="基于 RAGAnything 的多模态知识图谱 RAG 系统"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# 注册 API 路由
app.include_router(routes.router, prefix="/api")


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
