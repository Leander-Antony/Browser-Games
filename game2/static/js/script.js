let score = 0;
let timeLeft = 30;
let isGameOver = false;

const scoreElement = document.getElementById('score');
const timerElement = document.getElementById('timer');
const messageElement = document.getElementById('message');
const clickButton = document.getElementById('click-button');

// Function to update the score each time the button is clicked
const updateScore = () => {
    if (isGameOver) return; // If the game is over, stop updating score

    score++;
    scoreElement.textContent = score;
};

// Function to start and manage the timer
const startTimer = () => {
    const timerInterval = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(timerInterval); // Stop the timer
            messageElement.textContent = `Game Over! Your final score is: ${score}`;
            isGameOver = true;
        } else {
            timeLeft--;
            timerElement.textContent = timeLeft;
        }
    }, 1000);
};

// Start the timer as soon as the game starts
startTimer();

// Event listener for clicking the button
clickButton.addEventListener('click', updateScore);

// L5Y3QNXvjvkAfAKY leander