/**
 * Neural RAG - Query/Chat Interface
 * Question answering with streaming support
 */

const QueryManager = {
    messages: [],
    isStreaming: false,
    streamingEnabled: true,

    init() {
        // Load streaming preference
        const saved = localStorage.getItem(STORAGE_KEYS.streamingEnabled);
        this.streamingEnabled = saved !== 'false';

        this.bindEvents();
        this.updateDocumentScope();
    },

    bindEvents() {
        const input = document.getElementById('queryInput');
        const sendBtn = document.getElementById('sendQueryBtn');

        // Send button click
        sendBtn?.addEventListener('click', () => this.sendQuery());

        // Enter key (Ctrl+Enter to send)
        input?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                this.sendQuery();
            }
        });

        // Auto-resize textarea
        input?.addEventListener('input', () => {
            input.style.height = 'auto';
            input.style.height = Math.min(input.scrollHeight, 150) + 'px';
        });

        // Streaming toggle in settings
        const streamingToggle = document.getElementById('streamingToggle');
        if (streamingToggle) {
            streamingToggle.checked = this.streamingEnabled;
            streamingToggle.addEventListener('change', (e) => {
                this.streamingEnabled = e.target.checked;
                localStorage.setItem(STORAGE_KEYS.streamingEnabled, e.target.checked);
            });
        }
    },

    updateDocumentScope() {
        const select = document.getElementById('docScopeSelect');
        if (!select) return;

        // Keep first option (All Documents)
        while (select.options.length > 1) {
            select.remove(1);
        }

        // Add completed documents
        if (window.DocumentManager) {
            const docs = DocumentManager.getDocumentsForSelect();
            docs.forEach(doc => {
                const option = document.createElement('option');
                option.value = doc.id;
                option.textContent = truncateText(doc.name, 30);
                select.appendChild(option);
            });
        }
    },

    async sendQuery() {
        const input = document.getElementById('queryInput');
        const question = input?.value?.trim();

        if (!question || this.isStreaming) return;

        const mode = document.getElementById('modeSelect')?.value || 'mix';
        const docScope = document.getElementById('docScopeSelect')?.value;
        const docIds = docScope && docScope !== 'all' ? [docScope] : null;

        // Clear input
        input.value = '';
        input.style.height = 'auto';

        // Add user message
        this.addMessage('user', question);

        // Remove welcome message
        const welcome = document.querySelector('.welcome-message');
        if (welcome) welcome.remove();

        // Add assistant message placeholder
        const assistantMessage = this.addMessage('assistant', '', true);

        this.isStreaming = true;
        this.updateSendButton(true);

        try {
            if (this.streamingEnabled) {
                await this.executeStreamingQuery(question, mode, docIds, assistantMessage);
            } else {
                await this.executeNormalQuery(question, mode, docIds, assistantMessage);
            }
        } catch (error) {
            this.updateMessageContent(assistantMessage, `错误：${error.message}`);
            Toast.error(`查询失败：${error.message}`);
        } finally {
            this.isStreaming = false;
            this.updateSendButton(false);
            this.removeTypingIndicator(assistantMessage);
        }
    },

    async executeNormalQuery(question, mode, docIds, messageEl) {
        const startTime = Date.now();

        const result = await QueryApi.query(question, mode, docIds);

        const duration = (Date.now() - startTime) / 1000;

        this.updateMessageContent(messageEl, result.answer, {
            mode,
            duration,
            sources: result.sources
        });
    },

    async executeStreamingQuery(question, mode, docIds, messageEl) {
        const startTime = Date.now();
        let fullText = '';
        let sources = [];

        await QueryApi.queryStream(
            question,
            mode,
            docIds,
            // On chunk
            (chunk) => {
                if (chunk.text) {
                    fullText += chunk.text;
                    this.updateMessageContent(messageEl, fullText, null, true);
                }
                if (chunk.sources) {
                    sources = chunk.sources;
                }
            },
            // On done
            () => {
                const duration = (Date.now() - startTime) / 1000;
                this.updateMessageContent(messageEl, fullText, {
                    mode,
                    duration,
                    sources
                });
            },
            // On error
            (error) => {
                this.updateMessageContent(messageEl, `错误：${error.message}`);
            }
        );
    },

    addMessage(role, content, isStreaming = false) {
        const container = document.getElementById('chatMessages');
        if (!container) return null;

        const message = document.createElement('div');
        message.className = `message ${role}`;

        const avatar = role === 'user' ? '👤' : '🤖';

        message.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-text">
                    ${content ? this.formatContent(content) : ''}
                    ${isStreaming ? '<span class="streaming-cursor"></span>' : ''}
                </div>
                <div class="message-meta"></div>
            </div>
        `;

        if (isStreaming && !content) {
            const textEl = message.querySelector('.message-text');
            textEl.innerHTML = `
                <div class="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            `;
        }

        container.appendChild(message);
        this.scrollToBottom();

        this.messages.push({ role, content });

        return message;
    },

    updateMessageContent(messageEl, content, meta = null, isStreaming = false) {
        if (!messageEl) return;

        const textEl = messageEl.querySelector('.message-text');
        const metaEl = messageEl.querySelector('.message-meta');

        if (textEl) {
            textEl.innerHTML = this.formatContent(content);
            if (isStreaming) {
                textEl.innerHTML += '<span class="streaming-cursor"></span>';
            }
        }

        if (metaEl && meta) {
            let metaHtml = '';

            if (meta.mode) {
                metaHtml += `<span>模式：${QUERY_MODES[meta.mode]?.label || meta.mode}</span>`;
            }

            if (meta.duration) {
                metaHtml += `<span>${formatDuration(meta.duration)}</span>`;
            }

            metaEl.innerHTML = metaHtml;

            // Add sources if available
            if (meta.sources && meta.sources.length > 0) {
                const sourcesEl = document.createElement('div');
                sourcesEl.className = 'message-sources';
                sourcesEl.innerHTML = `
                    <div class="message-sources-title">来源：</div>
                    <ul>
                        ${meta.sources.map(s => `<li>${escapeHtml(s)}</li>`).join('')}
                    </ul>
                `;
                messageEl.querySelector('.message-content').appendChild(sourcesEl);
            }
        }

        this.scrollToBottom();
    },

    removeTypingIndicator(messageEl) {
        const cursor = messageEl?.querySelector('.streaming-cursor');
        const typing = messageEl?.querySelector('.typing-indicator');
        cursor?.remove();
        typing?.remove();
    },

    formatContent(content) {
        if (!content) return '';

        // Convert markdown to HTML
        let html = markdownToHtml(escapeHtml(content));

        // Wrap in paragraph if needed
        if (!html.startsWith('<p>')) {
            html = `<p>${html}</p>`;
        }

        return html;
    },

    scrollToBottom() {
        const container = document.getElementById('chatMessages');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    },

    updateSendButton(isLoading) {
        const btn = document.getElementById('sendQueryBtn');
        if (!btn) return;

        if (isLoading) {
            btn.disabled = true;
            btn.innerHTML = `<div class="loading-spinner spinner-sm"></div>`;
        } else {
            btn.disabled = false;
            btn.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"/>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
            `;
        }
    },

    clearConversation() {
        const container = document.getElementById('chatMessages');
        if (!container) return;

        container.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="12" r="10"/>
                        <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                        <line x1="12" y1="17" x2="12.01" y2="17"/>
                    </svg>
                </div>
                <h3>向文档知识库提问</h3>
                <p>系统会基于已上传文档抽取出的知识进行检索与回答。</p>
            </div>
        `;

        this.messages = [];
    }
};
