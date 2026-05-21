# 标注: pure-001.md

> 文件路径: benchmarks/enterprise_project_docs/corpus/pure_srs/pure-001.md
> 标注日期: 2026-05-20
> 标注人: Felix

---

## 第 1 步：通读印象

(2-3 句话讲文档大致内容)

> 
面向印度警务人员的从起诉、公民界面再到应用配置等的需求描述
---

## 第 2 步：实体清单

(读到重要名词就填一行,15-25 个就够,**原文列必须填英文原词**)

| # | 原文 | 我猜的类型 | 信心 | 备注 |
|---|------|----------|------|------|
| 1 |  CCTNS | system | 高 |  |
| 2 | police |  stakeholder | 高 |  |
| 3 | Citizens | stakeholder | 中 |  |
| 4 | The Registration module | Module | 高 |  |
| 5 | complainants | Stakeholder | 中 |  |
| 6 | the investigation process | Process | 高 |  |
| 7 | The Investigation module | Module | 高 |  |
| 8 | Registration | FunctionalRequirement | 中 |  |
| 9 | Prosecution | FunctionalRequirement | 中 | The Prosecution module感觉他们又是同一个东西，但是它又可以被分到module|
| 10 | police station | Other | 中 |  |
| 11 | courts | Other | 中 |  |
| 12 | Search | FunctionalRequirement | 中 | 跟prosecution和registration是同一个道理 |
| 13 | user | Stakeholder | 中 | 感觉user还是警察 |
| 14 | Citizen Interface |  Interface | 高 |  |
| 15 | Navigation | FunctionalRequirement | 中 |  |
| 16 | the states’ requirements | Other | 中 |  |
| 17 | helps keep the application configured according
to the states’ requirements in addition to keeping data elements/rules up to date | FunctionalRequirement | 中 |  |



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

- information这个词感觉是一个比较虚的词，不应该被抽出来
- information such as act and sections, state specific data, castes, tribes,property information这些information感觉又可以落到实处
- 

---

## 第 4 步：整体感觉

**Schema v2 适配度**: 高 / 中 / 低 — **__**

**核心发现** (3-5 条):

1. 这篇文章是印度警察系统的一个像需求文档的东西，但是第一次写核心发现我也不知道范式是什么，具体要写些什么样的东西
2. 浏览下来，发现这篇内容主语全算起来都不是很多，很多时候句子都很长，而且这次感觉非功能需求基本没有，而且也没有验收标准，但是功能需求，那种可以写的很长的，这次应该是少写了
3. 还有个问题，police personnel和police是什么关系，这俩可以都抽吗，感觉不太行，但是如果是这样的话，留哪个呢

1. 角色层粒度问题: police / police personnel / user / complainants / Citizens 
   这些角色实体边界混乱
   → schema 该不该区分 "群体" (Citizens) vs "个体" (complainant)?
   → ExternalActor 类需要明确"包含组织"(courts/police station)

2. Module vs FunctionalRequirement 边界
   → "Registration" 这个词既是 module 名又是功能名,LLM 抽取时容易冲突
   → 文档里 module 名经常被单独提及,容易被误抽成 FR

3. 信息类实体的粒度
   → "information" 单独抽没意义,但 "act and sections" / "castes" / 
     "property information" 这些具体信息应该抽成 DataEntity
   → schema 没明说 DataEntity 的粒度,需要 review

→ 标准做法：实体归一化。把 police / police personnel / designated constable 都归一到 canonical name "Police"，作为同一个 Stakeholder 节点。
**建议**:

- 这个建议我还不知道咋写，你可以在这次review之后，跟我打个样
-

## 第 4 步：整体感觉

**Schema v2 适配度**: **中-高**

**核心发现** (5 条):

1. **PURE 风格 SRS 文档密度低**: 单文档主要描述模块功能定位,
   FR/UserStory/AC 出现频率低,Module + Stakeholder + Process 是主要实体。
   → 推论:schema v2 中 FR/UserStory/AC 在 PURE 子集上覆盖率会低,
   这是 corpus 特征不是 schema 问题。

2. **Stakeholder vs ExternalActor 边界**:
   - police, police personnel, designated constable → Stakeholder ✅
   - Citizens, complainants, courts, police station → 都是系统外部
   - v2 的 ExternalActor description 现在写 "外部用户/客户",
     **需要明确扩展到 "外部组织" (courts, police station 等)**

3. **Module 名容易被误抽成 FR**:
   - "Registration" / "Prosecution" / "Search" 这些词既出现在 module 名
     ("Registration Module") 中,也常单独出现
   - LLM 抽取时容易把单独的 "Search" 抽成 FunctionalRequirement
   - **需要在 prompt 中明确**:模块名出现不带 "the system shall" 等动作
     句式时,只抽为 Module 不抽为 FR

4. **实体归一化的关键性**:
   - police / police personnel / designated constable 是同一概念的不同粒度
   - Citizens / complainants 是同一群体的不同称呼
   - 已有 normalizer.py 处理,**确认覆盖到这类企业文档场景**

5. **DataEntity 粒度问题**:
   - "information" 单独不抽
   - "act and sections" / "castes" / "property information" 这些具体
     信息应抽为 DataEntity
   - schema 中 DataEntity 的 description **可以补一句"具体的业务数据/
     字段/记录类型,排除泛词 information/data"**

**建议**:

- v2 调整: ExternalActor description 扩展为"外部用户/客户/组织"
- prompt 调整: 明确"Module 名不抽为 FR"的规则
- normalizer.py: 用本篇测试角色归一化效果
- DataEntity description 加约束语句