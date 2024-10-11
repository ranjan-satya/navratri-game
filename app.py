from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
server = app

# Manager's words (without emojis) - now 20 words
manager_words = [
    "Garba", "Durga", "Rangoli", "Aarti", "Pooja Thali", "Chaniya Choli", 
    "Navratri Colors", "Trishul", "Shakti", "Folk Dance", "Dandiya", 
    "Bhajan", "Mata Rani", "Devotion", "Fasting", "Kumkum", 
    "Chanting", "Festival Lights", "Mandir", "Blessings"
]

# In-memory storage for player submissions and session status
players_submissions = []
session_active = False  # This will track the session status

@app.route('/')
def index():
    return "Welcome to Navratri Game"

@app.route('/player')
def player():
    return render_template('player.html')

@app.route('/manager')
def manager():
    return render_template('manager.html')

# API to start a new game session
@app.route('/start_session', methods=['POST'])
def start_session():
    global players_submissions, session_active
    players_submissions = []  # Clear previous submissions
    session_active = True  # Mark session as active
    return jsonify({"message": "Game session started!"})

# API to stop the game session
@app.route('/stop_session', methods=['POST'])
def stop_session():
    global session_active
    session_active = False  # Mark session as inactive
    return jsonify({"message": "Game session stopped!"})

@app.route('/submit_player', methods=['POST'])
def submit_player():
    if not session_active:
        return jsonify({"message": "Game session is not active!"}), 403  # Reject if session is not active

    data = request.json
    player_name = data['name']
    submitted_words = data['words']

    # Add player submission to in-memory storage
    players_submissions.append({
        'name': player_name,
        'words': submitted_words
    })

    return jsonify({"message": "Submission successful!"})

@app.route('/get_results', methods=['GET'])
def get_results():
    results = []
    
    for submission in players_submissions:
        player_name = submission['name']
        submitted_words = submission['words']

        # Check matches by comparing submitted words with manager words
        matches = len(set(submitted_words).intersection(set(manager_words)))

        results.append({
            'name': player_name,
            'words': submitted_words,
            'matches': matches
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
