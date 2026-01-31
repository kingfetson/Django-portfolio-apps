// landing/static/landing/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    // ===== SMOOTH SCROLLING =====
    initSmoothScrolling();
    
    // ===== SKILL BAR ANIMATIONS =====
    initSkillAnimations();
    
    // ===== DISH CARD ANIMATIONS =====
    initDishAnimations();
    
    // ===== LAZY LOADING IMAGES =====
    initLazyLoading();
    
    // ===== MENU TOGGLE FOR MOBILE =====
    initMobileMenu();
    
    // ===== API INTEGRATIONS =====
    initAPIIntegrations();
});

// ===== SMOOTH SCROLLING =====
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update URL without page reload
                history.pushState(null, null, targetId);
            }
        });
    });
}

// ===== SKILL BAR ANIMATIONS =====
function initSkillAnimations() {
    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressFill = entry.target.querySelector('.progress-fill');
                if (progressFill) {
                    const width = progressFill.style.width;
                    progressFill.style.width = '0%';
                    
                    // Trigger reflow
                    progressFill.offsetHeight;
                    
                    progressFill.style.transition = 'width 1.5s ease-in-out';
                    progressFill.style.width = width;
                    progressFill.classList.add('animate-progress');
                }
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.skill-card').forEach(card => {
        observer.observe(card);
    });
}

// ===== DISH CARD ANIMATIONS =====
function initDishAnimations() {
    const dishObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                dishObserver.unobserve(entry.target);
            }
        });
    }, { 
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });
    
    // Set initial state for dish cards
    document.querySelectorAll('.dish-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        card.style.transitionDelay = (index * 0.1) + 's';
        dishObserver.observe(card);
    });
}

// ===== LAZY LOADING IMAGES =====
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for older browsers
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.getAttribute('data-src');
        });
    }
}

// ===== MOBILE MENU TOGGLE =====
function initMobileMenu() {
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.querySelector('nav');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('mobile-active');
            menuToggle.classList.toggle('active');
            
            // Toggle aria-expanded for accessibility
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', !isExpanded);
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!navMenu.contains(event.target) && !menuToggle.contains(event.target)) {
                navMenu.classList.remove('mobile-active');
                menuToggle.classList.remove('active');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
}

// ===== API INTEGRATIONS =====
function initAPIIntegrations() {
    // You can add API integration functions here
    // Example: fetchWeatherData(), fetchQuote(), etc.
    
    // Check if API widgets exist and initialize them
    if (document.getElementById('weather-data')) {
        fetchWeatherData();
    }
    
    if (document.getElementById('quote-data')) {
        fetchQuote();
    }
    
    if (document.getElementById('github-data')) {
        fetchGitHubStats();
    }
}

// ===== WEATHER API =====
function fetchWeatherData() {
    const weatherElement = document.getElementById('weather-data');
    if (!weatherElement) return;
    
    weatherElement.innerHTML = '<div class="loading">Loading weather...</div>';
    
    fetch('/api/weather/?city=London&country=GB')
        .then(response => {
            if (!response.ok) throw new Error('Weather API failed');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const weather = data.data;
                weatherElement.innerHTML = `
                    <div class="weather-data animate-fade-in">
                        <div class="weather-icon">
                            <img src="${weather.icon_url}" alt="${weather.description}" width="60" height="60">
                        </div>
                        <div class="weather-info">
                            <h4>${weather.city}, ${weather.country}</h4>
                            <div class="weather-temp">${weather.temperature}°C</div>
                            <div class="weather-details">
                                ${weather.description} • Feels like ${weather.feels_like}°C<br>
                                Humidity: ${weather.humidity}% • Wind: ${weather.wind_speed} m/s
                            </div>
                        </div>
                    </div>
                `;
            } else {
                weatherElement.innerHTML = '<div class="error">Weather data unavailable</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching weather:', error);
            weatherElement.innerHTML = '<div class="error">Weather data unavailable</div>';
        });
}

// ===== QUOTE API =====
function fetchQuote() {
    const quoteElement = document.getElementById('quote-data');
    if (!quoteElement) return;
    
    quoteElement.innerHTML = '<div class="loading">Loading quote...</div>';
    
    fetch('/api/quote/')
        .then(response => {
            if (!response.ok) throw new Error('Quote API failed');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const quote = data.data;
                quoteElement.innerHTML = `
                    <blockquote class="animate-fade-in stagger-delay-1">
                        "${quote.quote}"
                    </blockquote>
                    <div class="quote-author animate-fade-in stagger-delay-2">
                        — ${quote.author}
                        ${quote.source !== 'Fallback' ? `<br><small>Source: ${quote.source}</small>` : ''}
                    </div>
                `;
            } else {
                quoteElement.innerHTML = '<div class="error">Quote unavailable</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching quote:', error);
            quoteElement.innerHTML = '<div class="error">Quote unavailable</div>';
        });
}

// ===== GITHUB STATS API =====
function fetchGitHubStats() {
    const githubElement = document.getElementById('github-data');
    if (!githubElement) return;
    
    // Replace with your GitHub username
    const githubUsername = 'octocat';
    
    githubElement.innerHTML = '<div class="loading">Loading GitHub stats...</div>';
    
    fetch(`/api/github/?username=${githubUsername}`)
        .then(response => {
            if (!response.ok) throw new Error('GitHub API failed');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const github = data.data;
                const user = github.user;
                const repos = github.repositories;
                
                githubElement.innerHTML = `
                    <div class="github-stats">
                        <div class="stat-item animate-scale-in stagger-delay-1">
                            <div class="stat-number">${user.public_repos}</div>
                            <div class="stat-label">Repositories</div>
                        </div>
                        <div class="stat-item animate-scale-in stagger-delay-2">
                            <div class="stat-number">${user.followers}</div>
                            <div class="stat-label">Followers</div>
                        </div>
                        <div class="stat-item animate-scale-in stagger-delay-3">
                            <div class="stat-number">${user.following}</div>
                            <div class="stat-label">Following</div>
                        </div>
                        <div class="stat-item animate-scale-in stagger-delay-4">
                            <div class="stat-number">${user.public_gists}</div>
                            <div class="stat-label">Gists</div>
                        </div>
                    </div>
                    
                    ${repos.length > 0 ? `
                    <div class="github-repos mt-40">
                        <h4>Recent Repositories</h4>
                        ${repos.slice(0, 3).map((repo, index) => `
                            <div class="repo-item animate-fade-in stagger-delay-${index + 1}">
                                <div class="repo-name">
                                    <a href="${repo.html_url}" target="_blank" rel="noopener">${repo.name}</a>
                                    ${repo.language ? `<span class="tag">${repo.language}</span>` : ''}
                                </div>
                                <div class="repo-description">${repo.description || 'No description'}</div>
                            </div>
                        `).join('')}
                    </div>
                    ` : ''}
                `;
            } else {
                githubElement.innerHTML = '<div class="error">GitHub data unavailable</div>';
            }
        })
        .catch(error => {
            console.error('Error fetching GitHub data:', error);
            githubElement.innerHTML = '<div class="error">GitHub data unavailable</div>';
        });
}

// ===== HELPER FUNCTIONS =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add resize listener with debounce
window.addEventListener('resize', debounce(function() {
    // Handle responsive behaviors
}, 250));



 * Main JavaScript for Portfolio Website
 * Includes widget functionality and interactive elements
 */

// Import theme manager
import './theme.js';

// Widget API functions
const WidgetManager = {
    async fetchWeatherData() {
        try {
            const response = await fetch('/api/weather/');
            const data = await response.json();
            this.updateWeatherWidget(data);
        } catch (error) {
            console.error('Weather fetch failed:', error);
            this.showWeatherError();
        }
    },
    
    updateWeatherWidget(data) {
        const widget = document.getElementById('weather-data');
        if (widget && data.success) {
            widget.innerHTML = `
                <div class="flex items-center justify-between">
                    <div>
                        <div class="text-2xl font-bold">${data.data.temperature}°C</div>
                        <div class="text-sm text-light">${data.data.city}, ${data.data.country}</div>
                    </div>
                    <img src="${data.data.icon_url}" alt="${data.data.description}" class="w-12 h-12">
                </div>
                <div class="mt-2 text-sm">
                    <div>Feels like: ${data.data.feels_like}°C</div>
                    <div>Humidity: ${data.data.humidity}%</div>
                    <div>Wind: ${data.data.wind_speed} m/s</div>
                </div>
            `;
            widget.classList.remove('loading');
        }
    },
    
    showWeatherError() {
        const widget = document.getElementById('weather-data');
        if (widget) {
            widget.innerHTML = '<div class="text-center text-light">Weather data unavailable</div>';
            widget.classList.remove('loading');
        }
    },
    
    async fetchQuoteData() {
        try {
            const response = await fetch('/api/quote/');
            const data = await response.json();
            this.updateQuoteWidget(data);
        } catch (error) {
            console.error('Quote fetch failed:', error);
            this.showQuoteError();
        }
    },
    
    updateQuoteWidget(data) {
        const widget = document.getElementById('quote-data');
        if (widget && data.success) {
            widget.innerHTML = `
                <div class="italic text-lg">"${data.data.quote}"</div>
                <div class="mt-2 text-right text-sm text-light">— ${data.data.author}</div>
            `;
            widget.classList.remove('loading');
        }
    },
    
    showQuoteError() {
        const widget = document.getElementById('quote-data');
        if (widget) {
            widget.innerHTML = '<div class="text-center text-light">Quote unavailable</div>';
            widget.classList.remove('loading');
        }
    },
    
    async fetchGitHubData(username) {
        try {
            const response = await fetch(`/api/github/?username=${username}`);
            const data = await response.json();
            this.updateGitHubWidget(data);
        } catch (error) {
            console.error('GitHub fetch failed:', error);
            this.showGitHubError();
        }
    },
    
    updateGitHubWidget(data) {
        const widget = document.getElementById('github-data');
        if (widget && data.success) {
            widget.innerHTML = `
                <div class="grid grid-cols-2 gap-3">
                    <div class="text-center">
                        <div class="text-2xl font-bold">${data.data.user.public_repos}</div>
                        <div class="text-xs text-light">Repositories</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold">${data.data.user.followers}</div>
                        <div class="text-xs text-light">Followers</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold">${data.data.user.following}</div>
                        <div class="text-xs text-light">Following</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold">${data.data.user.public_gists}</div>
                        <div class="text-xs text-light">Gists</div>
                    </div>
                </div>
            `;
            widget.classList.remove('loading');
        }
    },
    
    showGitHubError() {
        const widget = document.getElementById('github-data');
        if (widget) {
            widget.innerHTML = '<div class="text-center text-light">GitHub data unavailable</div>';
            widget.classList.remove('loading');
        }
    }
};

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// Intersection Observer for animations
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements with animation classes
    document.querySelectorAll('.fade-in-up, .slide-in-left, .scale-in').forEach(el => {
        observer.observe(el);
    });
}

// Mobile menu toggle
function initMobileMenu() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            menuToggle.setAttribute('aria-expanded', 
                mobileMenu.classList.contains('hidden') ? 'false' : 'true'
            );
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenu.contains(e.target) && !menuToggle.contains(e.target)) {
                mobileMenu.classList.add('hidden');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    initSmoothScrolling();
    initAnimations();
    initMobileMenu();
    
    // Expose widget functions to global scope for template usage
    window.fetchWeatherData = () => WidgetManager.fetchWeatherData();
    window.fetchQuoteData = () => WidgetManager.fetchQuoteData();
    window.fetchGitHubData = (username) => WidgetManager.fetchGitHubData(username);
    
    // Auto-initialize widgets based on data attributes
    document.querySelectorAll('[data-widget]').forEach(widget => {
        const type = widget.dataset.widget;
        switch(type) {
            case 'weather':
                WidgetManager.fetchWeatherData();
                break;
            case 'quote':
                WidgetManager.fetchQuoteData();
                break;
            case 'github':
                const username = widget.dataset.username;
                if (username) WidgetManager.fetchGitHubData(username);
                break;
        }
    });
    
    // Update current year in footer
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
});

// Error handling
window.addEventListener('error', (e) => {
    console.error('Script error:', e.error);
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { WidgetManager };
}
