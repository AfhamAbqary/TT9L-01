from flask import Blueprint, render_template, request, session, redirect, url_for
from pocketbase import PocketBase 
from pocketbase.client import FileUpload
from ..extensions import client

quiz_bp = Blueprint("quiz", __name__, static_folder="", template_folder="templates")

@quiz_bp.route("/", methods=["POST", "GET"])
def home():
    if client.auth_store.base_model is not None:
        userdata = client.auth_store.base_model
        classes = [client.collection("Class").get_one(f"{i}") for i in userdata.classes]
        for i in classes:
            print(i)
        return render_template("quiz.html", quiz=classes)
    else:
        return "<h1>PLEASE LOG IN</h1>"

@quiz_bp.route("/<classid>", methods=['POST', 'GET'])
def quizpage(classid):
    class_data = client.collection("Class").get_one(classid) #fetch data
    
    # render quizpage
    #return render_template("quizpage.html", class_data=class_data)

    #test without fetching database
    return render_template("quizpage2.html", class_data=class_data)
