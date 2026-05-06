/**
 * Neural RAG - Configuration
 * API endpoints, constants, and settings
 */

const API_BASE_URL = window.location.origin;

const API_ENDPOINTS = {
    // V1 API (preferred)
    v1: {
        upload: `${API_BASE_URL}/api/v1/documents/upload`,
        documents: `${API_BASE_URL}/api/v1/documents`,
        query: `${API_BASE_URL}/api/v1/query`,
        queryStream: `${API_BASE_URL}/api/v1/query/stream`,
        graph: `${API_BASE_URL}/api/v1/graph`,
        graphStats: `${API_BASE_URL}/api/v1/graph/stats`,
        graphSubgraph: `${API_BASE_URL}/api/v1/graph/subgraph`,
        health: `${API_BASE_URL}/api/v1/health`,
        healthDetailed: `${API_BASE_URL}/api/v1/health/detailed`,
        config: `${API_BASE_URL}/api/v1/config`,
    },
    // Legacy API (fallback)
    legacy: {
        upload: `${API_BASE_URL}/api/upload`,
        documents: `${API_BASE_URL}/api/documents`,
        query: `${API_BASE_URL}/api/query`,
        graph: `${API_BASE_URL}/api/graph`,
    }
};

// Use V1 API by default
const API = API_ENDPOINTS.v1;

const QUERY_MODES = {
    mix: { label: '混合模式（推荐）', description: '结合局部实体和全局关系检索' },
    local: { label: '局部检索', description: '聚焦特定实体及其上下文' },
    global: { label: '全局检索', description: '面向更广范围的关系检索' },
    hybrid: { label: '向量+图谱', description: '结合向量检索与图谱检索' },
    naive: { label: '基础向量检索', description: '仅使用基础向量检索' },
};

const STATUS_CONFIG = {
    pending: {
        label: '等待中',
        class: 'status-warning',
        color: 'var(--warning)',
    },
    processing: {
        label: '处理中',
        class: 'status-processing',
        color: 'var(--info)',
    },
    completed: {
        label: '已完成',
        class: 'status-success',
        color: 'var(--success)',
    },
    failed: {
        label: '失败',
        class: 'status-error',
        color: 'var(--error)',
    },
};

const GRAPH_NODE_COLORS = {
    PERSON: 'var(--graph-node-person)',
    ORGANIZATION: 'var(--graph-node-org)',
    LOCATION: 'var(--graph-node-location)',
    CONCEPT: 'var(--graph-node-concept)',
    TECHNOLOGY: 'var(--graph-node-tech)',
    DEFAULT: 'var(--graph-node-default)',
};

// Polling configuration
const POLL_CONFIG = {
    interval: 2000,           // Status check interval (ms)
    maxAttempts: 300,         // Max polling attempts (10 min)
    graphRefreshDelay: 3000,  // Delay before refreshing graph after doc complete
};

// Local storage keys
const STORAGE_KEYS = {
    theme: 'neural-rag-theme',
    defaultQueryMode: 'neural-rag-default-mode',
    streamingEnabled: 'neural-rag-streaming',
};

// File upload config
const UPLOAD_CONFIG = {
    maxFileSize: 100 * 1024 * 1024, // 100MB
    allowedExtensions: [
        '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',
        '.txt', '.md', '.jpg', '.jpeg', '.png', '.bmp'
    ],
};
