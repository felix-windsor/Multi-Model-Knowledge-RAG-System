# 标注: blog-001.md (美团 LongCat 开源 General 365)

> 文件路径: benchmarks/enterprise_project_docs/corpus/tech_blog/blog-001.md
> 标注日期: 2026-05-20
> 标注人: Felix

---

## 第 1 步：通读印象

(2-3 句话讲文档大致内容)

> 

---

## 第 2 步：实体清单

(15-20 个,业务实体保留中文,通用类型用英文)

| # | 原文 (短标签) | 我猜的类型 | 信心 | 备注 |
|---|------|----------|------|------|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |
| 6 |  |  |  |  |
| 7 |  |  |  |  |
| 8 |  |  |  |  |
| 9 |  |  |  |  |
| 10 |  |  |  |  |
| 11 |  |  |  |  |
| 12 |  |  |  |  |
| 13 |  |  |  |  |
| 14 |  |  |  |  |
| 15 |  |  |  |  |

**Schema v2 的 15 类参考:**
- 需求层: `FunctionalRequirement` / `NonFunctionalRequirement` / `UserStory` / `AcceptanceCriteria`
- 系统层: `System` / `Module` / `Interface` / `DataEntity`
- 角色层: `Stakeholder` / `Team` / `ExternalActor`
- 流程层: `Process` / `Decision` / `Constraint`
- 兜底: `Other`

**信心列填:** 高 / 中 / 低

---

## 第 3 步：拿不准 / 没合适类的实体

(列出标注时让你犹豫的实体)

- 
- 
- 

---

## 第 4 步：整体感觉

**Schema v2 适配度**: 高 / 中 / 低 — **__**

**核心发现** (3-5 条, 重点是: 这种"非项目文档"类型的中文技术文章, schema 适配度如何?):

1. 
2. 
3. 

**建议**:

- 

---

## 第 5 步：与前 3 篇的四方对比

| 维度 | pure-001 | prd-048 | prd-034 | blog-001 |
| --- | --- | --- | --- | --- |
| 文档类型 | 工业 SRS | agile 技术 PRD | 现代正规 SRS | **中文技术评测发布** |
| 结构化程度 | 低 | 中 | 高 | **低 (叙述性中文)** |
| 是否项目文档 | 是 | 是 | 是 | **半是 (是评测发布, 非项目 spec)** |
| FR 出现 |  |  |  |  |
| Module 出现 |  |  |  |  |
| Decision 出现 |  |  |  |  |
| AC 出现 |  |  |  |  |
| 语言 | EN | EN | EN | **ZH** |
| Other 桶占比 | 低 | 低 | 低 | **预期高** |
| schema 适配度 |  |  |  |  |

**核心结论** (1-2 句话, schema 在中文 + 非项目文档上的表现):
>