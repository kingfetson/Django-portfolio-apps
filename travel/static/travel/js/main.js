// Travel App JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Travel app JavaScript loaded');
    
    // Initialize wishlist buttons
    initWishlistButtons();
    
    // Add hover effects to cards
    initCardHoverEffects();
    
    // Initialize any filter functionality
    initFilters();
});

function initWishlistButtons() {
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            const destinationId = this.dataset.destinationId;
            if (destinationId) {
                toggleWishlist(destinationId, this);
            }
        });
    });
}

function toggleWishlist(destinationId, button) {
    // For now, just toggle visual state
    // In a real app, you would make an AJAX call to your backend
    const icon = button.querySelector('i');
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        button.style.background = '#c0392b';
        button.innerHTML = '<i class="fas fa-heart"></i> In Wishlist';
        showNotification('Added to wishlist!');
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        button.style.background = '#e74c3c';
        button.innerHTML = '<i class="far fa-heart"></i> Wishlist';
        showNotification('Removed from wishlist');
    }
}

function initCardHoverEffects() {
    const cards = document.querySelectorAll('.destination-card, .trip-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'var(--box-shadow, 0 4px 12px rgba(0,0,0,0.1))';
        });
    });
}

function initFilters() {
    // Add active state to filter buttons
    const filterButtons = document.querySelectorAll('.continent-btn, .filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // If it's a regular link, let it proceed
            if (this.href) return;
            
            e.preventDefault();
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Add filter logic here if needed
            console.log('Filter clicked:', this.textContent);
        });
    });
}

function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #2ecc71;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
