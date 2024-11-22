from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

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

if __name__ == "__main__":
    app.run(debug=True)
