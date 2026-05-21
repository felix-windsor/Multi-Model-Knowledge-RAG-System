# 标注: prd-048.md (Night Watch — GitHub Projects as PRD Source of Truth)

> 文件路径: benchmarks/enterprise_project_docs/corpus/github_prd/prd-048.md
> 标注日期: 2026-05-20
> 标注人: Felix

---

## 第 1 步：通读印象

(2-3 句话讲文档大致内容)

> 

---

## 第 2 步：实体清单

(读到重要名词就填一行,15-25 个就够,**原文列必须填英文原词**)

| # | 原文 | 我猜的类型 | 信心 | 备注 |
|---|------|----------|------|------|
| 1 | PRD | data entity | 高 | 发现一个问题没有data entity |
| 2 | All phases complete | AcceptanceCriteria | 高 |  |
| 3 | All specified tests pass | AcceptanceCriteria | 高 |
| 4 | GitHubProjectsProvider can manage boards/issues | FunctionalRequirement | 高 | Phase 2 outcome |FunctionalRequirement | 高 |  |
| 5 | agents | ExternalActor | 高 | 外部 AI agent (Claude/Codex) 调用 night-watch CLI |
| 6 | night-watch | system | 中 |  |
| 7 | GitHub Projects V2 | ExternalActor | 高 | 被对接的外部 GitHub 服务 |
| 8 | `night-watch board` CLI commands | FunctionalRequirement | 中 |  |
| 8a | board setup creates GitHub Project | FunctionalRequirement | 高 | |
| 8b | board create-prd creates issue on board | FunctionalRequirement | 高 | |
| 8c | board next-issue returns first Ready issue | FunctionalRequirement | 高 | |
| 9 | PRD lifecycle states (Draft→Ready→...→Done) | Process | 中 | 描述 PRD 在 board 上的状态机 |
| 10 | `yarn verify` passes | AcceptanceCriteria | 高 |  |
| 11 | The `IBoardProvider` interface and types exist, along with a factory that can instantiate providers. `yarn verify` passes. |  | FunctionalRequirement | 中 |
| 12 | GitHub | other |  |  |
| 13 | agent skill files | dataentity |  |  |
| 14 | PRD Creation Flow | Process | 高 | board create-prd 的执行序列 |
| 15 | Agent Execution Flow | Process | 高 | agent 拿任务到完成的序列 |
| 16 | Complexity score 8 (HIGH mode) | Constraint | 高 | 复杂度约束 |
| 17 | Use gh api graphql instead of separate auth | Decision | 高 | |
| 18 | Board columns: Draft→Ready→IP→Review→Done | Decision | 高 | |
| 19 | Each PRD phase/task = one GitHub Issue | Decision | 高 | |
| 20 | Backward compatible: fallback to filesystem when not configured | Decision | 高 | |
**Schema v2 的 15 类参考:**
- 需求层: `FunctionalRequirement` / `NonFunctionalRequirement` / `UserStory` / `AcceptanceCriteria`
- 系统层: `System` / `Module` / `Interface` / `DataEntity`
- 角色层: `Stakeholder` / `Team` / `ExternalActor`
- 流程层: `Process` / `Decision` / `Constraint`
- 兜底: `Other`

**信心列填:** 高 / 中 / 低

---

## 第 3 步：拿不准 / 没合适类的实体

(列出标注时让你犹豫的实体,以及为什么)

- 我发现一个很大的问题，这是一篇技术文档，然后很多的都是函数文件夹或者命名，那就有问题啦，我们没有data entity，而且如果每个代码文件都算一个实体，那这篇会抽出非常多的实体，但是实际上又没有什么很大的用处，我不知道该如何处理
- 下面都有很多mermaid图了，感觉还是没有什么作用，感觉cli，gh，api，agent都是实体，但是没有什么放进去的必要

- 里面还有具体代码的部分，你认为需要如何做呢，因为已经不是自然语言描述的部分了
这次拿不准的东西太多了
---

## 第 4 步：整体感觉

**Schema v2 适配度**: 高 / 中 / 低 — **__**

**核心发现** (更新):

1. 跳过 code/mermaid (prompt 硬约束)
2. 跳过 markdown section headings, 抽下方内容 (prompt 硬约束)
3. Context-aware type 判断 (同一词在不同文档可能 type 不同)
4. **Homonym (同名异义) 处理**: 同名但 type 不同的实体应保留为独立节点,
   不能强制合并。LightRAG 默认 merge 逻辑在此场景下丢失信息,
   schema validator 需要 type-aware merging。
   - 实例: "agent" 在 prd-048 是 ExternalActor (外部 AI 服务),
     在 night-watch 架构文档可能是 Module (项目内代码),
     在金融公司 PRD 可能是 Stakeholder (内部团队)。
**建议**:

- 上述发现我觉得写到后面的提取的系统prompt中
- 然后关于agent那里我就有疑问了，那种语境下如何区分呢

---

## 第 5 步：与 pure-001 的对比 (本篇特有)

prd-048 是 **agile 风格 PRD**，pure-001 是 **正规军 SRS**。两者风格差异很大，对比观察：

| 维度 | pure-001 (PURE SRS) | prd-048 (Night Watch PRD) |
| --- | --- | --- |
| FunctionalRequirement 密度 | 感觉这次密度很高 |  |
| UserStory 出现 |  |  |
| AcceptanceCriteria 出现 | 这次也有出现了 |  |
| Decision / 决策类实体 |  |  |
| 主要实体类型 |  |  |

**结论**:
感觉有很多摸不准的地方