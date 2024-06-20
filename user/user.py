from flask import Blueprint, render_template, request, session, redirect, url_for
from pocketbase import PocketBase #MAKE SURE TO INSTALL Pocketbase BEFOREHAND
from pocketbase.client import FileUpload
from ..extensions import client, cipher

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def home():
    try:
        userdata = client.auth_store.base_model #Get user data from session saved
        username = userdata.username
        email = userdata.email
        teacher = "Teacher" if userdata.teacher else "Student"
        classes= [client.collection("Class").get_one(f"{i}").title for i in userdata.classes] #Get every classes registered for user
        return render_template("user.html", username=username, email=email, Teacher=teacher, Class=classes)
    except Exception as e:
        return render_template("user.html", username=e)
    

@user_bp.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        print(password)
        try:
            client.collection("users").auth_with_password(user, password) #Authorize login for data fetching and writing to database
            session["login"] = [user,cipher.encrypt(password)] #Save login info to session
            session["lasturl"] = "user.home"
            return redirect(url_for("user.home"))
        except Exception as e:
            print("Error:", e) #Prints error for message flashing later :TO DO
            return render_template("login.html")
    else:
        return render_template("login.html")

@user_bp.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        email = request.form['email'],
        password = request.form['password']
        passwordC = request.form['passwordC']
        name = request.form['name']
        print(password)
        try:
            client.collection("users").create(
                {
                    "username": user,
                    "email": email[0],
                    "password": password,
                    "passwordConfirm": passwordC,
                    "emailVisibility": False,
                    "name": name,
                    "Teacher": False,
                    "Class": []
                }
            )
            print("Success")
            session["lasturl"] = "user.home"
            return redirect(url_for("user.login"))
        except Exception as e:
            for i in e.__dict__["data"]["data"]:
                print(f'{i}:' + e.__dict__["data"]["data"][i]["message"])
            return render_template("signup.html")
    else:
        return render_template("signup.html")
    
@user_bp.route("/logout", methods=["POST","GET"])
def logout():
    client.auth_store.clear()
    session.pop("login", None)
    return render_template("logout.html")
    #return redirect(url_for(session["lasturl"]))