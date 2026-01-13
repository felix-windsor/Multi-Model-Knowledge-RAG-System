# 启动指南 - V2.0

## 快速启动（推荐）

### 1. 启动基础设施服务

```powershell
# 在项目根目录
docker-compose up -d
```

这将启动：
- ✅ Qdrant (端口 6333) - 向量数据库
- ✅ Redis (端口 6379) - 缓存和任务队列
- ✅ PostgreSQL (端口 5432) - 文档元数据
- ✅ MinIO (端口 9000, 9001) - 对象存储

### 2. 验证服务状态

```powershell
docker-compose ps
```

应该看到 4 个服务都是 `Up` 状态：

```
NAME              IMAGE                    STATUS
rag_minio         minio/minio:latest       Up
rag_postgres      postgres:15-alpine       Up
rag_qdrant        qdrant/qdrant:latest     Up
rag_redis         redis:7-alpine           Up
```

### 3. 启动后端服务器

```powershell
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. (可选) 启动 Celery Worker

如果要使用 Celery 进行后台任务处理：

```powershell
# 在另一个终端窗口
cd backend
celery -A app.tasks.celery_app worker --loglevel=info --pool=solo
```

**注意**: Windows 下需要添加 `--pool=solo` 参数

### 5. 访问应用

- **前端界面**: http://localhost:8000/static/index.html
- **API 文档**: http://localhost:8000/docs
- **Qdrant 仪表板**: http://localhost:6333/dashboard
- **MinIO 控制台**: http://localhost:9001 (minioadmin/minioadmin)

---

## 详细步骤

### 环境配置

1. **复制环境变量文件**:
```powershell
cd backend
copy env.example .env
```

2. **编辑 .env 文件**，设置你的 API Key:

```bash
# LLM 配置
LLM_API_KEY=sk-your-openai-key-here
LLM_MODEL=gpt-4o
LLM_BINDING_HOST=https://api.openai.com/v1

# V2.0 性能功能（已启用）
USE_CELERY=false  # 如果要用 Celery，设为 true
ENABLE_QUERY_STREAMING=true
ENABLE_SEMANTIC_CACHE=true
```

### 安装依赖

```powershell
cd backend

# 如果还没有虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 检查服务连接

```powershell
# 测试 Redis
redis-cli ping
# 应该返回: PONG

# 测试 Qdrant
curl http://localhost:6333/
# 应该返回 JSON 响应

# 测试 PostgreSQL
# 使用任何 PostgreSQL 客户端连接 localhost:5432
# 用户名: rag_user, 密码: rag_password, 数据库: rag_db
```

---

## 故障排除

### 问题 1: 端口已被占用

**错误**: `Bind for 0.0.0.0:6379 failed: port is already allocated`

**解决**:
```powershell
# 查看占用端口的进程
netstat -ano | findstr :6379

# 停止冲突服务或修改 docker-compose.yml 中的端口映射
# 例如改为 "6380:6379"
```

### 问题 2: Docker 服务无法启动

**解决**:
```powershell
# 查看日志
docker-compose logs qdrant
docker-compose logs redis

# 重启服务
docker-compose restart qdrant
```

### 问题 3: Celery Worker 启动失败

**Windows 用户常见问题**: 需要使用 `--pool=solo`

```powershell
celery -A app.tasks.celery_app worker --loglevel=info --pool=solo
```

### 问题 4: 依赖安装失败

```powershell
# 升级 pip
python -m pip install --upgrade pip

# 单独安装可能有问题的包
pip install sentence-transformers
pip install qdrant-client
pip install httpx[http2]
```

---

## 开发模式 vs 生产模式

### 开发模式（当前）

```
┌─────────────────┐
│   You (dev)     │
└────────┬────────┘
         │
    ┌────▼─────────────────────────┐
    │ FastAPI (本地运行)           │
    │ uvicorn app.main:app --reload│
    └────┬─────────────────────────┘
         │
    ┌────▼────────────────┐
    │ Docker Services     │
    │ - Qdrant            │
    │ - Redis             │
    │ - PostgreSQL        │
    │ - MinIO             │
    └─────────────────────┘
```

**优点**:
- 代码自动重载（--reload）
- 易于调试
- 快速迭代

### 生产模式（可选）

取消注释 `docker-compose.yml` 中的 `backend` 和 `celery_worker` 服务：

```powershell
docker-compose up -d
```

所有服务都在 Docker 中运行。

---

## 性能优化功能状态

检查当前启用的功能：

```python
# 在 Python REPL 中
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> os.getenv("ENABLE_QUERY_STREAMING")
'true'
>>> os.getenv("ENABLE_SEMANTIC_CACHE")
'true'
```

---

## 停止服务

### 停止后端服务器

在运行 uvicorn 的终端按 `Ctrl+C`

### 停止 Celery Worker

在运行 celery 的终端按 `Ctrl+C`

### 停止 Docker 服务

```powershell
# 停止但保留数据
docker-compose stop

# 停止并删除容器（数据保留在 ./data/ 中）
docker-compose down

# 停止并删除所有数据（慎用！）
docker-compose down -v
rm -r data/
```

---

## 监控和日志

### 查看 Docker 服务日志

```powershell
# 所有服务
docker-compose logs -f

# 特定服务
docker-compose logs -f qdrant
docker-compose logs -f redis
```

### 查看后端日志

FastAPI 日志会直接显示在终端

### 查看 Celery 日志

Celery worker 日志会显示在运行它的终端

---

## 下一步

1. ✅ 上传一个测试文档
2. ✅ 等待处理完成（查看终端日志）
3. ✅ 尝试查询功能
4. ✅ 查看知识图谱

如有问题，请参考：
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - 详细的 Docker 配置
- [QUICKSTART_V2.md](QUICKSTART_V2.md) - V2.0 完整指南
- [PERFORMANCE_OPTIMIZATIONS.md](PERFORMANCE_OPTIMIZATIONS.md) - 性能优化说明
