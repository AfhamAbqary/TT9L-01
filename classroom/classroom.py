from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client, ckeditor
from datetime import date

classroom_bp = Blueprint("classroom", __name__)

@classroom_bp.route("/",  methods=['POST', 'GET'])
def home():
    if client.auth_store.base_model != None:
        userdata = client.collection("users").get_one( client.auth_store.base_model.id )
        classes= [client.collection("Class").get_one(i) for i in userdata.classes]
        classesid = list(userdata.classes)
        print(classesid)

        if request.method == 'POST':
            title = request.form.get('title')
            if userdata.teacher:
                if 'create' in request.form:
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

                elif 'leave' in request.form:
                    id = request.form['leave']
                    classesid.remove(id)
                    print('Classes: ', classesid)
                    client.collection("users").update( userdata.id, {
                                    'Classes': classesid
                                    })
                    
                    for i in client.collection("Class").get_one(id).students:
                        classes = client.collection("users").get_one(i).classes
                        client.collection("users").update( i, {
                                       'Classes': classesid
                                       })
                    client.collection('Class').delete(id)
            else:
                if 'leave' in request.form:
                    id = request.form['leave']
                    classesid.remove(id)
                    client.collection("users").update( userdata.id, {
                                    'Classes': classesid
                                    })
                elif 'join' in request.form:
                    try:
                        classesid.append(title)
                        client.collection('users').update(userdata.id, {
                                "Classes": classesid
                        })

                    except Exception as e:
                        for i in e.__dict__["data"]["data"]:
                            print(f'{i}:' + e.__dict__["data"]["data"][i]["message"])
                        
            return redirect(url_for("classroom.home"))
        return render_template("classroom.html", classroom=classes, teacher=userdata.teacher)
    else:
        return "<h1>UNDER CONSTRUCTION</h1>"
    
@classroom_bp.route("/<classid>", methods=['POST', 'GET'])
def classpage(classid):
    Class= client.collection("Class").get_one(classid)
    userdata = client.auth_store.base_model
    if request.method == 'POST':
        print(request.form['create post'])
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
        data = {
            'field': field
        }
        client.collection('Class').update(classid, data)
        return redirect(url_for('classroom.classpage', classid = classid))
    return render_template('classpage.html', teacher=userdata.teacher, ClassName=Class , Class=dict(reversed(list(Class.field.items()))))
    