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


# Pages
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


# Users
@app.route("/users", methods=["GET"])
def get_users():
    return redirect(url_for("index"))


@app.route("/users", methods=["POST"])
def create_user():
    password = request.form.get("password")
    user = {
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "password": password
    }
    print(user)
    return redirect(url_for("index"))


@app.route("/users/:id", methods=["DELETE"])
def delete_user():
    return redirect(url_for("index"))


# Donations
@app.route("/donations", methods=["GET"])
def get_donations():
    return redirect(url_for("index"))


@app.route("/donations/new", methods=["GET"])
def new_donation():
    return render_template("new_donation.html")


@app.route("/donations", methods=["POST"])
def create_donation():
    donation = {
        "donor_id": "",
        "charity_id": request.form.get("charity_id"),
        "amount_given": request.form.get("amount_given"),
        "created_on": request.form.get("date_given")
    }
    # donations.insert_one(donation)
    return redirect(url_for("index"))


# Charities
@app.route("/charities", methods=["GET"])
def get_charities():
    return redirect(url_for("index"))


@app.route("/charities/", methods=["POST"])
def create_charity():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
