/**
 * 配置文件
 */

const API_BASE_URL = window.location.origin + '/api';

const API_ENDPOINTS = {
    upload: `${API_BASE_URL}/upload`,
    documents: `${API_BASE_URL}/documents`,
    query: `${API_BASE_URL}/query`,
    queryStream: `${API_BASE_URL}/query/stream`,  // V2.0: SSE streaming endpoint
    graph: `${API_BASE_URL}/graph`,
};

const QUERY_MODES = {
    mix: '混合模式',
    local: '本地模式',
    global: '全局模式',
    hybrid: '混合检索',
    naive: '简单检索',
};

const STATUS_LABELS = {
    processing: '处理中',
    completed: '已完成',
    failed: '失败',
};

const STATUS_COLORS = {
    processing: 'warning',
    completed: 'success',
    failed: 'danger',
};

// 轮询间隔（毫秒）
const POLL_INTERVAL = 2000;

// 自动刷新图谱延迟（毫秒）
const GRAPH_REFRESH_DELAY = 3000;
