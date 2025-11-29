class SnakeGame {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.gridSize = 20;
        this.tileCount = this.canvas.width / this.gridSize;
        
        this.snake = [
            { x: 5, y: 5 }
        ];
        this.food = { x: 10, y: 10 };
        this.direction = { x: 0, y: 0 };
        this.score = 0;
        this.fruitsEaten = 0;
        this.highScore = parseInt(localStorage.getItem('snakeHighScore')) || 0;
        this.gameRunning = false;
        this.gamePaused = false;
        this.lastUpdateTime = 0;
        this.renderLoopId = null;
        
        // Interpolation variables for smooth movement
        this.interpolationProgress = 0;
        this.previousSnake = [];
        this.gameSpeed = 200;
        
        // Input optimization
        this.nextDirection = { x: 0, y: 0 };
        this.inputBuffer = null;
        this.lastInputTime = 0;
        
        this.initializeUI();
        this.bindEvents();
        this.updateScore();
        this.draw();
        this.startRenderLoop();
    }
    
    initializeUI() {
        this.scoreElement = document.getElementById('score');
        this.highScoreElement = document.getElementById('high-score');
        this.finalScoreElement = document.getElementById('final-score');
        this.finalScoreSubmitElement = document.getElementById('final-score-submit');
        this.gameOverScreen = document.getElementById('game-over-screen');
        this.gameStartOverlay = document.getElementById('game-start-overlay');
        
        // New screen elements
        this.scoreSubmissionScreen = document.getElementById('score-submission-screen');
        this.navigationScreen = document.getElementById('navigation-screen');
        
        // Flag display elements
        this.flagCard = document.getElementById('flag-card');
        this.flagText = document.getElementById('flag-text');
        this.copyFlagBtn = document.getElementById('copy-flag-btn');
        
        // High score upload elements
        this.playerNameInput = document.getElementById('player-name');
        this.submitScoreBtn = document.getElementById('submit-score-btn');
        this.skipUploadBtn = document.getElementById('skip-upload-btn');
        this.uploadStatus = document.getElementById('upload-status');
        
        this.startBtn = document.getElementById('start-btn');
        this.playAgainBtn = document.getElementById('play-again-btn');
        
        this.highScoreElement.textContent = this.highScore;
    }
    
    bindEvents() {
        // Button events
        this.startBtn.addEventListener('click', () => this.startGame());
        this.playAgainBtn.addEventListener('click', () => this.startGame());
        
        // High score upload events
        this.submitScoreBtn.addEventListener('click', () => this.submitHighScore());
        this.skipUploadBtn.addEventListener('click', () => this.skipScoreUpload());
        
        // Flag copy button
        this.copyFlagBtn.addEventListener('click', () => this.copyFlag());
        
        // Enter key for name input
        this.playerNameInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.submitHighScore();
            }
        });
        
        // Keyboard events
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
    }
    
    handleKeyPress(e) {
        if (!this.gameRunning) return;
        
        const key = e.key.toLowerCase();
        const currentTime = performance.now();
        
/*         // Prevent rapid key presses (debounce)
        if (currentTime - this.lastInputTime < 50) return;
        this.lastInputTime = currentTime;
         */
        // Movement controls with immediate response
        let newDirection = null;
        
        switch (key) {
            case 'arrowup':
            case 'w':
                if (this.direction.y === 0 && this.nextDirection.y === 0) {
                    newDirection = { x: 0, y: -1 };
                }
                break;
            case 'arrowdown':
            case 's':
                if (this.direction.y === 0 && this.nextDirection.y === 0) {
                    newDirection = { x: 0, y: 1 };
                }
                break;
            case 'arrowleft':
            case 'a':
                if (this.direction.x === 0 && this.nextDirection.x === 0) {
                    newDirection = { x: -1, y: 0 };
                }
                break;
            case 'arrowright':
            case 'd':
                if (this.direction.x === 0 && this.nextDirection.x === 0) {
                    newDirection = { x: 1, y: 0 };
                }
                break;
        }
        
        if (newDirection) {
            // Buffer the input for the next game update
            this.inputBuffer = newDirection;
            this.nextDirection = newDirection;
        }
    }
    
    startGame() {
        this.resetGame();
        this.gameRunning = true;
        this.direction = { x: 1, y: 0 }; // Start moving right
        
        // Initialize interpolation
        this.previousSnake = this.snake.map(segment => ({...segment}));
        this.interpolationProgress = 0;
        this.lastUpdateTime = performance.now();
        
        this.gameStartOverlay.classList.add('hidden');
        this.gameOverScreen.classList.add('hidden');
        
        // Hide both game over screens
        this.scoreSubmissionScreen.classList.add('hidden');
        this.navigationScreen.classList.add('hidden');
        
        this.gameLoop();
    }
    
    resetGame() {
        this.snake = [{ x: 5, y: 5 }];
        this.direction = { x: 0, y: 0 };
        this.score = 0;
        this.fruitsEaten = 0;
        this.gameRunning = false;
        this.gamePaused = false;
        
        // Reset interpolation variables
        this.interpolationProgress = 0;
        this.previousSnake = [{ x: 5, y: 5 }];
        this.lastUpdateTime = 0;
        
        // Clear input buffer
        this.nextDirection = { x: 0, y: 0 };
        this.inputBuffer = null;
        this.lastInputTime = 0;
        
        this.generateFood();
        this.updateScore();
        // draw() is handled by the render loop
        
        this.gameStartOverlay.classList.remove('hidden');
        this.gameOverScreen.classList.add('hidden');
    }
    
    startRenderLoop() {
        let lastRenderTime = 0;
        const targetFPS = 60;
        const frameTime = 1000 / targetFPS;
        
        const renderFrame = (currentTime) => {
            // Throttle to target FPS for better performance
            if (currentTime - lastRenderTime >= frameTime) {
                // Calculate interpolation progress for smooth movement
                if (this.gameRunning && this.lastUpdateTime > 0) {
                    const timeSinceUpdate = currentTime - this.lastUpdateTime;
                    this.interpolationProgress = Math.min(timeSinceUpdate / this.gameSpeed, 1);
                }
                
                // Render the game
                this.draw();
                lastRenderTime = currentTime;
            }
            
            // Continue render loop
            this.renderLoopId = requestAnimationFrame(renderFrame);
        };
        
        this.renderLoopId = requestAnimationFrame(renderFrame);
    }
    
    stopRenderLoop() {
        if (this.renderLoopId) {
            cancelAnimationFrame(this.renderLoopId);
            this.renderLoopId = null;
        }
    }
    
    gameLoop() {
        if (!this.gameRunning) return;
        
        // Calculate speed: reduce speed increase and cap after 10 fruits
        const speedIncrease = Math.min(this.fruitsEaten, 10) * 10; // 10ms per fruit
        this.gameSpeed = Math.max(120, 200 - speedIncrease); // Start at 200ms, minimum 120ms
        
        setTimeout(() => {
            // Apply buffered input immediately
            if (this.inputBuffer) {
                this.direction = this.inputBuffer;
                this.inputBuffer = null;
            }
            
            // Store previous snake position for interpolation
            this.previousSnake = this.snake.map(segment => ({...segment}));
            
            this.update();
            
            // Reset interpolation and update timing
            this.interpolationProgress = 0;
            this.lastUpdateTime = performance.now();
            
            if (this.gameRunning) {
                this.gameLoop();
            }
        }, this.gameSpeed);
    }
    
    update() {
        const head = { ...this.snake[0] };
        head.x += this.direction.x;
        head.y += this.direction.y;
        
        // Check wall collision
        if (head.x < 0 || head.x >= this.tileCount || head.y < 0 || head.y >= this.tileCount) {
            this.gameOver();
            return;
        }
        
        // Check self collision
        for (let segment of this.snake) {
            if (head.x === segment.x && head.y === segment.y) {
                this.gameOver();
                return;
            }
        }
        
        this.snake.unshift(head);
        
        // Check food collision
        if (head.x === this.food.x && head.y === this.food.y) {
            this.score += 10;
            this.fruitsEaten++;
            this.generateFood();
            this.updateScore();
        } else {
            this.snake.pop();
        }
    }
    
    generateFood() {
        do {
            this.food = {
                x: Math.floor(Math.random() * this.tileCount),
                y: Math.floor(Math.random() * this.tileCount)
            };
        } while (this.snake.some(segment => segment.x === this.food.x && segment.y === this.food.y));
    }
    
    draw() {
        // Clear canvas efficiently - retro black background
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Save context for performance
        this.ctx.save();
        
        // Draw snake with smooth interpolation
        const size = this.gridSize - 4;
        const radius = 6;
        
        for (let i = 0; i < this.snake.length; i++) {
            const segment = this.snake[i];
            let renderX = segment.x;
            let renderY = segment.y;
            
            // Apply interpolation for smooth movement (only for first few segments for performance)
            if (this.gameRunning && this.previousSnake.length > i && this.interpolationProgress < 1 && i < 5) {
                const prevSegment = this.previousSnake[i];
                if (prevSegment) {
                    // Interpolate between previous and current position
                    renderX = prevSegment.x + (segment.x - prevSegment.x) * this.interpolationProgress;
                    renderY = prevSegment.y + (segment.y - prevSegment.y) * this.interpolationProgress;
                }
            }
            
            const x = renderX * this.gridSize + 2;
            const y = renderY * this.gridSize + 2;
            
            if (i === 0) {
                // Draw snake head with special styling
                this.drawSnakeHead(x, y, size, radius);
            } else {
                // Draw snake body segments with reduced complexity for tail
                this.drawSnakeBody(x, y, size, radius, i);
            }
        }
        
        // Draw food with improved styling
        this.drawFood();
        
        // Draw subtle grid lines
        this.drawGrid();
        
        // Restore context
        this.ctx.restore();
    }
    
    drawSnakeHead(x, y, size, radius) {
        // Retro green snake head with smoother gradient
        const headGradient = this.ctx.createLinearGradient(x, y, x + size, y + size);
        headGradient.addColorStop(0, '#0f0');
        headGradient.addColorStop(0.5, '#0d0');
        headGradient.addColorStop(1, '#0a0');
        
        this.ctx.fillStyle = headGradient;
        this.ctx.fillRect(x, y, size, size);
        
        // Add retro glow effect
        this.ctx.shadowColor = '#0f0';
        this.ctx.shadowBlur = 8;
        this.ctx.fillRect(x, y, size, size);
        this.ctx.shadowBlur = 0;
        
        // Add border for definition
        this.ctx.strokeStyle = '#0f0';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(x, y, size, size);
        
        // Draw simple eyes
        this.drawSnakeEyes(x, y, size);
    }
    
    drawSnakeBody(x, y, size, radius, segmentIndex) {
        // Smooth gradient for body segments
        const intensity = 1 - (segmentIndex * 0.02); // Gradual fade
        const bodyGradient = this.ctx.createLinearGradient(x, y, x + size, y + size);
        
        const baseGreen = Math.floor(220 * intensity);
        bodyGradient.addColorStop(0, `rgb(0, ${Math.min(255, baseGreen + 35)}, 0)`);
        bodyGradient.addColorStop(0.5, `rgb(0, ${baseGreen}, 0)`);
        bodyGradient.addColorStop(1, `rgb(0, ${Math.max(100, baseGreen - 30)}, 0)`);
        
        this.ctx.fillStyle = bodyGradient;
        this.ctx.fillRect(x, y, size, size);
        
        // Add subtle glow that fades with distance
        this.ctx.shadowColor = '#0f0';
        this.ctx.shadowBlur = Math.max(2, 6 * intensity);
        this.ctx.fillRect(x, y, size, size);
        this.ctx.shadowBlur = 0;
        
        // Add border for smooth definition
        this.ctx.strokeStyle = `rgba(0, ${Math.floor(255 * intensity)}, 0, 0.6)`;
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(x, y, size, size);
    }
    
    drawSnakeEyes(x, y, size) {
        const eyeSize = 2;
        const eyeOffset = size * 0.3;
        
        // Simple black square eyes for retro look
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(x + eyeOffset - eyeSize/2, y + eyeOffset - eyeSize/2, eyeSize, eyeSize);
        this.ctx.fillRect(x + size - eyeOffset - eyeSize/2, y + eyeOffset - eyeSize/2, eyeSize, eyeSize);
    }
    
    drawScalePattern(x, y, size, segmentIndex) {
        // Add subtle scale pattern to body segments
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.lineWidth = 1;
        
        const offset = (segmentIndex % 2) * (size / 4);
        
        // Draw diagonal lines for scale effect
        this.ctx.beginPath();
        this.ctx.moveTo(x + offset, y);
        this.ctx.lineTo(x + size/2 + offset, y + size);
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.moveTo(x + size/2 + offset, y);
        this.ctx.lineTo(x + size + offset, y + size);
        this.ctx.stroke();
    }
    
    drawFood() {
        const x = this.food.x * this.gridSize + 2;
        const y = this.food.y * this.gridSize + 2;
        const size = this.gridSize - 4;
        
        // Retro yellow food
        this.ctx.fillStyle = '#ff0';
        this.ctx.fillRect(x, y, size, size);
        
        // Add glow effect
        this.ctx.shadowColor = '#ff0';
        this.ctx.shadowBlur = 15;
        this.ctx.fillRect(x, y, size, size);
        this.ctx.shadowBlur = 0;
        
        // Add border
        this.ctx.strokeStyle = '#cc0';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x, y, size, size);
    }
    
    drawGrid() {
        // Draw subtle retro grid lines
        this.ctx.strokeStyle = 'rgba(0, 255, 0, 0.1)';
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        
        // Draw all vertical lines
        for (let i = 0; i <= this.tileCount; i++) {
            this.ctx.moveTo(i * this.gridSize, 0);
            this.ctx.lineTo(i * this.gridSize, this.canvas.height);
        }
        
        // Draw all horizontal lines
        for (let i = 0; i <= this.tileCount; i++) {
            this.ctx.moveTo(0, i * this.gridSize);
            this.ctx.lineTo(this.canvas.width, i * this.gridSize);
        }
        
        this.ctx.stroke();
    }
    
    drawRoundedRect(x, y, width, height, radius) {
        this.ctx.beginPath();
        this.ctx.moveTo(x + radius, y);
        this.ctx.lineTo(x + width - radius, y);
        this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        this.ctx.lineTo(x + width, y + height - radius);
        this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        this.ctx.lineTo(x + radius, y + height);
        this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        this.ctx.lineTo(x, y + radius);
        this.ctx.quadraticCurveTo(x, y, x + radius, y);
        this.ctx.closePath();
    }
    
    updateScore() {
        this.scoreElement.textContent = this.score;
        // Don't update high score during gameplay - we'll handle it in gameOver
        this.highScoreElement.textContent = this.highScore;
    }
    
    gameOver() {
        this.gameRunning = false;
        
        // Set scores in both elements
        this.finalScoreElement.textContent = this.score;
        this.finalScoreSubmitElement.textContent = this.score;
        
        // Check if this is a new personal high score BEFORE updating it
        const isNewHighScore = this.score > this.highScore;
        
        // Update high score if it's a new record
        if (isNewHighScore) {
            this.highScore = this.score;
            this.highScoreElement.textContent = this.highScore;
            localStorage.setItem('snakeHighScore', this.highScore);
            
            // Show score submission screen first
            this.scoreSubmissionScreen.classList.remove('hidden');
            this.navigationScreen.classList.add('hidden');
            
            // Focus on name input
            setTimeout(() => {
                if (this.playerNameInput) {
                    this.playerNameInput.focus();
                }
            }, 100);
        } else {
            // Show navigation screen directly if no high score
            this.scoreSubmissionScreen.classList.add('hidden');
            this.navigationScreen.classList.remove('hidden');
        }
        
        // Reset upload interface
        this.resetUploadInterface();
        
        this.gameOverScreen.classList.remove('hidden');
    }
    
    resetUploadInterface() {
        this.playerNameInput.value = '';
        this.uploadStatus.classList.add('hidden');
        this.uploadStatus.className = 'upload-status hidden';
        this.submitScoreBtn.disabled = false;
        this.skipUploadBtn.disabled = false;
        this.playerNameInput.disabled = false;
    }
    
    async submitHighScore() {
        const playerName = this.playerNameInput.value.trim();
        
        if (!playerName) {
            this.showUploadStatus('Please enter your name', 'error');
            this.playerNameInput.focus();
            return;
        }
        
        if (playerName.length > 50) {
            this.showUploadStatus('Name must be 50 characters or less', 'error');
            return;
        }
        
        // Disable inputs during submission
        this.submitScoreBtn.disabled = true;
        this.skipUploadBtn.disabled = true;
        this.playerNameInput.disabled = true;
        
        this.showUploadStatus('Submitting score...', 'loading');
        
        try {
            const response = await fetch('/api/submit-score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    score: this.score,
                    playerName: playerName
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showUploadStatus('Score submitted successfully! 🎉', 'success');
                
                // Check if flag was returned
                if (data.flag) {
                    this.displayFlag(data.flag);
                }
                
                // Transition to navigation screen after successful submission
                setTimeout(() => {
                    this.showNavigationScreen();
                }, 1500);
            } else {
                this.showUploadStatus(data.error || 'Failed to submit score', 'error');
                this.enableUploadInputs();
            }
        } catch (error) {
            console.error('Failed to submit score:', error);
            this.showUploadStatus('Network error. Please try again.', 'error');
            this.enableUploadInputs();
        }
    }
    
    skipScoreUpload() {
        this.showNavigationScreen();
    }
    
    showNavigationScreen() {
        this.scoreSubmissionScreen.classList.add('hidden');
        this.navigationScreen.classList.remove('hidden');
    }
    
    showUploadStatus(message, type) {
        this.uploadStatus.textContent = message;
        this.uploadStatus.className = `upload-status ${type}`;
        this.uploadStatus.classList.remove('hidden');
    }
    
    enableUploadInputs() {
        this.submitScoreBtn.disabled = false;
        this.skipUploadBtn.disabled = false;
        this.playerNameInput.disabled = false;
    }
    
    displayFlag(flag) {
        this.flagText.textContent = flag;
        this.flagCard.classList.remove('hidden');
    }
    
    copyFlag() {
        const flagText = this.flagText.textContent;
        navigator.clipboard.writeText(flagText).then(() => {
            const originalText = this.copyFlagBtn.textContent;
            this.copyFlagBtn.textContent = '✓ Copied!';
            setTimeout(() => {
                this.copyFlagBtn.textContent = originalText;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy flag:', err);
        });
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SnakeGame();
});