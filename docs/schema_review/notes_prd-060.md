# 标注: prd-060.md (Night Watch — Merge Orchestrator Job)

> 文件路径: benchmarks/enterprise_project_docs/corpus/github_prd/prd-060.md
> 标注日期: 2026-05-20
> 标注人: Felix

---

## 第 1 步：通读印象

(2-3 句话讲文档大致内容)

> 
还是一个具体的执行文档，目标是合并编排工作，有一个自己的模版编排格式
---

## 第 2 步：实体清单

(读到重要名词就填一行,15-20 个,**原文列填短标签**)

| # | 原文 | 我猜的类型 | 信心 | 备注 |
|---|------|----------|------|------|
| 1 | Complexity: 7 → HIGH mode | Constraint | 高 |  |
| 2 | Auto-merge feature | Module | 中 | 当前嵌在 reviewer 里的自动合并模块 |
| 3 | user (developer) | ExternalActor | 高 | CLI 工具的外部使用者 |
| 4 | Merge Orchestrator | Module | 高 | 本 PRD 的核心新建模块 |
| 5 | scans all open PRs | FunctionalRequirement | 中 |  |
| 6 | resolves conflicts | FunctionalRequirement | 中 |  |
| 7 | Reviewer | Module | 高 | night-watch 自己的 reviewer 模块 |
| 8 | UI toggle | DataEntity | 中 |  |（太细，放弃）
| 9 | Rebase after each merge: yes (sequential, safe) | Decision | 中 |  |
| 10 | Merge order: FIFO (oldest PR first by creation date) | Decision | 中 |  |
| 11 | Full user flow | Process | 中 | 这种感觉是都有的，很多地方都可以写成full user flow，但是这样不就串台了吗 |
| 12 | `yarn verify` passes | AcceptanceCriteria` | 高 |  |
| 13 | Reviewer no longer auto-merges | FunctionalRequirement | 中 |  |
| 14 | Cron install includes merger entry when enabled | AcceptanceCriteria | 中 |  |
| 15 |  |  |  |  |
| 16 |  |  |  |  |
| 17 |  |  |  |  |
| 18 |  |  |  |  |
| 19 |  |  |  |  |
| 20 |  |  |  |  |

**Schema v2 的 15 类参考:**
- 需求层: `FunctionalRequirement` / `NonFunctionalRequirement` / `UserStory` / `AcceptanceCriteria`
- 系统层: `System` / `Module` / `Interface` / `DataEntity`
- 角色层: `Stakeholder` / `Team` / `ExternalActor`
- 流程层: `Process` / `Decision` / `Constraint`
- 兜底: `Other`

**抽取规则提醒** (你已总结):
- 跳过 code block / mermaid 图块 / markdown section headings
- 不抽: 代码符号 / 文件路径 / 命令行工具名 / 抽象品质词
- Context-aware 类型判断 (同一词不同文档可能不同 type)
- Homonym 处理: 同名但 type 不同 → 独立节点
- name 是 3-8 字短标签, description 是完整描述

**信心列填:** 高 / 中 / 低

---

## 第 3 步：拿不准 / 没合适类的实体

(列出标注时让你犹豫的实体)

- | Full user flow | Process | 中 | 这种感觉是都有的，很多地方都可以写成full user flow，但是这样不就串台了吗  这里是我一个比较大的疑问，type一致，但是很多地方都是这么说的，难道要把process拉出来吗，那万一process很长咋办
- 

---

## 第 4 步：整体感觉

**Schema v2 适配度**: 高 / 中 / 低 — **__**

**核心发现** (3-5 条, 重点是: prd-048 的发现在 prd-060 是否重复出现):

1. 还是full uer flow的问题
2. 其他地方，感觉还是较为一致的
3. 

**核心发现** (基于同 repo 对比):

1. **schema 稳定性确认**: prd-048 的 5 类核心实体 (Constraint / Decision / 
   FR / AC / Module) 在 prd-060 全部复现, 覆盖率一致。night-watch-cli 
   repo 的 PRD template 在 schema v2 上表现稳定。

2. **name 字段命名规范的重要性**: "Full user flow" 这种通用章节标题不能
   直接作为 name (会和其他文档的 "Full user flow" 撞), 必须由 LLM 
   提炼具体身份 (如 "Repo-wide merge orchestration flow")。
   → prompt 增加约束: name 必须能唯一识别该实体, 不能用文档通用章节名。

3. **同 PRD 内 user vs Reviewer 的 type 差异**: 同一份文档里 "user" 是
   ExternalActor (外部 CLI 使用者), "Reviewer" 是 Module (内部代码模块)。
   验证 context-aware type 判断不仅跨文档,在同一文档内也存在。

**建议**:

- 

---

## 第 5 步：与 prd-048 对比 (同 repo,验证发现稳定性)

| 维度 | prd-048 | prd-060 |
| --- | --- | --- |
| FR 密度 |  |  |
| AC 出现 |  |  |
| Decision 类数量 |  |  |
| Constraint (Complexity Score) |  |  |
| "agent" 实体出现 + type |  |  |
| Code/Mermaid 占比 |  |  |
| 主要实体类型 |  |  |

**核心结论** (1 句话):
> 两个文档排版比较一致

(例如: "同 repo 同风格 PRD 在 schema 上表现一致" / "prd-048 的 N 条发现全部复现" / "prd-060 出现新问题: ...")