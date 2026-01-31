
/**
 * Theme Management System
 * Handles dark/light mode toggling and persistence
 */

class ThemeManager {
    constructor() {
        this.themeToggle = document.querySelector('.theme-toggle');
        this.themeIcon = this.themeToggle?.querySelector('i');
        this.currentTheme = this.getPreferredTheme();
        
        this.init();
    }
    
    init() {
        this.setTheme(this.currentTheme);
        this.bindEvents();
        this.addSystemThemeListener();
    }
    
    getPreferredTheme() {
        // Check localStorage first
        const storedTheme = localStorage.getItem('theme');
        if (storedTheme) {
            return storedTheme;
        }
        
        // Check system preference
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        
        // Default to light
        return 'light';
    }
    
    setTheme(theme) {
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.updateIcon();
    }
    
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
        
        // Dispatch custom event for other components to react
        document.dispatchEvent(new CustomEvent('themeChange', { 
            detail: { theme: newTheme } 
        }));
    }
    
    updateIcon() {
        if (!this.themeIcon) return;
        
        if (this.currentTheme === 'dark') {
            this.themeIcon.classList.remove('fa-moon');
            this.themeIcon.classList.add('fa-sun');
            this.themeToggle.setAttribute('aria-label', 'Switch to light mode');
        } else {
            this.themeIcon.classList.remove('fa-sun');
            this.themeIcon.classList.add('fa-moon');
            this.themeToggle.setAttribute('aria-label', 'Switch to dark mode');
        }
    }
    
    bindEvents() {
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
            this.themeToggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleTheme();
                }
            });
        }
    }
    
    addSystemThemeListener() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        
        const handleChange = (e) => {
            // Only update if user hasn't manually set a preference
            if (!localStorage.getItem('theme')) {
                const newTheme = e.matches ? 'dark' : 'light';
                this.setTheme(newTheme);
            }
        };
        
        // Modern browsers
        if (mediaQuery.addEventListener) {
            mediaQuery.addEventListener('change', handleChange);
        } 
        // Legacy browsers
        else if (mediaQuery.addListener) {
            mediaQuery.addListener(handleChange);
        }
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
    
    // Add theme class to body for compatibility
    const updateBodyClass = () => {
        const theme = document.documentElement.getAttribute('data-theme');
        document.body.classList.toggle('dark-theme', theme === 'dark');
        document.body.classList.toggle('light-theme', theme === 'light');
    };
    
    // Initial update
    updateBodyClass();
    
    // Listen for theme changes
    document.addEventListener('themeChange', updateBodyClass);
    
    // Observe attribute changes
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.attributeName === 'data-theme') {
                updateBodyClass();
            }
        });
    });
    
    observer.observe(document.documentElement, { attributes: true });
});

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
