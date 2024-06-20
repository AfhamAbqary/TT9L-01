from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client, ckeditor
from datetime import date

classroom_bp = Blueprint("classroom", __name__)

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
    
@classroom_bp.route("/<classid>", methods=['POST', 'GET'])
def classpage(classid):
    Class= client.collection("Class").get_one(classid).field
    if request.method == 'POST':
        title = request.form.get('title')
        data = request.form.get('ckeditor')
        field2 = client.collection("Class").get_one(classid)
        field = { f'messages{len(field2.field)}' :{
            'date': {},
            'file': {},
            'title': title,
            'text': data
            }}
        field.update(field2.field)
        print(field)
        data = {
            'field': field
        }
        print(data)
        client.collection('Class').update(classid, data)
        return redirect(url_for('classroom.classpage', classid = classid))
    return render_template('classpage.html', Class=dict(reversed(list(Class.items()))))
    