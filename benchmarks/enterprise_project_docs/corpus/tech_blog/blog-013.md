# CIKM 2024 |

Source: https://tech.meituan.com/2024/10/31/cikm-2024-meituan.html
Source site: 美团技术团队
Published: 2024-10-31T00:00:00+00:00
Author: soulteary@gmail.com
License: 转载需注明出处 (CC-BY-like)
Language: zh

---

> 本文精选了美团技术团队被 CIKM 2024 收录的 8 篇论文进行解读，覆盖了自监督学习、解释生成、CTR预测、跨域推荐、向量召回、图像生成、时效预测等多个技术领域。这些论文有美团独立研究，还有跟高校、科研机构合作的成果。希望能给从事相关研究工作的同学带来一些帮助或启发。

CIKM是信息检索、知识管理和数据库领域中顶级的国际学术会议，自1992年以来，CIKM成功汇聚上述三个领域的一流研究人员和开发人员，为交流有关信息与知识管理研究、数据和知识库的最新发展提供了一个国际论坛。大会的目的在于明确未来知识与信息系统发展将面临的挑战和问题，并通过征集和评估应用性和理论性强的顶尖研究成果以确定未来的研究方向。2024年，CIKM共收到全球1496篇论文投稿，最终347篇被接收，接收率约为23%。

![](https://p0.meituan.net/meituantechblog/4ec8fc866879f4704bb971e69d43354d5111649.png)

## 01 论文标题：Relative Contrastive Learning for Sequential Recommendation with Similarity-based Positive Sample Selection

**论文作者**：Zhikai Wang（Shanghai Jiao Tong University），Yanyan Shen（Shanghai Jiao Tong University），Zexi Zhang（Shanghai Jiao Tong University），Li He（Meituan），Yichun Li（Meituan），Hao Gu（Meituan）

**论文类型**：Poster（Full Research Paper track ）

**论文地址**：[PDF](https://dl.acm.org/doi/pdf/10.1145/3627673.3679681)

![](https://p0.meituan.net/meituantechblog/9eeb35352f25c5a556b113e3b65acec9354025.png)

**论文简介**：推荐领域通常面临严重的数据稀疏性问题，对比学习作为一种自监督学习方法，通过提供额外的自监督信号来增强序列推荐模型的训练。现有方法通常依赖数据增强策略来创建正样本并促进表示不变性，但往往一些策略涉及到内容排序和内容替换可能会无意中改变序列中的用户意图信息。基于自监督对比学习的方法通过选择相同目标序列（与同一目标物品的交互序列）作为正样本，为基于增强的对比学习方法提供了一种替代方案。然而，基于 SCL 的方法存在相同目标序列稀缺的问题，因而缺乏足够的对比学习信号。

本论文提出使用相似序列（具有不同的目标内容）作为额外的正样本，并引入了一种名为相对对比学习 (RCL) 的新方法用于序列推荐。所提出的 RCL 包含两级正样本选择模块和相对对比学习模块，前者模块选择相同目标序列作为强正样本，并使用相似序列作为弱正样本，后者模块采用加权的相对对比损失，确保每个序列与其强正样本的表示更接近，而不是弱正样本。在公开数据集和点评业务数据集上 RCL 都优于现有方法，该算法在论文接收前已在大众点评首页信息流推荐场景落地并取得显著的效果。

## 02 论文标题：Aligning Explanations for Recommendation with Rating and Feature via Maximizing Mutual Information

**论文作者**： Yurou Zhao（Renmin University of China），Yiding Sun（Renmin University of China），Ruidong Han（Meituan），Fei Jiang（Meituan），Lu Guan（Meituan），Xiang Li（Meituan），Wei Lin（Meituan），Weizhi Ma（Tsinghua University），Jiaxin Mao\*（Renmin University of China）

**论文类型**：Research Track Full Paper

**论文下载**：[PDF](https://arxiv.org/pdf/2407.13274)

![](https://p0.meituan.net/meituantechblog/00a1badca7666806309db2a680612eed91158.png)

**论文简介**：为用户提供基于自然语言的解释以证明推荐有助于提高用户满意度并赢得用户信任。然而，由于当前的解释生成方法通常被训练以模仿现有用户评论为目标，生成的解释往往与推荐商品的预测评分或是一些重要特征不一致，导致这些解释不能真正地帮助用户在推荐平台上做出明智的决策。为了解决这个问题，本文提出了名为MMI（最大化互信息）的优化框架，以增强生成的自然语言解释与推荐商品的预测评分/重要特征之间的一致性。

具体来说，本文使用互信息（Mutual Information, 简称MI）作为解释与预测评分/商品特征一致性的衡量标准，并训练一个基于MINE方法的互信息估计神经网络，将此神经网络作为后续的MI估计器。然后，我们将一个训练好的解释生成模型视为主干模型，基于来自MI估计器的奖励对其进行基于强化学习的微调。微调过程会指导原先的主干生成模型学习会生成与商品的预测评分及重要特征更一致的解释。在三个公开数据集上的实验表明，MMI框架可以提升不同的主模型，使它们在与推荐商品的预测评分和重要特征的一致性方面优于现有的模型。此外，本文通过用户实验验证了MI增强的解释确实有助于用户的决策，并且由于它们更好的一致性特点，与其他方法生成解释相比更能让用户满意。

## 03 论文标题：Enhancing CTR prediction through Sequential Recommendation Pre-training: Introducing the SRP4CTR framework

**论文作者**Ruidong Han（Meituan），Qianzhong Li（Meituan），He Jiang（Meituan），Rui Li（Meituan），Yurou Zhao（Meituan），Xiang Li（Meituan），Wei Lin（Meituan）

**论文类型**：Short Paper

**论文下载**：[PDF](https://arxiv.org/pdf/2407.19658)

![](https://p0.meituan.net/meituantechblog/58c8a7446fb7cc068252586591c639fe168795.png)

**论文简介**：理解用户兴趣对于点击率（CTR）预测任务至关重要。在序列推荐中，通过自监督学习从用户历史行为中进行预训练可以更好地理解用户动态偏好，展现出与CTR任务直接集成的潜力。以往的方法将预训练模型集成到下游任务中，仅用于提取语义信息或单独的用户兴趣编码，然后将这些信息作为特征加入下游模型。然而，这些方法忽略讨论了下游任务中的额外推理成本，且没有考虑如何将预训练模型中的信息高效的转移到CTR任务预测的特定估计项中。

为了解决这一问题，本文提出了增强CTR预测的序列推荐预训练框架（SRP4CTR）。首先，我们系统的讨论了引入预训练模型对推理成本的影响。随后，我们引入了一种新的预训练方法来尽可能保证编码时信息的完整性。在微调过程中，本文还引入了一个交叉注意力模块，以较低的成本建立了估计项与预训练模型之间的桥梁。此外，本文采用了一种新的自查询技术，以促进从预训练模型到工业CTR模型间的知识转移。离线和在线实验表明，本文的方法优于以前的基线模型。

## 04 论文标题：EXIT: An EXplicit Interest Transfer Framework for Cross-Domain Recommendation

**论文作者**：Lei Huang（Meituan），Weitao Li（Meituan），Chenrui Zhang，Jinpeng Wang（Meituan），Xianchun Yi（Meituan），Sheng Chen（Meituan），

**论文类型**：Applied Research Paper

**论文下载**：[PDF](https://arxiv.org/pdf/2407.20121)

![](https://p0.meituan.net/meituantechblog/523b971167ad9437806221e1063aa0092553393.png)

**论文简介**：跨域推荐是指利用其他领域的知识增强推荐系统对用户兴趣的预测精度，在工业应用中受到了广泛关注。现有的隐式建模跨域推荐方法并未考虑不同域之间服务功能和商品展现形式的差异，导致在落地过程中产生严重的负迁移问题。例如，用户在金刚和搜索中大量表达对医药、闪购等紧急需求的兴趣，直接将这些信号用于推荐系统并大量推送医药和闪购产品显然不合适。为解决这一挑战，本文提出了一种显式兴趣迁移框架，通过显式建模不同的用户上下文场景下源域信号向目标域迁移的概率，实现对目标域兴趣信号的筛选。无需复杂的网络结构及繁琐的模型训练过程，本文提出的显式框架能快速在工业推荐系统落地，为跨域推荐提供了一种简单而有效的解决方案。该算法已在美团首页推荐系统部署上线。

**论文作者**：Yadong Zhang（Meituan），Yuqing Song（Meituan），Siyu Lu（Meituan），Qiang Liu（Meituan），Xingxing Wang（Meituan）

**论文类型**：Short Paper

**论文下载**：[PDF](https://dl.acm.org/doi/pdf/10.1145/3627673.3680005)

![](https://p0.meituan.net/meituantechblog/98efa20529bd262475821dfa922c389b681112.png)

**论文简介**：向量召回是搜索系统的重要能力之一，通过将搜索词、用户和商品的信息编码为稠密向量，为用户检索出高质量的候选。然而，在即时零售场景下，搜索词（Query）存在两类极端问题：1）短Query通常为模糊意图，例如鲜花，2）长Query包含大量噪声实体，例如巧克力鲜花费列罗。这两类情况导致很难识别用户确切的搜索意图。实际上，消费者对于搜索的商品有心理图像预期，反映了他们特定的购买意图，基于此，本文提出了视觉预期增强的多模态检索模型来建模用户的潜在视觉偏好。具体来说，通过重建Query共性和用户个性的图像表征，并且与语义、用户行为序列等多模态信息相融合，增强了对用户搜索意图的理解，从而提升检索效果。通过搜索广告系统中的在线A/B实验，该方法在相较于基线在收入、点击和点击率等关键指标上取得了显著提升。此外，审稿人评价本文是多模态增强搜索理解的首批论文之一。

## 06 论文标题：Design Element Aware Poster Layout Generation

**论文作者**：Yinan Li（Meituan），Jia Chen（Meituan），Yin Bai（Meituan），Jia Cheng（Meituan），Jun Lei（Meituan）

**论文类型**：Full Research Paper

**论文下载**：[PDF](https://dl.acm.org/doi/pdf/10.1145/3627673.3679557)

![](https://p0.meituan.net/meituantechblog/72cad02d9f3b634cdd641047a607eb46215012.png)

**论文简介**：图像创意在广告系统中起着重要的作用，利用商户素材制作优质的图片创意能够帮助广告主吸引更多的用户、获得更多的点击。海报布局生成领域虽然在近期取得了显著进展，但现有的方法多关注于对海报背景的理解，而忽略了设计元素（例如文字、Logo和底纹）对布局的影响，这导致生成的布局经常存在明显的视觉瑕疵，包括（1）尺寸不当，例如将较短的文字放入较大的文本框中或将长文本放入较小的文本框中，以及（2）图像失真，例如拉伸变形的logo图标。 为此，本文定义了一个新的布局生成任务：感知设计元素的海报布局生成，该任务要求生成的布局不仅适配于背景图片，还要与给定的设计元素相匹配。

本文提出了一种名为Design Element aware Transformer (DET)的编码器-解码器网络，以生成既适合背景图像，又适配设计元素的合理布局。其中，编码器通过可变形自注意力从背景图像及其显著性图中提取细粒度的多尺度表示，解码器接收背景特征，通过可变形交叉注意力的方式将给定的设计元素内容特征、期望的宽高比特征与背景特征进行关联，生成最适合各个给定的设计元素布局位置。同时，本文提出了一种新的评估指标AspDiff，用于衡量生成的布局与给定设计元素的匹配程度。 在三个公开海报数据集上的定量和定性评估表明，与其他布局生成方法相比，DET生成的布局框能更好的适配给定的设计元素，取得更好的视觉效果。该算法在论文接收前已应用上线，在展示、联盟等站内外主要广告场景中落地。

## 07 论文标题：Process-Informed Deep Learning for Enhanced Order Fulfillment Cycle Time Prediction in On-Demand Grocery Retailing

**论文作者**：Jiawen Wei（Meituan），Ziwen Ye（Meituan），Chuan Yang（Nankai University），Chen Chen（Meituan），Guangrui Ma（Meituan）

**论文类型**：Applied Research Paper

**论文下载**：[PDF](https://dl.acm.org/doi/pdf/10.1145/3627673.3680056)

![](https://p0.meituan.net/meituantechblog/7b3949a4b160d2d5a4a820ad506336855224593.jpg)

**论文简介**：在即时零售（On-demand Grocery Retail, OGR）领域，准确预测订单履约周期时间（Order Fulfillment Cycle Time, OFCT）对于提高客户满意度和运营效率至关重要。由于自营前置仓+配送的模式，小象这类OGR平台有着与即时外卖配送（On-demand Food Delivery, OFD）平台不一样的运营调度策略和可用数据，面临着截然不同的时效预测挑战。本文阐述了两种领域下时效预测问题的区别，提出了一种基于物理世界OGR订单履行过程的深度学习模型，用显式建模的方式刻画了订单量、生产能力、配送能力及调度策略等多种因素对OGR履约时效的影响。具体来说，我们使用多个循环神经网络（RNN）模块来动态评估生产和配送阶段的产能负载，并结合一系列专门的注意力模块来捕捉订单-订单之间以及潜在骑手-订单之间的相互作用对调度系统中订单履约优先级的影响。此外，我们的方法还利用深度贝叶斯多目标学习（DBMTL）来识别订单履约前序阶段对后续阶段的影响。该方法在小象数据集上已验证其优越性。我们的研究在OFCT预测方面取得了显著进展，为寻求优化履约流程和提升客户体验的OGR平台提供了深刻洞见。

## 08 论文标题：《Collaborative Scope: Encountering the Substitution Effect within the Delivery Scope in Online Food Delivery Platform》

**论文作者**：Yida Zhu（Meituan），Liying Chen（Meituan），Chen Zheng（Meituan），Jia Shi（Meituan），Daping Xiong（Meituan），Zewen Huang（Meituan），Shihao Ren（Meituan），Shuiping Chen（Meituan），Jinghua Hao（Meituan），Renqing He（Meituan）

**论文类型**：Applied Research Paper

**论文下载**：[PDF](https://dl.acm.org/doi/pdf/10.1145/3627673.3680029)

![](https://p0.meituan.net/meituantechblog/50c59c9ed4069be24644288c9297b63f3105294.png)

**论文简介**：商家配送范围定义了为顾客提供服务的地理区域，决定了用户所能看到的商家集合。在绘制这些范围时，构建准确的订单转化预估模型和合理刻画配送难度，是平衡平台规模与配送体验及效率的关键。目前的方法忽略了用户在选择商家时商家之间存在的替代关系这一前提，从单个商家的视角预估转化率。此外，由于大规模商家组合优化求解的复杂性，也增加了多商家联合决策的难度。

基于此，本论文将问题建模为多商家选品问题，提出了一种基于机器学习+组合优化的决策算法框架，从用户视角预估不同商家集合下的订单变化，确保其符合商家间存在替代关系的先验假设。为了解决求解效率问题，通过在组合优化中引入一阶泰勒级数近似的方法进行了优化。该算法框架在美团拼好饭业务上已全量，线上结果显示，在规模不受影响的情况下，通过降低订单交付距离，显著提高了交付效率。

| 本文系美团技术团队出品，著作权归属美团。欢迎出于分享和交流等非商业目的转载或使用本文内容，敬请注明“内容转载自美团技术团队”。本文未经许可，不得进行商业性转载或者使用。任何商用行为，请发送邮件至tech@meituan.com申请授权。
