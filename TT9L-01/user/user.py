from flask import *
from pocketbase import PocketBase #MAKE SURE TO INSTALL Pocketbase BEFOREHAND
from pocketbase.client import FileUpload

user = Blueprint("user", __name__, static_folder="", template_folder="templates")
client = PocketBase('https://alma-mater.pockethost.io')

@user.route("/")
def home():
    return "<h1>UNDER CONSTRUCTION</h1>"

@user.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        try:
            client.collection("users").auth_with_password(user, password)
            return redirect(url_for(user))
        except:
            print("Information wrong")
            return render_template("login.html")
    else:
        return render_template("login.html")

@user.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        email = request.form['email'],
        password = request.form['password']
        passwordC = request.form['passwordC']
        name = request.form['name']
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
            return redirect(url_for("user.home"))
        except:
            print("Something went wrong!")
            return render_template("signup.html")
    else:
        return render_template("signup.html")