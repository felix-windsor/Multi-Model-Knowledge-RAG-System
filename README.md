# 知识图谱 RAG 系统

基于 RAGAnything 的多模态知识图谱 RAG 系统,支持文档上传、智能处理、知识查询和图谱可视化。

## 功能特性

- **📄 文档上传**: 支持 PDF、图片、Office 文档、文本等多种格式
- **🔍 智能处理**: 自动解析文档,提取文本、图片、表格、公式等多模态内容
- **💬 知识查询**: 基于处理后的文档进行智能问答,支持多种查询模式
- **🕸️ 图谱可视化**: 交互式 2D 知识图谱展示,可视化实体和关系
- **🤖 多模型支持**: 支持 OpenAI、Qwen、Ollama、LM Studio 等多种 LLM 提供商

## 技术栈

**后端**:
- FastAPI - 高性能 Web 框架
- RAGAnything - 多模态 RAG 核心库
- LightRAG - 底层 RAG 框架
- Pydantic - 数据验证

**前端**:
- HTML5 + Bootstrap 5 - 响应式界面
- Vanilla JavaScript - 原生 JS 实现
- vis.js - 图谱可视化

## 项目结构

```
Multi-Model-Knowledge-RAG-System/
│
├── backend/                          # 后端服务
│   ├── knowledge-graph-rag/          # 核心 RAG 库
│   ├── app/                          # Web 应用
│   │   ├── api/                      # API 路由
│   │   ├── models/                   # 数据模型
│   │   ├── services/                 # 业务逻辑
│   │   ├── config.py                 # 配置管理
│   │   ├── dependencies.py           # 依赖注入
│   │   └── main.py                   # 应用入口
│   ├── requirements.txt              # Python 依赖
│   └── .env.example                  # 环境变量模板
│
├── frontend/                         # 前端
│   ├── index.html                    # 主页面
│   └── assets/                       # 静态资源
│       ├── css/                      # 样式
│       └── js/                       # JavaScript
│
├── data/                             # 数据存储
│   ├── uploads/                      # 上传文件
│   ├── storage/                      # RAG 存储
│   └── output/                       # 解析输出
│
├── scripts/                          # 启动脚本
│   ├── start.bat                     # Windows
│   └── start.sh                      # Linux/Mac
│
└── README.md                         # 项目文档
```

## 快速开始

### 前置要求

- Python 3.8+
- pip

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd Multi-Model-Knowledge-RAG-System
```

2. **配置环境变量**
```bash
cd backend
cp .env.example .env
# 编辑 .env 文件,配置 LLM API Key 等参数
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **启动服务器**

**Windows**:
```bash
cd ..
scripts\start.bat
```

**Linux/Mac**:
```bash
cd ..
chmod +x scripts/start.sh
./scripts/start.sh
```

5. **访问应用**
- 主页面: http://localhost:8000
- API 文档: http://localhost:8000/docs

## 环境变量配置

编辑 `backend/.env` 文件:

```env
# LLM 配置
LLM_PROVIDER=openai                   # 提供商: openai, qwen, ollama, lmstudio
LLM_MODEL=gpt-4o                      # 模型名称
LLM_API_KEY=sk-your-api-key           # API Key
LLM_BASE_URL=https://api.openai.com/v1

# Embedding 配置
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIM=3072

# 存储配置
STORAGE_DIR=../data/storage
UPLOAD_DIR=../data/uploads
OUTPUT_DIR=../data/output

# 文档处理配置
MAX_CONCURRENT_FILES=2

# 服务器配置
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 多 LLM 提供商配置

#### OpenAI
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-your-openai-key
LLM_BASE_URL=https://api.openai.com/v1
```

#### Qwen (通义千问)
```env
LLM_PROVIDER=qwen
LLM_MODEL=qwen-turbo
LLM_API_KEY=sk-your-qwen-key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

#### Ollama (本地)
```env
LLM_PROVIDER=ollama
LLM_MODEL=qwen2.5:14b
LLM_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=bge-m3:latest
```

#### LM Studio (本地)
```env
LLM_PROVIDER=lmstudio
LLM_MODEL=local-model
LLM_BASE_URL=http://localhost:1234/v1
```

## API 文档

### 1. 上传文档
```http
POST /api/upload
Content-Type: multipart/form-data

file: <binary>
```

### 2. 获取文档状态
```http
GET /api/documents/{doc_id}
```

### 3. 获取文档列表
```http
GET /api/documents
```

### 4. 知识查询
```http
POST /api/query
Content-Type: application/json

{
  "question": "什么是机器学习?",
  "mode": "mix",
  "doc_ids": ["doc-123"]
}
```

**查询模式**:
- `mix`: 混合模式 (推荐)
- `local`: 本地模式
- `global`: 全局模式
- `hybrid`: 混合检索
- `naive`: 简单检索

### 5. 导出知识图谱
```http
GET /api/graph?doc_id=<doc_id>&limit=1000
```

## 使用示例

### 1. 上传文档
1. 在左侧"文档上传"区域选择文件
2. 点击"上传文档"按钮
3. 等待处理完成(可在文档列表中查看状态)

### 2. 知识查询
1. 在中间"知识查询"区域输入问题
2. 选择查询模式
3. 点击"查询"按钮
4. 查看回答结果

### 3. 查看知识图谱
1. 在右侧"知识图谱"区域点击"刷新图谱"
2. 浏览交互式图谱
3. 点击节点查看详情
4. 双击节点聚焦查看

## 开发指南

### 后端开发

修改 API 逻辑:
- API 路由: `backend/app/api/`
- 业务逻辑: `backend/app/services/`
- 数据模型: `backend/app/models/`

启动开发服务器:
```bash
cd backend
uvicorn app.main:app --reload
```

### 前端开发

修改前端文件:
- HTML: `frontend/index.html`
- CSS: `frontend/assets/css/styles.css`
- JavaScript: `frontend/assets/js/`

## 注意事项

1. **首次使用**: 请先配置 `.env` 文件中的 LLM API Key
2. **存储目录**: 确保 `data/` 目录有读写权限
3. **文档格式**: Office 文档转换需要安装 LibreOffice
4. **内存使用**: 大文件处理可能需要较多内存

## 常见问题

### Q: 上传文档失败?
A: 检查文件格式是否支持,以及 `data/uploads` 目录权限

### Q: 查询没有结果?
A: 确保文档已处理完成(状态为"已完成")

### Q: 图谱显示为空?
A: 可能是文档尚未处理完成,或者没有提取到实体

### Q: API Key 错误?
A: 检查 `.env` 文件中的 `LLM_API_KEY` 配置是否正确

## 贡献

欢迎提交 Issue 和 Pull Request!

## 许可证

MIT License

## 致谢

- [LightRAG](https://github.com/HKUDS/LightRAG) - 底层 RAG 框架
- [RAGAnything](https://github.com/HKUDS/RAGAnything) - 多模态 RAG 核心
- [vis.js](https://visjs.org/) - 图谱可视化库
