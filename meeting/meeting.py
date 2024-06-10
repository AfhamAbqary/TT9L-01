from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client

meet_bp = Blueprint("meet", __name__)

@meet_bp.route("/<postid>")
def join(postid):
    post = client.collection("posts").get_one(postid)
    print(postid)
    userdata = client.auth_store.base_model
    return render_template('meetjoin.html', user=userdata)