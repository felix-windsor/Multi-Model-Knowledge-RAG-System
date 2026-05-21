# 标注: prd-034.md (MUSUBI v5.0.0 Software Requirements Specification)

> 文件路径: benchmarks/enterprise_project_docs/corpus/github_prd/prd-034.md
> 标注日期: 2026-05-20
> 标注人: Felix

---

## 第 1 步：通读印象

(2-3 句话讲文档大致内容)
做了一个定义提升自己AI产品的要求报告

---

## 第 2 步：实体清单

(读到重要名词就填一行,15-20 个,**name 列填短标签 3-8 字**)

| # | 原文 (短标签) | 我猜的类型 | 信心 | 备注 |
|---|------|----------|------|------|
| 1 | MUSUBI | system | 高 |  |
| 2 | OpenHands | ExternalActor | 高 |  |

| 4 | Appropriate topic tags (ai-coding, sdd, specification-driven-development, claude-code, etc.) | FunctionalRequirement | 中 |  |
| 5 | Repository appears in top 10 results | AcceptanceCriteria | 中 | Repository appears in top 10 results for "sdd tool" and "ai coding agent" on GitHub search |
| 6 | README includes animated demo GIF | AcceptanceCriteria | 中 |  |
| 7 | Submission PR created for all 4 lists | AcceptanceCriteria | 中 |  |
| 8 | English tutorial articles (Dev.to, Hashnode, Medium) | Other  | 中 |  |
| 9 | Headless browser operation (Chrome, Firefox, Safari) | FunctionalRequirement | 中 |  |
| 10 | **Priority**: P1 (High) | Constraint | 中 |  |（直接放成属性）
| 11 |  |  |  |  |
| 12 |  |  |  |  |
| 13 |  |  |  |  |
| 14 |  |  |  |  |
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
- **name 是 3-8 字短标签** (不能用通用章节名如 "Full user flow")
- description 字段放完整描述, 想多长就多长

**信心列填:** 高 / 中 / 低

---

## 第 3 步：拿不准 / 没合适类的实体

(列出标注时让你犹豫的实体)

- | 10 | **Priority**: P1 (High) | Constraint | 中 |  |
- | 2 | OpenHands | ExternalActor | 高 |  |

---

## 第 4 步：整体感觉

**Schema v2 适配度**: 高 / 中 / 低 — **__**

**核心发现** (3-5 条):

1. 这一版文档写的更加正规，
2. 回忆一下，前面有说过一个这样的问题，但是对于priority这种，难道是要把前面的具体任务加上，才能构成一个可用的constraint吗
3. 

**建议**:

- 

**核心发现** (3 条):

1. **MUSUBI v5 是强模板化 SRS** — 整篇文档由 Priority 体系 (P0-P3) + 
   固定字段 Requirements 组成,每条 Requirement 都有相同的字段位置。
   实体抽取在这种文档上几乎机械化。

2. **Priority 是抽取粒度问题** — P0/P1/P2/P3 单独不是 entity (没有 identity), 
   应整体抽为一个 Constraint 节点 (覆盖 Priority + Version + Time window 三元绑定)。
   这是 schema v2 在"项目战略约束"场景下的新发现。

3. **Corpus 结构化光谱影响 schema validator 价值** — 三篇 review 文档 
   (pure-001 叙述性 / prd-048 半模板 / prd-034 强模板) 的结构化程度差异显著。
   schema validator 在强模板文档上提升空间小,在叙述性文档上价值才真正体现。
   → ablation 报告必须按 doc_subtype 分组,否则均值会掩盖真实改进。

**核心发现 #4**: corpus 选择偏差 (selection bias) 警告

review 抽样的 5 篇文档中,prd-034 (MUSUBI v5) 是少数派——它是
高度结构化的"理想 SRS"。实际企业文档分布更接近 corpus 里的:

  - PURE 120 篇 (叙述性,占 60%)
  - night-watch 25 篇 (半模板,占 12.5%)
  - 中文 tech blog 33 篇 (半模板架构演进,占 16.5%)
  - MUSUBI 强模板 SRS (占 < 5%)

→ 评测和 ablation 要按 doc_subtype 分组报告,**不能用"强模板表现好"
  代表"系统在企业文档上表现好"**。这种 selection bias 是 RAG 评测
  里的常见陷阱。

**建议**:

- manifest.json 增加 doc_subtype 字段 (narrative_srs / semi_template_prd / 
  strict_template_srs / architecture_blog),评测时按 subtype 分组
- Priority 体系抽取规则进 prompt: "Priority + 版本 + 时间" 类信息整体抽为一个 
  Constraint, 不要逐条抽

---

## 第 5 步：与 pure-001 / prd-048 的三方对比

prd-034 是 **现代正规 SRS**，介于 PURE 的"旧式工业 SRS"和 prd-048 的"agile 技术 PRD"之间。三方对比观察 schema 在不同 SRS 风格上的表现：

| 维度 | pure-001 (旧式 PURE SRS) | prd-048 (agile 技术 PRD) | prd-034 (现代正规 SRS) |
| --- | --- | --- | --- |
| FR 密度 |  |  |  |
| UserStory 出现 |  |  |  |
| AC 出现 |  |  |  |
| Decision 数量 |  |  |  |
| Constraint 显式 |  |  |  |
| 代码/Mermaid 占比 |  |  |  |
| 主要实体类型 |  |  |  |
| 风格特点 |  |  |  |

**核心结论** (1 句话):
> 
我已经开始感慨了，其实 ai 很难代替真正的程序员，因为真正的程序员大量的工作其实是在做判断，和选择，然后在工作的过程中，发现原有哪里做的不好，而且不是说，ai不能生成文档或者代码，而是你要看基于你们的项目你到底有没有自己的领悟与判断，好的思考与想法，只能说ai可能给你引导，然后你们再共同往那里走，但是如何诞生和细节如何打磨，都是需要人一点点扣的

说到底是，如果你自己都不懂，那么你大概率用ai做出来的是一个自嗨的玩具，而不是一个供人使用的产品


(例如: "现代 SRS 兼具 PURE 的正规结构 + agile PRD 的实现细节,是两种风格的中间态" / 
     "prd-034 出现 PURE 和 prd-048 都没覆盖的新实体类型: ...")