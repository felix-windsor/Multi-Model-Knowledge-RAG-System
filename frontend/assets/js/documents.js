/**
 * Neural RAG - Document Management
 * Upload, list, delete, and status polling
 */

const DocumentManager = {
    documents: [],
    selectedIds: new Set(),
    pollingIntervals: new Map(),

    init() {
        this.bindEvents();
        this.loadDocuments();
    },

    bindEvents() {
        // File input and browse button
        const fileInput = document.getElementById('fileInput');
        const browseBtn = document.getElementById('browseBtn');
        const uploadZone = document.getElementById('uploadZone');

        browseBtn?.addEventListener('click', () => fileInput?.click());
        uploadZone?.addEventListener('click', (e) => {
            if (e.target === uploadZone || e.target.closest('.upload-icon') || e.target.closest('h3') || e.target.closest('p')) {
                fileInput?.click();
            }
        });

        fileInput?.addEventListener('change', (e) => {
            if (e.target.files?.length > 0) {
                this.handleFiles(Array.from(e.target.files));
                e.target.value = ''; // Reset for re-upload of same file
            }
        });

        // Drag and drop
        if (uploadZone) {
            uploadZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadZone.classList.add('drag-over');
            });

            uploadZone.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadZone.classList.remove('drag-over');
            });

            uploadZone.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadZone.classList.remove('drag-over');
                if (e.dataTransfer?.files?.length > 0) {
                    this.handleFiles(Array.from(e.dataTransfer.files));
                }
            });

            // Track mouse position for hover effect
            uploadZone.addEventListener('mousemove', (e) => {
                const rect = uploadZone.getBoundingClientRect();
                const x = ((e.clientX - rect.left) / rect.width) * 100;
                const y = ((e.clientY - rect.top) / rect.height) * 100;
                uploadZone.style.setProperty('--mouse-x', `${x}%`);
                uploadZone.style.setProperty('--mouse-y', `${y}%`);
            });
        }

        // Refresh button
        document.getElementById('refreshDocsBtn')?.addEventListener('click', () => {
            this.loadDocuments();
        });

        // Select all checkbox
        document.getElementById('selectAllDocs')?.addEventListener('change', (e) => {
            this.toggleSelectAll(e.target.checked);
        });

        // Delete selected button
        document.getElementById('deleteSelectedBtn')?.addEventListener('click', () => {
            this.deleteSelected();
        });
    },

    async handleFiles(files) {
        for (const file of files) {
            // Validate file
            const ext = '.' + file.name.split('.').pop().toLowerCase();
            if (!UPLOAD_CONFIG.allowedExtensions.includes(ext)) {
                Toast.error(`Invalid file type: ${file.name}`);
                continue;
            }

            if (file.size > UPLOAD_CONFIG.maxFileSize) {
                Toast.error(`File too large: ${file.name} (max ${formatFileSize(UPLOAD_CONFIG.maxFileSize)})`);
                continue;
            }

            await this.uploadFile(file);
        }
    },

    async uploadFile(file) {
        // Add temporary item to list
        const tempId = `temp-${Date.now()}`;
        this.addTempDocument(tempId, file.name);

        try {
            const result = await DocumentApi.upload(file, (progress) => {
                this.updateUploadProgress(tempId, progress);
            });

            // Remove temp and refresh list
            this.removeTempDocument(tempId);

            Toast.success(`Uploaded: ${file.name}`);

            // Refresh document list
            await this.loadDocuments();

            // Start polling for processing status
            const docId = result.doc_id || result.document_id;
            if (docId) {
                this.startPolling(docId);
            }

        } catch (error) {
            this.removeTempDocument(tempId);
            Toast.error(`Upload failed: ${error.message}`);
        }
    },

    addTempDocument(tempId, filename) {
        const list = document.getElementById('documentList');
        const emptyState = list?.querySelector('.empty-state');
        if (emptyState) emptyState.remove();

        const item = document.createElement('div');
        item.className = 'document-item processing';
        item.id = tempId;
        item.innerHTML = `
            <div class="doc-checkbox">
                <label class="checkbox-wrapper">
                    <input type="checkbox" disabled>
                    <span class="checkmark"></span>
                </label>
            </div>
            <div class="doc-info">
                <div class="doc-name">${escapeHtml(filename)}</div>
                <div class="doc-meta">
                    <span>Uploading...</span>
                </div>
                <div class="progress-bar" style="margin-top: 8px;">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
            </div>
        `;

        list?.prepend(item);
    },

    updateUploadProgress(tempId, progress) {
        const item = document.getElementById(tempId);
        const progressFill = item?.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.style.width = `${progress}%`;
        }
    },

    removeTempDocument(tempId) {
        document.getElementById(tempId)?.remove();
    },

    async loadDocuments() {
        try {
            this.documents = await DocumentApi.list();
            this.render();
            this.updateStatusBar();

            // Resume polling for processing documents
            this.documents.forEach(doc => {
                if (doc.status === 'processing' || doc.status === 'pending') {
                    this.startPolling(doc.doc_id);
                }
            });
        } catch (error) {
            console.error('Failed to load documents:', error);
            Toast.error('Failed to load documents');
        }
    },

    render() {
        const list = document.getElementById('documentList');
        if (!list) return;

        if (!this.documents || this.documents.length === 0) {
            list.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                            <polyline points="13 2 13 9 20 9"/>
                        </svg>
                    </div>
                    <p>No documents yet</p>
                    <span>Upload your first document to get started</span>
                </div>
            `;
            return;
        }

        list.innerHTML = this.documents.map(doc => this.renderDocumentItem(doc)).join('');

        // Bind events to new items
        list.querySelectorAll('.document-item').forEach(item => {
            const docId = item.dataset.docId;

            // Checkbox
            const checkbox = item.querySelector('input[type="checkbox"]');
            checkbox?.addEventListener('change', (e) => {
                e.stopPropagation();
                this.toggleSelection(docId, e.target.checked);
            });

            // Click to view details
            item.addEventListener('click', (e) => {
                if (!e.target.closest('.doc-checkbox') && !e.target.closest('.doc-actions')) {
                    this.showDetails(docId);
                }
            });

            // Delete button
            const deleteBtn = item.querySelector('.btn-delete');
            deleteBtn?.addEventListener('click', (e) => {
                e.stopPropagation();
                this.confirmDelete([docId]);
            });

            // Retry button
            const retryBtn = item.querySelector('.btn-retry');
            retryBtn?.addEventListener('click', (e) => {
                e.stopPropagation();
                // For now just show a message - would need to re-upload
                Toast.info('Please re-upload the document to retry');
            });
        });

        // Update selection state
        this.updateSelectionUI();
    },

    renderDocumentItem(doc) {
        const status = STATUS_CONFIG[doc.status] || STATUS_CONFIG.pending;
        const isSelected = this.selectedIds.has(doc.doc_id);
        const isProcessing = doc.status === 'processing' || doc.status === 'pending';

        return `
            <div class="document-item ${isSelected ? 'selected' : ''} ${isProcessing ? 'processing' : ''}"
                 data-doc-id="${doc.doc_id}">
                <div class="doc-checkbox">
                    <label class="checkbox-wrapper" onclick="event.stopPropagation()">
                        <input type="checkbox" ${isSelected ? 'checked' : ''}>
                        <span class="checkmark"></span>
                    </label>
                </div>
                <div class="doc-info">
                    <div class="doc-name" title="${escapeHtml(doc.filename)}">${escapeHtml(doc.filename)}</div>
                    <div class="doc-meta">
                        <span>${formatDate(doc.created_at)}</span>
                        ${doc.chunks_count ? `<span>${doc.chunks_count} chunks</span>` : ''}
                    </div>
                </div>
                <div class="doc-status">
                    <span class="status-badge ${status.class}">${status.label}</span>
                </div>
                <div class="doc-actions">
                    ${doc.status === 'failed' ? `
                        <button class="btn btn-icon btn-retry" title="Retry">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="23 4 23 10 17 10"/>
                                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
                            </svg>
                        </button>
                    ` : ''}
                    <button class="btn btn-icon btn-delete" title="Delete">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"/>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                        </svg>
                    </button>
                </div>
            </div>
        `;
    },

    toggleSelection(docId, selected) {
        if (selected) {
            this.selectedIds.add(docId);
        } else {
            this.selectedIds.delete(docId);
        }
        this.updateSelectionUI();
    },

    toggleSelectAll(selected) {
        if (selected) {
            this.documents.forEach(doc => this.selectedIds.add(doc.doc_id));
        } else {
            this.selectedIds.clear();
        }
        this.render();
    },

    updateSelectionUI() {
        const deleteBtn = document.getElementById('deleteSelectedBtn');
        const selectAllCheckbox = document.getElementById('selectAllDocs');
        const count = this.selectedIds.size;

        if (deleteBtn) {
            deleteBtn.disabled = count === 0;
            const countSpan = deleteBtn.querySelector('.delete-count');
            if (countSpan) {
                countSpan.textContent = count > 0 ? `(${count})` : '';
            }
        }

        if (selectAllCheckbox) {
            selectAllCheckbox.checked = count > 0 && count === this.documents.length;
            selectAllCheckbox.indeterminate = count > 0 && count < this.documents.length;
        }
    },

    async showDetails(docId) {
        try {
            const doc = await DocumentApi.get(docId);
            const status = STATUS_CONFIG[doc.status] || STATUS_CONFIG.pending;

            const content = `
                <div class="doc-details">
                    <div class="detail-row">
                        <span class="detail-label">File Name</span>
                        <span class="detail-value">${escapeHtml(doc.filename)}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Status</span>
                        <span class="detail-value">
                            <span class="status-badge ${status.class}">${status.label}</span>
                        </span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Progress</span>
                        <span class="detail-value">${doc.progress || 0}%</span>
                    </div>
                    ${doc.step ? `
                        <div class="detail-row">
                            <span class="detail-label">Current Step</span>
                            <span class="detail-value">${doc.step}</span>
                        </div>
                    ` : ''}
                    <div class="detail-row">
                        <span class="detail-label">Chunks</span>
                        <span class="detail-value">${doc.chunks_count || 0}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Created</span>
                        <span class="detail-value">${doc.created_at ? new Date(doc.created_at).toLocaleString() : '-'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Updated</span>
                        <span class="detail-value">${doc.updated_at ? new Date(doc.updated_at).toLocaleString() : '-'}</span>
                    </div>
                    ${doc.error_message ? `
                        <div class="detail-error">
                            <strong>Error:</strong> ${escapeHtml(doc.error_message)}
                        </div>
                    ` : ''}
                </div>
                <style>
                    .doc-details { display: flex; flex-direction: column; gap: var(--space-3); }
                    .detail-row { display: flex; justify-content: space-between; padding: var(--space-2) 0; border-bottom: 1px solid var(--surface-border); }
                    .detail-label { color: var(--text-tertiary); }
                    .detail-value { color: var(--text-primary); font-family: var(--font-mono); font-size: var(--text-sm); }
                    .detail-error { margin-top: var(--space-4); padding: var(--space-3); background: var(--error-muted); border-radius: var(--radius-md); color: var(--error); font-size: var(--text-sm); }
                </style>
            `;

            Modal.showDocument('Document Details', content);
        } catch (error) {
            Toast.error(`Failed to load details: ${error.message}`);
        }
    },

    confirmDelete(docIds) {
        const count = docIds.length;
        const message = count === 1
            ? 'Are you sure you want to delete this document? This action cannot be undone.'
            : `Are you sure you want to delete ${count} documents? This action cannot be undone.`;

        Modal.confirm(
            'Delete Document' + (count > 1 ? 's' : ''),
            message,
            () => this.performDelete(docIds),
            { danger: true, confirmText: 'Delete' }
        );
    },

    async performDelete(docIds) {
        try {
            await DocumentApi.deleteMultiple(docIds);

            // Stop polling for deleted docs
            docIds.forEach(id => this.stopPolling(id));

            // Clear from selection
            docIds.forEach(id => this.selectedIds.delete(id));

            Toast.success(`Deleted ${docIds.length} document(s)`);

            // Refresh list
            await this.loadDocuments();

            // Refresh graph
            if (window.GraphManager) {
                GraphManager.loadGraph();
            }
        } catch (error) {
            Toast.error(error.message);
        }
    },

    deleteSelected() {
        if (this.selectedIds.size === 0) return;
        this.confirmDelete(Array.from(this.selectedIds));
    },

    startPolling(docId) {
        if (this.pollingIntervals.has(docId)) return;

        let attempts = 0;

        const poll = async () => {
            if (attempts >= POLL_CONFIG.maxAttempts) {
                this.stopPolling(docId);
                return;
            }

            attempts++;

            try {
                const doc = await DocumentApi.get(docId);

                if (doc.status === 'completed' || doc.status === 'failed') {
                    this.stopPolling(docId);
                    await this.loadDocuments();

                    if (doc.status === 'completed') {
                        Toast.success(`Document processed: ${doc.filename}`);

                        // Refresh graph after delay
                        setTimeout(() => {
                            if (window.GraphManager) {
                                GraphManager.loadGraph();
                            }
                        }, POLL_CONFIG.graphRefreshDelay);
                    } else {
                        Toast.error(`Processing failed: ${doc.filename}`);
                    }
                }
            } catch (error) {
                console.error('Polling error:', error);
            }
        };

        const intervalId = setInterval(poll, POLL_CONFIG.interval);
        this.pollingIntervals.set(docId, intervalId);

        // Initial poll
        poll();
    },

    stopPolling(docId) {
        const intervalId = this.pollingIntervals.get(docId);
        if (intervalId) {
            clearInterval(intervalId);
            this.pollingIntervals.delete(docId);
        }
    },

    updateStatusBar() {
        const totalDocs = document.getElementById('totalDocsCount');
        if (totalDocs) {
            totalDocs.textContent = this.documents.length;
        }
    },

    // Get documents for query scope dropdown
    getDocumentsForSelect() {
        return this.documents
            .filter(doc => doc.status === 'completed')
            .map(doc => ({
                id: doc.doc_id,
                name: doc.filename
            }));
    }
};
