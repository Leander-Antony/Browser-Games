from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
mongo_uri = os.getenv('MONGO_URI')

client = MongoClient(mongo_uri)
db = client['games']
data_collection = db['clicker']

app = Flask(__name__)

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["games"]
clicker_collection = db["clicker"]

@app.route('/')
def home():
    # Fetch top 5 scores, sorted by descending order
    leaderboard = clicker_collection.find().sort("score", -1).limit(5)
    leaderboard = list(leaderboard)  # Convert cursor to a list to pass to the template
    return render_template('index.html', leaderboard=leaderboard)

@app.route('/save_score', methods=['POST'])
def save_score():
    score = request.json.get('score')
    if score is not None:
        # Insert the score into the MongoDB collection
        clicker_collection.insert_one({"score": score})
        return jsonify({"message": "Score saved successfully!"}), 200
    else:
        return jsonify({"error": "No score provided!"}), 400

@app.route('/submit-score', methods=['POST'])
def submit_score():
    data = request.get_json()
    player_name = data['player_name']
    score = data['score']

    # Insert the player's score into the database
    data_collection.insert_one({'player_name': player_name, 'score': score})

    # Fetch the updated leaderboard sorted by score in descending order
    leaderboard = list(data_collection.find().sort("score", -1).limit(10))

    # Convert leaderboard entries to JSON-friendly format
    leaderboard_data = [{'player_name': entry['player_name'], 'score': entry['score']} for entry in leaderboard]

    # Return the leaderboard as a JSON response
    return jsonify({'leaderboard': leaderboard_data})

@app.route('/get-leaderboard', methods=['GET'])
def get_leaderboard():
    # Fetch the leaderboard from the database
    leaderboard = list(data_collection.find().sort("score", -1).limit(10))

    # Convert leaderboard entries to JSON-friendly format
    leaderboard_data = [{'player_name': entry['player_name'], 'score': entry['score']} for entry in leaderboard]

    # Return the leaderboard as a JSON response
    return jsonify({'leaderboard': leaderboard_data})

if __name__ == "__main__":
    app.run(debug=True)
