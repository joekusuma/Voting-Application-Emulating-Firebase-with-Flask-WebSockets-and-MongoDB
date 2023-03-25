from flask import Blueprint, render_template

# from .extensions import mongo
from pymongo import MongoClient

main = Blueprint("main", __name__)

dsci551db = MongoClient(
    "mongodb+srv://dsci551:w8QBPtSfunya7Gy0@clusterdsci551.s85edni.mongodb.net/?retryWrites=true&w=majority"
)


@main.route("/")
def index():
    user_collection = dsci551db.dsci551.users
    user_collection.insert_one({"name": "Tiger", "age": 24})
    user_collection.insert_one({"name": "Joe", "age": 22})
    return "<h1>Added a User!</h1>"
    # return render_template("index.html")


@main.route("/find")
def find():
    user_collection = dsci551db.dsci551.users
    user = user_collection.find_one({"name": "Tiger"})
    return f"<h1>User: { user['name']} age: {user['age']}</h1>"
    # return render_template("index.html")


@main.route("/update")
def update():
    user_collection = dsci551db.dsci551.users
    filter = {"name": "Tiger"}
    newvalues = {"$set": {"age": 80}}
    user_collection.update_one(filter, newvalues)
    return "<h1>Updated User!</h1>"
    # return render_template("index.html")


@main.route("/delete")
def delete():
    user_collection = dsci551db.dsci551.users
    filter = {"name": "Tiger"}
    user_collection.delete_one(filter)
    return "<h1>Deleted User!</h1>"
    # return render_template("index.html")
