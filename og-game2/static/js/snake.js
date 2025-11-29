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
        
        // Server-side validation
        this.scoreToken = null;
        this.playerId = null;
        this.serverFood = null;  // Food position from server
        
        // Interpolation variables for smooth movement
        this.interpolationProgress = 0;
        this.previousSnake = [];
        this.gameSpeed = 200;
        
        // Input optimization
        this.nextDirection = { x: 0, y: 0 };
        this.inputBuffer = null;
        
        // Cache gradients for performance (created once, reused every frame)
        this.cachedGradients = null;
        
        // Sleeping snake animation state
        this.isSleeping = false;
        this.sleepAnimationTime = 0;
        this.zzzParticles = [];
        
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
    
    async startGame() {
        // Initialize game session with server
        try {
            const response = await fetch('/api/game/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            if (data.success) {
                this.playerId = data.playerId;
                this.serverFood = data.food;  // Get initial food position from server
                this.scoreToken = null;
                
                console.log('Game started! Server food position:', data.food);
            } else {
                console.error('Failed to start game session');
                alert('Failed to start game. Please refresh the page.');
                return;
            }
        } catch (error) {
            console.error('Error starting game:', error);
            alert('Network error. Please check your connection.');
            return;
        }
        
        this.resetGame();
        
        // IMPORTANT: Set food AFTER resetGame() so it doesn't get overwritten
        this.food = { x: this.serverFood.x, y: this.serverFood.y };
        console.log('Client food set to match server:', this.food);
        
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
        
        // DON'T generate food here - food comes from server in startGame()!
        // this.generateFood();
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
                const deltaTime = currentTime - lastRenderTime;
                
                // Calculate interpolation progress for smooth movement
                if (this.gameRunning && this.lastUpdateTime > 0) {
                    const timeSinceUpdate = currentTime - this.lastUpdateTime;
                    this.interpolationProgress = Math.min(timeSinceUpdate / this.gameSpeed, 1);
                }
                
                // Update sleeping animation
                if (this.isSleeping) {
                    this.updateSleepingAnimation(deltaTime);
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
    
    gameLoop() {
        // Don't continue if not running or if snake is sleeping
        if (!this.gameRunning || this.isSleeping) return;
        
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
            this.updateScore();
            
            console.log('Food collision detected!');
            
            // Validate with server and get new food position
            this.validateFoodWithServer();
        } else {
            this.snake.pop();
        }
    }
    
    async validateFoodWithServer() {
        try {
            console.log('Sending to server:');
            console.log('  playerId:', this.playerId);
            console.log('  scoreToken:', this.scoreToken);
            
            const response = await fetch('/api/game/food', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    playerId: this.playerId,
                    scoreToken: this.scoreToken  // Send current token to track score
                })
            });
            
            const data = await response.json();
            console.log('Server response:', data);
            
            if (data.success) {
                // Check if snake is sleeping
                if (data.snake_sleeping) {
                    this.scoreToken = data.scoreToken;
                    this.gameRunning = false;
                    this.showSleepingSnakePopup(data.score, data.message, data.hint);
                    return;
                }
                
                // Update score token
                this.scoreToken = data.scoreToken;
                
                // Update food position from server
                this.serverFood = data.newFood;
                this.food = { x: data.newFood.x, y: data.newFood.y };
                
                console.log('Server validated! New food:', this.food);
            } else {
                // Check if snake is already sleeping
                if (data.snake_sleeping) {
                    this.gameRunning = false;
                    this.showSleepingSnakePopup(data.current_score, data.message, data.hint);
                    return;
                }
                
                console.error('Server validation failed:', data.error);
                this.gameRunning = false;
                alert('Server validation failed. Game stopped.');
            }
        } catch (error) {
            console.error('Error validating with server:', error);
            // Continue game even if server request fails (for local testing)
            this.generateFood();
        }
    }
    
    showSleepingSnakePopup(score, message, hint) {
        // IMMEDIATELY stop the game and activate sleeping mode to prevent further movement
        this.gameRunning = false;
        this.isSleeping = true;
        this.sleepAnimationTime = 0;
        this.zzzParticles = [];
        
        // Hide the food by moving it off-screen
        this.food = { x: -1, y: -1 };
        this.serverFood = { x: -1, y: -1 };
        
        // Make sure game over screen stays hidden (don't show Play Again button)
        this.gameOverScreen.classList.add('hidden');
        
        // Show non-invasive message
        this.showSleepyMessage(message, hint);
    }
    
    showSleepyMessage(message, hint) {
        // Remove any existing message
        const existingMsg = document.getElementById('sleepy-message');
        if (existingMsg) {
            existingMsg.remove();
        }
        
        // Create message banner at bottom of game-container (outside canvas)
        const gameContainer = document.querySelector('.game-container');
        const messageDiv = document.createElement('div');
        messageDiv.id = 'sleepy-message';
        messageDiv.style.cssText = `
            position: absolute;
            bottom: 0px;
            left: 0px;
            right: 0px;
            background: rgba(15, 15, 15, 0.95);
            border-top: 2px solid #ffd700;
            padding: 10px 15px;
            border-radius: 0;
            z-index: 100;
            text-align: center;
            box-shadow: 0 -2px 20px rgba(255, 215, 0, 0.3);
            animation: slideUp 0.5s ease-out;
        `;
        
        messageDiv.innerHTML = `
            <div style="color: #ffd700; font-size: 1rem; font-weight: bold; margin-bottom: 4px;">
                🐍💤 Snake is Sleepy!
            </div>
            <div style="color: #0f0; font-size: 0.85rem; line-height: 1.3;">
                ${message || "The snake doesn't get paid enough to work anymore..."}
            </div>
        `;
        
        // Add animation keyframes
        if (!document.getElementById('sleepy-message-styles')) {
            const style = document.createElement('style');
            style.id = 'sleepy-message-styles';
            style.textContent = `
                @keyframes slideUp {
                    from {
                        transform: translateY(20px);
                        opacity: 0;
                    }
                    to {
                        transform: translateY(0);
                        opacity: 1;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        gameContainer.appendChild(messageDiv);
    }
    
    generateFood() {
        // Fallback for client-side generation (should use server food)
        do {
            this.food = {
                x: Math.floor(Math.random() * this.tileCount),
                y: Math.floor(Math.random() * this.tileCount)
            };
        } while (this.snake.some(segment => segment.x === this.food.x && segment.y === this.food.y));
    }
    
    initializeGradients() {
        // Create reusable gradients for better performance
        const size = this.gridSize - 4;
        
        // Head gradient
        const headGradient = this.ctx.createLinearGradient(0, 0, size, size);
        headGradient.addColorStop(0, '#0f0');
        headGradient.addColorStop(0.5, '#0d0');
        headGradient.addColorStop(1, '#0a0');
        
        // Body gradients (pre-create a few for different intensities)
        const bodyGradients = [];
        for (let i = 0; i < 10; i++) {
            const intensity = 1 - (i * 0.02);
            const gradient = this.ctx.createLinearGradient(0, 0, size, size);
            const baseGreen = Math.floor(220 * intensity);
            gradient.addColorStop(0, `rgb(0, ${Math.min(255, baseGreen + 35)}, 0)`);
            gradient.addColorStop(0.5, `rgb(0, ${baseGreen}, 0)`);
            gradient.addColorStop(1, `rgb(0, ${Math.max(100, baseGreen - 30)}, 0)`);
            bodyGradients.push(gradient);
        }
        
        this.cachedGradients = {
            head: headGradient,
            body: bodyGradients
        };
    }
    
    draw() {
        // Clear canvas efficiently - retro black background
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Initialize cached gradients on first draw
        if (!this.cachedGradients) {
            this.initializeGradients();
        }
        
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
        
        // Draw sleeping animation LAST so it's on top (absolute foreground)
        this.drawSleepingAnimation();
    }
    
    drawSnakeHead(x, y, size, radius) {
        // Use cached gradient for better performance
        this.ctx.fillStyle = this.cachedGradients.head;
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
        // Use cached gradient for better performance
        const gradientIndex = Math.min(segmentIndex - 1, 9); // Index 0-9 for cached gradients
        const intensity = 1 - (segmentIndex * 0.02); // Gradual fade
        
        this.ctx.fillStyle = this.cachedGradients.body[gradientIndex];
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
        
        if (this.isSleeping) {
            // Draw closed eyes (horizontal lines)
            this.ctx.strokeStyle = '#000';
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.moveTo(x + eyeOffset - 2, y + eyeOffset);
            this.ctx.lineTo(x + eyeOffset + 2, y + eyeOffset);
            this.ctx.moveTo(x + size - eyeOffset - 2, y + eyeOffset);
            this.ctx.lineTo(x + size - eyeOffset + 2, y + eyeOffset);
            this.ctx.stroke();
        } else {
            // Simple black square eyes for retro look
            this.ctx.fillStyle = '#000';
            this.ctx.fillRect(x + eyeOffset - eyeSize/2, y + eyeOffset - eyeSize/2, eyeSize, eyeSize);
            this.ctx.fillRect(x + size - eyeOffset - eyeSize/2, y + eyeOffset - eyeSize/2, eyeSize, eyeSize);
        }
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
    
    updateSleepingAnimation(deltaTime) {
        if (!this.isSleeping) return;
        
        this.sleepAnimationTime += deltaTime;
        
        // Spawn new ZZZ particles periodically
        if (this.sleepAnimationTime % 800 < deltaTime) {
            const head = this.snake[0];
            const headX = head.x * this.gridSize + this.gridSize / 2;
            const headY = head.y * this.gridSize;
            
            this.zzzParticles.push({
                x: headX + (Math.random() - 0.5) * 10,
                y: headY,
                opacity: 1,
                size: 16 + Math.random() * 6, // Reduced size (was 22 + Math.random() * 10)
                speed: 0.5 + Math.random() * 0.5,
                drift: 0.8 + Math.random() * 0.4 // Diagonal drift to the right (was (Math.random() - 0.5) * 0.3)
            });
        }
        
        // Update ZZZ particles
        for (let i = this.zzzParticles.length - 1; i >= 0; i--) {
            const particle = this.zzzParticles[i];
            particle.y -= particle.speed;
            particle.x += particle.drift;
            particle.opacity -= 0.01;
            
            // Remove dead particles
            if (particle.opacity <= 0) {
                this.zzzParticles.splice(i, 1);
            }
        }
    }
    
    drawSleepingAnimation() {
        if (!this.isSleeping) return;
        
        // Draw ZZZ particles with speech balloon backgrounds
        this.ctx.save();
        for (const particle of this.zzzParticles) {
            this.ctx.globalAlpha = particle.opacity;
            
            // Draw speech balloon (white rounded rectangle)
            const padding = 8;
            const balloonWidth = particle.size * 0.8;
            const balloonHeight = particle.size * 1.1;
            const balloonX = particle.x - balloonWidth / 2;
            const balloonY = particle.y - balloonHeight + 5;
            const radius = 8;
            
            // Balloon body
            this.ctx.fillStyle = 'white';
            this.ctx.beginPath();
            this.ctx.moveTo(balloonX + radius, balloonY);
            this.ctx.lineTo(balloonX + balloonWidth - radius, balloonY);
            this.ctx.arcTo(balloonX + balloonWidth, balloonY, balloonX + balloonWidth, balloonY + radius, radius);
            this.ctx.lineTo(balloonX + balloonWidth, balloonY + balloonHeight - radius);
            this.ctx.arcTo(balloonX + balloonWidth, balloonY + balloonHeight, balloonX + balloonWidth - radius, balloonY + balloonHeight, radius);
            this.ctx.lineTo(balloonX + radius, balloonY + balloonHeight);
            this.ctx.arcTo(balloonX, balloonY + balloonHeight, balloonX, balloonY + balloonHeight - radius, radius);
            this.ctx.lineTo(balloonX, balloonY + radius);
            this.ctx.arcTo(balloonX, balloonY, balloonX + radius, balloonY, radius);
            this.ctx.closePath();
            this.ctx.fill();
            
            // Small tail pointing to snake
            this.ctx.beginPath();
            this.ctx.moveTo(balloonX + 10, balloonY + balloonHeight);
            this.ctx.lineTo(balloonX + 5, balloonY + balloonHeight + 8);
            this.ctx.lineTo(balloonX + 15, balloonY + balloonHeight);
            this.ctx.fill();
            
            // Draw black Z text
            this.ctx.fillStyle = 'black';
            this.ctx.font = `bold ${particle.size}px Arial`;
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText('Z', particle.x, particle.y - balloonHeight / 2 + 5);
        }
        this.ctx.restore();
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
        
        // Check if we have a score token
        if (!this.scoreToken) {
            this.showUploadStatus('No score token available. Did you eat any food?', 'error');
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
                    scoreToken: this.scoreToken,
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