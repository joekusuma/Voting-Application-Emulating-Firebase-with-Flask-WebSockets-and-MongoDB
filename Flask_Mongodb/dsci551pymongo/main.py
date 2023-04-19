from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from flask import Blueprint, render_template

dsci551db = MongoClient(
    "mongodb+srv://dsci551:w8QBPtSfunya7Gy0@clusterdsci551.s85edni.mongodb.net/?retryWrites=true&w=majority"
)

main = Blueprint("main", __name__)

polls = [
    {
        "id": 1,
        "title": "What is your favorite color?",
        "description": "Choose one of the following colors.",
        "options": ["Red", "Green", "Blue"],
        "votes": [3, 2, 1],
    },
    {
        "id": 2,
        "title": "What is your favorite food?",
        "description": "Choose one of the following foods.",
        "options": ["Pizza", "Burgers", "Tacos"],
        "votes": [5, 3, 2],
    },
    {
        "id": 3,
        "title": "What is your favorite movie?",
        "description": "Choose one of the following movies.",
        "options": ["Star Wars", "The Godfather", "The Shawshank Redemption"],
        "votes": [1, 4, 5],
    },
]

new_poll = []


@main.route("/")
def index():
    # user_collection = dsci551db.dsci551.users
    # user_collection.insert_one({"name": "Tiger", "age": 24})
    # user_collection.insert_one({"name": "Joe", "age": 22})
    return render_template("index.html")


@main.route("/find")
def find():
    # user_collection = dsci551db.dsci551.users
    # user = user_collection.find_one({"name": "Tiger"})
    return render_template("index.html", user=user)


@main.route("/update")
def update():
    # user_collection = dsci551db.dsci551.users
    # filter = {"name": "Tiger"}
    # newvalues = {"$set": {"age": 80}}
    # user_collection.update_one(filter, newvalues)
    return render_template("index.html")


@main.route("/delete")
def delete():
    # user_collection = dsci551db.dsci551.users
    # filter = {"name": "Tiger"}
    # user_collection.delete_one(filter)
    return render_template("index.html")

def get_next_id(poll_collection):
    latest_poll = poll_collection.find_one(sort=[("id", -1)])
    if latest_poll:
        return latest_poll["id"] + 1
    else:
        return 1
    
@main.route("/create-poll", methods=["GET", "POST"])
def create_poll():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        options = request.form["options"]
        poll_collection = dsci551db.dsci551.polls
        poll = {
            "id": get_next_id(poll_collection),
            "title": title,
            "description": description,
            "options": options.splitlines(),
            "votes": [0] * len(options.splitlines()),
        }
        poll_collection.insert_one(poll)
        return redirect(url_for("main.view_polls"))
    return render_template("create_poll.html")



@main.route("/view-polls")
def view_polls():
    poll_collection = dsci551db.dsci551.polls
    polls = []
    for index, poll in enumerate(poll_collection.find()):
        poll['id'] = index + 1
        polls.append(poll)
    return render_template("view_polls.html", polls=polls)



@main.route("/vote/<int:poll_id>", methods=["POST"])
def vote(poll_id):
    poll_collection = dsci551db.dsci551.polls
    poll = poll_collection.find_one({"id": poll_id})
    
    selected_option = request.form["option"]
    option_index = poll["options"].index(selected_option)
    poll["votes"][option_index] += 1
    poll_collection.update_one({"id": poll_id}, {"$set": poll})
    
    return redirect(url_for("main.view_polls"))





@main.route("/login")
def login():
    return render_template("login.html")

@main.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'GET':
    # handle GET request
        return render_template('create_account.html')

    elif request.method == 'POST':
        # handle POST request
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Please provide both a username and password')
            return redirect(url_for('create_account'))
        if db.users.find_one({'username': username}):
            flash('Username already exists')
            return redirect(url_for('create_account'))
        db.users.insert_one({'username': username, 'password': password})
        flash('Account created successfully')
        return redirect(url_for('login'))

    else:
        # handle other methods
        return 'Method not allowed'
app = Flask(__name__)
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
