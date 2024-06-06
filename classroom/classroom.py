from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client, ckeditor
from datetime import date

classroom_bp = Blueprint("classroom", __name__)

@classroom_bp.route("/",  methods=['POST', 'GET'])
def home():
    if client.auth_store.base_model != None:
        userdata = client.auth_store.base_model
        print(userdata.teacher, userdata.id)
        if userdata.teacher:
            classes= client.collection("Class").get_full_list(query_params={
                'filter': f'Teachers.id~"{userdata.id}"'
            })
        else:
            classes= client.collection("Class").get_full_list(query_params={
                'filter': f'Students.id?~"{userdata.id}"'
            })
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
                        client.collection('users').update(userdata.id, {
                            "Classes+": newclass.id
                        })
                    except Exception as e:
                        for i in e.__dict__["data"]["data"]:
                            print(f'{i}:' + e.__dict__["data"]["data"][i]["message"])

                elif 'leave' in request.form:
                    id = request.form['leave']
                    client.collection("users").update( userdata.id, {
                                    'Classes-': id
                                    })
                    
                    #for i in client.collection("Class").get_one(id).students:
                    #    classes = client.collection("users").get_one(i).classes
                    #    client.collection("users").update( i, {
                    #                   'Classes': classesid
                    #                   })
                    client.collection('Class').delete(id)
            else:
                if 'leave' in request.form:
                    id = request.form['leave']
                    client.collection("users").update( userdata.id, {
                                    'Classes-': id
                                    })
                    client.collection('Class').update(id, {
                            'Students-': userdata.id
                        })
                elif 'join' in request.form:
                    try:
                        client.collection('users').update(userdata.id, {
                                "Classes+": title
                        })
                        client.collection('Class').update(title, {
                            'Students+': userdata.id
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
    try:
        posts = client.collection('posts').get_full_list(query_params={
            "filter" : f'Owner.id="{classid}"',
            "sort": '-created'
        })
        userList = client.collection("users").get_full_list(query_params={
        'filter': f'Classes.id?="{classid}" && Teacher=false'
        })
        name = client.collection("Class").get_one(classid)
    except Exception as e:
        print(e.__dict__)
        #posts = {}
    userdata = client.auth_store.base_model
    if request.method == 'POST':
        if "create post" in request.form:
            title = request.form.get('title')
            data = request.form.get('ckeditor')
            client.collection("posts").create({
                "Title": title,
                "Text": data,
                "Url": "",
                "Owner": classid
            })
        elif "remove" in request.form:
            id = request.form['remove']
            print(id, classid)
            client.collection('Class').update(classid, {
                'Students-': id
            })
            client.collection("users").update(id, {
                'Classes-': classid
            })
        return redirect(url_for('classroom.classpage', classid = classid))
    return render_template('classpage.html', teacher=userdata.teacher, ClassName=name.title, post=posts, classid = classid, users=userList)

@classroom_bp.route("/<classid>/user")
def classusers(classid):
    return render_template('classuser.html')
    