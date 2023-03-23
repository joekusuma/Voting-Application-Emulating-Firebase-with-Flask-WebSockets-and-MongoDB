#database implementation test code

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "your_connection_string"
app.config["SECRET_KEY"] = "your_secret_key"
mongo = PyMongo(app)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    if "option" not in data:
        return jsonify({"error": "Option not provided"}), 400
    if "voter_id" not in data:
        return jsonify({"error": "Voter ID not provided"}), 400
    mongo.db.votes.insert_one(data)
    socketio.emit("vote", data, broadcast=True)
    return jsonify({"success": True})

@socketio.on("connect")
def on_connect():
    options = ["Option A", "Option B", "Option C"]
    vote_counts = {option: 0 for option in options}
    for vote in mongo.db.votes.find():
        option = vote["option"]
        if option in options:
            vote_counts[option] += 1
    socketio.emit("vote_counts", vote_counts)


@socketio.on("vote")
def on_vote(data):
    mongo.db.votes.insert_one(data)
    options = ["Option A", "Option B", "Option C"]
    vote_counts = {option: 0 for option in options}
    for vote in mongo.db.votes.find():
        option = vote["option"]
        if option in options:
            vote_counts[option] += 1
    socketio.emit("vote_counts", vote_counts)

