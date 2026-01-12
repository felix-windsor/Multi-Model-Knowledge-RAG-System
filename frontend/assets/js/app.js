/**
 * 主应用脚本
 */

/**
 * 页面加载完成后初始化
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('知识图谱 RAG 系统已启动');

    // 加载初始数据
    initializeApp();

    // 检查系统状态
    checkSystemHealth();
});

/**
 * 初始化应用
 */
async function initializeApp() {
    try {
        // 加载文档列表
        await refreshDocumentList();

        // 加载知识图谱
        await loadGraph();

        console.log('应用初始化完成');
    } catch (error) {
        console.error('应用初始化失败:', error);
    }
}

/**
 * 检查系统健康状态
 */
async function checkSystemHealth() {
    try {
        const response = await fetch('/health');

        if (response.ok) {
            const data = await response.json();
            updateSystemStatus(data.status === 'healthy' ? 'success' : 'warning');
        } else {
            updateSystemStatus('danger');
        }
    } catch (error) {
        console.error('健康检查失败:', error);
        updateSystemStatus('danger');
    }
}

/**
 * 更新系统状态显示
 */
function updateSystemStatus(status) {
    const statusElement = document.getElementById('systemStatus');

    if (statusElement) {
        const badge = statusElement.querySelector('.badge');
        badge.className = `badge bg-${status}`;

        const statusText = {
            success: '运行中',
            warning: '警告',
            danger: '异常'
        };

        badge.textContent = statusText[status] || '未知';
    }
}

/**
 * 显示成功消息
 */
function showSuccess(message) {
    showToast(message, 'success');
}

/**
 * 显示错误消息
 */
function showError(message) {
    showToast(message, 'danger');
}

/**
 * 显示提示消息
 */
function showToast(message, type = 'info') {
    // 创建 toast 容器（如果不存在）
    let toastContainer = document.getElementById('toastContainer');

    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.className = 'position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    // 创建 toast
    const toastId = `toast-${Date.now()}`;
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);

    // 显示 toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 3000
    });

    bsToast.show();

    // 移除已隐藏的 toast
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

/**
 * 显示模态框
 */
function showModal(title, content) {
    const modal = document.getElementById('nodeModal');

    if (modal) {
        const modalTitle = document.getElementById('nodeModalTitle');
        const modalBody = document.getElementById('nodeModalBody');

        modalTitle.textContent = title;
        modalBody.innerHTML = content;

        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
}

/**
 * 格式化文件大小
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * 格式化时间
 */
function formatTime(seconds) {
    if (seconds < 60) {
        return `${seconds.toFixed(1)}秒`;
    }

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);

    return `${minutes}分${remainingSeconds}秒`;
}

/**
 * 复制到剪贴板
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showSuccess('已复制到剪贴板');
    } catch (error) {
        console.error('复制失败:', error);
        showError('复制失败');
    }
}
