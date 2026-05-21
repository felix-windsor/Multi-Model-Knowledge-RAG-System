# 2024 |

Source: https://tech.meituan.com/2024/12/26/2024-happy-new-year-top10.html
Source site: 美团技术团队
Published: 2024-12-26T00:00:00+00:00
Author: soulteary@gmail.com
License: 转载需注明出处 (CC-BY-like)
Language: zh

---

岁月的车轮滚滚向前，我们即将挥别充满回忆的2024，迈入崭新的、充满希望的2025。在此，衷心感谢伙伴们过去一年的陪伴与支持。

![](https://p0.meituan.net/meituantechblog/b976fc16e0fb9e5060b6049585dabcad249415.jpg)

今天，我们整理了2024年美团技术团队最为热门的10篇技术文章，这些文章覆盖了基础理论、数据存储、因果推断、搜索推荐、智能测试、知识图谱、领域驱动设计等多个技术领域，期望这些精选内容能为大家带来一些启发或帮助。愿大家在新的一年里，持续深耕技术沃土，稳步前行，不断攀登新的高峰。

## 01 基本功 | 一文讲清多线程和多线程同步

![](https://p0.meituan.net/meituantechblog/46c434af68b098f65491bb9cc64a176f383178.jpg)

多线程编程是现代软件开发中的一项关键技术，在多线程编程中，开发者可以将复杂的任务分解为多个独立的线程，使其并行执行，从而充分利用多核处理器的优势。然而，多线程编程也带来了挑战，例如线程同步、死锁和竞态条件等问题。本篇文章将深入探讨多线程编程的基本概念（原子操作、CAS、Lock-free、内存屏障、伪共享、乱序执行等）、常见模式和最佳实践。通过具体的代码示例，希望能够帮助大家掌握多线程编程的核心技术，并在实际开发中应用这些知识，提升软件的性能和稳定性。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651778446&idx=1&sn=44306b644777a4d939730e7774071541&scene=21#wechat_redirect)）

## 02 DDD在大众点评交易系统演进中的应用

![](https://p0.meituan.net/meituantechblog/0365d5c51db9c02682794df240eb7eb7626207.jpg)

本文整理自美团技术沙龙第73期《基于领域驱动设计（DDD）的架构演进和实践》（[B站视频](https://www.bilibili.com/video/BV1nt4y1J7hH/?spm_id_from=333.999.0.0&vd_source=aea2a93491bea0d72f7e5b8a79085d70)），主要介绍了DDD的核心概念、常见的设计思路，并结合DDD介绍大众点评交易系统的演进过程，最后做了一些总结和思考。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651777662&idx=1&sn=22ba8694d0a0d1da7c47b0a6a1367fab&scene=21#wechat_redirect)）

## 03 美团大规模KV存储挑战与架构实践

![](https://p0.meituan.net/meituantechblog/01f2c4d5e7f9df82909c160a655a2295822233.jpg)

KV 存储作为美团一项重要的在线存储服务，承载了在线服务每天万亿级的请求量，并且保持着 99.995% 的服务可用性。文章主要分为四个部分：第一部分介绍了美团 KV 存储发展历程；第二部分分享了内存 KV Squirrel 挑战和架构实践；第三部分阐述了持久化 KV Cellar 挑战和架构实践；最后一部分介绍了未来的发展规划。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651777161&idx=1&sn=4af6d7e62a38bb77dceb91c4540465f0&scene=21#wechat_redirect)）

## 04 领域驱动设计DDD在B端营销系统的实践

![](https://p0.meituan.net/meituantechblog/0365d5c51db9c02682794df240eb7eb7626207.jpg)

本文整理自美团技术沙龙第73期《基于领域驱动设计（DDD）的架构演进和实践》（[B站视频](https://www.bilibili.com/video/BV1xV4y1H7Zq/?spm_id_from=333.999.0.0&vd_source=aea2a93491bea0d72f7e5b8a79085d70)），系统复杂性根源于隐晦（难理解），耦合（难改动）和变化（难扩展），DDD正是应对系统复杂性的重要方法。本文针对B端营销系统设计中的复杂性，从战略设计，战术设计到代码架构，详细介绍了DDD在各个阶段的实践，期望为大家提供一些可供参考和借鉴的思路。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651777906&idx=1&sn=37acea4022171310137ca827ee3b0946&scene=21#wechat_redirect)）

## 05 美团外卖基于GPU的向量检索系统实践

![](https://p0.meituan.net/meituantechblog/4e2bb348cad03f1b902d4daf746a894b634490.jpg)

搜索业务具有数据量大、过滤比高等特点，为了在保证高召回率的同时进一步提高检索性能，美团技术团队基于GPU实现了支持向量+标量混合检索的通用检索系统，召回率与检索性能均有较大提升。本文介绍了在GPU向量检索系统建设中遇到的挑战及解决思路。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651777342&idx=1&sn=dc20d77aad1708540f5da04c455a0a62&scene=21#wechat_redirect)）

## 06 分布式因果推断在美团履约平台的探索与实践

![](https://p0.meituan.net/meituantechblog/b1ba1af05ab096f85793f2b7de7e2cb4137836.jpg)

美团履约平台技术部在因果推断领域持续的探索和实践中，自研了一系列分布式的工具。本文重点介绍了分布式因果树算法的实现，并系统地阐述如何设计实现一种分布式因果树算法，以及因果效应评估方面qini\_curve/qini\_score的不足与应对技巧。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651776841&idx=1&sn=0c2c31f78de4a81f354282858f740df0&scene=21#wechat_redirect)）

## 07 搜索广告召回技术在美团的实践

![](https://p0.meituan.net/meituantechblog/17afed96d483f02ad8ee51344d1633fe316154.jpg)

内容整理自美团技术沙龙第81期《美团在广告算法领域的探索及实践》（[B站视频](https://www.bilibili.com/video/BV1gM4m1r7DQ/?spm_id_from=333.999.0.0&vd_source=aea2a93491bea0d72f7e5b8a79085d70)）。本文首先介绍了美团搜索广告的三个阶段：多策略关键词挖掘、分层召回体系、生成式召回；然后重点介绍了生成式关键词召回、多模态生成式向量召回、生成式相关性判断在美团的实践。最后是一些经验分享及总结。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651778297&idx=1&sn=e0c8566c3f745a3a252a753e0fefd373&scene=21#wechat_redirect)）

## 08 Spark向量化计算在美团生产环境的实践

![](https://p0.meituan.net/meituantechblog/2b0acd4d384dcdbca6cff3d85f3381a9364468.jpg)

Apache Spark是一个优秀的计算引擎，广泛应用于数据工程、机器学习等领域。向量化执行技术在不升级硬件的情况下，既可获得资源节省，又能加速作业执行。Gluten+Velox解决方案为Spark换上了向量化执行引擎，本文阐述了美团在这一方向的实践和思考。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651778181&idx=1&sn=493994faeae26da30594ca37e4214b58&scene=21#wechat_redirect)）

## 09 基于多模态信息抽取的菜品知识图谱构建

![](https://p0.meituan.net/meituantechblog/2f4be0dc7125cf51652a44aba61ac497510042.jpg)

菜品作为到店餐饮各相关业务的基石，提供了更细粒度的视角理解餐饮供给，为到餐精细化运营提供了抓手。美团技术团队与天津大学刘安安教授团队展开了“基于多模态信息抽取的菜品知识图谱构建”的科研合作，利用多模态检索实现图文食材的识别，扩展了多模态菜品食材识别的范围，提升了食材识别的准确性。该项工作提出了一个跨模态食材级数据集，该数据集提供食材及其关系有助于增强对中国烹饪的理解。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651777797&idx=1&sn=70ea8de1fba0f6d6d54dfb08ea2b02ef&scene=21#wechat_redirect)）

## 10 AutoConsis：UI内容一致性智能检测

![](https://p0.meituan.net/meituantechblog/ddfc648151fc2ffa23692b173296daac142209.jpg)

美团技术团队与复旦大学计算机学院周扬帆教授团队展开了大前端智能化测试领域的科研合作，从UI界面内容一致性校验入手，实现了一套自动化智能检测流程，相关论文被软件工程领域具有国际影响力的会议ICSE 2024（CCF-A类会议）的Software In Practice Track（软件工程实践应用）收录。（[阅读全文](https://mp.weixin.qq.com/s?__biz=MjM5NjQ5MTI5OA==&mid=2651779616&idx=1&sn=e859f480e9a6b34ed89f3772f221b58b&scene=21#wechat_redirect)）

## 2025 Happy New Year

新年的钟声渐渐临近，愿我们共同迎接崭新的起点。在此，向各位伙伴致以最诚挚的祝福！愿幸福、平安、健康，事业蒸蒸日上。祝福大家新年快乐，万事顺意！
