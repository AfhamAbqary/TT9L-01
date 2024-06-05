from flask import Flask, Blueprint, session, render_template

home_bp = Blueprint("home", __name__)

@home_bp.route("/") #Home page
def home():
    session["lasturl"] = "home"
    return render_template("index.html")
