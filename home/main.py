from flask import Flask, Blueprint, session, render_template, redirect, url_for
from ..extensions import client

home_bp = Blueprint("home", __name__)

@home_bp.route("/") #Home page
def home():
    try:
        if client.auth_store.base_model != None:
            login = True
            userdata = client.auth_store.base_model
            if userdata.teacher:
                classes= client.collection("Class").get_full_list(query_params={
                    'filter': f'Teachers.id~"{userdata.id}"'
                })
            else:
                classes= client.collection("Class").get_full_list(query_params={
                    'filter': f'Students.id?~"{userdata.id}"'
                })

            return render_template("index.html", classroom=classes, name=userdata.username, login=login)
        else:
            login = False
            return render_template("index.html", login=login)
    except Exception as e:
        return render_template("Error.html", error=e)
