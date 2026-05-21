# 10倍降本、10倍无损弹性！Kafka Serverless 基础版与专业版重磅发布！

Source: https://developer.aliyun.com/article/1659837
Source site: 阿里云开发者社区
Source column: RocketMQ
Published: 2025-04-03 14:56:52
Author: unknown
License: 转载需注明出处 (CC-BY-like)
Language: zh

---

云消息队列 Kafka 版基于 Apache Kafka 构建，提供高吞吐量与高可扩展性的分布式消息队列服务，广泛应用于日志收集、监控数据聚合、流式数据处理及在离线分析等场景，是 AI 与大数据时代企业数据处理体系的核心组件。

云消息队列 Kafka 版围绕“经济、稳定、弹性”三大核心方向，基于阿里云基础设施对 Apache Kafka 进行深度重构。通过存算分离的 Serverless 架构升级，在保障高可用性与安全可靠的同时，支持读写秒级弹性，秒级分区迁移，并提供灵活的按量付费。

3 月 27 日，阿里云消息队列 ApsaraMQ 与全球消息流领域领导者 Confluent 联合举办“云原生 Kafka 线上沙龙”，重磅发布云消息队列 Kafka 版 Serverless 系列基础版与专业版，与现有的标准版共同构建分层的规格体系，精准适配企业多样化业务需求。

### 精准选型，技术降本，实现60%-90%成本优化

* **基础版****[new]****：**SLA 99.5%，采用更大比例的低成本资源（包括 HDD、OSS、Spot 实例等），适合测试或流量稳定的业务场景。
* **标准版：**SLA 99.95%，2 倍无损弹性，兼顾性能与稳定性，推荐用于生产环境。
* **专业版****[new]****：**SLA 99.99%，3AZ 环境容灾，RTO=数秒，RPO=0，10 倍无损弹性，是企业级场景的推荐版本。

以搭建一个吞吐量 1200MB/s，读写比 1:1，SSD 云盘三副本的 Kafka 集群为例，云消息队列 Kafka 版 Serverless 系列相比自建显著降低成本：基础版大约降低**90%**，标准版大约降低**75%**，专业版大约降低 **60%**。

### Kafka Serverless 架构升级的五大核心特性

* **强兼容性：**100% 协议兼容和广泛适配开源 Apache Kafka 的生态工具与组件。
* **高性能**：

* 高吞吐：盘古 DFS 支持跨数据中心的容灾策略以及单存储节点打满 200 Gbps 网络的 IOPS 处理能力同时读写吞吐可横向扩展，数据可靠性达到 12 个 9，可用性高达 5 个 9。
* 低延时：存储低延时，通过用户态协议栈、闪存介质和高性能 RDMA 网络，支持百微秒级平均延迟，毫秒级长尾延迟。计算低延时，针对平均延迟，计算层无复制流量，可以充分降低网络吞吐以避免拥塞；针对长尾延迟，使用新一代分代无暂停 GC 和基于 eRDMA 的共享内存，实现的高性能内核网络协议栈，能带来最高约 30% 的时延减少和最高约 5% 的 CPU 资源节省。

* **高可用：**采用轻量且安全的 HA 机制代替开源传统的 ISR 复制，支持跨 K8s 集群、跨可用区、跨  Region 的容灾能力，确保在 K8s 集群级和 AZ 级故障时，仍具备极高可用保障。
* **秒级弹性：**通过存算分离架构实现计算节点无状态，结合轻量级 HA 机制保障秒级故障恢复，从而实现资源的秒级弹性。
* **低成本：**采用按量付费的计费模型，结合资源弹性与存储优化技术，显著降低使用成本。

### Kafka Serverless 对比开源的七大关键优势

#### 1. 计算成本

开源 Apache Kafka 通常基于本地盘或云盘构建，为保证可用性至少需要 2 副本或 3 副本，Follower 节点流量复制会带来额外的 CPU 消耗。

云消息队列 Kafka 版 Serverless 系列通过存算分离架构实现计算层单副本，免去流量复制和额外 CPU 消耗。**相比于开源版本，计算成本至少降低 50%****。**

#### 2. 网络成本

开源 Apache Kafka 基于复制保障高可用性，其分布式架构容易面临网络带宽瓶颈问题，部分云厂商的跨可用区数据传输会产生额外费用。

云消息队列 Kafka 版 Serverless 系列没有流量复制，极大优化网络带宽，单 Broker 性能得到显著提升。此外，还优化了 AZ 级可用区间的数据传输成本。

**在网络成本方面，流量越大、规格越大，云消息队列 Kafka 版 Serverless 系列的优势越明显。**

#### 3. 存储成本

*（以下存储价格仅供参考，实际价格以官方为准）*

开源 Apache Kafka 为避免处理本地盘故障和数据迁移，通常基于云盘构建 3 副本集群，存储成本较高（PL0 约 1.5元/G/月、PL1 约 3.0元/G/月）。

云消息队列 Kafka 版 Serverless 系列通过智能分层和存储优化，基于高性能盘古、低成本 HDD 及海量 OSS，推出三个规格，其对应的存储成本为：基础版约 0. 25元/G/月、标准版约 0.55元/G/月、专业版约 1.00元/G/月。**对比开源基于云盘构建 3 副本集群的存储成本，实现 10 倍的优化。**

此外，开源 Apache Kafka 需承担自运维带来的稳定性风险及人力成本，而云消息队列 Kafka 版 Serverless 系列全托管、免运维，并提供 SLA 保障，显著降低运维复杂度和成本。

#### 4. 分区迁移

开源 Apache Kafka 节点是有状态的，分区迁移涉及大量复制，受到原始节点负载数据量和磁盘吞吐等因素影响，TB 级数据至少需要小时级的恢复时长。

云消息队列 Kafka 版 Serverless 系列基于高性能分布式文件系统的一写多读能力，Follower 仅需作为计算资源的热备存在，只保有极少的元数据，无任何数据复制，可实现极快的分区迁移。

**分区迁移方面，云消息队列 Kafka 版 Serverless 系列从开源的 Kafka 小时级优化到秒级。**

#### 5. 弹性扩缩

开源 Apache Kafka 通常需要人工购买 ECS 进行部署扩容，并且 1TB 数据迁移至少需要小时级。

云消息队列 Kafka 版 Serverless 系列基于 ECS 池化和其他资源供应优化，实现多维度阶梯弹性能力：**20 MB/s - 1 GB/s 实现无损弹性，1 GB/s – 3 GB/s 实现秒级弹性，3 GB/s 以上 实现分钟级弹性。**

#### 6. 故障恢复

开源 Apache Kafka 在节点故障时，宕机节点的分区会在集群里执行并行 MakeLeader，重启后 Leader 与 Follower 需要双向数据恢复，导致端到端恢复时间较长。

云消息队列 Kafka 版 Serverless 系列通过新的机制优化该过程：新 Leader 实时感知并接管旧 Leader 目录，只需扫描极少数据，即可快速恢复。结合 ZK 的超时检测和 Kafka 的快速恢复，**实现秒级 RTO，以及存算分离架构下的最优 RTO****。**同时，支持按 Topic 优先级或其他业务维度恢复分区，进一步降低核心 Topic 的故障恢复时长。

#### 7. 读写分离

开源 Apache Kafka 存算一体架构基于本地盘和本地文件系统构建，磁盘读写共享吞吐和 IOPS，大量冷读操作会严重影响写性能。此外，由于存算比例绑定，不能灵活调整适配，整个链路的稳定性都可能受到冷读影响。

云消息队列 Kafka 版 Serverless 系列在计算层实现了网络线程、IO 线程、缓存等隔离；存储层基于弹性云盘、盘古分布式文件系统、对象存储等构建智能分层架构，实现灵活的冷热比例和端到端资源隔离。**通过读写分离替代开源的读写一体，有效避免了大量冷读对在线服务的影响****，**在保障服务质量的同时提升资源利用率。

阿里云消息队列 Kafka 版 Serverless 系列通过以上创新升级，对 Apache Kafka 进行了深度重构和优化，构建了端到端的竞争力，帮助企业进一步降低技术门槛和运维复杂度，带来成本效益、稳定可靠、灵活弹性，和高吞吐、低延时等显著优势，为企业在 AI 与大数据时代的高效数据处理提供了强有力的支撑。

以下是您可能感兴趣的一些实用信息，欢迎查看了解更多~

 **费用测算小助手**

如果您希望测算成本，可以试试我们的 Serverless 价格计算器，帮您快速估算费用*https://account.aliyun.com/login/login.htm?oauth\_callback=https%3A%2F%2Fkafkanext.console.aliyun.com%2Fserverless-calculator&lang=zh*

 **地域覆盖说明**  

目前基础版和专业版已覆盖华南、华东等主流地域，具体的支持列表可在这里查看*https://help.aliyun.com/zh/apsaramq-for-kafka/cloud-message-queue-for-kafka/product-overview/supported-regions*

 **规格选型指南**  

不同规格类型的详细说明供您参考，帮助您选择最适合自己的规格

*https://help.aliyun.com/zh/apsaramq-for-kafka/cloud-message-queue-for-kafka/product-overview/instance-editions*

 **开源对比优势**  

关于我们和开源版相比，有什么差异化优势，这份对比文档会帮您一目了然地了解

*https://help.aliyun.com/zh/apsaramq-for-kafka/cloud-message-queue-for-kafka/product-overview/comparison-between-message-queue-for-apache-kafka-and-open-source-apache-kafka*

点击此处，观看 3 月 27 日《ApsaraMQ x Confluent｜云原生 Kafka 线上沙龙》直播回放。云原生 Kafka 问卷调研截至 4 月 10 日，诚邀您参与反馈宝贵意见，阿里云定制背包和水杯等你来领！
