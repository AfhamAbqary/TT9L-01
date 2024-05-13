from flask import Blueprint, render_template, request, session, redirect, url_for
from pocketbase import PocketBase #MAKE SURE TO INSTALL Pocketbase BEFOREHAND
from pocketbase.client import FileUpload
from ..extensions import client

classroom_bp = Blueprint("classroom", __name__, static_folder="", template_folder="templates")
client = PocketBase('https://alma-mater.pockethost.io')

@classroom_bp.route("/")
def home():
    if client.auth_store.base_model == None:
        client.collection("users").auth_with_password(session["login"][0], session["login"][1])
        userdata = client.auth_store.base_model
        classes= [client.collection("Class").get_one(f"{i}").title for i in userdata.classes]
        return render_template("classroom.html", classroom=classes)
    else:
        return "<h1>UNDER CONSTRUCTION</h1>"
    