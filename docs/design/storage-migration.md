# API 与存储层完整迁移设计方案

> 创建日期：2026-01-28
> 状态：已设计，待实施

## 一、迁移目标

将现有的内存字典存储（`_document_store`, `_task_store`）完全替换为存储抽象层（StorageManager），实现：

- 通过环境变量 `STORAGE_BACKEND=local|database` 切换存储后端
- 保持 API 响应格式不变，确保前端和客户端无感知
- 所有 Service 层通过依赖注入获取 StorageManager
- 本地模式和数据库模式功能完全一致
- 完整的测试覆盖和文档更新

## 二、核心架构变化

### 迁移前架构

```
API Routes → Service (静态方法) → 内存字典 (_document_store)
```

### 迁移后架构

```
API Routes → Service (实例方法) → StorageManager → Local/Database Storage
                ↑
         依赖注入 (FastAPI Depends)
```

### 三大组件职责

1. **StorageManager**：统一入口，组合 documents/tasks/webhooks 三个存储实例
2. **Service 层**：业务逻辑协调，组合多个存储操作，处理事务
3. **API 层**：HTTP 接口，数据验证，调用 Service 层

## 三、数据模型改进

### Task 模型扩展

在 `backend/app/storage/models.py` 中，Task 模型需要添加 `step` 字段：

```python
class Task(BaseModel):
    """Represents a background processing task for document ingestion."""

    id: UUID
    document_id: UUID
    task_type: str
    status: TaskStatus = TaskStatus.PENDING
    progress: int = Field(default=0, ge=0, le=100)
    step: Optional[str] = None  # 新增：当前处理步骤描述
    retry_count: int = 0
    max_retries: int = 3
    last_error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
```

**用途**：存储 "准备 AI 模型"、"提取实体关系" 等步骤信息。

### ID 格式统一策略

**问题**：旧代码使用字符串 ID（`doc-xxx`），新模型使用 UUID。

**解决方案**：
1. **存储层**：统一使用 UUID（标准格式）
2. **API 层**：为了向后兼容，接受两种格式
3. **响应格式**：返回标准 UUID 字符串

**兼容性处理**：
```python
def parse_doc_id(doc_id: str) -> UUID:
    """将旧格式 ID 转换为 UUID"""
    if doc_id.startswith("doc-"):
        # 提取 hex 部分，补全到 32 位
        hex_part = doc_id[4:].replace("-", "")
        hex_full = hex_part.ljust(32, '0')
        return UUID(hex_full)
    return UUID(doc_id)
```

## 四、Service 层重构

### 从静态方法到依赖注入

**旧设计（静态方法）**：
```python
class DocumentService:
    @staticmethod
    def create_document_record(doc_id, filename, ...):
        _document_store[doc_id] = {...}
```

**新设计（依赖注入）**：
```python
class DocumentService:
    def __init__(self, storage: StorageManager):
        self.storage = storage

    async def create_document(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str
    ) -> Document:
        return await self.storage.documents.create(
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type
        )
```

### FastAPI 依赖注入

在 `backend/app/dependencies.py` 中添加：

```python
from app.storage.factory import get_storage_manager

async def get_document_service(
    storage: StorageManager = Depends(get_storage_manager)
) -> DocumentService:
    return DocumentService(storage)

async def get_task_service(
    storage: StorageManager = Depends(get_storage_manager)
) -> TaskService:
    return TaskService(storage)

async def get_webhook_service(
    storage: StorageManager = Depends(get_storage_manager)
) -> WebhookService:
    return WebhookService(storage)
```

### API 路由使用

```python
@router.post("/upload")
async def upload_document(
    file: UploadFile,
    doc_service: DocumentService = Depends(get_document_service),
    task_service: TaskService = Depends(get_task_service)
):
    # 使用注入的服务
    document = await doc_service.create_document(...)
    task = await task_service.create_task(...)
```

### 三大 Service 核心方法

**DocumentService**：
- `create_document()` - 创建文档记录
- `get_document()` - 获取单个文档
- `get_document_with_status()` - 获取文档及聚合状态
- `list_documents()` - 列出所有文档
- `list_documents_with_status()` - 批量获取文档状态
- `update_status()` - 更新文档状态
- `delete_document()` - 删除文档
- `create_document_with_task()` - 事务创建文档+任务+webhook

**TaskService**：
- `create_task()` - 创建任务
- `get_task()` - 获取任务
- `get_tasks_by_document()` - 获取文档的所有任务
- `update_progress()` - 更新进度和步骤
- `complete_task()` / `fail_task()` - 完成/失败任务
- `cancel_task()` - 取消任务

**WebhookService**：
- `create_webhook()` - 注册回调
- `get_webhooks_by_document()` - 获取文档的回调
- `deliver_webhook()` - 发送回调（实际 HTTP 请求）
- `mark_delivered()` / `mark_failed()` - 标记状态
- `retry_failed_webhooks()` - 重试失败的回调

## 五、事务支持与错误处理

### 事务场景

文档上传流程需要原子性操作：

```python
async def upload_document_flow(file, callback_url):
    # 这三个操作需要保证原子性
    document = await storage.documents.create(...)      # 1
    task = await storage.tasks.create(...)              # 2
    if callback_url:
        webhook = await storage.webhooks.create(...)    # 3
```

如果步骤 2 失败，步骤 1 应该回滚，否则会有孤儿数据。

### 存储抽象层添加事务接口

在 `backend/app/storage/base.py` 中添加：

```python
class DocumentStorage(ABC):
    @abstractmethod
    async def begin_transaction(self):
        """开始事务"""
        pass

    @abstractmethod
    async def commit_transaction(self):
        """提交事务"""
        pass

    @abstractmethod
    async def rollback_transaction(self):
        """回滚事务"""
        pass
```

TaskStorage 和 WebhookStorage 同样添加。

### 数据库实现：真实事务

```python
# DatabaseDocumentStorage
async def begin_transaction(self):
    self.conn = await self.pool.acquire()
    self.tx = self.conn.transaction()
    await self.tx.start()

async def commit_transaction(self):
    await self.tx.commit()
    await self.pool.release(self.conn)

async def rollback_transaction(self):
    await self.tx.rollback()
    await self.pool.release(self.conn)
```

### 本地实现：补偿机制

```python
# LocalDocumentStorage
async def begin_transaction(self):
    # 记录当前状态快照
    self._tx_snapshot = copy.deepcopy(self._store)

async def rollback_transaction(self):
    # 恢复到快照状态
    self._store = self._tx_snapshot
    self._tx_snapshot = None
```

### StorageManager 统一事务接口

```python
class StorageManager:
    async def begin_transaction(self):
        await self.documents.begin_transaction()
        await self.tasks.begin_transaction()
        await self.webhooks.begin_transaction()

    async def commit(self):
        await self.documents.commit_transaction()
        await self.tasks.commit_transaction()
        await self.webhooks.commit_transaction()

    async def rollback(self):
        await self.documents.rollback_transaction()
        await self.tasks.rollback_transaction()
        await self.webhooks.rollback_transaction()
```

### Service 层使用事务

```python
class DocumentService:
    async def create_document_with_task(
        self,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str,
        callback_url: Optional[str] = None
    ) -> tuple[Document, Task, Optional[Webhook]]:
        """事务创建文档、任务、Webhook"""
        try:
            await self.storage.begin_transaction()

            # 创建文档
            document = await self.storage.documents.create(
                filename=filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=mime_type
            )

            # 创建任务
            task = await self.storage.tasks.create(
                document_id=document.id,
                task_type="document_processing"
            )

            # 创建 webhook（如果需要）
            webhook = None
            if callback_url:
                webhook = await self.storage.webhooks.create(
                    document_id=document.id,
                    callback_url=callback_url,
                    event_type="document.processed"
                )

            await self.storage.commit()
            return document, task, webhook

        except Exception as e:
            await self.storage.rollback()
            raise ServiceError(f"Failed to create document: {e}")
```

### 错误处理层次

1. **存储层错误**：数据库连接失败、文件 I/O 错误 → 抛出 `StorageError`
2. **Service 层错误**：业务逻辑错误 → 抛出 `ServiceError`
3. **API 层错误**：捕获并转换为 HTTP 状态码

```python
# 自定义异常
class StorageError(Exception):
    """存储层错误"""
    pass

class ServiceError(Exception):
    """业务逻辑错误"""
    pass

# API 层处理
@router.post("/upload")
async def upload_document(...):
    try:
        result = await doc_service.create_document_with_task(...)
        return wrap_response(data=result)
    except StorageError as e:
        raise HTTPException(status_code=500, detail="Storage error")
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## 六、API 响应聚合与数据查询

### 聚合查询需求

GET `/api/v1/documents/{doc_id}` 需要返回完整的文档状态：

```json
{
  "doc_id": "uuid",
  "filename": "example.pdf",
  "status": "processing",
  "progress": 45,              // 来自 Task
  "step": "提取实体关系",       // 来自 Task
  "chunks_count": 12,          // 来自 Task.result
  "callback_url": "https://...", // 来自 Webhook
  "created_at": "...",
  "updated_at": "..."
}
```

### DocumentService 聚合方法

```python
class DocumentService:
    async def get_document_with_status(
        self,
        doc_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """获取文档及其处理状态（聚合 Document + Task + Webhook）"""

        # 1. 获取文档基本信息
        document = await self.storage.documents.get(doc_id)
        if not document:
            return None

        # 2. 获取最新任务（按创建时间倒序）
        tasks = await self.storage.tasks.get_by_document(doc_id)
        latest_task = tasks[0] if tasks else None

        # 3. 获取 webhook（如果有）
        webhooks = await self.storage.webhooks.get_by_document(doc_id)
        webhook = webhooks[0] if webhooks else None

        # 4. 组合数据
        return {
            "doc_id": str(document.id),
            "filename": document.filename,
            "file_path": document.file_path,
            "file_size": document.file_size,
            "status": latest_task.status if latest_task else document.status,
            "progress": latest_task.progress if latest_task else 0,
            "step": latest_task.step if latest_task else "等待处理",
            "chunks_count": (
                latest_task.result.get("chunks_count", 0)
                if latest_task and latest_task.result
                else 0
            ),
            "callback_url": webhook.callback_url if webhook else None,
            "error_message": document.error_message or (
                latest_task.last_error if latest_task else None
            ),
            "created_at": document.created_at,
            "updated_at": document.updated_at
        }
```

### 批量查询优化

列表接口需要避免 N+1 查询，添加批量查询接口：

**存储抽象层扩展**：
```python
class TaskStorage(ABC):
    @abstractmethod
    async def get_by_documents_batch(
        self,
        doc_ids: List[UUID]
    ) -> List[Task]:
        """批量查询多个文档的任务"""
        pass
```

**DocumentService 批量方法**：
```python
async def list_documents_with_status(
    self,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """批量获取文档状态"""

    # 1. 获取所有文档
    documents = await self.storage.documents.list(limit=limit)

    # 2. 批量获取所有文档的任务（一次查询）
    doc_ids = [doc.id for doc in documents]
    all_tasks = await self.storage.tasks.get_by_documents_batch(doc_ids)

    # 3. 按 document_id 分组
    tasks_by_doc = {}
    for task in all_tasks:
        if task.document_id not in tasks_by_doc:
            tasks_by_doc[task.document_id] = []
        tasks_by_doc[task.document_id].append(task)

    # 4. 组合数据
    results = []
    for doc in documents:
        tasks = tasks_by_doc.get(doc.id, [])
        latest_task = max(tasks, key=lambda t: t.created_at) if tasks else None

        results.append({
            "doc_id": str(doc.id),
            "filename": doc.filename,
            "status": latest_task.status if latest_task else doc.status,
            "progress": latest_task.progress if latest_task else 0,
            "step": latest_task.step if latest_task else "等待处理",
            "created_at": doc.created_at,
            "updated_at": doc.updated_at
        })

    return results
```

## 七、测试策略

### 测试层次

1. **单元测试**：测试单个组件
   - 存储层测试：Local/Database 实现的 CRUD 操作
   - Service 层测试：业务逻辑（使用 mock storage）
   - 工具函数测试：ID 转换、数据验证等

2. **集成测试**：测试完整流程
   - API 端到端测试：上传 → 处理 → 查询 → 删除
   - 事务测试：回滚机制是否正确
   - 并发测试：多个请求同时处理

### 测试框架

```python
# backend/requirements-dev.txt
pytest==7.4.0
pytest-asyncio==0.21.0
pytest-cov==4.1.0
httpx==0.24.0           # 测试 FastAPI
faker==19.0.0           # 生成测试数据
```

### 测试目录结构

```
backend/tests/
├── conftest.py                    # pytest fixtures
├── unit/
│   ├── storage/
│   │   ├── test_local_storage.py
│   │   └── test_database_storage.py
│   └── services/
│       ├── test_document_service.py
│       ├── test_task_service.py
│       └── test_webhook_service.py
├── integration/
│   ├── test_document_flow.py     # 完整上传处理流程
│   ├── test_query_flow.py        # 查询流程
│   └── test_transaction.py       # 事务测试
└── fixtures/
    └── sample_documents/          # 测试文件
```

### 关键 Fixtures

```python
# conftest.py
import pytest
from app.storage.factory import create_storage_manager

@pytest.fixture
async def local_storage():
    """本地存储实例（使用临时目录）"""
    storage = await create_storage_manager(backend="local", test_mode=True)
    yield storage
    await storage.cleanup()

@pytest.fixture
async def database_storage():
    """数据库存储实例（使用测试数据库）"""
    storage = await create_storage_manager(
        backend="database",
        database_url="postgresql://test:test@localhost:5432/test_ragdb"
    )
    yield storage
    await storage.cleanup()

@pytest.fixture
def sample_document_file():
    """示例文档文件"""
    from io import BytesIO
    content = b"Sample PDF content"
    return BytesIO(content)
```

### 测试覆盖率目标

- 存储层：90%+ 覆盖率
- Service 层：85%+ 覆盖率
- API 层：80%+ 覆盖率

## 八、实施计划

### 分阶段迁移策略

**阶段 1：模型与存储层完善（1-2 天）**
- [ ] 1.1 修改 `backend/app/storage/models.py`，Task 添加 `step` 字段
- [ ] 1.2 修改 `backend/app/storage/base.py`，添加 `get_by_documents_batch` 接口
- [ ] 1.3 修改 `backend/app/storage/base.py`，添加事务接口（begin/commit/rollback）
- [ ] 1.4 实现 LocalDocumentStorage 的批量查询
- [ ] 1.5 实现 LocalTaskStorage 的批量查询
- [ ] 1.6 实现 DatabaseDocumentStorage 的批量查询
- [ ] 1.7 实现 DatabaseTaskStorage 的批量查询
- [ ] 1.8 实现数据库存储的事务支持
- [ ] 1.9 本地存储的补偿式事务
- [ ] 1.10 单元测试：存储层新功能

**阶段 2：Service 层重构（2-3 天）**
- [ ] 2.1 重构 DocumentService 为实例方法
- [ ] 2.2 实现 DocumentService.create_document()
- [ ] 2.3 实现 DocumentService.get_document_with_status()
- [ ] 2.4 实现 DocumentService.list_documents_with_status()
- [ ] 2.5 实现 DocumentService.create_document_with_task()（事务）
- [ ] 2.6 重构 TaskService 为实例方法
- [ ] 2.7 实现 TaskService 的所有方法
- [ ] 2.8 重构 WebhookService 为实例方法
- [ ] 2.9 实现 WebhookService 的所有方法
- [ ] 2.10 单元测试：Service 层

**阶段 3：依赖注入与 API 集成（2-3 天）**
- [ ] 3.1 更新 `backend/app/dependencies.py` 添加 Service 注入函数
- [ ] 3.2 更新 `backend/app/api/v1/documents.py` 使用新 Service
- [ ] 3.3 更新 `backend/app/api/v1/query.py`（如果涉及）
- [ ] 3.4 更新 `backend/app/api/v1/tasks.py` 使用新 Service
- [ ] 3.5 更新 `backend/app/api/upload.py` (Legacy) 使用新 Service
- [ ] 3.6 更新 `backend/app/api/documents.py` (Legacy) 使用新 Service
- [ ] 3.7 删除旧的内存存储代码
- [ ] 3.8 集成测试：完整 API 流程

**阶段 4：完整测试与文档（1-2 天）**
- [ ] 4.1 端到端测试：上传 → 处理 → 查询 → 删除
- [ ] 4.2 测试本地模式和数据库模式切换
- [ ] 4.3 测试事务回滚机制
- [ ] 4.4 测试并发场景
- [ ] 4.5 性能基准测试（可选）
- [ ] 4.6 更新 API 文档
- [ ] 4.7 更新 CLAUDE.md
- [ ] 4.8 Git commit 和 PR

### 回滚计划

每个阶段完成后创建 git tag：
```bash
git tag api-migration-phase-1
git tag api-migration-phase-2
git tag api-migration-phase-3
git tag api-migration-phase-4
```

## 九、配置管理与部署

### 环境变量配置

```bash
# === 存储后端配置 ===
STORAGE_BACKEND=local              # local | database

# === 本地存储配置 ===
LOCAL_STORAGE_DIR=./data/storage   # JSON 文件存储路径

# === PostgreSQL 配置（元数据、任务、Webhook）===
DATABASE_URL=postgresql+asyncpg://rag:password@localhost:5432/ragdb
DATABASE_POOL_SIZE=10              # 连接池大小
DATABASE_MAX_OVERFLOW=20           # 最大溢出连接
DATABASE_POOL_TIMEOUT=30           # 连接超时（秒）

# === Qdrant 配置（向量存储）===
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# === Neo4j 配置（知识图谱）===
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=rag123456
NEO4J_DATABASE=neo4j

# === 性能优化 ===
ENABLE_QUERY_CACHE=true            # 启用查询缓存
CACHE_TTL=300                      # 缓存过期时间（秒）
```

### 配置验证

```python
# backend/app/config.py
class Settings(BaseSettings):
    STORAGE_BACKEND: str = "local"
    DATABASE_URL: Optional[str] = None

    def validate_storage_config(self):
        """验证存储配置"""
        if self.STORAGE_BACKEND == "database":
            if not self.DATABASE_URL:
                raise ValueError(
                    "DATABASE_URL is required when STORAGE_BACKEND=database"
                )
```

### 优雅启动与关闭

```python
# backend/app/main.py
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时
    settings = get_settings()
    settings.validate_storage_config()

    storage_manager = await create_storage_manager(
        backend=settings.STORAGE_BACKEND,
        database_url=settings.DATABASE_URL
    )
    app.state.storage = storage_manager

    logger.info(f"Storage backend: {settings.STORAGE_BACKEND}")

    yield

    # 关闭时
    await storage_manager.close()
    logger.info("Storage closed gracefully")

app = FastAPI(lifespan=lifespan)
```

### 部署场景

**场景 1：开发/本地模式**
```bash
STORAGE_BACKEND=local
# 所有数据存本地 JSON 文件
# - 文档元数据：data/storage/documents.json
# - 向量：data/storage/vdb_*.json
# - 图谱：data/storage/graph_*.graphml
```

**场景 2：生产/数据库模式**
```bash
STORAGE_BACKEND=database

# PostgreSQL（文档元数据、任务、Webhook）
DATABASE_URL=postgresql+asyncpg://rag:rag123@postgres:5432/ragdb

# Qdrant（向量存储 - LightRAG 已集成）
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# Neo4j（知识图谱 - LightRAG 已集成）
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=rag123456

# 启动完整环境
docker-compose up -d
```

**说明**：当 `STORAGE_BACKEND=database` 时，同时启用：
- PostgreSQL（本次迁移重点）
- Qdrant（LightRAG 已支持）
- Neo4j（LightRAG 已支持）

### 性能优化点

1. **连接池复用**：数据库连接池在启动时创建，所有请求共享
2. **批量查询**：使用 `get_by_documents_batch` 减少数据库往返
3. **响应缓存**：文档状态缓存 5 分钟（可配置）
4. **异步 I/O**：并发获取文档、任务、webhook 数据

```python
# 并发获取示例
document, tasks, webhooks = await asyncio.gather(
    storage.documents.get(doc_id),
    storage.tasks.get_by_document(doc_id),
    storage.webhooks.get_by_document(doc_id)
)
```

## 十、验收标准

### 功能验收

- [ ] 所有现有 API 功能正常（Legacy + V1）
- [ ] 本地模式和数据库模式功能一致
- [ ] 事务回滚正确工作
- [ ] Webhook 回调正常触发
- [ ] 文档上传、处理、查询、删除完整流程

### 性能验收

- [ ] 文档上传响应时间 < 500ms
- [ ] 文档列表查询（100 条）< 200ms
- [ ] 数据库模式下并发 10 请求无错误
- [ ] 内存占用无明显增加

### 测试验收

- [ ] 单元测试覆盖率 > 85%
- [ ] 集成测试通过
- [ ] 端到端测试通过
- [ ] 本地/数据库模式切换测试通过

### 文档验收

- [ ] API 文档更新
- [ ] CLAUDE.md 更新
- [ ] 设计文档完整
- [ ] 实施计划详细

## 十一、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| API 响应格式变化导致前端兼容性问题 | 前端报错，用户无法使用 | 保持响应格式不变，增加集成测试 |
| 事务实现不完善导致数据不一致 | 孤儿数据，状态异常 | 充分测试事务回滚，添加数据一致性检查 |
| 性能下降影响用户体验 | 响应变慢，超时 | 批量查询优化，连接池配置，性能基准测试 |
| 迁移过程引入 bug | 功能异常，数据丢失 | 分阶段迁移，充分测试，保留回滚能力 |
| ID 格式兼容性问题 | 旧数据无法访问 | ID 转换函数，向后兼容处理 |

## 十二、后续优化方向

1. **缓存层**：引入 Redis 缓存文档状态，减少数据库查询
2. **消息队列**：使用 Celery/RabbitMQ 处理后台任务，提高可靠性
3. **读写分离**：数据库主从复制，读写分离提升性能
4. **API 版本化**：逐步弃用 Legacy API，统一使用 V1 API
5. **监控告警**：添加存储层性能监控，及时发现问题

---

**设计完成日期**：2026-01-28
**预计实施周期**：6-10 天
**优先级**：高
