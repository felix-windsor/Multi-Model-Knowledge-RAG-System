/**
 * 文档上传功能
 */

// 当前正在轮询的文档
const pollingDocuments = new Set();

/**
 * 上传文件
 */
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        showError('请选择要上传的文件');
        return;
    }

    // 显示加载状态
    setUploadButtonLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(API_ENDPOINTS.upload, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '上传失败');
        }

        const result = await response.json();

        if (result.success) {
            showSuccess(`文件上传成功！文档 ID: ${result.doc_id}`);
            fileInput.value = '';

            // 刷新文档列表
            await refreshDocumentList();

            // 开始轮询文档状态
            startPollingDocumentStatus(result.doc_id);
        } else {
            throw new Error(result.message || '上传失败');
        }
    } catch (error) {
        console.error('上传失败:', error);
        showError(`上传失败: ${error.message}`);
    } finally {
        setUploadButtonLoading(false);
    }
}

/**
 * 刷新文档列表
 */
async function refreshDocumentList() {
    try {
        const response = await fetch(API_ENDPOINTS.documents);

        if (!response.ok) {
            throw new Error('获取文档列表失败');
        }

        const data = await response.json();
        renderDocumentList(data.documents);
    } catch (error) {
        console.error('获取文档列表失败:', error);
    }
}

/**
 * 渲染文档列表
 */
function renderDocumentList(documents) {
    const listElement = document.getElementById('documentList');

    if (!documents || documents.length === 0) {
        listElement.innerHTML = `
            <div class="text-center text-muted py-3">
                <small>暂无文档</small>
            </div>
        `;
        return;
    }

    listElement.innerHTML = documents.map(doc => {
        const statusColor = STATUS_COLORS[doc.status] || 'secondary';
        const statusLabel = STATUS_LABELS[doc.status] || doc.status;
        const createdAt = doc.created_at ? new Date(doc.created_at).toLocaleString('zh-CN') : '';

        return `
            <div class="list-group-item document-item" onclick="viewDocumentDetails('${doc.doc_id}')">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <div class="fw-bold text-truncate" style="max-width: 200px;" title="${doc.filename}">
                            ${doc.filename}
                        </div>
                        <small class="text-muted">${createdAt}</small>
                        ${doc.chunks_count > 0 ? `<small class="text-muted d-block">${doc.chunks_count} 个块</small>` : ''}
                    </div>
                    <span class="badge bg-${statusColor} status-badge">${statusLabel}</span>
                </div>
                ${doc.status === 'processing' ? `
                    <div class="progress mt-2" style="height: 4px;">
                        <div class="progress-bar progress-bar-striped progress-bar-animated"
                             role="progressbar"
                             style="width: 100%">
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
}

/**
 * 查看文档详情
 */
async function viewDocumentDetails(docId) {
    try {
        const response = await fetch(`${API_ENDPOINTS.documents}/${docId}`);

        if (!response.ok) {
            throw new Error('获取文档详情失败');
        }

        const doc = await response.json();

        const details = `
            <div class="mb-2"><strong>文档 ID:</strong> ${doc.doc_id}</div>
            <div class="mb-2"><strong>文件名:</strong> ${doc.filename}</div>
            <div class="mb-2"><strong>状态:</strong> <span class="badge bg-${STATUS_COLORS[doc.status]}">${STATUS_LABELS[doc.status]}</span></div>
            <div class="mb-2"><strong>进度:</strong> ${doc.progress}%</div>
            ${doc.step ? `<div class="mb-2"><strong>当前步骤:</strong> ${doc.step}</div>` : ''}
            <div class="mb-2"><strong>块数量:</strong> ${doc.chunks_count}</div>
            ${doc.created_at ? `<div class="mb-2"><strong>创建时间:</strong> ${new Date(doc.created_at).toLocaleString('zh-CN')}</div>` : ''}
            ${doc.updated_at ? `<div class="mb-2"><strong>更新时间:</strong> ${new Date(doc.updated_at).toLocaleString('zh-CN')}</div>` : ''}
            ${doc.error_message ? `<div class="alert alert-danger mt-2 mb-0"><strong>错误:</strong> ${doc.error_message}</div>` : ''}
        `;

        showModal('文档详情', details);
    } catch (error) {
        console.error('获取文档详情失败:', error);
        showError(`获取文档详情失败: ${error.message}`);
    }
}

/**
 * 开始轮询文档状态
 */
function startPollingDocumentStatus(docId) {
    if (pollingDocuments.has(docId)) {
        return;
    }

    pollingDocuments.add(docId);

    const pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_ENDPOINTS.documents}/${docId}`);

            if (!response.ok) {
                clearInterval(pollInterval);
                pollingDocuments.delete(docId);
                return;
            }

            const status = await response.json();

            // 如果状态已完成或失败，停止轮询
            if (status.status === 'completed' || status.status === 'failed') {
                clearInterval(pollInterval);
                pollingDocuments.delete(docId);

                // 刷新文档列表
                await refreshDocumentList();

                // 如果完成，自动刷新图谱
                if (status.status === 'completed') {
                    setTimeout(() => {
                        loadGraph();
                    }, GRAPH_REFRESH_DELAY);
                }
            }
        } catch (error) {
            console.error('轮询文档状态失败:', error);
            clearInterval(pollInterval);
            pollingDocuments.delete(docId);
        }
    }, POLL_INTERVAL);
}

/**
 * 设置上传按钮加载状态
 */
function setUploadButtonLoading(isLoading) {
    const btnText = document.getElementById('uploadBtnText');
    const spinner = document.getElementById('uploadSpinner');
    const btn = btnText.closest('button');

    if (isLoading) {
        btnText.textContent = '上传中...';
        spinner.classList.remove('d-none');
        btn.disabled = true;
    } else {
        btnText.textContent = '上传文档';
        spinner.classList.add('d-none');
        btn.disabled = false;
    }
}
