"""V1 知识图谱 API"""
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from app.dependencies import get_rag_instance
from app.services.graph_service import GraphService
from app.middleware.auth import verify_api_key
from app.middleware.response import wrap_response, ErrorCode
from app.models.response import V1GraphData, V1GraphNode, V1GraphEdge, V1GraphStatsData

router = APIRouter()


@router.get("")
async def get_knowledge_graph(
    doc_id: Optional[str] = Query(None, description="可选的文档 ID 过滤"),
    limit: int = Query(1000, description="返回的最大节点数", ge=1, le=5000),
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    获取完整图谱（vis.js 格式）

    - **doc_id**: 可选的文档 ID 过滤
    - **limit**: 返回的最大节点数
    """
    try:
        graph_service = GraphService(rag)
        graph_data = await graph_service.export_graph(doc_id, limit)

        nodes = [
            V1GraphNode(
                id=n["id"],
                label=n["label"],
                type=n.get("type", "concept"),
                description=n.get("description", "")
            ).model_dump()
            for n in graph_data["nodes"]
        ]

        edges = [
            {"from": e["from"], "to": e["to"], "label": e.get("label", "")}
            for e in graph_data["edges"]
        ]

        return wrap_response(
            data=V1GraphData(
                nodes=nodes,
                edges=edges
            ).model_dump()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.RAG_ERROR,
                message=f"获取图谱失败: {str(e)}"
            )
        )


@router.get("/entities")
async def get_entities(
    doc_id: Optional[str] = Query(None, description="可选的文档 ID 过滤"),
    entity_type: Optional[str] = Query(None, description="实体类型过滤"),
    limit: int = Query(100, description="返回的最大数量", ge=1, le=1000),
    offset: int = Query(0, description="偏移量", ge=0),
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    获取实体列表

    - **doc_id**: 可选的文档 ID 过滤
    - **entity_type**: 可选的实体类型过滤
    - **limit**: 返回的最大数量
    - **offset**: 分页偏移量
    """
    try:
        graph_service = GraphService(rag)
        graph_data = await graph_service.export_graph(doc_id, limit + offset)

        entities = graph_data["nodes"]

        # 类型过滤
        if entity_type:
            entities = [e for e in entities if e.get("type") == entity_type]

        # 分页
        entities = entities[offset:offset + limit]

        return wrap_response(
            data={
                "total": len(graph_data["nodes"]),
                "entities": [
                    {
                        "id": e["id"],
                        "label": e["label"],
                        "type": e.get("type", "concept"),
                        "description": e.get("description", "")
                    }
                    for e in entities
                ]
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.RAG_ERROR,
                message=f"获取实体失败: {str(e)}"
            )
        )


@router.get("/relations")
async def get_relations(
    doc_id: Optional[str] = Query(None, description="可选的文档 ID 过滤"),
    entity: Optional[str] = Query(None, description="实体名称过滤（查找与该实体相关的关系）"),
    limit: int = Query(100, description="返回的最大数量", ge=1, le=1000),
    offset: int = Query(0, description="偏移量", ge=0),
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    获取关系列表

    - **doc_id**: 可选的文档 ID 过滤
    - **entity**: 可选的实体名称过滤
    - **limit**: 返回的最大数量
    - **offset**: 分页偏移量
    """
    try:
        graph_service = GraphService(rag)
        graph_data = await graph_service.export_graph(doc_id, 5000)

        relations = graph_data["edges"]

        # 实体过滤
        if entity:
            relations = [
                r for r in relations
                if r.get("from") == entity or r.get("to") == entity
            ]

        total = len(relations)

        # 分页
        relations = relations[offset:offset + limit]

        return wrap_response(
            data={
                "total": total,
                "relations": [
                    {
                        "from": r["from"],
                        "to": r["to"],
                        "label": r.get("label", ""),
                        "weight": r.get("width", 1.0)
                    }
                    for r in relations
                ]
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.RAG_ERROR,
                message=f"获取关系失败: {str(e)}"
            )
        )


@router.get("/subgraph")
async def get_subgraph(
    entity: Optional[str] = Query(None, description="中心实体名称"),
    depth: int = Query(2, description="查询深度", ge=1, le=5),
    doc_ids: Optional[str] = Query(None, description="文档 ID 列表（逗号分隔）"),
    limit: int = Query(100, description="最大节点数", ge=1, le=1000),
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    获取子图（按实体/文档筛选）

    - **entity**: 中心实体名称
    - **depth**: 查询深度 (1-5)
    - **doc_ids**: 文档 ID 列表（逗号分隔）
    - **limit**: 最大节点数
    """
    try:
        graph_service = GraphService(rag)

        # 如果指定了中心实体，获取相关子图
        if entity:
            # 获取完整图谱
            full_graph = await graph_service.export_graph(None, 5000)

            # BFS 查找相关节点
            related_nodes = set()
            current_level = {entity}

            for _ in range(depth):
                next_level = set()
                for edge in full_graph["edges"]:
                    if edge["from"] in current_level:
                        next_level.add(edge["to"])
                        related_nodes.add(edge["from"])
                        related_nodes.add(edge["to"])
                    if edge["to"] in current_level:
                        next_level.add(edge["from"])
                        related_nodes.add(edge["from"])
                        related_nodes.add(edge["to"])
                current_level = next_level

            # 过滤节点和边
            nodes = [n for n in full_graph["nodes"] if n["id"] in related_nodes][:limit]
            node_ids = {n["id"] for n in nodes}
            edges = [
                e for e in full_graph["edges"]
                if e["from"] in node_ids and e["to"] in node_ids
            ]

        else:
            # 没有指定实体，返回完整图谱（带 limit）
            doc_id = doc_ids.split(",")[0] if doc_ids else None
            graph_data = await graph_service.export_graph(doc_id, limit)
            nodes = graph_data["nodes"]
            edges = graph_data["edges"]

        return wrap_response(
            data={
                "nodes": [
                    {
                        "id": n["id"],
                        "label": n["label"],
                        "type": n.get("type", "concept")
                    }
                    for n in nodes
                ],
                "edges": [
                    {
                        "from": e["from"],
                        "to": e["to"],
                        "label": e.get("label", "")
                    }
                    for e in edges
                ]
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.RAG_ERROR,
                message=f"获取子图失败: {str(e)}"
            )
        )


@router.get("/stats")
async def get_graph_stats(
    rag=Depends(get_rag_instance),
    api_key: str = Depends(verify_api_key)
):
    """
    获取图谱统计信息
    """
    try:
        graph_service = GraphService(rag)
        graph_data = await graph_service.export_graph(None, 10000)

        nodes = graph_data["nodes"]
        edges = graph_data["edges"]

        # 统计实体类型分布
        entity_types = {}
        for node in nodes:
            node_type = node.get("type", "concept")
            entity_types[node_type] = entity_types.get(node_type, 0) + 1

        # 计算 Top 实体（按连接数）
        node_connections = {}
        for edge in edges:
            node_connections[edge["from"]] = node_connections.get(edge["from"], 0) + 1
            node_connections[edge["to"]] = node_connections.get(edge["to"], 0) + 1

        top_entities = sorted(
            [
                {"id": k, "connections": v}
                for k, v in node_connections.items()
            ],
            key=lambda x: x["connections"],
            reverse=True
        )[:10]

        return wrap_response(
            data=V1GraphStatsData(
                total_entities=len(nodes),
                total_relations=len(edges),
                entity_types=entity_types,
                top_entities=top_entities
            ).model_dump()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=wrap_response(
                code=ErrorCode.RAG_ERROR,
                message=f"获取统计信息失败: {str(e)}"
            )
        )
