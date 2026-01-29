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
    mix: { label: 'Mix (Recommended)', description: 'Combines local and global search' },
    local: { label: 'Local', description: 'Focus on specific entities' },
    global: { label: 'Global', description: 'Broader context search' },
    hybrid: { label: 'Hybrid', description: 'Vector + graph search' },
    naive: { label: 'Naive', description: 'Simple vector search' },
};

const STATUS_CONFIG = {
    pending: {
        label: 'Pending',
        class: 'status-warning',
        color: 'var(--warning)',
    },
    processing: {
        label: 'Processing',
        class: 'status-processing',
        color: 'var(--info)',
    },
    completed: {
        label: 'Completed',
        class: 'status-success',
        color: 'var(--success)',
    },
    failed: {
        label: 'Failed',
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
