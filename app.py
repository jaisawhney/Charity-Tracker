from flask import Flask, flash, render_template, redirect, url_for, request, escape, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from functools import wraps

import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

host = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/Charity-tracker")
client = MongoClient(host=host)
db = client.get_default_database()

users = db.users
donations = db.donations
charities = db.charities


def require_login(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        email = session.get("email")
        if not email or not users.find_one({"email": email}):
            flash("Login is needed to view that page!", "signin_error")
            return redirect(url_for("login"))
        return function(*args, **kwargs)

    return wrapper


# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login_submit():
    user = users.find_one({"email": request.form.get("email")})
    password = request.form.get("password")

    if not user or not check_password_hash(user["password"], password):
        flash("Incorrect login details!", "signup_error")
        return redirect(url_for("login"))
    session["email"] = user.get("email")
    return redirect(url_for("view_dashboard"))


@app.route("/dashboard", methods=["GET"])
@require_login
def view_dashboard():
    user = users.find_one({"email": session.get("email")})
    all_donations = donations.find({"donor_id": user["_id"]})
    donation_count = donations.count_documents({"donor_id": user["_id"]})
    return render_template("dashboard.html", user=user, donations=all_donations, donation_count=donation_count)


# Users
@app.route("/users", methods=["GET"])
def get_users():
    return redirect(url_for("index"))


@app.route("/users", methods=["POST"])
def create_user():
    first_name = escape(request.form.get("first_name"))
    last_name = escape(request.form.get("last_name"))
    email = escape(request.form.get("email"))
    password = request.form.get("password")

    if not first_name or not last_name or not email or not password:
        flash("One or more required fields were missing!", "signup_error")
        return redirect(url_for("signup"))

    if users.find_one({"email": email}):
        flash("That email already exists!", "signup_error")
        return redirect(url_for("signup"))

    password_hash = generate_password_hash(password)
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password_hash
    }
    users.insert_one(user)
    return redirect(url_for("login"))


@app.route("/users/:id", methods=["DELETE"])
def delete_user():
    return redirect(url_for("index"))


# Donations
@app.route("/donations", methods=["GET"])
def get_donations():
    return redirect(url_for("index"))


@app.route("/donations/new", methods=["GET"])
@require_login
def new_donation():
    return render_template("log_donation.html")


@app.route("/donations", methods=["POST"])
@require_login
def create_donation():
    user = users.find_one({"email": session.get("email")})
    donation = {
        "donor_id": user["_id"],
        "charity_id": request.form.get("charity_id"),
        "amount_given": request.form.get("amount_given"),
        "created_on": request.form.get("date_given")
    }
    donations.insert_one(donation)
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
