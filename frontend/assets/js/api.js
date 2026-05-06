/**
 * Neural RAG - API Client
 * HTTP requests and error handling
 */

const ApiClient = {
    // Optional API key (set via settings or environment)
    apiKey: null,

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (this.apiKey) {
            headers['X-API-Key'] = this.apiKey;
        }

        return headers;
    },

    async request(url, options = {}) {
        const defaultOptions = {
            headers: this.getHeaders(),
        };

        // Merge headers
        if (options.headers) {
            options.headers = { ...defaultOptions.headers, ...options.headers };
        }

        const response = await fetch(url, { ...defaultOptions, ...options });

        if (!response.ok) {
            let errorMessage = `HTTP ${response.status}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.message || errorData.detail || errorMessage;
            } catch {
                // Ignore JSON parse errors
            }
            throw new Error(errorMessage);
        }

        return response;
    },

    async get(url) {
        const response = await this.request(url);
        return response.json();
    },

    async post(url, data) {
        const response = await this.request(url, {
            method: 'POST',
            body: JSON.stringify(data),
        });
        return response.json();
    },

    async delete(url) {
        const response = await this.request(url, {
            method: 'DELETE',
        });
        return response.json();
    },

    async uploadFile(url, file, onProgress) {
        const formData = new FormData();
        formData.append('file', file);

        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();

            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable && onProgress) {
                    const percent = Math.round((e.loaded / e.total) * 100);
                    onProgress(percent);
                }
            });

            xhr.addEventListener('load', () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        resolve(JSON.parse(xhr.responseText));
                    } catch {
                        resolve(xhr.responseText);
                    }
                } else {
                    let errorMessage = `上传失败：${xhr.status}`;
                    try {
                        const errorData = JSON.parse(xhr.responseText);
                        errorMessage = errorData.message || errorData.detail || errorMessage;
                    } catch {
                        // Ignore
                    }
                    reject(new Error(errorMessage));
                }
            });

            xhr.addEventListener('error', () => {
                reject(new Error('上传失败：网络错误'));
            });

            xhr.open('POST', url);

            if (this.apiKey) {
                xhr.setRequestHeader('X-API-Key', this.apiKey);
            }

            xhr.send(formData);
        });
    },

    // Stream response handling for SSE
    async streamPost(url, data, onChunk, onDone, onError) {
        try {
            const response = await this.request(url, {
                method: 'POST',
                body: JSON.stringify(data),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();

                if (done) {
                    if (onDone) onDone();
                    break;
                }

                buffer += decoder.decode(value, { stream: true });

                // Process SSE events
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') {
                            if (onDone) onDone();
                            return;
                        }
                        try {
                            const parsed = JSON.parse(data);
                            if (onChunk) onChunk(parsed);
                        } catch {
                            // Plain text chunk
                            if (onChunk) onChunk({ text: data });
                        }
                    }
                }
            }
        } catch (error) {
            if (onError) onError(error);
            throw error;
        }
    }
};

// ============================================
// API Methods
// ============================================

const DocumentApi = {
    async list() {
        try {
            const response = await ApiClient.get(API.documents);
            // Handle V1 API response format
            if (response.data && response.data.documents) {
                return response.data.documents;
            }
            // Legacy format
            return response.documents || [];
        } catch (error) {
            // Try legacy API as fallback
            try {
                const response = await ApiClient.get(API_ENDPOINTS.legacy.documents);
                return response.documents || [];
            } catch {
                throw error;
            }
        }
    },

    async get(docId) {
        try {
            const response = await ApiClient.get(`${API.documents}/${docId}`);
            return response.data || response;
        } catch (error) {
            // Try legacy API
            try {
                return await ApiClient.get(`${API_ENDPOINTS.legacy.documents}/${docId}`);
            } catch {
                throw error;
            }
        }
    },

    async upload(file, onProgress) {
        try {
            const response = await ApiClient.uploadFile(API.upload, file, onProgress);
            return response.data || response;
        } catch (error) {
            // Try legacy API
            try {
                return await ApiClient.uploadFile(API_ENDPOINTS.legacy.upload, file, onProgress);
            } catch {
                throw error;
            }
        }
    },

    async delete(docId) {
        return await ApiClient.delete(`${API.documents}/${docId}`);
    },

    async deleteMultiple(docIds) {
        const results = await Promise.allSettled(
            docIds.map(id => this.delete(id))
        );

        const failed = results.filter(r => r.status === 'rejected');
        if (failed.length > 0) {
            throw new Error(`有 ${failed.length} 个文档删除失败`);
        }

        return true;
    }
};

const QueryApi = {
    async query(question, mode = 'mix', docIds = null) {
        const payload = {
            question,
            mode,
        };

        if (docIds && docIds.length > 0) {
            payload.doc_ids = docIds;
        }

        try {
            const response = await ApiClient.post(API.query, payload);
            return response.data || response;
        } catch (error) {
            // Try legacy API
            try {
                return await ApiClient.post(API_ENDPOINTS.legacy.query, payload);
            } catch {
                throw error;
            }
        }
    },

    async queryStream(question, mode, docIds, onChunk, onDone, onError) {
        const payload = {
            question,
            mode,
        };

        if (docIds && docIds.length > 0) {
            payload.doc_ids = docIds;
        }

        return ApiClient.streamPost(API.queryStream, payload, onChunk, onDone, onError);
    }
};

const GraphApi = {
    async get(docId = null, limit = 1000) {
        let url = `${API.graph}?limit=${limit}`;
        if (docId) {
            url += `&doc_id=${docId}`;
        }

        try {
            const response = await ApiClient.get(url);
            return response.data || response;
        } catch (error) {
            // Try legacy API
            try {
                let legacyUrl = `${API_ENDPOINTS.legacy.graph}?limit=${limit}`;
                if (docId) legacyUrl += `&doc_id=${docId}`;
                return await ApiClient.get(legacyUrl);
            } catch {
                throw error;
            }
        }
    },

    async getStats() {
        try {
            const response = await ApiClient.get(API.graphStats);
            return response.data || response;
        } catch {
            return { total_nodes: 0, total_edges: 0 };
        }
    }
};

const HealthApi = {
    async check() {
        try {
            const response = await ApiClient.get(API.health);
            return response.data || response;
        } catch {
            return { status: 'unhealthy' };
        }
    },

    async detailed() {
        try {
            const response = await ApiClient.get(API.healthDetailed);
            return response.data || response;
        } catch {
            return {
                status: 'unhealthy',
                components: { qdrant: false, neo4j: false }
            };
        }
    }
};

const ConfigApi = {
    async get() {
        try {
            const response = await ApiClient.get(API.config);
            return response.data || response;
        } catch {
            return null;
        }
    }
};
