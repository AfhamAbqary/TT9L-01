from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client, cipher

user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def home():
    try:
        # Get current user data and pass along to variables
        userdata = client.auth_store.base_model 
        username = userdata.username
        email = userdata.email
        teacher = "Teacher" if userdata.teacher else "Student"

        if userdata.teacher: # Check if user is a teacher or student
            classes= client.collection("Class").get_full_list(query_params={ # Get list of class of user
                'filter': f'Teachers.id~"{userdata.id}"'
            })

        else:
            classes= client.collection("Class").get_full_list(query_params={  # Get list of class of user
                'filter': f'Students.id?~"{userdata.id}"'
            })

        return render_template("user.html", username=username, email=email, Teacher=teacher, Class=classes) # Pass data to HTML
    except Exception as e:
        return render_template("user.html", username=e)
    

@user_bp.route("/login", methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'POST': # POST request from HTML
            # Get data from forms
            user = request.form['username']
            password = request.form['password']

            try:
                client.collection("users").auth_with_password(user, password) #Authorize login for data fetching and writing to database
                session["login"] = [user,cipher.encrypt(password)] #Save login info to session
                return redirect(url_for("user.home")) # Redirect to user profile
            
            except Exception as e:
                print("Error:", e) 
                return render_template("login.html")
            
        else:
            return render_template("login.html")
        
    except Exception as e:
        return render_template("Error.html", error=e)

@user_bp.route("/signup", methods=["POST","GET"])
def signup():
    try:
        if request.method == 'POST': # POST request from HTML
            # Get data from forms
            user = request.form['username']
            email = request.form['email']
            password = request.form['password']
            passwordC = request.form['passwordC']
            name = request.form['name']

            try:
                client.collection("users").create( # Create user from data 
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
                
                return redirect(url_for("user.login")) # Redirect to login page
            
            except Exception as e:
                for i in e.__dict__["data"]["data"]:
                    print(f'{i}:' + e.__dict__["data"]["data"][i]["message"])

                return render_template("signup.html") # Redirect to Sign Up page again if error
            
        else:
            return render_template("signup.html")
        
    except Exception as e:
        return render_template("Error.html", error=e)
    
@user_bp.route("/logout")
def logout():
    try:
        client.auth_store.clear() # clear user login
        session.pop("login", None) # Remove user data from session
        return redirect(url_for("home.home")) # Redirect to main home page
    
    except Exception as e:
        return render_template("Error.html", error=e)
    #return redirect(url_for(session["lasturl"]))

@user_bp.route("/change", methods=["POST","GET"])
def change():
    try:
        if request.method == "POST": # POST request from HTML
            # Get data from forms
            userdata = client.auth_store.base_model
            username = request.form.get("Username")
            new_password = request.form.get("new-password")
            password = request.form.get("password")
            confirm_password = request.form.get("repeat-password")
            email = userdata.email

            if new_password and confirm_password: # Check if user want to change password
                client.collection("users").update(userdata.id, {# Update new & password
                    "password": new_password, 
                    "passwordConfirm": confirm_password,
                    "oldPassword": password
                })

            elif username: # Check if user want to change username
                client.collection("users").update(userdata.id, { # Update new username
                    "username": username
                })

            elif new_password and confirm_password and username: # Check if user want to username & password
                client.collection("users").update(userdata.id, { # Update new username & password
                    "username": username,
                    "password": new_password,
                    "passwordConfirm": confirm_password,
                    "oldPassword": password
                })

            client.auth_store.clear() # Clear user login
            session.pop("login", None) # Remove user data from session
            
            if new_password: # Check if new password is registered
                client.collection("users").auth_with_password(email, new_password) # Login with new password
                session["login"] = [email,cipher.encrypt(new_password)] # Save login info to session

            else: # Check if no new password registered
                client.collection("users").auth_with_password(email, password) # Login with password
                session["login"] = [email,cipher.encrypt(password)]  # Save login info to session

            return redirect(url_for("user.home")) # redirect to profile page
        return render_template("loginchange.html") # Load change HTML page
    except Exception as e:
        return render_template("Error.html", error=e)

