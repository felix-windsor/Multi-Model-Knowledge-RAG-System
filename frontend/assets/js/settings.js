/**
 * Neural RAG - Settings Management
 * System info, preferences, and data management
 */

const SettingsManager = {
    init() {
        this.bindEvents();
        this.loadSettings();
        this.loadSystemInfo();
    },

    bindEvents() {
        // Default query mode
        const defaultModeSelect = document.getElementById('defaultModeSelect');
        defaultModeSelect?.addEventListener('change', (e) => {
            localStorage.setItem(STORAGE_KEYS.defaultQueryMode, e.target.value);

            // Also update the query page dropdown
            const queryModeSelect = document.getElementById('modeSelect');
            if (queryModeSelect) {
                queryModeSelect.value = e.target.value;
            }
        });

        // Clear all documents
        document.getElementById('clearAllDocsBtn')?.addEventListener('click', () => {
            this.confirmClearAllDocuments();
        });

        // Reset graph
        document.getElementById('resetGraphBtn')?.addEventListener('click', () => {
            this.confirmResetGraph();
        });
    },

    loadSettings() {
        // Load default query mode
        const savedMode = localStorage.getItem(STORAGE_KEYS.defaultQueryMode);
        if (savedMode) {
            const defaultModeSelect = document.getElementById('defaultModeSelect');
            if (defaultModeSelect) {
                defaultModeSelect.value = savedMode;
            }

            // Apply to query page
            const queryModeSelect = document.getElementById('modeSelect');
            if (queryModeSelect) {
                queryModeSelect.value = savedMode;
            }
        }

        // Load streaming preference
        const streamingEnabled = localStorage.getItem(STORAGE_KEYS.streamingEnabled);
        const streamingToggle = document.getElementById('streamingToggle');
        if (streamingToggle) {
            streamingToggle.checked = streamingEnabled !== 'false';
        }
    },

    async loadSystemInfo() {
        // Check backend health
        await this.updateHealthStatus();

        // Load config
        await this.updateConfigInfo();

        // Start periodic health checks
        setInterval(() => this.updateHealthStatus(), 30000);
    },

    async updateHealthStatus() {
        try {
            const health = await HealthApi.detailed();

            // Backend status
            const backendStatus = document.getElementById('backendStatus');
            if (backendStatus) {
                if (health.status === 'healthy') {
                    backendStatus.textContent = '在线';
                    backendStatus.className = 'info-value status-badge status-success';
                } else {
                    backendStatus.textContent = '降级';
                    backendStatus.className = 'info-value status-badge status-warning';
                }
            }

            // Qdrant status
            const qdrantStatus = document.getElementById('qdrantStatus');
            if (qdrantStatus) {
                qdrantStatus.textContent = health.components?.qdrant ? '在线' : '离线';
                qdrantStatus.classList.toggle('online', health.components?.qdrant);
                qdrantStatus.classList.toggle('offline', !health.components?.qdrant);
            }

            // Neo4j status
            const neo4jStatus = document.getElementById('neo4jStatus');
            if (neo4jStatus) {
                neo4jStatus.textContent = health.components?.neo4j ? '在线' : '离线';
                neo4jStatus.classList.toggle('online', health.components?.neo4j);
                neo4jStatus.classList.toggle('offline', !health.components?.neo4j);
            }

            // Vector DB status (in settings)
            const vectorDbStatus = document.getElementById('vectorDbStatus');
            if (vectorDbStatus) {
                vectorDbStatus.textContent = health.components?.qdrant ? 'Qdrant 在线' : 'Qdrant 离线';
            }

            // Graph DB status (in settings)
            const graphDbStatus = document.getElementById('graphDbStatus');
            if (graphDbStatus) {
                graphDbStatus.textContent = health.components?.neo4j ? 'Neo4j 在线' : 'Neo4j 离线';
            }

            // Update connection indicator
            const connectionStatus = document.getElementById('connectionStatus');
            if (connectionStatus) {
                if (health.status === 'healthy') {
                    connectionStatus.classList.remove('disconnected');
                    connectionStatus.querySelector('span:last-child').textContent = '已连接';
                } else {
                    connectionStatus.classList.add('disconnected');
                    connectionStatus.querySelector('span:last-child').textContent = '未连接';
                }
            }

        } catch (error) {
            console.error('Health check failed:', error);

            const backendStatus = document.getElementById('backendStatus');
            if (backendStatus) {
                backendStatus.textContent = '离线';
                backendStatus.className = 'info-value status-badge status-error';
            }

            const connectionStatus = document.getElementById('connectionStatus');
            if (connectionStatus) {
                connectionStatus.classList.add('disconnected');
                connectionStatus.querySelector('span:last-child').textContent = '未连接';
            }
        }
    },

    async updateConfigInfo() {
        try {
            const config = await ConfigApi.get();

            if (config) {
                // LLM Provider
                const llmProvider = document.getElementById('llmProvider');
                if (llmProvider) {
                    llmProvider.textContent = config.llm_provider || '-';
                }

                // Embedding Model
                const embeddingModel = document.getElementById('embeddingModel');
                if (embeddingModel) {
                    const modelName = config.embedding_model || '-';
                    const dim = config.embedding_dim ? ` (${config.embedding_dim}d)` : '';
                    embeddingModel.textContent = modelName + dim;
                }
            }
        } catch (error) {
            console.error('Failed to load config:', error);
        }
    },

    confirmClearAllDocuments() {
        Modal.confirm(
            '清空全部文档',
            `
                <p>确定要删除<strong>全部文档</strong>吗？</p>
                <p style="color: var(--error); margin-top: var(--space-2);">
                    这会移除所有已上传文件及其处理结果。此操作不可撤销。
                </p>
            `,
            async () => {
                await this.clearAllDocuments();
            },
            { danger: true, confirmText: '全部删除' }
        );
    },

    async clearAllDocuments() {
        try {
            if (window.DocumentManager) {
                const docs = DocumentManager.documents;

                if (docs.length === 0) {
                    Toast.info('当前没有可删除的文档');
                    return;
                }

                const docIds = docs.map(d => d.doc_id);
                await DocumentApi.deleteMultiple(docIds);

                Toast.success(`已删除 ${docIds.length} 个文档`);

                // Refresh everything
                await DocumentManager.loadDocuments();
                await GraphManager.loadGraph();
            }
        } catch (error) {
            Toast.error(`清空文档失败：${error.message}`);
        }
    },

    confirmResetGraph() {
        Modal.confirm(
            '重置知识图谱',
            `
                <p>确定要重置<strong>知识图谱</strong>吗？</p>
                <p style="color: var(--warning); margin-top: var(--space-2);">
                    这会清空已抽取的实体和关系。文档会保留，但需要重新处理。
                </p>
            `,
            async () => {
                await this.resetGraph();
            },
            { danger: true, confirmText: '重置图谱' }
        );
    },

    async resetGraph() {
        // Note: This would need a backend endpoint to actually reset the graph
        // For now just show a message
        Toast.info('重置图谱需要后端接口支持，请联系管理员。');
    }
};
