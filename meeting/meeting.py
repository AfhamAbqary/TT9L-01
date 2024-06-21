from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client

meet_bp = Blueprint("meet", __name__)

@meet_bp.route("/<postid>")
def join(postid):
    try:
        userdata = client.auth_store.base_model # Get data of current user
        return render_template('meetjoin.html', user=userdata) # Load HTML with userdata
    except Exception as e:
        return render_template("Error.html", error=e)