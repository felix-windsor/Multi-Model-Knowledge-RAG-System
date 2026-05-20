# 企业内网多模态知识库 RAG 系统

面向高安全内网企业场景的本地化多模态 Knowledge Graph RAG 应用。项目基于 FastAPI、RAGAnything/LightRAG 和本地部署的大模型服务，支持复杂文档上传解析、实体关系抽取、混合检索问答、知识图谱可视化和 API 化调用，用于加速内部文档阅读与知识查询。

这个项目最初来自 KG-RAG research 原型，后续围绕企业内部 RAG 方案“切分粗糙、检索策略单一、复杂文档支持不足”的问题，尝试将原型迁移为内网可运行的 AI 应用。

## 项目背景

项目面向内网和数据不出域场景，敏感文档不能直接调用外部大模型 API。系统通过本地模型服务提供文本理解和多模态文档解析能力：

- 文本大语言模型：用于问答生成、摘要、实体关系理解。
- 多模态模型：用于图片、图表、扫描件和复杂版面理解。

项目目标是将本地模型能力接入文档处理和问答链路，形成一个“上传文档后即可快速阅读、定位、提问和查看知识关系”的内部工具。

## 解决的问题

传统企业 RAG 常见方案是固定规则切分加向量检索。这个方式实现简单，但在复杂文档场景下容易出现：

- 章节、表格、图示和上下文关系被切断。
- 检索只看语义相似度，缺少实体和关系视角。
- 图片、表格、公式、流程图等多模态内容难以进入检索链路。
- 回答缺少来源和结构化解释。
- 云端模型不可用，需要全部在内网和本地模型环境中运行。

本项目通过多模态解析、知识图谱抽取和混合检索，将 RAG 从“简单检索问答”扩展为“复杂文档阅读加速工具”。

## 核心能力

- **多格式文档上传**：支持 PDF、图片、Office 文档、Markdown、文本等格式。
- **异步文档处理**：上传后立即返回 `doc_id` 和 `task_id`，后台执行解析、实体关系抽取和图谱构建。
- **本地模型适配**：支持 OpenAI-compatible API、Ollama、LM Studio 等接入方式，便于对接内网模型服务。
- **多模态解析**：支持文本、图片、表格、公式等内容进入统一 RAG 链路。
- **KG-RAG 检索增强**：基于 RAGAnything / LightRAG 支持 `local`、`global`、`hybrid`、`mix`、`naive` 多种查询模式。
- **自研抽取核心**：在 `backend/app/rag_core/` 实现中文企业文档 closed schema 抽取，将实体类型约束为 15 类、关系类型约束为 14 类，并支持 raw type 到 canonical type 的 drift mapping、关系合法性矩阵、实体去重率、无效关系率和关系置信度统计。
- **抽取质量 Sidecar**：可通过 `CUSTOM_GRAPH_EXTRACTION_ENABLED=true` 在文档上传后台任务中同步生成每篇文档的抽取质量报告，并写入任务结果。
- **知识图谱可视化**：将实体和关系导出为 vis.js 可视化格式，辅助理解文档结构。
- **服务层工程化**：抽象 `DocumentService`、`TaskService`、`WebhookService` 和 `StorageManager`。
- **API 化集成**：提供上传、任务状态、文档问答、流式问答、图谱导出、健康检查等 V1 API。

## 系统架构

```text
内部用户 / 业务系统
        |
        v
FastAPI V1 API
  - 文档上传
  - 任务状态
  - 文档问答
  - 图谱导出
  - 健康检查
        |
        v
Service Layer
  - DocumentService
  - TaskService
  - WebhookService
        |
        v
StorageManager
  - Local JSON Storage
  - Database-style Storage
        |
        v
RAGAnything / LightRAG
  - 多模态解析
  - Chunk / Embedding
  - Entity / Relation Extraction
  - KG-RAG Query
        |
        v
本地模型服务
  - 文本大语言模型
  - 多模态文档理解模型
```

前端由 FastAPI 直接托管，无需单独启动前端服务。

## 技术栈

**后端**

- FastAPI：API 服务和静态资源托管
- Pydantic / pydantic-settings：请求模型和配置管理
- RAGAnything / LightRAG：多模态 RAG 与 KG-RAG 核心能力
- Qdrant / Neo4j：向量和图谱存储后端选项
- pytest：单元测试和集成测试

**前端**

- HTML5 + Bootstrap 5
- Vanilla JavaScript
- vis.js 知识图谱可视化

**模型与部署**

- 本地大模型服务
- OpenAI-compatible 本地推理服务
- 纯内网部署

## 目录结构

```text
backend/
  app/
    api/v1/                 # V1 API：documents/query/graph/tasks/health/config
    services/               # DocumentService / TaskService / WebhookService
    storage/                # StorageManager 和本地/数据库存储实现
    middleware/             # API Key 鉴权与统一响应
    models/                 # 请求与响应模型
    rag_core/               # 自研中文企业文档实体/关系抽取核心
    config.py               # 读取项目根目录 .env
    dependencies.py         # FastAPI 依赖注入与 RAG 实例创建
  knowledge_graph_rag/      # vendored RAGAnything / LightRAG 相关代码
  tests/                    # 单元测试与集成测试

frontend/
  index.html
  assets/js/                # 上传、问答、图谱、配置等前端逻辑
  assets/css/

docs/
  guides/                   # 工程迁移与使用指南
  career/                   # 简历、面试讲稿和项目包装材料
  plans/                    # 历史设计方案

data/
  uploads/                  # 上传文件
  storage/                  # 本地存储
```

## 评估资产

- `benchmarks/synthetic_controlled_200x420/`：200 篇合成/脱敏企业文档和 420 条评测问题，覆盖技术手册、流程制度、API 配置、表格台账、扫描图示 5 类资料。
- `benchmarks/changsha_jingjia_public_multiformat_200/`：200 篇长沙景嘉微及相关公开多格式文档清单，覆盖 PDF、DOC、DOCX、XLS、XLSX、CSV、HTML；原始文件位于 ignored 的 `data/full_online_changsha_jingjia_eval_20260519/`。
- `scripts/evaluate_custom_extraction.py`：输出自研抽取核心的 JSON 解析成功率、schema 校验成功率、实体/关系 drift count、实体去重率、无效关系率、平均耗时和平均关系置信度。
- `scripts/validate_public_multiformat_eval_dataset.py`：校验公开多格式 benchmark 的 manifest、格式分布、分类分布和本地 raw 文件完整性。
- `backend/tests/rag_core/test_extractor.py`：覆盖 JSON 修复、类型漂移兜底、实体合并、缺失端点降权等关键异常场景。
- `backend/app/services/extraction_sidecar_service.py`：复用文档解析缓存，对上传文档生成 sidecar 抽取质量报告。

## 快速启动

### 1. 安装依赖

```bash
pip install -r backend/requirements.txt
```

### 2. 配置环境变量

项目读取根目录 `.env`，不是 `backend/.env`。

```bash
cp env.example .env
```

核心配置：

```env
LLM_PROVIDER=openai
LLM_MODEL=local-chat-model
LLM_API_KEY=internal-key
LLM_BASE_URL=http://your-internal-model-gateway/v1

VISION_PROVIDER=openai
VISION_MODEL=local-vision-model
VISION_BASE_URL=http://your-internal-model-gateway/v1

EMBEDDING_MODEL=text-embedding-local
EMBEDDING_DIM=3072

STORAGE_BACKEND=local
API_KEYS=sk-internal-demo

CUSTOM_GRAPH_EXTRACTION_ENABLED=true
CUSTOM_GRAPH_EXTRACTION_MAX_CHARS=1200
```

如果使用 Qdrant + Neo4j：

```bash
docker compose up -d qdrant neo4j
```

并配置：

```env
STORAGE_BACKEND=qdrant_neo4j
QDRANT_URL=http://localhost:6333
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
```

### 3. 启动服务

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

访问：

- 前端页面：http://localhost:8000
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/v1/health

## V1 API

### 健康检查

```http
GET /api/v1/health
GET /api/v1/health/detailed
```

### 上传文档

```http
POST /api/v1/documents/upload
Content-Type: multipart/form-data
X-API-Key: <internal-api-key>

file=<binary>
callback_url=<optional>
```

返回：

```json
{
  "code": 0,
  "message": "Document upload started",
  "data": {
    "doc_id": "uuid",
    "task_id": "uuid",
    "status": "processing",
    "filename": "manual.pdf"
  }
}
```

### 查询任务状态

```http
GET /api/v1/tasks/{task_id}
X-API-Key: <internal-api-key>
```

### 文档问答

```http
POST /api/v1/query
Content-Type: application/json
X-API-Key: <internal-api-key>

{
  "question": "总结这份文档的关键风险点",
  "mode": "mix",
  "doc_ids": [],
  "top_k": 10
}
```

### 流式问答

```http
POST /api/v1/query/stream
Content-Type: application/json
X-API-Key: <internal-api-key>

{
  "question": "这份文档涉及哪些关键设备？",
  "mode": "hybrid"
}
```

### 图谱导出

```http
GET /api/v1/graph?doc_id=<doc_id>&limit=1000
X-API-Key: <internal-api-key>
```

## 查询模式说明

| 模式 | 适用场景 |
| --- | --- |
| `mix` | 默认推荐，综合局部内容和全局关系 |
| `local` | 需要围绕局部片段回答的问题 |
| `global` | 需要从整体实体关系理解的问题 |
| `hybrid` | 需要结合向量召回和图谱关系的问题 |
| `naive` | 基础检索模式，用作 baseline |

## 测试

默认运行单元测试，不依赖外部 Qdrant / Neo4j：

```bash
cd backend
python -m pytest
```

运行单个测试文件：

```bash
cd backend
python -m pytest tests/test_config.py
```

运行集成测试前先启动外部服务：

```bash
docker compose up -d qdrant neo4j
cd backend
python -m pytest -m integration
```

## 当前边界与后续优化

当前系统更接近企业内网 AI 应用原型和 API 化前期版本，已经具备主要链路，但仍有几个适合继续补强的方向：

- 补齐问答来源追踪，返回文档、页码、chunk、分数和实体路径。
- 增加检索评估集，对比粗切分 baseline 与 KG-RAG / hybrid 检索效果。
- 将 FastAPI background task 替换或扩展为队列式任务系统。
- 补充本地模型服务部署文档。
- 增加结构化日志、模型调用超时、并发控制和运行指标。

## 许可证与致谢

MIT License

核心依赖：

- [LightRAG](https://github.com/HKUDS/LightRAG)
- [RAGAnything](https://github.com/HKUDS/RAGAnything)
- [vis.js](https://visjs.org/)

## 快速启动

```bash
# 1. 安装后端依赖
pip install -r backend/requirements.txt

# 2. 准备根目录 .env，并填写 LLM_PROVIDER / LLM_MODEL / LLM_API_KEY / LLM_BASE_URL
cp env.example .env

# 3. 如使用 Qdrant + Neo4j 存储，先启动外部服务
docker compose up -d qdrant neo4j

# 启动集成前端的 FastAPI 服务
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
