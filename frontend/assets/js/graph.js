/**
 * 知识图谱可视化
 */

let network = null;
let nodesDataSet = null;
let edgesDataSet = null;

/**
 * 加载知识图谱
 */
async function loadGraph(docId = null) {
    const spinner = document.getElementById('graphSpinner');
    spinner.classList.remove('d-none');

    try {
        const url = docId
            ? `${API_ENDPOINTS.graph}?doc_id=${docId}&limit=1000`
            : `${API_ENDPOINTS.graph}?limit=1000`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('加载图谱失败');
        }

        const data = await response.json();
        renderGraph(data);
        updateGraphStats(data.stats);
    } catch (error) {
        console.error('加载图谱失败:', error);
        showError(`加载图谱失败: ${error.message}`);
    } finally {
        spinner.classList.add('d-none');
    }
}

/**
 * 渲染知识图谱
 */
function renderGraph(data) {
    const container = document.getElementById('graphContainer');

    // 创建数据集
    nodesDataSet = new vis.DataSet(data.nodes.map(node => ({
        id: node.id,
        label: node.label,
        title: createNodeTooltip(node),
        color: node.color || '#9E9E9E',
        shape: node.shape || 'dot',
        size: 20,
        font: {
            size: 14,
            color: '#333333'
        },
        data: node  // 保存完整节点数据
    })));

    edgesDataSet = new vis.DataSet(data.edges.map(edge => ({
        from: edge.from,
        to: edge.to,
        label: edge.label || '',
        width: edge.width || 1,
        arrows: 'to',
        font: {
            size: 10,
            align: 'middle',
            color: '#666666'
        },
        smooth: {
            type: 'continuous'
        }
    })));

    // 配置选项
    const options = {
        nodes: {
            borderWidth: 2,
            borderWidthSelected: 3,
            shadow: true
        },
        edges: {
            color: {
                color: '#848484',
                highlight: '#2B7CE9',
                hover: '#2B7CE9'
            },
            smooth: {
                type: 'continuous',
                roundness: 0.5
            }
        },
        physics: {
            enabled: true,
            stabilization: {
                enabled: true,
                iterations: 100,
                updateInterval: 25
            },
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.3,
                springLength: 95,
                springConstant: 0.04,
                damping: 0.09,
                avoidOverlap: 0.1
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 200,
            navigationButtons: true,
            keyboard: true
        }
    };

    // 创建网络
    network = new vis.Network(container, {
        nodes: nodesDataSet,
        edges: edgesDataSet
    }, options);

    // 绑定事件
    bindGraphEvents();
}

/**
 * 绑定图谱事件
 */
function bindGraphEvents() {
    if (!network) return;

    // 点击节点
    network.on('click', function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = nodesDataSet.get(nodeId);
            showNodeDetails(node.data);
        }
    });

    // 双击节点 - 聚焦
    network.on('doubleClick', function(params) {
        if (params.nodes.length > 0) {
            network.focus(params.nodes[0], {
                scale: 1.5,
                animation: {
                    duration: 1000,
                    easingFunction: 'easeInOutQuad'
                }
            });
        }
    });

    // 稳定完成
    network.on('stabilizationIterationsDone', function() {
        network.setOptions({ physics: false });
    });
}

/**
 * 创建节点工具提示
 */
function createNodeTooltip(node) {
    return `
        <div style="max-width: 300px;">
            <strong>${node.label}</strong><br>
            <em>类型: ${node.type}</em><br>
            ${node.description ? `<div style="margin-top: 5px;">${node.description.substring(0, 100)}...</div>` : ''}
        </div>
    `;
}

/**
 * 显示节点详情
 */
function showNodeDetails(node) {
    const details = `
        <div class="mb-2"><strong>标签:</strong> ${node.label}</div>
        <div class="mb-2"><strong>类型:</strong> <span class="badge" style="background-color: ${node.color}">${node.type}</span></div>
        ${node.description ? `
            <div class="mb-2">
                <strong>描述:</strong>
                <p class="mt-1">${node.description}</p>
            </div>
        ` : ''}
        <div class="mt-3">
            <button class="btn btn-sm btn-primary" onclick="searchRelatedNodes('${node.id}')">
                查看相关节点
            </button>
        </div>
    `;

    showModal('节点详情', details);
}

/**
 * 搜索相关节点
 */
function searchRelatedNodes(nodeId) {
    if (!network) return;

    // 获取连接的节点
    const connectedNodes = network.getConnectedNodes(nodeId);

    // 高亮显示
    network.selectNodes([nodeId, ...connectedNodes]);

    // 聚焦到节点
    network.focus(nodeId, {
        scale: 1.2,
        animation: {
            duration: 1000,
            easingFunction: 'easeInOutQuad'
        }
    });

    // 关闭模态框
    const modal = bootstrap.Modal.getInstance(document.getElementById('nodeModal'));
    if (modal) {
        modal.hide();
    }
}

/**
 * 重置图谱视图
 */
function resetGraph() {
    if (network) {
        network.fit({
            animation: {
                duration: 1000,
                easingFunction: 'easeInOutQuad'
            }
        });

        // 取消选择
        network.unselectAll();

        // 重新启用物理引擎
        network.setOptions({ physics: true });
        setTimeout(() => {
            network.setOptions({ physics: false });
        }, 2000);
    }
}

/**
 * 更新图谱统计
 */
function updateGraphStats(stats) {
    const statsDiv = document.getElementById('graphStats');

    if (stats) {
        statsDiv.innerHTML = `
            <span><strong>节点:</strong> ${stats.total_nodes}</span>
            <span class="ms-3"><strong>边:</strong> ${stats.total_edges}</span>
        `;
    }
}

/**
 * 按类型筛选节点
 */
function filterNodesByType(type) {
    if (!nodesDataSet || !network) return;

    const allNodes = nodesDataSet.get();

    if (type === 'all') {
        // 显示所有节点
        allNodes.forEach(node => {
            nodesDataSet.update({ id: node.id, hidden: false });
        });
    } else {
        // 筛选特定类型
        allNodes.forEach(node => {
            const shouldShow = node.data.type === type;
            nodesDataSet.update({ id: node.id, hidden: !shouldShow });
        });
    }

    network.fit();
}

/**
 * 搜索节点
 */
function searchNodes(query) {
    if (!nodesDataSet || !network || !query) {
        resetGraph();
        return;
    }

    const allNodes = nodesDataSet.get();
    const matchingNodes = allNodes.filter(node =>
        node.label.toLowerCase().includes(query.toLowerCase()) ||
        (node.data.description && node.data.description.toLowerCase().includes(query.toLowerCase()))
    );

    if (matchingNodes.length > 0) {
        const nodeIds = matchingNodes.map(n => n.id);
        network.selectNodes(nodeIds);

        // 聚焦到第一个匹配节点
        network.focus(nodeIds[0], {
            scale: 1.5,
            animation: {
                duration: 1000,
                easingFunction: 'easeInOutQuad'
            }
        });
    } else {
        showError('未找到匹配的节点');
    }
}
