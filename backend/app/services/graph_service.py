"""知识图谱导出服务"""
from typing import Optional, Dict, List, Any
import networkx as nx


class GraphService:
    """知识图谱服务"""

    def __init__(self, rag):
        """
        初始化图谱服务

        Args:
            rag: RAGAnything 实例
        """
        self.rag = rag

    async def export_graph(
        self,
        doc_id: Optional[str] = None,
        limit: int = 1000
    ) -> Dict[str, Any]:
        """
        导出知识图谱为 vis.js 格式

        Args:
            doc_id: 可选的文档 ID 过滤
            limit: 返回的最大节点数

        Returns:
            包含 nodes, edges, stats 的字典
        """
        # 1. 从 LightRAG 提取实体和关系
        entities, relations = await self._get_graph_data(doc_id, limit)

        # 2. 转换为 vis.js 格式
        nodes = self._format_nodes(entities)
        edges = self._format_edges(relations)

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges)
            }
        }

    async def _get_graph_data(
        self,
        doc_id: Optional[str],
        limit: int
    ) -> tuple[List[Dict], List[Dict]]:
        """
        从 LightRAG 的 NetworkX 图中提取实体和关系
        """
        entities = []
        relations = []

        try:
            # 确保 LightRAG 已初始化
            if not hasattr(self.rag, 'lightrag') or self.rag.lightrag is None:
                await self.rag._ensure_lightrag_initialized()

            # 访问 NetworkX 图
            if hasattr(self.rag.lightrag, 'chunk_entity_relation_graph'):
                graph_storage = self.rag.lightrag.chunk_entity_relation_graph

                # 获取 NetworkX 图对象
                if hasattr(graph_storage, '_graph') and isinstance(graph_storage._graph, nx.Graph):
                    G = graph_storage._graph

                    print(f"Found NetworkX graph with {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

                    # 提取节点（实体）
                    for node_id in list(G.nodes())[:limit]:
                        node_data = G.nodes[node_id]

                        # 尝试从 full_entities 获取完整信息
                        entity_info = None
                        if hasattr(self.rag.lightrag, 'full_entities'):
                            entity_info = await self.rag.lightrag.full_entities.get_by_id(node_id)

                        if entity_info:
                            entities.append({
                                "entity_name": node_id,
                                "entity_type": entity_info.get("entity_type", "concept"),
                                "description": entity_info.get("description", "")[:200]
                            })
                        else:
                            entities.append({
                                "entity_name": node_id,
                                "entity_type": node_data.get("entity_type", "concept"),
                                "description": node_data.get("description", "")[:200] if "description" in node_data else ""
                            })

                    print(f"Extracted {len(entities)} entities")

                    # 提取边（关系）
                    for src, tgt, edge_data in G.edges(data=True):
                        relations.append({
                            "src_id": src,
                            "tgt_id": tgt,
                            "keywords": edge_data.get("keywords", ""),
                            "weight": edge_data.get("weight", 1.0)
                        })

                    print(f"Extracted {len(relations)} relations")

        except Exception as e:
            print(f"Error getting graph data: {e}")
            import traceback
            traceback.print_exc()

        return entities, relations

    def _format_nodes(self, entities: List[Dict]) -> List[Dict]:
        """格式化节点为 vis.js 格式"""
        nodes = []

        for e in entities:
            entity_name = e.get("entity_name", e.get("label", e.get("id", "Unknown")))
            entity_type = e.get("entity_type", "concept")
            description = e.get("description", "")[:200]

            nodes.append({
                "id": entity_name,
                "label": entity_name,
                "type": entity_type,
                "description": description,
                "color": self._get_color_by_type(entity_type),
                "shape": "diamond" if e.get("is_multimodal") else "dot"
            })

        return nodes

    def _format_edges(self, relations: List[Dict]) -> List[Dict]:
        """格式化边为 vis.js 格式"""
        edges = []

        for r in relations:
            src_id = r.get("src_id", r.get("source", ""))
            tgt_id = r.get("tgt_id", r.get("target", ""))
            keywords = r.get("keywords", r.get("label", ""))

            # 提取第一个关键词作为标签
            label = keywords.split(",")[0] if keywords else ""

            edges.append({
                "from": src_id,
                "to": tgt_id,
                "label": label,
                "width": r.get("weight", 1.0)
            })

        return edges

    def _get_color_by_type(self, entity_type: str) -> str:
        """根据实体类型返回颜色"""
        colors = {
            "concept": "#4CAF50",
            "person": "#2196F3",
            "organization": "#FF9800",
            "location": "#9C27B0",
            "table": "#F44336",
            "image": "#00BCD4",
            "equation": "#FFEB3B",
        }
        return colors.get(entity_type, "#9E9E9E")

    def _get_sample_entities(self) -> List[Dict]:
        """返回示例实体数据（用于测试）"""
        return [
            {
                "entity_name": "机器学习",
                "entity_type": "concept",
                "description": "一种人工智能技术"
            },
            {
                "entity_name": "深度学习",
                "entity_type": "concept",
                "description": "机器学习的一个分支"
            },
            {
                "entity_name": "神经网络",
                "entity_type": "concept",
                "description": "深度学习的基础"
            },
            {
                "entity_name": "数据科学",
                "entity_type": "concept",
                "description": "利用数据进行分析和建模"
            }
        ]

    def _get_sample_relations(self, entity_ids: List[str]) -> List[Dict]:
        """返回示例关系数据（用于测试）"""
        if len(entity_ids) < 2:
            return []

        return [
            {
                "src_id": "机器学习",
                "tgt_id": "深度学习",
                "keywords": "包含",
                "weight": 1.0
            },
            {
                "src_id": "深度学习",
                "tgt_id": "神经网络",
                "keywords": "基于",
                "weight": 1.0
            },
            {
                "src_id": "机器学习",
                "tgt_id": "数据科学",
                "keywords": "应用于",
                "weight": 1.0
            }
        ]
