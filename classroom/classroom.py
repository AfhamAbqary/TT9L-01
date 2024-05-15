from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client

classroom_bp = Blueprint("classroom", __name__, static_folder="", template_folder="templates")

@classroom_bp.route("/")
def home():
    if client.auth_store.base_model != None:
        userdata = client.auth_store.base_model
        classes= [client.collection("Class").get_one(f"{i}") for i in userdata.classes]
        for i in classes:
            print(i.id)
        print(classes)
        return render_template("classroom.html", classroom=classes)
    else:
        return "<h1>UNDER CONSTRUCTION</h1>"
    
@classroom_bp.route("/<classid>")
def classpage(classid):
    Class= client.collection("Class").get_one(classid).field
    for i in Class:
        print(Class[i]['text'])
    return render_template('classpage.html', Class=Class)
    