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
                    backendStatus.textContent = 'Online';
                    backendStatus.className = 'info-value status-badge status-success';
                } else {
                    backendStatus.textContent = 'Degraded';
                    backendStatus.className = 'info-value status-badge status-warning';
                }
            }

            // Qdrant status
            const qdrantStatus = document.getElementById('qdrantStatus');
            if (qdrantStatus) {
                qdrantStatus.textContent = health.components?.qdrant ? 'Online' : 'Offline';
                qdrantStatus.classList.toggle('online', health.components?.qdrant);
                qdrantStatus.classList.toggle('offline', !health.components?.qdrant);
            }

            // Neo4j status
            const neo4jStatus = document.getElementById('neo4jStatus');
            if (neo4jStatus) {
                neo4jStatus.textContent = health.components?.neo4j ? 'Online' : 'Offline';
                neo4jStatus.classList.toggle('online', health.components?.neo4j);
                neo4jStatus.classList.toggle('offline', !health.components?.neo4j);
            }

            // Vector DB status (in settings)
            const vectorDbStatus = document.getElementById('vectorDbStatus');
            if (vectorDbStatus) {
                vectorDbStatus.textContent = health.components?.qdrant ? 'Qdrant Online' : 'Qdrant Offline';
            }

            // Graph DB status (in settings)
            const graphDbStatus = document.getElementById('graphDbStatus');
            if (graphDbStatus) {
                graphDbStatus.textContent = health.components?.neo4j ? 'Neo4j Online' : 'Neo4j Offline';
            }

            // Update connection indicator
            const connectionStatus = document.getElementById('connectionStatus');
            if (connectionStatus) {
                if (health.status === 'healthy') {
                    connectionStatus.classList.remove('disconnected');
                    connectionStatus.querySelector('span:last-child').textContent = 'Connected';
                } else {
                    connectionStatus.classList.add('disconnected');
                    connectionStatus.querySelector('span:last-child').textContent = 'Disconnected';
                }
            }

        } catch (error) {
            console.error('Health check failed:', error);

            const backendStatus = document.getElementById('backendStatus');
            if (backendStatus) {
                backendStatus.textContent = 'Offline';
                backendStatus.className = 'info-value status-badge status-error';
            }

            const connectionStatus = document.getElementById('connectionStatus');
            if (connectionStatus) {
                connectionStatus.classList.add('disconnected');
                connectionStatus.querySelector('span:last-child').textContent = 'Disconnected';
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
            'Clear All Documents',
            `
                <p>Are you sure you want to delete <strong>all documents</strong>?</p>
                <p style="color: var(--error); margin-top: var(--space-2);">
                    This will remove all uploaded files and their processed data.
                    This action cannot be undone.
                </p>
            `,
            async () => {
                await this.clearAllDocuments();
            },
            { danger: true, confirmText: 'Delete All' }
        );
    },

    async clearAllDocuments() {
        try {
            if (window.DocumentManager) {
                const docs = DocumentManager.documents;

                if (docs.length === 0) {
                    Toast.info('No documents to delete');
                    return;
                }

                const docIds = docs.map(d => d.doc_id);
                await DocumentApi.deleteMultiple(docIds);

                Toast.success(`Deleted ${docIds.length} documents`);

                // Refresh everything
                await DocumentManager.loadDocuments();
                await GraphManager.loadGraph();
            }
        } catch (error) {
            Toast.error(`Failed to clear documents: ${error.message}`);
        }
    },

    confirmResetGraph() {
        Modal.confirm(
            'Reset Knowledge Graph',
            `
                <p>Are you sure you want to reset the <strong>knowledge graph</strong>?</p>
                <p style="color: var(--warning); margin-top: var(--space-2);">
                    This will clear all extracted entities and relationships.
                    Documents will remain but will need to be reprocessed.
                </p>
            `,
            async () => {
                await this.resetGraph();
            },
            { danger: true, confirmText: 'Reset Graph' }
        );
    },

    async resetGraph() {
        // Note: This would need a backend endpoint to actually reset the graph
        // For now just show a message
        Toast.info('Graph reset requires backend support. Please contact administrator.');
    }
};
