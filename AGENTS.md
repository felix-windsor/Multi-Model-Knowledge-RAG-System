# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

A multimodal Knowledge Graph RAG system built on RAGAnything/LightRAG. Supports document upload (PDF, images, Office docs), intelligent processing with entity/relation extraction, knowledge queries, and interactive graph visualization.

## Commands

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run the server (from project root)
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run unit tests (default, no external deps)
cd backend && python -m pytest

# Run a single test file
cd backend && python -m pytest tests/test_config.py

# Run integration tests (requires Docker: docker-compose up -d qdrant neo4j)
cd backend && python -m pytest -m integration

# Run both unit and integration tests
cd backend && python -m pytest -m ""
```

Access: http://localhost:8000 (frontend) | http://localhost:8000/docs (API docs)

## Architecture

```
Frontend (HTML + Bootstrap + JS)         Served by FastAPI at /, no separate server
    ↓
FastAPI Routes (backend/app/api/)        /api/v1/* (primary), /api/* (legacy)
    ↓
Services (backend/app/services/)         DocumentService, TaskService, WebhookService
    ↓
StorageManager (backend/app/storage/)    Unified abstraction over storage backends
    ↓
Storage Backends                         Local (JSON files) or Qdrant+Neo4j (Docker)
    ↓
RAGAnything + LightRAG                   Multimodal RAG with vector/graph storage
```

**Key patterns:**
- **Service Layer**: Business logic in `services/` — DocumentService, TaskService, WebhookService
- **Repository Pattern**: `StorageManager` coordinates document, task, and webhook storage with transaction support
- **Dependency Injection**: FastAPI `Depends()` wires services and storage via `dependencies.py`
- **Background Tasks**: Document processing is async with progress tracking via TaskService

## Key Files

| Area | Files |
|------|-------|
| App entrypoint | `backend/app/main.py` |
| V1 API routes | `backend/app/api/v1/{documents,query,graph,tasks,config}.py` |
| Legacy API routes | `backend/app/api/{upload,documents,query,graph}.py` |
| Middleware | `backend/app/middleware/{auth,response}.py` |
| Services | `backend/app/services/{document_service,task_service,webhook_service}.py` |
| Storage interfaces | `backend/app/storage/base.py`, `backend/app/storage/models.py` |
| Local storage impl | `backend/app/storage/local/{document,task,webhook}.py` |
| Database storage impl | `backend/app/storage/database/{document,task,webhook}.py` |
| DI providers | `backend/app/dependencies.py` |
| Request/Response models | `backend/app/models/{request,response}.py` |
| Config (loads root `.env`) | `backend/app/config.py` |
| RAG core | `backend/knowledge_graph_rag/raganything.py` |
| Frontend | `frontend/index.html`, `frontend/assets/js/{app,upload,query,graph}.js` |

## Configuration

All config is in the root `.env` file (not `backend/.env`), loaded by `backend/app/config.py` via pydantic-settings.

**Required:** `LLM_API_KEY`, `LLM_PROVIDER` (openai/qwen/ollama/lmstudio), `LLM_MODEL`, `LLM_BASE_URL`

**Storage:** `STORAGE_BACKEND=local` (default, JSON files in `data/storage/`) or `STORAGE_BACKEND=qdrant_neo4j` (requires Docker services). Vision and Embedding configs inherit from LLM if left empty. See `env.example` for all options.

**API auth:** V1 endpoints use `X-API-Key` header. Configure via `API_KEYS=sk-key1,sk-key2` in `.env`. Empty = no auth (dev mode).

## Coding Standards

**No TODO comments.** Either implement the feature completely or omit it. Use GitHub Issues for tracking future work, not code comments. Exception: experimental branches only.

## Important Gotchas

- `backend/knowledge_graph_rag/` is a vendored copy of RAGAnything source, not installed via pip
- The `.env` file must be in the **project root**, not in `backend/`
- Frontend is served by FastAPI's static file mount — no separate frontend build or server
- Document processing runs as async background tasks (uploads return immediately)
- `pytest.ini` defaults to unit tests only; integration tests need `-m integration`
- External dependency: **LibreOffice** is required for Office document conversion
