// DOM Elements
const startGameBtn = document.getElementById('start-game-btn');
const resetGameBtn = document.getElementById('reset-game-btn');
const playerInfo = document.getElementById('player-info');
const playerName = document.getElementById('player-name');
const playerScore = document.getElementById('player-score');
const welcomeScreen = document.getElementById('welcome-screen');
const puzzleCard = document.getElementById('puzzle-card');
const completionScreen = document.getElementById('completion-screen');
const puzzleTitle = document.getElementById('puzzle-title');
const puzzleDifficulty = document.getElementById('puzzle-difficulty');
const puzzleDescription = document.getElementById('puzzle-description');
const puzzleTime = document.getElementById('puzzle-time');
const puzzleAttempts = document.getElementById('puzzle-attempts');
const hintsUsed = document.getElementById('hints-used');
const timeProgress = document.getElementById('time-progress');
const attemptsProgress = document.getElementById('attempts-progress');
const hintsProgress = document.getElementById('hints-progress');
const towerProgress = document.getElementById('tower-progress');
const currentLevel = document.getElementById('current-level');
const levelCount = document.getElementById('level-count');
const scoreValue = document.getElementById('score-value');
const finalScore = document.getElementById('final-score');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const hintBtn = document.getElementById('hint-btn');
const startDialogOverlay = document.getElementById('start-dialog-overlay');
const closeDialogBtn = document.getElementById('close-dialog-btn');
const playerNameInput = document.getElementById('player-name-input');
const beginAdventureBtn = document.getElementById('begin-adventure-btn');
const currentYear = document.getElementById('current-year');

// Set current year in footer
currentYear.textContent = new Date().getFullYear();

// Game state
let gameState = {
    currentLevel: 0,
    score: 0,
    hintsUsed: 0,
    playerName: '',
    gameStarted: false,
    gameCompleted: false,
    currentPuzzle: null,
    elapsedTime: 0,
    timerInterval: null
};

// Event Listeners
startGameBtn.addEventListener('click', () => {
    startDialogOverlay.style.display = 'flex';
});

closeDialogBtn.addEventListener('click', () => {
    startDialogOverlay.style.display = 'none';
});

beginAdventureBtn.addEventListener('click', () => {
    const name = playerNameInput.value.trim();
    if (name) {
        startGame(name);
        startDialogOverlay.style.display = 'none';
    }
});

resetGameBtn.addEventListener('click', resetGame);

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

hintBtn.addEventListener('click', requestHint);

// Game Functions
function startGame(name) {
    gameState.playerName = name;
    gameState.gameStarted = true;
    gameState.currentLevel = 0;
    gameState.score = 0;
    gameState.hintsUsed = 0;
    gameState.gameCompleted = false;
    
    // Update UI
    startGameBtn.style.display = 'none';
    resetGameBtn.style.display = 'block';
    playerInfo.style.display = 'flex';
    playerName.textContent = `Player: ${name}`;
    playerScore.textContent = `Score: ${gameState.score}`;
    welcomeScreen.style.display = 'none';
    puzzleCard.style.display = 'block';
    completionScreen.style.display = 'none';
    
    // Enable chat
    chatInput.disabled = false;
    sendBtn.disabled = false;
    hintBtn.disabled = false;
    
    // Clear chat
    chatMessages.innerHTML = '';
    
    // Add welcome message
    addBotMessage(`Welcome to the Mystical Tower, ${name}! I am your guide through this mysterious place. Solve the puzzles to advance through the tower and escape. Type 'hint' if you need assistance.`);
    
    // Load first puzzle
    fetchPuzzle(gameState.currentLevel);
}

function resetGame() {
    // Clear timer if running
    if (gameState.timerInterval) {
        clearInterval(gameState.timerInterval);
        gameState.timerInterval = null;
    }
    
    // Reset game state
    gameState = {
        currentLevel: 0,
        score: 0,
        hintsUsed: 0,
        playerName: '',
        gameStarted: false,
        gameCompleted: false,
        currentPuzzle: null,
        elapsedTime: 0,
        timerInterval: null
    };
    
    // Update UI
    startGameBtn.style.display = 'block';
    resetGameBtn.style.display = 'none';
    playerInfo.style.display = 'none';
    welcomeScreen.style.display = 'flex';
    puzzleCard.style.display = 'none';
    completionScreen.style.display = 'none';
    
    // Disable chat
    chatInput.disabled = true;
    sendBtn.disabled = true;
    hintBtn.disabled = true;
    
    // Clear chat
    chatMessages.innerHTML = '';
    
    // Reset input
    chatInput.value = '';
    playerNameInput.value = '';
}

function fetchPuzzle(level) {
    // Show loading state
    puzzleTitle.textContent = 'Loading...';
    puzzleDescription.textContent = 'Fetching the next puzzle...';
    
    // Reset timer
    if (gameState.timerInterval) {
        clearInterval(gameState.timerInterval);
    }
    
    gameState.elapsedTime = 0;
    updateTimer();
    
    // Fetch puzzle from backend
    fetch(`/api/puzzle/${level}`)
        .then(response => response.json())
        .then(data => {
            gameState.currentPuzzle = data;
            displayPuzzle(data);
            startTimer();
            
            // Add puzzle introduction message
            addBotMessage(`You've encountered a new puzzle: ${data.title}. ${data.description}`);
        })
        .catch(error => {
            console.error('Error fetching puzzle:', error);
            addBotMessage('I seem to be having trouble retrieving the next puzzle. Please try again later.');
        });
}

function displayPuzzle(puzzle) {
    // Update puzzle card
    puzzleTitle.textContent = puzzle.title;
    puzzleDescription.textContent = puzzle.description;
    
    // Set difficulty badge
    const difficultyLabel = getDifficultyLabel(puzzle.difficulty);
    puzzleDifficulty.textContent = difficultyLabel;
    puzzleDifficulty.className = 'badge'; // Reset class
    puzzleDifficulty.classList.add(getDifficultyClass(puzzle.difficulty));
    
    // Update stats
    puzzleAttempts.textContent = puzzle.attempts || 0;
    attemptsProgress.style.width = `${Math.min(100, ((puzzle.attempts || 0) / 5) * 100)}%`;
    
    // Update tower progress
    fetch('/api/puzzles/count')
        .then(response => response.json())
        .then(data => {
            const totalPuzzles = data.count;
            towerProgress.style.width = `${((gameState.currentLevel + 1) / totalPuzzles) * 100}%`;
            currentLevel.textContent = `Level ${gameState.currentLevel + 1}`;
            levelCount.textContent = `${gameState.currentLevel + 1} / ${totalPuzzles}`;
        });
}

function startTimer() {
    gameState.timerInterval = setInterval(() => {
        gameState.elapsedTime++;
        updateTimer();
    }, 1000);
}

function updateTimer() {
    const minutes = Math.floor(gameState.elapsedTime / 60);
    const seconds = gameState.elapsedTime % 60;
    puzzleTime.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    // Update progress bar (5 minutes max)
    timeProgress.style.width = `${Math.min(100, (gameState.elapsedTime / 300) * 100)}%`;
}

function sendMessage() {
    const message = chatInput.value.trim();
    if (!message || !gameState.gameStarted) return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input
    chatInput.value = '';
    
    // Process message
    processUserMessage(message);
}

function processUserMessage(message) {
    // Check if it's a hint request
    if (message.toLowerCase() === 'hint') {
        requestHint();
        return;
    }
    
    // Send to backend for processing
    fetch('/api/answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            level: gameState.currentLevel,
            answer: message,
            hintsUsed: gameState.hintsUsed
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Update attempts
        if (gameState.currentPuzzle) {
            gameState.currentPuzzle.attempts = (gameState.currentPuzzle.attempts || 0) + 1;
            puzzleAttempts.textContent = gameState.currentPuzzle.attempts;
            attemptsProgress.style.width = `${Math.min(100, (gameState.currentPuzzle.attempts / 5) * 100)}%`;
        }
        
        // Check if correct
        if (data.correct) {
            // Update score
            gameState.score += data.score;
            playerScore.textContent = `Score: ${gameState.score}`;
            scoreValue.textContent = gameState.score;
            
            // Add success message
            addBotMessage(`Congratulations! You've solved the puzzle and earned ${data.score} points. Let's continue to the next challenge.`);
            
            // Stop timer
            if (gameState.timerInterval) {
                clearInterval(gameState.timerInterval);
                gameState.timerInterval = null;
            }
            
            // Advance to next level after delay
            setTimeout(() => {
                gameState.currentLevel++;
                
                // Check if game completed
                fetch('/api/puzzles/count')
                    .then(response => response.json())
                    .then(countData => {
                        if (gameState.currentLevel >= countData.count) {
                            completeGame();
                        } else {
                            fetchPuzzle(gameState.currentLevel);
                        }
                    });
            }, 2000);
        } else {
            // Add response message
            addBotMessage(data.message);
        }
    })
    .catch(error => {
        console.error('Error processing answer:', error);
        addBotMessage('I seem to be having trouble processing your answer. Please try again.');
    });
}

function requestHint() {
    fetch('/api/hint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            level: gameState.currentLevel,
            hintsUsed: gameState.hintsUsed
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.hint) {
            gameState.hintsUsed++;
            hintsUsed.textContent = `${gameState.hintsUsed}/3`;
            hintsProgress.style.width = `${(gameState.hintsUsed / 3) * 100}%`;
            
            // Add hint message
            addBotMessage(`Hint: ${data.hint}`);
        } else {
            // No more hints available
            addBotMessage(data.message);
        }
    })
    .catch(error => {
        console.error('Error requesting hint:', error);
        addBotMessage('I seem to be having trouble retrieving a hint. Please try again.');
    });
}

function completeGame() {
    // Update UI
    puzzleCard.style.display = 'none';
    completionScreen.style.display = 'flex';
    finalScore.textContent = gameState.score;
    
    // Update game state
    gameState.gameCompleted = true;
    
    // Add completion message
    addBotMessage('Congratulations! You have successfully escaped the Mystical Tower. Your journey is complete!');
    
    // Disable chat input
    chatInput.disabled = true;
    sendBtn.disabled = true;
    hintBtn.disabled = true;
}

function addUserMessage(content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.textContent = content;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(content) {
    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator';
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'typing-dot';
        typingIndicator.appendChild(dot);
    }
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Simulate typing delay
    setTimeout(() => {
        // Remove typing indicator
        chatMessages.removeChild(typingIndicator);
        
        // Add bot message
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}

function getDifficultyLabel(difficulty) {
    if (difficulty <= 1) return 'Easy';
    if (difficulty <= 2) return 'Medium';
    if (difficulty <= 3) return 'Hard';
    return 'Expert';
}

function getDifficultyClass(difficulty) {
    if (difficulty <= 1) return 'easy';
    if (difficulty <= 2) return 'medium';
    if (difficulty <= 3) return 'hard';
    return 'expert';
}

// Add difficulty classes to CSS
document.head.insertAdjacentHTML('beforeend', `
    <style>
        .badge.easy { background-color: #10b981; }
        .badge.medium { background-color: #f59e0b; }
        .badge.hard { background-color: #f97316; }
        .badge.expert { background-color: #ef4444; }
    </style>
`);