from flask import * #MAKE SURE TO INSTALL FLASK BEFOREHAND
#from flask_ckeditor import CKEditor
from pocketbase import PocketBase #MAKE SURE TO INSTALL Pocketbase BEFOREHAND
from pocketbase.client import FileUpload
from user.user import user

app = Flask(__name__)
app.register_blueprint(user, url_prefix="/user")

app.secret_key = "ALMA"

client = PocketBase('https://alma-mater.pockethost.io')

#https://tailwindcss.com/docs/installation THIS IS FOR STYLING, LOOK AT THIS WHEN YOU WANT TO STYLE YOUR WEBSITE

@app.route("/") #Home page
def home():
    session["lasturl"] = "home"
    return render_template("index.html")
    
if __name__ == "__main__":
    app.run(debug = True)
