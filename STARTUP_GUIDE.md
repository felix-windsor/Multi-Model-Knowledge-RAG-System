# 项目启动指南

本文档提供知识图谱 RAG 系统的完整启动方法。

## 重要提示

**本项目采用前后端集成架构:**
- **只需启动后端服务器**,前端会自动可用
- 访问 `http://localhost:8000` 即可使用完整系统
- 无需单独启动前端服务器
- 前后端同源,无 CORS 跨域问题

---

## 前置要求

- **Python**: 3.8+ (推荐 3.10+)
- **Conda 环境**: raganything (已配置)
- **API Key**: OpenAI API Key (或其他支持的 LLM 提供商)
- **操作系统**: Windows, Linux, 或 macOS

---

## 快速启动 (推荐)

### 方式一: 使用启动脚本

**Windows:**
```bash
cd d:\code_project\Multi-Model-Knowledge-RAG-System
scripts\start.bat
```

**Linux/Mac:**
```bash
cd /path/to/Multi-Model-Knowledge-RAG-System
chmod +x scripts/start.sh
./scripts/start.sh
```

---

## 手动启动 (详细步骤)

### 第 1 步: 激活 Conda 环境

```bash
conda activate raganything
```

### 第 2 步: 进入项目目录

```bash
cd d:\code_project\Multi-Model-Knowledge-RAG-System\backend
```

### 第 3 步: 配置环境变量

检查并编辑 `.env` 文件:

```bash
# 如果 .env 不存在,从模板复制
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# 编辑配置文件
notepad .env              # Windows
nano .env                 # Linux/Mac
```

**必填配置项:**

```env
# LLM 配置 (必填)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-your-openai-api-key-here
LLM_BASE_URL=https://api.openai.com/v1

# Embedding 配置
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIM=3072

# 存储路径 (可选,使用默认值)
STORAGE_DIR=../data/storage
UPLOAD_DIR=../data/uploads
OUTPUT_DIR=../data/output
```

**支持的 LLM 提供商:**
- `openai` - OpenAI GPT 系列
- `qwen` - 阿里云通义千问
- `ollama` - 本地 Ollama
- `lmstudio` - LM Studio

### 第 4 步: 安装依赖 (首次运行)

如果是首次运行或更新了依赖,需要安装:

```bash
pip install -r requirements.txt
```

**如果遇到安装问题:**

```bash
# 手动安装核心依赖
pip install --no-deps lightrag-hku
pip install fastapi uvicorn[standard] python-multipart python-dotenv
pip install pydantic pydantic-settings aiofiles
pip install mineru huggingface_hub Pillow reportlab markdown weasyprint
pip install configparser google-api-core google-genai nano-vectordb
pip install pandas pipmaster pypinyin xlsxwriter

# 升级到兼容版本
pip install "fastapi>=0.115.0" --upgrade
```

### 第 5 步: 启动服务器

**推荐方式 (开发模式,带热重载):**

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**其他启动方式:**

```bash
# 方式 A: 直接运行 Python 模块
python -m app.main

# 方式 B: 不带重载 (生产模式)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 方式 C: 多进程模式 (生产环境)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 方式 D: 指定不同端口
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 第 6 步: 验证启动成功

服务器启动后,你应该看到类似输出:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**快速验证 (3 步):**

**1. 测试健康检查**
```bash
curl http://localhost:8000/health
# 期望输出: {"status":"healthy"}
```

**2. 访问前端页面**
- 在浏览器中打开: http://localhost:8000
- 期望看到: 知识图谱 RAG 系统界面 (包含文档上传、知识查询、知识图谱三个区域)

**3. 测试 API 端点**
```bash
curl http://localhost:8000/api/documents
# 期望输出: [] (空数组,表示暂无文档)
```

**如果以上三项都成功,说明系统已正常启动。**

---

## 🌐 访问项目

启动成功后,可以通过以下地址访问:

| 功能 | URL | 说明 |
|------|-----|------|
| **前端主页** | http://localhost:8000 | Web UI (文档上传、知识查询、图谱可视化) |
| **API 文档** | http://localhost:8000/docs | Swagger UI 交互式文档 |
| **API 备选文档** | http://localhost:8000/redoc | ReDoc 风格文档 |
| **健康检查** | http://localhost:8000/health | 服务器状态检查 |
| **静态资源** | http://localhost:8000/static/* | 前端静态文件 (CSS, JS, 图片等) |

---

## 🎨 前端访问

**前端已集成在后端服务器中,无需单独启动!**

只要后端服务器运行,前端就会自动可用:

### 推荐方式: 直接访问集成前端

启动后端后,直接在浏览器中访问:
```
http://localhost:8000
```

**优势:**
- 无需单独启动前端服务器
- 前后端同源,无 CORS 问题
- 所有 API 自动可用
- 静态资源正确加载

### 🔧 开发调试方式 (可选)

如果需要单独调试前端,可以使用以下方式:

**方式 1: 直接打开文件**
```bash
# Windows
start frontend\index.html

# Linux/Mac
open frontend/index.html
```
⚠️ **注意**: 此方式可能存在 CORS 跨域问题,需要配置浏览器允许本地文件访问。

**方式 2: VS Code Live Server**
1. 安装 VS Code 扩展: "Live Server"
2. 打开 `frontend/index.html`
3. 右键选择 "Open with Live Server"
4. 修改 `frontend/assets/js/config.js` 中的 API 地址为 `http://localhost:8000/api`

⚠️ **注意**: 使用此方式时,确保修改前端的 API 配置指向后端服务器

---

## 📚 使用示例

### 1. 上传文档

**使用 API:**

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@your_document.pdf"
```

**使用前端:**
- 访问 http://localhost:8000
- 在左侧"文档上传"区域点击"选择文件"
- 选择文档后点击"上传文档"
- 在文档列表中查看处理状态

### 2. 知识查询

**使用 API:**

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "这个文档主要讲了什么?",
    "mode": "mix"
  }'
```

**查询模式说明:**
- `mix` - 混合模式 (推荐,自动选择最佳策略)
- `local` - 本地模式 (基于实体检索)
- `global` - 全局模式 (基于社区检索)
- `hybrid` - 混合检索 (结合向量和图检索)
- `naive` - 简单检索 (仅向量相似度)

### 3. 查看知识图谱

**使用 API:**

```bash
# 获取前 100 个节点
curl http://localhost:8000/api/graph?limit=100

# 获取特定文档的图谱
curl http://localhost:8000/api/graph?doc_id=doc-abc123&limit=500
```

### 4. 查看文档列表

```bash
curl http://localhost:8000/api/documents
```

### 5. 查看文档状态

```bash
curl http://localhost:8000/api/documents/{doc_id}
```

---

## 🛑 停止服务器

在运行 uvicorn 的终端窗口中按:

- **Windows**: `Ctrl + C`
- **Linux/Mac**: `Ctrl + C`

或者在后台运行时:

```bash
# 查找进程
ps aux | grep uvicorn          # Linux/Mac
netstat -ano | findstr :8000   # Windows

# 杀死进程
kill <PID>                     # Linux/Mac
taskkill /F /PID <PID>         # Windows
```

---

## ❓ 常见问题

### 问题 1: 端口被占用

**错误信息:**
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

**解决方法:**

```bash
# 查找占用端口的进程
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <进程ID>

# Linux/Mac
lsof -i :8000
kill -9 <PID>

# 或使用其他端口
python -m uvicorn app.main:app --port 8001 --reload
```

### 问题 2: 找不到 knowledge_graph_rag 模块

**错误信息:**
```
ModuleNotFoundError: No module named 'knowledge_graph_rag'
```

**解决方法:**

```bash
# 确保在 backend 目录下运行
cd d:\code_project\Multi-Model-Knowledge-RAG-System\backend
pwd  # 确认当前目录

# 检查模块是否存在
ls knowledge_graph_rag/  # Linux/Mac
dir knowledge_graph_rag\ # Windows

# 测试导入
python -c "import sys; sys.path.insert(0, '.'); from knowledge_graph_rag import RAGAnything; print('OK')"
```

### 问题 3: API Key 未配置

**错误信息:**
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
llm_api_key
  Field required
```

**解决方法:**

```bash
# 编辑 .env 文件
notepad backend\.env  # Windows
nano backend/.env     # Linux/Mac

# 确保配置了正确的 API Key
LLM_API_KEY=sk-your-actual-api-key-here
```

### 问题 4: 依赖版本冲突

**错误信息:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages...
```

**解决方法:**

```bash
# 强制升级关键包
pip install "fastapi>=0.115.0" --upgrade --force-reinstall
pip install "anyio>=4.0" --upgrade
pip install "pydantic>=2.9.0" --upgrade
```

### 问题 5: numpy 编译错误

**错误信息:**
```
ERROR: Unknown compiler(s): [['icl'], ['cl'], ['cc'], ['gcc']...
```

**解决方法:**

```bash
# numpy 2.x 不需要编译,直接安装
pip install numpy --upgrade

# 然后不检查依赖安装 lightrag
pip install --no-deps lightrag-hku
```

### 问题 6: 前端无法加载或显示空白页

**问题:** 访问 http://localhost:8000 显示空白页或报错

**解决方法:**

1. 确认后端已启动: `curl http://localhost:8000/health`
2. 检查 `frontend/index.html` 文件是否存在
3. 检查浏览器控制台 (F12) 的错误信息
4. 验证静态文件路径: `curl -I http://localhost:8000/static/index.html`
5. 确认 `backend/app/main.py` 中已正确挂载静态文件

**如果看到 404 错误:**
```bash
# 检查前端文件是否存在
ls frontend/index.html          # Linux/Mac
dir frontend\index.html         # Windows
```

### 问题 7: API 请求返回 404

**问题:** 前端页面加载正常,但 API 调用失败

**解决方法:**

1. 检查 API 端点是否正确: `curl http://localhost:8000/api/documents`
2. 访问 API 文档确认端点: http://localhost:8000/docs
3. 检查前端 `config.js` 中的 `API_BASE_URL` 配置
4. 查看浏览器 Network 面板的请求详情
5. 确认 CORS 配置正确 (已默认允许所有来源)

---

## 🔧 高级配置

### 使用其他 LLM 提供商

**通义千问 (Qwen):**

```env
LLM_PROVIDER=qwen
LLM_MODEL=qwen-max
LLM_API_KEY=sk-your-qwen-api-key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

**Ollama (本地):**

```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2:latest
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
```

**LM Studio (本地):**

```env
LLM_PROVIDER=lmstudio
LLM_MODEL=local-model
LLM_API_KEY=lmstudio
LLM_BASE_URL=http://localhost:1234/v1
```

### 调整并发处理

在 `.env` 中配置:

```env
# 同时处理的文档数
MAX_CONCURRENT_FILES=2

# 上下文窗口大小
CONTEXT_WINDOW=1

# 上下文模式 (page 或 chunk)
CONTEXT_MODE=page
```

### 修改存储路径

```env
STORAGE_DIR=D:/my_rag_data/storage
UPLOAD_DIR=D:/my_rag_data/uploads
OUTPUT_DIR=D:/my_rag_data/output
```

---

## 📖 相关文档

- [README.md](README.md) - 项目概述
- [QUICKSTART.md](QUICKSTART.md) - 5分钟快速开始
- [docs/API.md](docs/API.md) - 详细 API 文档
- [docs/INSTALLATION.md](docs/INSTALLATION.md) - 安装指南
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - 部署指南
- [CLAUDE.md](CLAUDE.md) - 项目架构说明

---

## 💡 提示

1. **首次运行**: 系统会自动下载必要的模型,可能需要几分钟
2. **开发模式**: 使用 `--reload` 参数,代码修改后自动重启
3. **生产环境**: 使用多进程模式 `--workers 4` 提高性能
4. **日志查看**: 添加 `--log-level debug` 查看详细日志
5. **API 文档**: 访问 `/docs` 可以直接测试所有接口

---

## 🆘 获取帮助

如遇到问题:

1. 检查 [常见问题](#❓-常见问题) 部分
2. 查看服务器日志输出
3. 访问 http://localhost:8000/docs 测试 API
4. 检查 `.env` 配置是否正确
5. 确认所有依赖已正确安装

---

## 启动检查清单

在启动前,确认以下事项:

- [ ] 已激活 raganything conda 环境
- [ ] 已进入 `backend` 目录
- [ ] `.env` 文件存在且配置了 API Key
- [ ] 已安装所有依赖 (`pip install -r requirements.txt`)
- [ ] 端口 8000 未被占用
- [ ] `knowledge_graph_rag` 目录存在
- [ ] `data` 目录结构完整

---

**准备就绪,现在可以启动项目了。**

## 快速启动命令摘要

```bash
# Windows 完整启动命令
conda activate raganything
cd d:\code_project\Multi-Model-Knowledge-RAG-System\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
# Linux/Mac 完整启动命令
conda activate raganything
cd /path/to/Multi-Model-Knowledge-RAG-System/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📖 启动后访问

| 访问内容 | 地址 | 说明 |
|---------|------|------|
| 🎨 **前端界面** | http://localhost:8000 | **主要访问地址** - 文档上传、知识查询、图谱可视化 |
| 📚 API 文档 | http://localhost:8000/docs | Swagger UI - 测试和调试 API |
| ❤️ 健康检查 | http://localhost:8000/health | 验证服务器状态 |

**记住: 只要启动后端,前端就自动可用。**
