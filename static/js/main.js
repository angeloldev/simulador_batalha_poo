/**
 * Medieval Fantasy Battle Simulator - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Health bar animations
    const healthBars = document.querySelectorAll('.health-fill');
    healthBars.forEach(bar => {
        // Slight delay before animation to ensure the DOM is fully rendered
        setTimeout(() => {
            const width = bar.getAttribute('style').replace('width: ', '').replace('%;', '');
            
            // Add color based on health percentage
            if (parseFloat(width) < 25) {
                bar.classList.add('critical');
            } else if (parseFloat(width) < 50) {
                bar.classList.add('low');
            }
            
            // Add transition for smoother future updates
            bar.style.transition = 'width 0.5s ease, background-color 0.5s ease';
        }, 100);
    });
    
    // Character card hover effect
    const characterCards = document.querySelectorAll('.character-card');
    characterCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
        });
    });
    
    // Add sound effects to battle actions if we're on a battle page
    const battleActions = document.querySelectorAll('.btn-action, .ability-item');
    if (battleActions.length > 0) {
        battleActions.forEach(action => {
            action.addEventListener('click', function() {
                const actionType = this.getAttribute('data-action');
                
                // Play different sound effects based on action type
                // Note: In a real implementation, you would add actual audio files
                // This is just a placeholder for demonstration
                
                // Add visual feedback on click
                this.classList.add('clicked');
                setTimeout(() => {
                    this.classList.remove('clicked');
                }, 150);
            });
        });
    }
    
    // Add battle log auto-scroll if we're on a battle view page
    const logEntries = document.getElementById('log-entries');
    if (logEntries) {
        logEntries.scrollTop = logEntries.scrollHeight;
    }
    
    // Battle ending animation when a winner is declared
    const winnerAnnouncement = document.querySelector('.winner-announcement');
    if (winnerAnnouncement) {
        // Add a subtle pulse animation to the winner announcement
        winnerAnnouncement.classList.add('pulse-animation');
    }
    
    // Handle responsive navigation for mobile
    const navItems = document.querySelectorAll('nav ul li a');
    
    // Add animations to stat numbers when viewing character details
    const statValues = document.querySelectorAll('.stat-value');
    if (statValues.length > 0) {
        statValues.forEach(value => {
            const originalText = value.textContent;
            const numberValue = parseInt(originalText);
            
            if (!isNaN(numberValue)) {
                // Animation to count up to the actual value
                let startValue = 0;
                const duration = 1000; // 1 second animation
                const frameDuration = 1000 / 60; // 60fps
                const totalFrames = duration / frameDuration;
                const valueIncrement = numberValue / totalFrames;
                
                const counter = setInterval(() => {
                    startValue += valueIncrement;
                    
                    if (startValue >= numberValue) {
                        value.textContent = originalText;
                        clearInterval(counter);
                    } else {
                        value.textContent = Math.floor(startValue);
                    }
                }, frameDuration);
            }
        });
    }
});

// Add CSS class for clicked state to battle action buttons
document.head.insertAdjacentHTML('beforeend', `
    <style>
    .btn-action.clicked, .ability-item.clicked {
        transform: scale(0.95);
        opacity: 0.8;
    }
    
    .pulse-animation {
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .critical {
        background-color: #ef4444 !important;
    }
    
    .low {
        background-color: #f59e0b !important;
    }
    </style>
`);