# 企业内网多模态知识库 RAG 系统

本项目是一个面向企业内网知识库场景的多模态 Knowledge Graph RAG 应用，支持文档上传、异步解析、混合检索问答、知识图谱导出和前端可视化。系统重点处理服务器资源受限、数据不能出域、文档格式复杂、抽取结果需要可评估的问题。

项目适合作为企业内部 AI Search、Copilot、知识问答或文档分析系统的后端原型。

## 上游致谢

本项目基于 RAGAnything 1.2.8 和 LightRAG 二次开发。上游项目提供了多模态文档解析、图谱增强 RAG、向量检索和多查询模式等核心能力。

本仓库保留 `backend/knowledge_graph_rag/` 作为上游相关代码的 vendored 版本，便于在内网环境中部署和调试。项目中的服务层、存储抽象、API 封装、异步任务、closed schema 抽取和评测资产，是围绕企业内网工程化落地补充的增量部分。

## 本项目增量

| 模块 | 本项目增量 |
| --- | --- |
| FastAPI 服务层 | 在 `backend/app/` 下封装 V1 API、统一响应、API Key 鉴权、健康检查、文档上传、任务查询、问答和图谱导出。 |
| 异步任务 | 上传后返回 `doc_id` 和 `task_id`，后台执行解析和抽取，避免大文件阻塞接口响应。 |
| 存储抽象 | 通过 `StorageManager` 支持本地 JSON 存储和 Qdrant + Neo4j 后端切换。 |
| 文档处理 | 面向 PDF、图片、Office、Markdown、文本等格式，接入多模态解析链路。 |
| Closed schema 抽取 | 自研中文企业文档 Graph RAG 抽取核心，约束 15 类实体和 14 类关系，支持 JSON 修复、类型漂移统计、实体归一化、关系合法性校验和置信度评分。 |
| 评测体系 | 构建 200 篇合成企业文档和 420 条评测问题，覆盖事实、摘要、实体关系、多跳和表格类问题，用于可重复评估。 |

## 技术栈

- 后端框架：FastAPI、Pydantic、pydantic-settings
- RAG 核心：RAGAnything 1.2.8、LightRAG
- 模型接入：OpenAI-compatible API、Qwen、Ollama、LM Studio
- 向量与图存储：Qdrant、Neo4j、本地 JSON 存储
- 前端：HTML、Bootstrap、Vanilla JavaScript、vis.js
- 测试：pytest、pytest-asyncio
- 部署：Docker Compose、本地或内网模型服务

## 快速开始

1. 安装依赖

```bash
pip install -r backend/requirements.txt
```

2. 配置环境变量

```bash
cp env.example .env
```

编辑项目根目录下的 `.env`，至少配置 `LLM_PROVIDER`、`LLM_MODEL`、`LLM_API_KEY`、`LLM_BASE_URL`。如果使用本地存储，可以保持 `STORAGE_BACKEND=local`。

3. 启动服务

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4. 打开页面和 API 文档

```text
Frontend: http://localhost:8000
API docs: http://localhost:8000/docs
Health: http://localhost:8000/api/v1/health
```

5. 运行测试

```bash
cd backend
python -m pytest
```

## 评测结果

在线全量评测报告记录了 200 篇合成企业文档入库和 420 条问题评估结果：

| 指标 | 结果 |
| --- | --- |
| 文档数量 | 200 |
| 评测问题 | 420 |
| 成功请求 | 420 / 420 |
| 关键词命中率 | 99.6% |
| 平均延迟 | 9.0s |
| P95 延迟 | 14.86s |
| 导出实体 | 239 |
| 导出关系 | 545 |

评测题型分布：

| 题型 | 数量 |
| --- | ---: |
| 事实查询 | 130 |
| 摘要归纳 | 70 |
| 实体关系 | 90 |
| 多跳推理 | 80 |
| 表格理解 | 50 |

复现评测时，先启动后端服务并完成模型配置，然后运行 benchmark 脚本：

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
python scripts/run_api_benchmark.py \
  --base-url http://localhost:8000 \
  --cases benchmarks/eval_cases/enterprise_420.json \
  --output-dir benchmarks/reports
```

## 评测局限

- 当前 200 篇企业文档为合成数据，适合做可重复回归评估，但可能存在 distribution bias，不能直接代表真实企业内网文档分布。
- 关键词命中率是 proxy metric，只能反映回答是否覆盖预期关键词，不等同于严格的 answer accuracy。
- 评测集中 distractor 文档不足，暂时不能完整衡量复杂干扰条件下的检索鲁棒性。
- 后续计划补充 LLM-as-judge、人工抽样标注、distractor corpus 和真实脱敏文档评估。

## 目录结构

```text
backend/
  app/                      # FastAPI 服务层、存储抽象、抽取核心和 API
  knowledge_graph_rag/      # RAGAnything / LightRAG vendored 代码
  tests/                    # 单元测试和集成测试

frontend/
  index.html                # FastAPI 托管的前端入口
  assets/                   # 前端脚本和样式

benchmarks/
  enterprise_rag_demo.md
  eval_cases.enterprise_rag_demo.json

docs/
  design/                   # 架构设计文档
  guides/                   # 使用和迁移指南
```

## 许可证

本项目遵循仓库中的 `LICENSE` 文件。使用上游 RAGAnything 和 LightRAG 相关能力时，请同时遵守对应上游项目的许可证要求。
