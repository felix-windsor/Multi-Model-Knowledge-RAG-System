/**
 * Neural RAG - Theme Management
 * Dark/Light theme switching with system preference support
 */

const ThemeManager = {
    currentTheme: 'dark',

    init() {
        // Load saved theme or detect system preference
        const savedTheme = localStorage.getItem(STORAGE_KEYS.theme);

        if (savedTheme && savedTheme !== 'system') {
            this.setTheme(savedTheme, false);
        } else {
            this.detectSystemTheme();
            // Listen for system theme changes
            this.watchSystemTheme();
        }

        // Bind toggle button
        const toggleBtn = document.getElementById('themeToggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggle());
        }

        // Bind settings theme options
        this.bindSettingsOptions();
    },

    setTheme(theme, save = true) {
        if (theme === 'system') {
            this.detectSystemTheme();
            if (save) localStorage.setItem(STORAGE_KEYS.theme, 'system');
            return;
        }

        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);

        if (save) {
            localStorage.setItem(STORAGE_KEYS.theme, theme);
        }

        // Update settings UI
        this.updateSettingsUI(theme);
    },

    toggle() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    },

    detectSystemTheme() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        this.setTheme(prefersDark ? 'dark' : 'light', false);
    },

    watchSystemTheme() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

        mediaQuery.addEventListener('change', (e) => {
            const savedTheme = localStorage.getItem(STORAGE_KEYS.theme);
            if (savedTheme === 'system' || !savedTheme) {
                this.setTheme(e.matches ? 'dark' : 'light', false);
            }
        });
    },

    bindSettingsOptions() {
        const themeOptions = document.querySelectorAll('.theme-option');

        themeOptions.forEach(option => {
            option.addEventListener('click', () => {
                const theme = option.dataset.theme;
                this.setTheme(theme);
            });
        });

        // Set initial active state
        const savedTheme = localStorage.getItem(STORAGE_KEYS.theme) || 'dark';
        this.updateSettingsUI(savedTheme === 'system' ? 'system' : this.currentTheme);
    },

    updateSettingsUI(activeTheme) {
        const themeOptions = document.querySelectorAll('.theme-option');

        themeOptions.forEach(option => {
            if (option.dataset.theme === activeTheme) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });

        // Check if system theme should be active
        const savedTheme = localStorage.getItem(STORAGE_KEYS.theme);
        if (savedTheme === 'system') {
            const systemOption = document.querySelector('.theme-option[data-theme="system"]');
            if (systemOption) {
                document.querySelectorAll('.theme-option').forEach(o => o.classList.remove('active'));
                systemOption.classList.add('active');
            }
        }
    }
};
