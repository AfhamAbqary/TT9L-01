from flask import Flask, Blueprint, session, render_template, redirect, url_for
from ..extensions import client

home_bp = Blueprint("home", __name__, static_folder="", template_folder="templates")

@home_bp.route("/") #Home page
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return render_template("Error.html", error=e)
