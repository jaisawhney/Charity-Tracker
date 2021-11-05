from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
import os

app = Flask(__name__)

host = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/Charity-tracker")
client = MongoClient(host=host)
db = client.get_default_database()

users = db.users
donations = db.donations
charities = db.charities

app = Flask(__name__)


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login_submit():
    return redirect(url_for("index"))


@app.route("/register", methods=["POST"])
def signup_submit():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
