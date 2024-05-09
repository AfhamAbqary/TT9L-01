from flask import *

app = Flask(__name__)

#https://tailwindcss.com/docs/installation

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

if __name__ == "__main__":
    app.run(debug=True)