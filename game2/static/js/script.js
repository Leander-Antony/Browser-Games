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

            // Send the score to the server when the game is over
            saveScore(score);
        } else {
            timeLeft--;
            timerElement.textContent = timeLeft;
        }
    }, 1000);
};

// Function to save score to the database using Flask
const saveScore = (score) => {
    fetch('/save_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ score: score })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error saving score:', error);
    });
};

// Start the timer as soon as the game starts
startTimer();

// Event listener for clicking the button
clickButton.addEventListener('click', updateScore);
