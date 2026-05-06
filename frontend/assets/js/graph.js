/**
 * Neural RAG - Knowledge Graph Visualization
 * vis.js network with fullscreen, search, and details panel
 */

const GraphManager = {
    network: null,
    nodesDataSet: null,
    edgesDataSet: null,
    isFullscreen: false,
    selectedNode: null,

    init() {
        this.bindEvents();
        this.loadGraph();
    },

    bindEvents() {
        // Search
        const searchInput = document.getElementById('graphSearch');
        searchInput?.addEventListener('input', debounce((e) => {
            this.searchNodes(e.target.value);
        }, 300));

        // Document filter
        document.getElementById('graphDocFilter')?.addEventListener('change', (e) => {
            this.loadGraph(e.target.value === 'all' ? null : e.target.value);
        });

        // Zoom controls
        document.getElementById('zoomInBtn')?.addEventListener('click', () => {
            if (this.network) {
                const scale = this.network.getScale() * 1.3;
                this.network.moveTo({ scale });
            }
        });

        document.getElementById('zoomOutBtn')?.addEventListener('click', () => {
            if (this.network) {
                const scale = this.network.getScale() / 1.3;
                this.network.moveTo({ scale });
            }
        });

        document.getElementById('resetViewBtn')?.addEventListener('click', () => {
            this.resetView();
        });

        // Fullscreen
        document.getElementById('fullscreenBtn')?.addEventListener('click', () => {
            this.toggleFullscreen();
        });

        // Close details panel
        document.getElementById('closeDetailsBtn')?.addEventListener('click', () => {
            this.hideDetailsPanel();
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'f' && document.activeElement?.tagName !== 'INPUT' &&
                document.activeElement?.tagName !== 'TEXTAREA') {
                const graphPanel = document.getElementById('panel-graph');
                if (graphPanel?.classList.contains('active')) {
                    e.preventDefault();
                    this.toggleFullscreen();
                }
            }
            if (e.key === 'Escape' && this.isFullscreen) {
                this.toggleFullscreen();
            }
        });
    },

    async loadGraph(docId = null) {
        const loading = document.getElementById('graphLoading');
        if (loading) loading.classList.remove('hidden');

        try {
            const data = await GraphApi.get(docId);

            this.renderGraph(data);
            this.updateStats(data.stats);
            this.updateDocumentFilter();

        } catch (error) {
            console.error('Failed to load graph:', error);
            Toast.error('加载知识图谱失败');
        } finally {
            if (loading) loading.classList.add('hidden');
        }
    },

    renderGraph(data) {
        const container = document.getElementById('graphContainer');
        if (!container) return;

        // Process nodes
        const nodes = (data.nodes || []).map(node => ({
            id: node.id,
            label: this.truncateLabel(node.label),
            title: this.createTooltip(node),
            color: this.getNodeColor(node.type),
            shape: 'dot',
            size: 15 + Math.min(node.connections || 0, 10),
            font: {
                color: 'var(--text-primary)',
                size: 12,
            },
            borderWidth: 2,
            borderWidthSelected: 3,
            shadow: {
                enabled: true,
                color: 'rgba(0, 212, 255, 0.3)',
                size: 10,
            },
            _data: node,
        }));

        // Process edges
        const edges = (data.edges || []).map(edge => ({
            from: edge.from,
            to: edge.to,
            label: edge.label || '',
            arrows: 'to',
            width: 1,
            color: {
                color: 'var(--graph-edge)',
                highlight: 'var(--graph-edge-hover)',
                hover: 'var(--graph-edge-hover)',
            },
            font: {
                color: 'var(--text-tertiary)',
                size: 10,
                strokeWidth: 0,
            },
            smooth: {
                type: 'continuous',
                roundness: 0.5,
            },
        }));

        this.nodesDataSet = new vis.DataSet(nodes);
        this.edgesDataSet = new vis.DataSet(edges);

        const options = {
            nodes: {
                font: {
                    face: 'DM Sans, sans-serif',
                },
            },
            edges: {
                smooth: {
                    type: 'continuous',
                },
            },
            physics: {
                enabled: true,
                stabilization: {
                    enabled: true,
                    iterations: 100,
                    updateInterval: 25,
                },
                barnesHut: {
                    gravitationalConstant: -3000,
                    centralGravity: 0.3,
                    springLength: 120,
                    springConstant: 0.04,
                    damping: 0.09,
                    avoidOverlap: 0.2,
                },
            },
            interaction: {
                hover: true,
                tooltipDelay: 200,
                hideEdgesOnDrag: true,
                hideEdgesOnZoom: true,
            },
        };

        // Create or update network
        if (this.network) {
            this.network.setData({
                nodes: this.nodesDataSet,
                edges: this.edgesDataSet,
            });
        } else {
            this.network = new vis.Network(container, {
                nodes: this.nodesDataSet,
                edges: this.edgesDataSet,
            }, options);

            // Bind network events
            this.bindNetworkEvents();
        }
    },

    bindNetworkEvents() {
        if (!this.network) return;

        // Click on node
        this.network.on('click', (params) => {
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const node = this.nodesDataSet.get(nodeId);
                this.showNodeDetails(node._data);
            } else {
                this.hideDetailsPanel();
            }
        });

        // Double-click to focus
        this.network.on('doubleClick', (params) => {
            if (params.nodes.length > 0) {
                this.network.focus(params.nodes[0], {
                    scale: 1.5,
                    animation: {
                        duration: 500,
                        easingFunction: 'easeInOutQuad',
                    },
                });
            }
        });

        // Stabilization complete
        this.network.on('stabilizationIterationsDone', () => {
            this.network.setOptions({ physics: false });
        });

        // Hover effects
        this.network.on('hoverNode', () => {
            document.body.style.cursor = 'pointer';
        });

        this.network.on('blurNode', () => {
            document.body.style.cursor = 'default';
        });
    },

    showNodeDetails(node) {
        const panel = document.getElementById('nodeDetailsPanel');
        const content = document.getElementById('nodeDetailsContent');

        if (!panel || !content || !node) return;

        this.selectedNode = node;

        // Get connected nodes
        const connectedIds = this.network.getConnectedNodes(node.id);
        const connectedEdges = this.network.getConnectedEdges(node.id);

        // Build relations list
        const relations = connectedEdges.map(edgeId => {
            const edge = this.edgesDataSet.get(edgeId);
            const isOutgoing = edge.from === node.id;
            const targetId = isOutgoing ? edge.to : edge.from;
            const targetNode = this.nodesDataSet.get(targetId);

            return {
                direction: isOutgoing ? '→' : '←',
                label: edge.label || '相关',
                target: targetNode?.label || '未知实体',
                targetId,
            };
        });

        const typeColor = this.getNodeColor(node.type);

        content.innerHTML = `
            <div class="node-label">${escapeHtml(node.label)}</div>
            <div class="node-type" style="background: ${typeColor}20; color: ${typeColor};">
                ${node.type || '实体'}
            </div>
            ${node.description ? `
                <div class="node-description">${escapeHtml(node.description)}</div>
            ` : ''}
            ${relations.length > 0 ? `
                <div class="node-relations">
                    <h4>关联关系（${relations.length}）</h4>
                    ${relations.slice(0, 10).map(r => `
                        <div class="relation-item" data-target-id="${r.targetId}">
                            <span class="relation-arrow">${r.direction}</span>
                            <span class="relation-label">${escapeHtml(r.label)}</span>
                            <span class="relation-target">${escapeHtml(r.target)}</span>
                        </div>
                    `).join('')}
                    ${relations.length > 10 ? `
                        <div class="relation-item" style="color: var(--text-muted);">
                            还有 ${relations.length - 10} 条关系
                        </div>
                    ` : ''}
                </div>
            ` : ''}
            <div style="margin-top: var(--space-4);">
                <button class="btn btn-primary btn-sm" id="queryNodeBtn">
                    询问该实体
                </button>
            </div>
        `;

        // Bind relation clicks
        content.querySelectorAll('.relation-item[data-target-id]').forEach(item => {
            item.addEventListener('click', () => {
                const targetId = item.dataset.targetId;
                this.network.focus(targetId, {
                    scale: 1.5,
                    animation: { duration: 500 },
                });
                this.network.selectNodes([targetId]);
                const targetNode = this.nodesDataSet.get(targetId);
                if (targetNode) {
                    this.showNodeDetails(targetNode._data);
                }
            });
        });

        // Bind query button
        content.querySelector('#queryNodeBtn')?.addEventListener('click', () => {
            // Switch to query tab and pre-fill
            const queryInput = document.getElementById('queryInput');
            if (queryInput) {
                queryInput.value = `请介绍一下“${node.label}”`;
            }
            // Switch tab
            document.querySelector('.tab-btn[data-tab="query"]')?.click();
        });

        panel.classList.add('active');
    },

    hideDetailsPanel() {
        const panel = document.getElementById('nodeDetailsPanel');
        panel?.classList.remove('active');
        this.selectedNode = null;
        this.network?.unselectAll();
    },

    searchNodes(query) {
        if (!this.nodesDataSet || !this.network) return;

        if (!query || query.trim() === '') {
            // Reset all nodes
            this.nodesDataSet.forEach(node => {
                this.nodesDataSet.update({
                    id: node.id,
                    opacity: 1,
                    font: { ...node.font, color: 'var(--text-primary)' },
                });
            });
            this.network.unselectAll();
            return;
        }

        const queryLower = query.toLowerCase();
        const matchingIds = [];

        this.nodesDataSet.forEach(node => {
            const matches = node.label.toLowerCase().includes(queryLower) ||
                (node._data?.description || '').toLowerCase().includes(queryLower);

            if (matches) {
                matchingIds.push(node.id);
                this.nodesDataSet.update({
                    id: node.id,
                    opacity: 1,
                });
            } else {
                this.nodesDataSet.update({
                    id: node.id,
                    opacity: 0.2,
                });
            }
        });

        if (matchingIds.length > 0) {
            this.network.selectNodes(matchingIds);

            // Focus on first match
            this.network.focus(matchingIds[0], {
                scale: 1.2,
                animation: { duration: 500 },
            });
        }
    },

    resetView() {
        if (!this.network) return;

        // Reset node opacity
        this.nodesDataSet?.forEach(node => {
            this.nodesDataSet.update({
                id: node.id,
                opacity: 1,
            });
        });

        // Clear search
        const searchInput = document.getElementById('graphSearch');
        if (searchInput) searchInput.value = '';

        // Fit view
        this.network.fit({
            animation: {
                duration: 500,
                easingFunction: 'easeInOutQuad',
            },
        });

        this.network.unselectAll();
        this.hideDetailsPanel();

        // Re-enable physics briefly
        this.network.setOptions({ physics: true });
        setTimeout(() => {
            this.network.setOptions({ physics: false });
        }, 2000);
    },

    toggleFullscreen() {
        const graphPanel = document.getElementById('panel-graph');
        if (!graphPanel) return;

        this.isFullscreen = !this.isFullscreen;

        if (this.isFullscreen) {
            graphPanel.classList.add('fullscreen');
            document.body.style.overflow = 'hidden';
        } else {
            graphPanel.classList.remove('fullscreen');
            document.body.style.overflow = '';
        }

        // Resize network
        setTimeout(() => {
            this.network?.fit();
        }, 100);
    },

    updateStats(stats) {
        if (!stats) return;

        document.getElementById('entityCount').textContent = stats.total_nodes || 0;
        document.getElementById('relationCount').textContent = stats.total_edges || 0;

        // Get doc count from document manager
        if (window.DocumentManager) {
            document.getElementById('docCount').textContent = DocumentManager.documents.length;
        }
    },

    updateDocumentFilter() {
        const select = document.getElementById('graphDocFilter');
        if (!select) return;

        // Keep first option
        while (select.options.length > 1) {
            select.remove(1);
        }

        // Add documents
        if (window.DocumentManager) {
            const docs = DocumentManager.getDocumentsForSelect();
            docs.forEach(doc => {
                const option = document.createElement('option');
                option.value = doc.id;
                option.textContent = truncateText(doc.name, 25);
                select.appendChild(option);
            });
        }
    },

    getNodeColor(type) {
        const typeUpper = (type || '').toUpperCase();

        const colorMap = {
            PERSON: '#f472b6',
            ORGANIZATION: '#60a5fa',
            ORG: '#60a5fa',
            LOCATION: '#34d399',
            LOC: '#34d399',
            CONCEPT: '#fbbf24',
            TECHNOLOGY: '#a78bfa',
            TECH: '#a78bfa',
            EVENT: '#fb923c',
            DATE: '#94a3b8',
            TIME: '#94a3b8',
        };

        return colorMap[typeUpper] || '#94a3b8';
    },

    truncateLabel(label, maxLength = 20) {
        if (!label) return '';
        if (label.length <= maxLength) return label;
        return label.substring(0, maxLength - 1) + '…';
    },

    createTooltip(node) {
        return `
            <div style="max-width: 250px; font-family: var(--font-body);">
                <strong>${escapeHtml(node.label)}</strong>
                ${node.type ? `<br><em style="color: #888;">${node.type}</em>` : ''}
                ${node.description ? `<br><span style="font-size: 12px;">${truncateText(node.description, 100)}</span>` : ''}
            </div>
        `;
    }
};
