from flask import Blueprint, render_template, request, session, redirect, url_for
from pocketbase import PocketBase 
from pocketbase.client import FileUpload
from ..extensions import client

quiz_bp = Blueprint("quiz", __name__, static_folder="", template_folder="website")

@quiz_bp.route("/")
def home():
    if client.auth_store.base_model != None:
        userdata = client.auth_store.base_model
        classes= [client.collection("Class").get_one(f"{i}").title for i in userdata.classes]
        return render_template("quiz.html", quiz=classes)
    else:
        return "<h1>UNDER CONSTRUCTION</h1>"