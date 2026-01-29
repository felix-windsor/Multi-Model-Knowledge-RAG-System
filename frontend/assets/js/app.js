/**
 * Neural RAG - Main Application
 * Initialization and tab management
 */

// ============================================
// Tab Management
// ============================================

const TabManager = {
    currentTab: 'documents',

    init() {
        this.bindEvents();
        this.showTab(this.currentTab);
    },

    bindEvents() {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const tab = btn.dataset.tab;
                if (tab) this.showTab(tab);
            });
        });
    },

    showTab(tabId) {
        this.currentTab = tabId;

        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabId);
        });

        // Update panels
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.toggle('active', panel.id === `panel-${tabId}`);
        });

        // Tab-specific initialization
        if (tabId === 'graph' && window.GraphManager?.network) {
            // Trigger resize for graph
            setTimeout(() => {
                GraphManager.network.fit();
            }, 100);
        }

        if (tabId === 'query' && window.QueryManager) {
            // Update document scope dropdown
            QueryManager.updateDocumentScope();
        }
    }
};

// ============================================
// Application Initialization
// ============================================

const App = {
    async init() {
        console.log('Neural RAG initializing...');

        // Initialize utilities
        Toast.init();

        // Initialize theme
        ThemeManager.init();

        // Initialize tab navigation
        TabManager.init();

        // Initialize modules
        DocumentManager.init();
        QueryManager.init();
        GraphManager.init();
        SettingsManager.init();

        console.log('Neural RAG ready');
    }
};

// ============================================
// Start Application
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    App.init();
});

// ============================================
// Global Error Handler
// ============================================

window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
});
