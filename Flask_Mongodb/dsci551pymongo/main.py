from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from pymongo import MongoClient

dsci551db = MongoClient(
    "mongodb+srv://dsci551:w8QBPtSfunya7Gy0@clusterdsci551.s85edni.mongodb.net/?retryWrites=true&w=majority"
)

main = Blueprint("main", __name__)

new_poll = []


def get_next_id(poll_collection):
    latest_poll = poll_collection.find_one(sort=[("id", -1)])
    if latest_poll:
        print("find last poll: ", latest_poll)
        return latest_poll["id"] + 1
    else:
        print("no poll found")
        return 1


@main.route("/create-poll", methods=["GET", "POST"])
def create_poll():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        options = request.form["options"]
        author = request.form["author"]
        age = int(request.form["age"])

        poll_collection = dsci551db.dsci551.polls
        poll = {
            "id": get_next_id(poll_collection),
            "title": title,
            "description": description,
            "options": options.splitlines(),
            "votes": [0] * len(options.splitlines()),
            "author": author,
        }
        poll_collection.insert_one(poll)

        user_collection = dsci551db.dsci551.users
        user_collection.insert_one({"name": author, "age": age})

        return redirect(url_for("main.view_polls"))
    return render_template("create_poll.html")


@main.route("/view-polls")
def view_polls():
    poll_collection = dsci551db.dsci551.polls
    polls = []
    for x in poll_collection.find():
        polls.append(x)
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


@main.route("/query", methods=["GET", "POST"])
def query_database():
    if request.method == "POST":
        order_by = request.form["orderBy"]
        limit_to_first = int(request.form["limitToFirst"])

        if order_by and limit_to_first:
            user_collection = dsci551db.dsci551.users
            users = user_collection.find().sort(order_by).limit(limit_to_first)
            return render_template("results.html", users=users)
        else:
            flash("Please provide both 'Order By' and 'Limit To First' values")
            return redirect(url_for("main.query_database"))

    return render_template("query.html")


@main.route("/login")
def login():
    return render_template("login.html")


@main.route("/create-user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        name = request.form["name"]
        age = int(request.form["age"])

        if not name or not age:
            flash("Please provide both a name and age")
            return redirect(url_for("main.create_user"))

        user_collection = dsci551db.dsci551.users
        user_collection.insert_one({"name": name, "age": age})
        flash("User created successfully")
        return redirect(url_for("main.create_user"))

    return render_template("create_user.html")


@main.route("/create-account", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        # handle GET request
        return render_template("create_account.html")

    elif request.method == "POST":
        # handle POST request
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            flash("Please provide both a username and password")
            return redirect(url_for("create_account"))
        if db.users.find_one({"username": username}):
            flash("Username already exists")
            return redirect(url_for("create_account"))
        db.users.insert_one({"username": username, "password": password})
        flash("Account created successfully")
        return redirect(url_for("login"))

    else:
        # handle other methods
        return "Method not allowed"


app = Flask(__name__)
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
