from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client, ckeditor
from datetime import date

classroom_bp = Blueprint("classroom", __name__, static_folder="", template_folder="templates")

@classroom_bp.route("/",  methods=['POST', 'GET'])
def home():
    if client.auth_store.base_model != None:
        userdata = client.auth_store.base_model
        classes= [client.collection("Class").get_one(f"{i}") for i in userdata.classes]
        if request.method == 'POST':
            title = request.form.get('title')
            if userdata.teacher:
                try:
                    newclass = client.collection('Class').create(
                        {
                            "Title": title,
                            "field": {},
                            "Teachers": userdata.id,
                            "Students": [
                            ]
                        }   
                    )
                    oldclasses = userdata.classes
                    newclass = [newclass.id] + oldclasses
                    client.collection('users').update(userdata.id, {
                        "Classes": newclass
                    })
                except Exception as e:
                    for i in e.__dict__["data"]["data"]:
                        print(f'{i}:' + e.__dict__["data"]["data"][i]["message"])
            else:
                try:
                    client.collection('users').update(userdata.id, {
                            "Classes": userdata.classes + [title]
                    })
                except Exception as e:
                    print(e)
            return redirect(url_for("classroom.home"))
        return render_template("classroom.html", classroom=classes, teacher=userdata.teacher)
    else:
        return "<h1>UNDER CONSTRUCTION</h1>"
    
@classroom_bp.route("/<classid>", methods=['POST', 'GET'])
def classpage(classid):
    Class= client.collection("Class").get_one(classid)
    userdata = client.auth_store.base_model
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
    return render_template('classpage.html', teacher=userdata.teacher, ClassName=Class , Class=dict(reversed(list(Class.field.items()))))
    