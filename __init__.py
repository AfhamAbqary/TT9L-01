from flask import Flask, render_template, session
from .home.main import home_bp
from .user.user import user_bp
from .classroom.classroom import classroom_bp
from .extensions import client, cipher, ckeditor

def create_app():
    app = Flask(__name__)

    app.secret_key = 'ALMA'
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'
    cipher.init_app(app)
    ckeditor.init_app(app)

    @app.before_request
    def load_database():
        if "login" in session and client.auth_store.base_model == None:
            client.collection("users").auth_with_password(session["login"][0], cipher.decrypt(session["login"][1]).decode())

    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(classroom_bp, url_prefix="/classroom")

    return app