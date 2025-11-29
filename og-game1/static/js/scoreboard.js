class Scoreboard {
    constructor() {
        this.loadingElement = document.getElementById('loading');
        this.scoreboardData = document.getElementById('scoreboard-data');
        this.noScoresElement = document.getElementById('no-scores');
        this.errorElement = document.getElementById('error-message');
        this.scoresTableBody = document.getElementById('scores-tbody');
        this.podiumContainer = document.getElementById('podium');
        
        this.loadScores();
    }
    
    async loadScores() {
        this.showLoading();
        
        try {
            const response = await fetch('/api/scores');
            
            if (!response.ok) {
                throw new Error('Failed to fetch scores');
            }
            
            const scores = await response.json();
            this.displayScores(scores);
            
        } catch (error) {
            console.error('Error loading scores:', error);
            this.showError();
        }
    }
    
    displayScores(scores) {
        this.hideAllSections();
        
        if (scores.length === 0) {
            this.noScoresElement.style.display = 'block';
            return;
        }
        
        // Display podium for top 3
        if (scores.length >= 1) {
            this.displayPodium(scores.slice(0, 3));
        }
        
        // Clear existing scores
        this.scoresTableBody.innerHTML = '';
        
        // Add scores to table with animation delay
        scores.forEach((score, index) => {
            const row = document.createElement('tr');
            row.style.animationDelay = `${index * 0.05}s`;
            
            // Add special styling for top 3
            if (index === 0) {
                row.classList.add('rank-first');
            } else if (index === 1) {
                row.classList.add('rank-second');
            } else if (index === 2) {
                row.classList.add('rank-third');
            }
            
            row.innerHTML = `
                <td class="rank-cell">
                    <span class="rank-number">${this.getRankDisplay(index + 1)}${index + 1}</span>
                </td>
                <td class="player-cell">${this.escapeHtml(score.name)}</td>
                <td class="score-cell">${this.formatScore(score.score)}</td>
                <td class="date-cell">${this.formatDate(score.date)}</td>
            `;
            
            this.scoresTableBody.appendChild(row);
        });
        
        this.scoreboardData.style.display = 'block';
    }
    
    displayPodium(topThree) {
        // Fill podium places
        topThree.forEach((score, index) => {
            const podiumPlace = document.getElementById(`podium-${index + 1}`);
            if (podiumPlace) {
                const nameElement = podiumPlace.querySelector('.podium-name');
                const scoreElement = podiumPlace.querySelector('.podium-score');
                
                if (nameElement) nameElement.textContent = this.escapeHtml(score.name);
                if (scoreElement) scoreElement.textContent = this.formatScore(score.score);
                
                // Add animation delay
                podiumPlace.style.animationDelay = `${index * 0.2}s`;
            }
        });
        
        this.podiumContainer.style.display = 'block';
    }
    
    getRankDisplay(rank) {
        const medals = {
            1: '🥇 ',
            2: '🥈 ',
            3: '🥉 '
        };
        return medals[rank] || '';
    }
    
    formatScore(score) {
        return score.toLocaleString();
    }
    
    formatDate(dateString) {
        if (!dateString) return 'Today';
        
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString();
        } catch (error) {
            return 'Unknown';
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    showLoading() {
        this.hideAllSections();
        this.loadingElement.style.display = 'block';
    }
    
    showError() {
        this.hideAllSections();
        this.errorElement.style.display = 'flex';
    }
    
    hideAllSections() {
        this.loadingElement.style.display = 'none';
        this.scoreboardData.style.display = 'none';
        this.noScoresElement.style.display = 'none';
        this.errorElement.style.display = 'none';
        this.podiumContainer.style.display = 'none';
    }
}

// Make loadScores function globally available for retry button
function loadScores() {
    if (window.scoreboard) {
        window.scoreboard.loadScores();
    }
}

// Initialize scoreboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.scoreboard = new Scoreboard();
});