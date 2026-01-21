# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A multimodal Knowledge Graph RAG system built on RAGAnything/LightRAG. Supports document upload (PDF, images, Office docs), intelligent processing with entity/relation extraction, knowledge queries, and interactive graph visualization.

## Quick Start

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Configure environment (copy and edit with your API key)
cp env.example .env
# Edit .env: set LLM_API_KEY and other provider settings

# Run the server (from project root)
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Or use scripts
scripts/start.bat  # Windows
./scripts/start.sh # Linux/Mac
```

Access: http://localhost:8000 (frontend) | http://localhost:8000/docs (API docs)

## Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (HTML + Bootstrap + JS)       │  Served by FastAPI, no separate server
├─────────────────────────────────────────┤
│  FastAPI Routes (backend/app/api/)      │  /upload, /documents, /query, /graph
├─────────────────────────────────────────┤
│  Services (backend/app/services/)       │  DocumentService, GraphService, LLMFactory
├─────────────────────────────────────────┤
│  RAGAnything (backend/knowledge_graph_rag/)  │  Multimodal RAG wrapper
├─────────────────────────────────────────┤
│  LightRAG + Storage                     │  Vector/graph/KV storage in data/storage/
└─────────────────────────────────────────┘
```

**Key patterns:**
- Dependency injection via FastAPI `Depends()` for RAG instance
- Factory pattern for multi-model LLM support (`LLMFactory`)
- Background tasks for async document processing
- Singleton RAG instance shared across requests

## Key Files

| Area | Files |
|------|-------|
| V1 API routes | `backend/app/api/v1/{documents,query,graph,tasks,config}.py` |
| Legacy API routes | `backend/app/api/{upload,documents,query,graph}.py` |
| Middleware | `backend/app/middleware/{auth,response}.py` |
| Business logic | `backend/app/services/{document_service,graph_service,task_service,webhook_service}.py` |
| Request/Response models | `backend/app/models/{request,response}.py` |
| App config | `backend/app/config.py` (loads from root `.env`) |
| RAG core | `backend/knowledge_graph_rag/raganything.py` |
| Frontend | `frontend/index.html`, `frontend/assets/js/{app,upload,query,graph}.js` |

## API Endpoints

### V1 API (推荐)

企业集成版 API，支持 API Key 认证、统一响应格式、Webhook 回调。

**认证方式**: `X-API-Key: sk-xxx` Header

**统一响应格式**:
```json
{
  "code": 0,
  "message": "success",
  "data": { ... },
  "request_id": "uuid-xxx"
}
```

#### 文档管理

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/documents/upload` | 上传文档（异步处理，支持 callback_url） |
| GET | `/api/v1/documents` | 获取文档列表 |
| GET | `/api/v1/documents/{doc_id}` | 获取文档详情和处理状态 |
| DELETE | `/api/v1/documents/{doc_id}` | 删除文档 |

#### 智能问答

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/v1/query` | 知识库问答 |
| POST | `/api/v1/query/stream` | 流式问答（SSE） |

#### 知识图谱

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/graph` | 获取完整图谱（vis.js 格式） |
| GET | `/api/v1/graph/entities` | 获取实体列表 |
| GET | `/api/v1/graph/relations` | 获取关系列表 |
| GET | `/api/v1/graph/subgraph` | 获取子图（按实体/文档筛选） |
| GET | `/api/v1/graph/stats` | 获取图谱统计信息 |

#### 任务管理

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/tasks/{task_id}` | 查询任务状态 |
| DELETE | `/api/v1/tasks/{task_id}` | 取消任务 |

#### 配置和健康检查

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/health` | 健康检查（无需认证） |
| GET | `/api/v1/config` | 获取当前配置（脱敏） |

### Legacy API (向后兼容)

旧版 API，保留用于向后兼容，建议迁移到 V1 API。

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/upload` | Upload document (multipart/form-data) |
| GET | `/api/documents` | List all documents |
| GET | `/api/documents/{doc_id}` | Get document status |
| POST | `/api/query` | Query knowledge base (body: `{question, mode, doc_ids}`) |
| GET | `/api/graph` | Export knowledge graph for vis.js |

Query modes: `mix` (recommended), `local`, `global`, `hybrid`, `naive`

## LLM Configuration

The `.env` file in the project root controls LLM settings. The config is loaded by `backend/app/config.py`.

**Required variables:**
- `LLM_API_KEY` - API key for your LLM provider
- `LLM_PROVIDER` - openai, qwen, ollama, or lmstudio
- `LLM_MODEL` - Model name (e.g., gpt-4o, qwen-turbo)
- `LLM_BASE_URL` - API endpoint

**OpenAI:**
```
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.openai.com/v1
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIM=3072
```

**Qwen:**
```
LLM_PROVIDER=qwen
LLM_MODEL=qwen-turbo
LLM_API_KEY=sk-...
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

**Ollama (local):**
```
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:14b
LLM_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=bge-m3:latest
EMBEDDING_DIM=1024
```

## API Key Configuration

V1 API 支持 API Key 认证，通过 `.env` 文件配置：

```
# API Keys（多个用逗号分隔）
# 留空则允许无认证访问（开发模式）
API_KEYS=sk-key1,sk-key2
```

**使用方式**:
```bash
curl -H "X-API-Key: sk-key1" http://localhost:8000/api/v1/health
```

## Data Directories

- `data/uploads/` - Uploaded documents
- `data/storage/` - RAG storage (vectors, graphs, KV)
- `data/output/` - Processed document output

## External Dependencies

- **LibreOffice** - Required for Office document conversion (doc, docx, ppt, pptx, xls, xlsx)
- **MinerU** - Document parser (installed via requirements.txt as `mineru[core]`)

## Notes

- Frontend is embedded in backend (no separate frontend server needed)
- The `knowledge_graph_rag/` module is a copy from RAGAnything source, not installed via pip
- Document processing runs as background tasks (non-blocking uploads)
- The `.env` file should be in the project root, not `backend/`
