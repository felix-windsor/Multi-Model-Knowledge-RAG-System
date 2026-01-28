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

## Testing

The project has two types of tests:

### Unit Tests (Default)

Unit tests have no external dependencies and run quickly. They use mocks to isolate functionality.

```bash
# Run all unit tests (default)
cd backend
python -m pytest

# Run specific test file
python -m pytest tests/test_config.py

# Run specific test categories
python -m pytest tests/storage/      # Storage layer tests
python -m pytest tests/services/     # Service layer tests

# Run with verbose output
python -m pytest -v

# Explicitly run only unit tests
python -m pytest -m unit
```

**Test Structure:**
```
backend/tests/
├── storage/           # Storage layer unit tests
│   ├── test_local_document.py
│   ├── test_local_task.py
│   └── test_local_webhook.py
├── services/          # Service layer unit tests
│   ├── test_document_service.py
│   └── test_task_service.py
├── integration/       # API integration tests
│   └── test_document_flow.py
│   └── test_database_backend.py
└── conftest.py        # Shared fixtures
```

**Available unit test files:**
- `tests/test_config.py` - Configuration validation
- `tests/test_health_check.py` - Storage health check functions
- `tests/test_health_api.py` - Health check API endpoints
- `tests/test_rag_instance.py` - RAG instance creation
- `tests/test_error_handling.py` - Error handling for unavailable storage

### Integration Tests (Requires Docker)

Integration tests require Docker services (Qdrant and Neo4j) to be running. They test real interactions with external services.

```bash
# Step 1: Start Docker services
docker-compose up -d qdrant neo4j

# Step 2: Wait for services to be ready (check health)
docker-compose ps

# Step 3: Run integration tests
cd backend
python -m pytest -m integration

# Run integration tests with verbose output
python -m pytest -m integration -v

# Run specific integration test
python -m pytest tests/integration/test_database_backend.py
```

**Integration test behavior:**
- Tests are automatically skipped if `STORAGE_BACKEND != qdrant_neo4j`
- Tests wait for services to be ready before running
- Tests skip if services are not available (no failures)
- Tests verify real database connections and operations

**Available integration test files:**
- `tests/integration/test_database_backend.py` - End-to-end tests with Qdrant and Neo4j

### Running All Tests

```bash
# Run both unit and integration tests
cd backend
python -m pytest -m ""

# Or explicitly
python -m pytest --co -q  # Show what would run
python -m pytest          # Run (will skip integration by default)
```

### Test Configuration

Tests are configured in `pytest.ini`:
- Unit tests run by default
- Integration tests require explicit `-m integration` flag
- Asyncio mode is set to auto for async tests
- Verbose output is enabled by default

## Architecture

```
┌─────────────────────────────────────────┐
│  Frontend (HTML + Bootstrap + JS)       │  Served by FastAPI, no separate server
├─────────────────────────────────────────┤
│  FastAPI Routes (backend/app/api/)      │  /api/v1/*, /api/* (legacy)
├─────────────────────────────────────────┤
│  Services (backend/app/services/)       │  DocumentService, TaskService, WebhookService
├─────────────────────────────────────────┤
│  StorageManager (backend/app/storage/)  │  Unified storage abstraction layer
├─────────────────────────────────────────┤
│  Storage Backends                       │  Local (JSON) or Database (PostgreSQL)
├─────────────────────────────────────────┤
│  RAGAnything + LightRAG                 │  Multimodal RAG with vector/graph storage
└─────────────────────────────────────────┘
```

**Key patterns:**
- **Service Layer Pattern**: Business logic encapsulated in services (DocumentService, TaskService, WebhookService)
- **Repository Pattern**: StorageManager provides unified interface to storage backends
- **Dependency Injection**: FastAPI `Depends()` for services and storage
- **Transaction Support**: Coordinated transactions across document, task, and webhook storage
- **Background Tasks**: Async document processing with progress tracking

## Key Files

| Area | Files |
|------|-------|
| V1 API routes | `backend/app/api/v1/{documents,query,graph,tasks,config}.py` |
| Legacy API routes | `backend/app/api/{upload,documents,query,graph}.py` |
| Middleware | `backend/app/middleware/{auth,response}.py` |
| Services | `backend/app/services/{document_service,task_service,webhook_service}.py` |
| Storage abstraction | `backend/app/storage/base.py` (interfaces), `backend/app/storage/models.py` |
| Local storage | `backend/app/storage/local/{document,task,webhook}.py` |
| Database storage | `backend/app/storage/database/{document,task,webhook}.py` |
| Dependencies | `backend/app/dependencies.py` (DI providers) |
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

**Config Inheritance:** Vision and Embedding configs inherit from LLM if left empty. See `env.example` for all options including Vision, Rerank, and mixed provider configurations.

**Performance Tuning:**
```
EMBEDDING_BATCH_NUM=10          # Batch size for embeddings
EMBEDDING_FUNC_MAX_ASYNC=8      # Max concurrent embedding calls
EMBEDDING_CACHE_ENABLED=true    # Enable embedding cache
EMBEDDING_CACHE_THRESHOLD=0.95  # Cache similarity threshold
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

## Storage Configuration

The system supports two storage backends for document metadata, tasks, and webhooks:

**Local Storage (default):**
```
STORAGE_BACKEND=local
```
Stores data as JSON files in `data/storage/`. Good for development and single-instance deployments.

**Database Storage:**
```
STORAGE_BACKEND=database
DATABASE_URL=postgresql://user:pass@localhost:5432/ragdb
```
Uses PostgreSQL for persistent storage. Recommended for production and multi-instance deployments.

**Storage Architecture:**
- `StorageManager`: Unified interface coordinating document, task, and webhook storage
- `DocumentStorage`: Document metadata (filename, status, file_path)
- `TaskStorage`: Processing tasks with progress tracking
- `WebhookStorage`: Callback URLs for async notifications
- Supports transactions across all storage types

## Data Directories

- `data/uploads/` - Uploaded documents
- `data/storage/` - RAG storage (vectors, graphs, KV) and local JSON storage
- `data/output/` - Processed document output

## RAG Storage Backend Configuration

The system supports two storage backends for RAG data: local file-based storage (development) and database storage with Qdrant and Neo4j (production).

### Local Storage (Development)

**Description:** File-based storage using LightRAG's built-in storage. Stores vectors, graph data, and key-value pairs in local files under `data/storage/`.

**Advantages:**
- Zero configuration - no external services required
- Fast setup for development and testing
- Simple to backup and migrate (just copy files)
- Ideal for single-instance deployments

**Disadvantages:**
- No concurrent access support
- Limited scalability
- No advanced query capabilities

**Configuration:**
```bash
# In .env file
STORAGE_BACKEND=local
STORAGE_DIR=../data/storage
```

**Usage:**
```bash
# No additional services needed - just run the server
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Database Storage (Production)

**Description:** Production-grade storage using Qdrant (vector database) and Neo4j (graph database). Provides concurrent access, scalability, and advanced query capabilities.

**Advantages:**
- Supports concurrent access from multiple instances
- Horizontally scalable
- Advanced query capabilities (vector similarity, graph traversal)
- Web UIs for data exploration
- Production-ready with health checks and monitoring

**Disadvantages:**
- Requires Docker services to be running
- More complex setup and configuration
- Higher resource requirements

**Configuration:**
```bash
# In .env file
STORAGE_BACKEND=qdrant_neo4j

# Qdrant settings
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=rag_collection

# Neo4j settings
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=rag123456
NEO4J_DATABASE=neo4j
```

**Usage:**
```bash
# Step 1: Start Docker services
docker-compose up -d qdrant neo4j

# Step 2: Wait for services to be ready (check health)
docker-compose ps

# Step 3: Run the server
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Switching Between Backends

**Important Notes:**
- Data is NOT automatically migrated between backends
- Switching backends will start with an empty knowledge base
- Backup your data before switching by exporting documents or copying `data/storage/`

**Steps to Switch:**

1. **Stop the server**
   ```bash
   # Press Ctrl+C in the terminal running uvicorn
   ```

2. **Update .env file**
   ```bash
   # For local storage
   STORAGE_BACKEND=local

   # OR for database storage
   STORAGE_BACKEND=qdrant_neo4j
   ```

3. **If switching TO database storage:**
   ```bash
   # Start required services
   docker-compose up -d qdrant neo4j

   # Verify services are running
   docker-compose ps
   ```

4. **If switching TO local storage:**
   ```bash
   # Optional: Stop database services to free resources
   docker-compose stop qdrant neo4j
   ```

5. **Restart the server**
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Re-upload documents**
   - Documents must be uploaded again to populate the new backend
   - Use the web UI or API to upload documents

### Viewing Stored Data

#### Qdrant (Vector Database)

**Web Dashboard:**
- URL: http://localhost:6333/dashboard
- Features: Browse collections, view vectors, inspect metadata, search similarity

**API:**
```bash
# List collections
curl http://localhost:6333/collections

# Get collection info
curl http://localhost:6333/collections/rag_collection

# View points count
curl http://localhost:6333/collections/rag_collection
```

**Python Script:**
```bash
# Use the provided script
python scripts/view_qdrant.py
```

#### Neo4j (Graph Database)

**Neo4j Browser:**
- URL: http://localhost:7474
- Username: `neo4j`
- Password: `rag123456` (from .env)

**Useful Cypher Queries:**
```cypher
// View all nodes and relationships
MATCH (n) RETURN n LIMIT 25

// Count entities and relationships
MATCH (e:Entity) RETURN count(e) as entity_count
MATCH ()-[r:RELATIONSHIP]->() RETURN count(r) as relation_count

// Find entities by source document
MATCH (e:Entity {source_id: "doc_xxx"}) RETURN e

// View entity relationships
MATCH (e:Entity)-[r:RELATIONSHIP]->(target)
WHERE e.name = "Entity Name"
RETURN e, r, target
```

**Python Script:**
```bash
# Use the provided script
python scripts/view_neo4j.py
```

### Health Checks

#### Check All Services

```bash
# Docker services
docker-compose ps

# Or check health status
docker-compose ps --format json | python -m json.tool
```

#### Individual Service Health

**Qdrant:**
```bash
# Health check
curl http://localhost:6333/healthz

# Readiness check
curl http://localhost:6333/readyz
```

**Neo4j:**
```bash
# HTTP endpoint
curl http://localhost:7474

# Bolt connection (requires cypher-shell)
cypher-shell -a bolt://localhost:7687 -u neo4j -p rag123456 "RETURN 1"
```

**Application Health:**
```bash
# API health endpoint
curl http://localhost:8000/api/v1/health

# Expected response:
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "healthy",
    "timestamp": "2026-01-28T12:00:00Z",
    "storage_backend": "qdrant_neo4j",
    "services": {
      "qdrant": "connected",
      "neo4j": "connected"
    }
  }
}
```

#### Troubleshooting

**Service not starting:**
```bash
# View logs
docker-compose logs qdrant
docker-compose logs neo4j

# Restart service
docker-compose restart qdrant neo4j

# Full restart
docker-compose down
docker-compose up -d
```

**Connection issues:**
```bash
# Check if ports are available
netstat -an | grep "6333\|7687\|7474"

# Check Docker network
docker network inspect rag-network
```

**Data corruption or reset:**
```bash
# WARNING: This will DELETE all data
docker-compose down -v  # Remove volumes
docker-compose up -d    # Recreate services
```

## External Dependencies

- **LibreOffice** - Required for Office document conversion (doc, docx, ppt, pptx, xls, xlsx)
- **MinerU** - Document parser (installed via requirements.txt as `mineru[core]`)

## Coding Standards

### No TODO Comments

**CRITICAL RULE**: Do NOT leave TODO comments in code. Either implement the feature completely or don't write it at all.

**Bad:**
```python
# TODO: Extract source information from answer
sources = []

# TODO: Get token usage
usage = {"prompt_tokens": 0, "completion_tokens": 0}
```

**Good - Option 1 (Complete Implementation):**
```python
# Extract sources from answer metadata
sources = extract_sources_from_answer(answer)

# Get actual token usage from LLM response
usage = {
    "prompt_tokens": answer.usage.prompt_tokens,
    "completion_tokens": answer.usage.completion_tokens
}
```

**Good - Option 2 (Don't Implement Yet):**
```python
# Simply omit the unimplemented feature
# Return minimal response until ready to implement
return {"answer": answer}
```

**Why this rule?**
- TODOs accumulate technical debt
- They create confusion about what's implemented vs planned
- They make code look unfinished and unprofessional
- If something is important, implement it now; if not, remove it

**Exceptions:**
- Only use TODO in experimental branches or prototypes
- NEVER in main/production branches

### Code Quality Guidelines

- Write complete, production-ready code
- If a feature is complex, break it into smaller PRs
- Document limitations clearly in docstrings, not as TODOs
- Use GitHub Issues/Jira for future work tracking, not code comments

## Notes

- Frontend is embedded in backend (no separate frontend server needed)
- The `knowledge_graph_rag/` module is a copy from RAGAnything source, not installed via pip
- Document processing runs as background tasks (non-blocking uploads)
- The `.env` file should be in the project root, not `backend/`
