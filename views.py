import pymongo

from flask import flash, render_template, redirect, url_for, request, escape, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from bson.objectid import ObjectId

from database import *
from flask import Blueprint

routes = Blueprint("routes", __name__)


def require_login(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        email = session.get("email")
        if not email or not users.find_one({"email": email}):
            session.pop("_flashes", None)
            flash("You must login to view that page!", "app_warning")
            return redirect(url_for("routes.login"))
        return function(*args, **kwargs)

    return wrapper


# Pages
@routes.route("/")
def index():
    return render_template("index.html")


@routes.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@routes.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("routes.login"))


@routes.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@routes.route("/login", methods=["POST"])
def login_submit():
    user = users.find_one({"email": request.form.get("email")})
    password = request.form.get("password")

    if not user or not check_password_hash(user["password"], password):
        flash("Incorrect login details!", "app_warning")
        return redirect(url_for("routes.login"))
    session["email"] = user.get("email")
    return redirect(url_for("routes.view_dashboard"))


@routes.route("/dashboard", methods=["GET"])
@require_login
def view_dashboard():
    user = users.find_one({"email": session.get("email")})
    user_donations = donations.find({"donor_id": user["_id"]}).sort("created_on", pymongo.DESCENDING)
    donation_info_cursor = donations.aggregate([{"$match": {"donor_id": user["_id"]}},
                                                {"$group": {"_id": None,
                                                            "total_given": {"$sum": "$amount_given"},
                                                            "total_donations": {"$sum": 1}}},
                                                {"$limit": 1}])
    donation_info_list = list(donation_info_cursor)
    donation_info = donation_info_list[0] if len(donation_info_list) != 0 else None
    return render_template("dashboard.html", user=user, donations=user_donations, donation_info=donation_info)


# Users
@routes.route("/users", methods=["GET"])
def get_users():
    return redirect(url_for("routes.index"))


@routes.route("/users", methods=["POST"])
def create_user():
    first_name = escape(request.form.get("first_name"))
    last_name = escape(request.form.get("last_name"))
    email = escape(request.form.get("email"))
    password = request.form.get("password")

    if not first_name or not last_name or not email or not password:
        flash("One or more required fields were missing!", "app_warning")
        return redirect(url_for("routes.signup"))

    if users.find_one({"email": email}):
        flash("That email already exists!", "app_warning")
        return redirect(url_for("routes.signup"))

    password_hash = generate_password_hash(password)
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password_hash
    }
    users.insert_one(user)
    return redirect(url_for("routes.login"))


# @routes.route("/users/<string:user_id>", methods=["DELETE"])
# def delete_user(user_id):
#    pass


# Donations
# @routes.route("/donations", methods=["GET"])
# def get_donations():
#    pass


@routes.route("/donations/new", methods=["GET"])
@require_login
def new_donation():
    return render_template("log_donation.html")


@routes.route("/donations", methods=["POST"])
@require_login
def create_donation():
    user = users.find_one({"email": session.get("email")})
    charity_name = request.form.get("charity_name")
    created_on = request.form.get("date_given")
    amount_given = request.form.get("amount_given")

    if not charity_name or not amount_given or not created_on:
        flash("One or more required fields were missing!", "app_warning")
        return redirect(url_for("routes.new_donation"))

    try:
        float(amount_given)
    except ValueError:
        flash("Invalid amount!", "app_warning")
        return redirect(url_for("routes.new_donation"))

    donation = {
        "donor_id": user["_id"],
        "charity_id": charity_name,
        "amount_given": float(amount_given),
        "created_on": created_on
    }
    donations.insert_one(donation)
    return redirect(url_for("routes.view_dashboard"))


@routes.route("/donations/<string:donation_id>", methods=["DELETE"])
@require_login
def delete_donation(donation_id):
    user = users.find_one({"email": session.get("email")})
    donations.remove({"_id": ObjectId(donation_id), "donor_id": user["_id"]})
    return "Donation deleted", 200
