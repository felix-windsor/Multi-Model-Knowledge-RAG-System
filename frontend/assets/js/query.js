/**
 * 知识查询功能
 */

// V2.0: 支持流式响应
const USE_STREAMING = true; // 可以改为从配置读取

/**
 * 执行查询
 */
async function executeQuery() {
    if (USE_STREAMING) {
        return executeQueryStreaming();
    }
    return executeQueryLegacy();
}

/**
 * 执行查询（流式响应） - V2.0
 */
async function executeQueryStreaming() {
    const questionInput = document.getElementById('queryInput');
    const modeSelect = document.getElementById('modeSelect');
    const question = questionInput.value.trim();
    const mode = modeSelect.value;

    if (!question) {
        showError('请输入问题');
        return;
    }

    // 显示加载状态
    setQueryButtonLoading(true);
    const resultDiv = document.getElementById('queryResult');
    resultDiv.innerHTML = `
        <div class="query-answer streaming">
            <h6>回答:</h6>
            <div class="answer-content" id="streamingAnswer"></div>
            <div class="query-meta" id="streamingMeta">
                <span>查询模式: ${QUERY_MODES[mode]}</span>
                <span class="ms-3">正在生成...</span>
            </div>
        </div>
    `;

    const answerDiv = document.getElementById('streamingAnswer');
    let accumulatedAnswer = '';
    let startTime = Date.now();

    try {
        const response = await fetch(API_ENDPOINTS.queryStream, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                mode: mode
            })
        });

        if (!response.ok) {
            throw new Error('流式查询失败');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));

                    if (data.type === 'chunk') {
                        accumulatedAnswer += data.content;
                        answerDiv.innerHTML = formatAnswer(accumulatedAnswer);
                        // 自动滚动到底部
                        answerDiv.scrollTop = answerDiv.scrollHeight;
                    } else if (data.type === 'done') {
                        const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
                        document.getElementById('streamingMeta').innerHTML = `
                            <span>查询模式: ${QUERY_MODES[mode]}</span>
                            <span class="ms-3">耗时: ${data.query_time.toFixed(2)}秒</span>
                        `;
                    } else if (data.type === 'error') {
                        throw new Error(data.message);
                    }
                }
            }
        }
    } catch (error) {
        console.error('流式查询失败:', error);
        resultDiv.innerHTML = `
            <div class="error-message">
                <strong>查询失败</strong>
                <div>${error.message}</div>
            </div>
        `;
    } finally {
        setQueryButtonLoading(false);
    }
}

/**
 * 执行查询（传统方式）
 */
async function executeQueryLegacy() {
    const questionInput = document.getElementById('queryInput');
    const modeSelect = document.getElementById('modeSelect');
    const question = questionInput.value.trim();
    const mode = modeSelect.value;

    if (!question) {
        showError('请输入问题');
        return;
    }

    // 显示加载状态
    setQueryButtonLoading(true);
    const resultDiv = document.getElementById('queryResult');
    resultDiv.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">查询中...</span>
            </div>
            <div class="mt-2 text-muted">正在查询知识库...</div>
        </div>
    `;

    try {
        const response = await fetch(API_ENDPOINTS.query, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                mode: mode
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '查询失败');
        }

        const result = await response.json();
        renderQueryResult(result);
    } catch (error) {
        console.error('查询失败:', error);
        resultDiv.innerHTML = `
            <div class="error-message">
                <strong>查询失败</strong>
                <div>${error.message}</div>
            </div>
        `;
    } finally {
        setQueryButtonLoading(false);
    }
}

/**
 * 渲染查询结果
 */
function renderQueryResult(result) {
    const resultDiv = document.getElementById('queryResult');

    const sourcesHtml = result.sources && result.sources.length > 0
        ? `
            <div class="mt-3">
                <strong>来源:</strong>
                <ul class="list-unstyled mt-2">
                    ${result.sources.map(source => `
                        <li class="text-muted small">• ${source}</li>
                    `).join('')}
                </ul>
            </div>
        `
        : '';

    resultDiv.innerHTML = `
        <div class="query-answer">
            <h6>回答:</h6>
            <div class="answer-content">${formatAnswer(result.answer)}</div>
            ${sourcesHtml}
            <div class="query-meta">
                <span>查询模式: ${QUERY_MODES[document.getElementById('modeSelect').value]}</span>
                <span class="ms-3">耗时: ${result.query_time.toFixed(2)}秒</span>
            </div>
        </div>
    `;
}

/**
 * 格式化答案文本
 */
function formatAnswer(answer) {
    // 简单的 Markdown 格式化
    let formatted = answer
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // 粗体
        .replace(/\*(.*?)\*/g, '<em>$1</em>')              // 斜体
        .replace(/\n\n/g, '</p><p>')                        // 段落
        .replace(/\n/g, '<br>');                            // 换行

    return `<p>${formatted}</p>`;
}

/**
 * 设置查询按钮加载状态
 */
function setQueryButtonLoading(isLoading) {
    const btnText = document.getElementById('queryBtnText');
    const spinner = document.getElementById('querySpinner');
    const btn = btnText.closest('button');

    if (isLoading) {
        btnText.textContent = '查询中...';
        spinner.classList.remove('d-none');
        btn.disabled = true;
    } else {
        btnText.textContent = '查询';
        spinner.classList.add('d-none');
        btn.disabled = false;
    }
}

/**
 * 处理回车键提交查询
 */
document.addEventListener('DOMContentLoaded', function() {
    const queryInput = document.getElementById('queryInput');
    if (queryInput) {
        queryInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                executeQuery();
            }
        });
    }
});
