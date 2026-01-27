# 数据库存储迁移设计方案

> 创建日期：2026-01-27
> 状态：待实施

## 一、项目目标

将 Multi-Model Knowledge RAG System 的数据从本地文件存储迁移到专业数据库，支持通过配置切换存储后端。

## 二、技术选型

| 数据类型 | 存储方案 | 选型理由 |
|---------|---------|---------|
| 文档元数据 / 任务 / Webhook | **PostgreSQL** | 关系型数据，事务支持，成熟稳定 |
| 向量 Embedding | **Qdrant** | 轻量高性能，API 友好，LightRAG 原生支持 |
| 知识图谱 | **Neo4j** | 图数据库标杆，Cypher 查询强大，生态成熟 |
| 部署方式 | **Docker Compose** | 一键启动，适合开发和小型生产环境 |
| 迁移策略 | **配置切换** | 通过环境变量切换存储后端，灵活可回退 |

## 三、架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│                   Storage Abstraction Layer                  │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │ DocumentStore │  │  TaskStore    │  │ WebhookStore  │   │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘   │
│          │                  │                  │            │
│    ┌─────┴─────┐      ┌─────┴─────┐      ┌─────┴─────┐     │
│    ▼           ▼      ▼           ▼      ▼           ▼     │
│  Local    PostgreSQL Local    PostgreSQL Local   PostgreSQL │
├─────────────────────────────────────────────────────────────┤
│                      LightRAG Core                           │
│          ┌─────────────────┬─────────────────┐              │
│          ▼                 ▼                 ▼              │
│       NanoVec           Qdrant           NetworkX           │
│       (local)          (database)         (local)           │
│                                              │              │
│                                           Neo4j             │
│                                         (database)          │
└─────────────────────────────────────────────────────────────┘
```

核心思路：
- 新增存储抽象层，定义统一接口
- 每种存储类型有两个实现：本地版 + 数据库版
- 通过 `STORAGE_BACKEND` 环境变量切换
- LightRAG 的向量和图谱存储通过其原生插件机制对接

## 四、数据模型

### 4.1 PostgreSQL 表结构

```sql
-- 文档表
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    file_size BIGINT,
    mime_type VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 任务表
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    last_error TEXT,
    result JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Webhook 表
CREATE TABLE webhooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    callback_url VARCHAR(500) NOT NULL,
    event_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    last_error TEXT,
    next_retry_at TIMESTAMP,
    delivered_at TIMESTAMP
);

-- 索引
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_document_id ON tasks(document_id);
CREATE INDEX idx_webhooks_status ON webhooks(status);
CREATE INDEX idx_webhooks_next_retry ON webhooks(next_retry_at)
    WHERE status = 'pending';
```

### 4.2 Qdrant Collection

```
Collection: documents
├── Vector: 文档/段落的 embedding（1024 或 3072 维）
├── Payload（附加数据）:
│   ├── doc_id: 文档 ID
│   ├── chunk_id: 分块 ID
│   ├── content: 原文内容
│   └── metadata: 其他元数据
└── Index: HNSW 索引（自动创建）
```

### 4.3 Neo4j 节点/关系

```
节点（Nodes）:
├── :Entity {id, name, type, description}
├── :Document {id, filename, created_at}
└── :Chunk {id, content, doc_id}

关系（Relationships）:
├── [:RELATED_TO {weight, description}]
├── [:EXTRACTED_FROM]
└── [:BELONGS_TO]
```

## 五、存储抽象层接口

```python
# backend/app/storage/base.py

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime


class DocumentStorage(ABC):
    """文档元数据的存储接口"""

    @abstractmethod
    async def create(self, filename: str, file_path: str,
                     file_size: int, mime_type: str) -> Document:
        pass

    @abstractmethod
    async def get(self, doc_id: UUID) -> Optional[Document]:
        pass

    @abstractmethod
    async def list(self, status: str = None,
                   limit: int = 100, offset: int = 0) -> List[Document]:
        pass

    @abstractmethod
    async def update_status(self, doc_id: UUID, status: str,
                           error_message: str = None) -> bool:
        pass

    @abstractmethod
    async def delete(self, doc_id: UUID) -> bool:
        pass


class TaskStorage(ABC):
    """任务的存储接口"""

    @abstractmethod
    async def create(self, document_id: UUID, task_type: str) -> Task:
        pass

    @abstractmethod
    async def get(self, task_id: UUID) -> Optional[Task]:
        pass

    @abstractmethod
    async def get_by_document(self, document_id: UUID) -> List[Task]:
        pass

    @abstractmethod
    async def list_pending(self, limit: int = 10) -> List[Task]:
        pass

    @abstractmethod
    async def start(self, task_id: UUID) -> bool:
        pass

    @abstractmethod
    async def update_progress(self, task_id: UUID, progress: int) -> bool:
        pass

    @abstractmethod
    async def complete(self, task_id: UUID, result: Any = None) -> bool:
        pass

    @abstractmethod
    async def fail(self, task_id: UUID, error: str) -> bool:
        pass

    @abstractmethod
    async def cancel(self, task_id: UUID) -> bool:
        pass


class WebhookStorage(ABC):
    """Webhook 的存储接口"""

    @abstractmethod
    async def create(self, document_id: UUID, callback_url: str,
                     event_type: str) -> Webhook:
        pass

    @abstractmethod
    async def get(self, webhook_id: UUID) -> Optional[Webhook]:
        pass

    @abstractmethod
    async def get_by_document(self, document_id: UUID) -> List[Webhook]:
        pass

    @abstractmethod
    async def list_pending(self, limit: int = 10) -> List[Webhook]:
        pass

    @abstractmethod
    async def mark_delivered(self, webhook_id: UUID) -> bool:
        pass

    @abstractmethod
    async def mark_failed(self, webhook_id: UUID, error: str,
                          retry_after: datetime = None) -> bool:
        pass


class StorageManager:
    """统一管理所有存储实例"""

    def __init__(self, documents: DocumentStorage,
                 tasks: TaskStorage, webhooks: WebhookStorage):
        self.documents = documents
        self.tasks = tasks
        self.webhooks = webhooks
```

## 六、RAG 存储集成

### 6.1 Qdrant 配置

```python
# backend/app/core/rag_factory.py

from lightrag.kg.qdrant_impl import QdrantStorage
from qdrant_client import QdrantClient

def create_rag_instance(settings) -> LightRAG:
    vector_storage = None

    if settings.STORAGE_BACKEND == "database":
        qdrant_client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            timeout=30,
        )
        if not _check_qdrant_health(qdrant_client):
            raise RuntimeError("Qdrant connection failed")

        vector_storage = QdrantStorage(
            client=qdrant_client,
            collection_name="documents",
            embedding_dim=settings.EMBEDDING_DIM,
        )

    return LightRAG(
        working_dir=settings.DATA_DIR,
        vector_storage=vector_storage,
        # ...
    )


def _check_qdrant_health(client) -> bool:
    try:
        client.get_collections()
        return True
    except Exception:
        return False
```

### 6.2 Neo4j 配置

```python
from lightrag.kg.neo4j_impl import Neo4jStorage
from neo4j import GraphDatabase

def create_rag_instance(settings) -> LightRAG:
    graph_storage = None

    if settings.STORAGE_BACKEND == "database":
        neo4j_driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
            max_connection_lifetime=300,
            max_connection_pool_size=10,
        )
        if not _check_neo4j_health(neo4j_driver):
            raise RuntimeError("Neo4j connection failed")

        graph_storage = Neo4jStorage(
            driver=neo4j_driver,
            database=settings.NEO4J_DATABASE,
        )

    return LightRAG(
        working_dir=settings.DATA_DIR,
        vector_storage=vector_storage,
        graph_storage=graph_storage,
    )


def _check_neo4j_health(driver) -> bool:
    try:
        with driver.session() as session:
            session.run("RETURN 1")
        return True
    except Exception:
        return False
```

## 七、Docker Compose 配置

### 7.1 docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./data/uploads:/app/data/uploads
      - ./data/output:/app/data/output
    depends_on:
      postgres:
        condition: service_healthy
      qdrant:
        condition: service_healthy
      neo4j:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped
    networks:
      - rag-network
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 1G

  postgres:
    image: postgres:16-alpine
    env_file:
      - .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - rag-network
    deploy:
      resources:
        limits:
          memory: 1G

  qdrant:
    image: qdrant/qdrant:latest
    volumes:
      - qdrant_data:/qdrant/storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/healthz"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - rag-network
    deploy:
      resources:
        limits:
          memory: 2G

  neo4j:
    image: neo4j:5-community
    env_file:
      - .env
    environment:
      NEO4J_AUTH: ${NEO4J_USER}/${NEO4J_PASSWORD}
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j_data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7474"]
      interval: 10s
      timeout: 10s
      retries: 5
    restart: unless-stopped
    networks:
      - rag-network
    deploy:
      resources:
        limits:
          memory: 2G

networks:
  rag-network:
    driver: bridge

volumes:
  postgres_data:
  qdrant_data:
  neo4j_data:
```

### 7.2 docker-compose.prod.yml

```yaml
version: '3.8'

services:
  postgres:
    ports: []

  qdrant:
    ports: []

  neo4j:
    ports: []
```

### 7.3 访问地址

| 服务 | 地址 | 用途 |
|------|------|------|
| 应用 | http://localhost:8000 | 主应用 |
| API 文档 | http://localhost:8000/docs | Swagger UI |
| Neo4j 浏览器 | http://localhost:7474 | 图谱可视化管理 |
| Qdrant 面板 | http://localhost:6333/dashboard | 向量数据管理 |

## 八、环境变量

```bash
# .env.example

# === 存储后端 ===
STORAGE_BACKEND=local  # local | database

# === PostgreSQL ===
POSTGRES_USER=rag
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_DB=ragdb
DATABASE_URL=postgresql://rag:your-secure-password-here@postgres:5432/ragdb

# === Qdrant ===
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# === Neo4j ===
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-secure-password-here
NEO4J_DATABASE=neo4j
```

## 九、文件结构

```
backend/
├── app/
│   ├── api/v1/              # API 路由（已有）
│   ├── services/            # 业务逻辑（已有）
│   ├── models/              # 数据模型（已有）
│   ├── storage/             # 新增：存储层
│   │   ├── __init__.py
│   │   ├── base.py          # 抽象接口
│   │   ├── local/           # 本地实现
│   │   │   ├── document.py
│   │   │   ├── task.py
│   │   │   └── webhook.py
│   │   └── database/        # 数据库实现
│   │       ├── document.py
│   │       ├── task.py
│   │       ├── webhook.py
│   │       └── connection.py
│   ├── core/                # 新增：核心组件
│   │   └── rag_factory.py   # RAG 实例工厂
│   └── config.py            # 配置（扩展）
├── scripts/
│   └── init.sql             # 数据库初始化
└── tests/
    └── storage/             # 存储层测试
        ├── test_local.py
        └── test_database.py

# 根目录
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
└── Dockerfile
```

## 十、实施步骤

### 阶段一：基础设施（1-2 天）

**目标：** 数据库服务能启动并连接

- [ ] 1.1 创建 docker-compose.yml
- [ ] 1.2 创建 docker-compose.prod.yml
- [ ] 1.3 创建 .env.example 模板
- [ ] 1.4 创建 scripts/init.sql
- [ ] 1.5 验证：docker-compose up -d 所有服务健康
- [ ] 1.6 验证：能连接 PostgreSQL
- [ ] 1.7 验证：能访问 Qdrant Dashboard
- [ ] 1.8 验证：能访问 Neo4j Browser

### 阶段二：存储抽象层（2-3 天）

**目标：** 定义接口 + 本地实现，现有功能不受影响

- [ ] 2.1 创建存储层目录结构
- [ ] 2.2 实现 DocumentStorage 接口
- [ ] 2.3 实现 TaskStorage 接口
- [ ] 2.4 实现 WebhookStorage 接口
- [ ] 2.5 实现 LocalDocumentStorage
- [ ] 2.6 实现 LocalTaskStorage
- [ ] 2.7 实现 LocalWebhookStorage
- [ ] 2.8 创建 StorageManager 和工厂函数
- [ ] 2.9 修改现有 Service 层使用新接口
- [ ] 2.10 验证：STORAGE_BACKEND=local 时所有功能正常

### 阶段三：数据库实现（3-5 天）

**目标：** 实现三个数据库的存储层

- [ ] 3.1 创建数据库实现目录结构
- [ ] 3.2 实现 PostgreSQL 连接池
- [ ] 3.3 实现 DatabaseDocumentStorage
- [ ] 3.4 实现 DatabaseTaskStorage
- [ ] 3.5 实现 DatabaseWebhookStorage
- [ ] 3.6 单元测试：PostgreSQL 存储层
- [ ] 3.7 配置 LightRAG 使用 Qdrant
- [ ] 3.8 测试：向量存储和检索
- [ ] 3.9 配置 LightRAG 使用 Neo4j
- [ ] 3.10 测试：图谱存储和查询
- [ ] 3.11 实现健康检查
- [ ] 3.12 实现优雅关闭

### 阶段四：集成测试与切换（1-2 天）

**目标：** 完整流程验证，确保可以在两种模式间切换

- [ ] 4.1 端到端测试：上传 → 处理 → 查询 → 返回
- [ ] 4.2 测试：Webhook 回调正常触发
- [ ] 4.3 测试：任务重试机制
- [ ] 4.4 测试：删除文档级联删除
- [ ] 4.5 测试：Neo4j 图谱可视化
- [ ] 4.6 测试：切换 STORAGE_BACKEND 后数据隔离
- [ ] 4.7 更新文档
- [ ] 4.8 性能基准测试（可选）

## 十一、验收标准

```bash
# 1. 本地模式正常
STORAGE_BACKEND=local pytest backend/tests/ -v  # 全部通过

# 2. 数据库模式正常
STORAGE_BACKEND=database pytest backend/tests/ -v  # 全部通过

# 3. 端到端流程
上传文档 → 处理完成 → 查询返回结果 → 图谱可查 → Webhook 触发
```

## 十二、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| LightRAG 对 Qdrant/Neo4j 支持不完善 | 需要修改 LightRAG 代码 | 提前验证 LightRAG 插件接口 |
| 数据迁移丢失 | 历史数据不可用 | 配置切换模式，可随时回退 |
| 性能下降 | 网络延迟影响响应 | 使用连接池，合理配置超时 |
| 运维复杂度增加 | 多服务管理困难 | Docker Compose 统一管理 |
