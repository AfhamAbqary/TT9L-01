from flask import Blueprint, render_template, request, session, redirect, url_for
from ..extensions import client, ckeditor, FileUpload, random
from datetime import date

classroom_bp = Blueprint("classroom", __name__)

@classroom_bp.route("/",  methods=['POST', 'GET'])
def home():
    try:
        userdata = client.auth_store.base_model
        print(userdata.teacher, userdata.id)

        if userdata.teacher: #Get collection of classes based on if user is teacher or student
            classes= client.collection("Class").get_full_list(query_params={ # Get list of classes of user
                'filter': f'Teachers.id~"{userdata.id}"'
            })

        else:
            classes= client.collection("Class").get_full_list(query_params={ # Get list of classes of user
                'filter': f'Students.id?~"{userdata.id}"'
            })


        if request.method == 'POST': # POST request from HTML
            title = request.form.get('title') # Get input by user ( class id @ class name)

            if userdata.teacher:
                # Options for teacher
                if 'create' in request.form: # Create new classroom
                    try:
                        newclass = client.collection('Class').create( # Create class based on form data
                            {
                                "Title": title,
                                "field": {},
                                "Teachers": userdata.id,
                                "Students": [
                                ]
                            }   
                        )
                        client.collection('users').update(userdata.id, { # Add classes to user's list of class
                            "Classes+": newclass.id
                        })
                        client.collection('Quiz').create({ # Create quiz page for newly created class
                            "id": newclass.id,
                            "Name": str(title) + " Quiz",
                            "Owner": userdata.id,
                            "Visible": False,
                        })

                    except Exception as e:
                        for i in e.__dict__["data"]["data"]:
                            print(f'{i}:' + e.__dict__["data"]["data"][i]["message"])

                elif 'leave' in request.form: # Destroy classroom
                    id = request.form['leave'] # Get id of class that wants to be removed
                    client.collection("users").update( userdata.id, { # Remove class from user's list of class
                                    'Classes-': id
                                    })

                    client.collection('Class').delete(id) # Delete class instance from database
                    client.collection('Quiz').delete(id)  # Delete quiz instance from database

            else:
                # Options for students
                if 'leave' in request.form: # Leave from classroom
                    id = request.form['leave'] # Get id of class that wants to be removed
                    client.collection("users").update( userdata.id, { # Remove class from user's list of class
                                    'Classes-': id
                                    })
                    client.collection('Class').update(id, { # Remove user from class's list of students
                            'Students-': userdata.id
                        })
                    
                elif 'join' in request.form: # Join classroom using invite code
                    try:
                        client.collection('users').update(userdata.id, { # Add class to user's list of class
                                "Classes+": title
                        })
                        client.collection('Class').update(title, { # Add user to class's list of students
                            'Students+': userdata.id
                        })

                    except Exception as e:
                        for i in e.__dict__["data"]["data"]:
                            print(f'{i}:' + e.__dict__["data"]["data"][i]["message"])
                        
            return redirect(url_for("classroom.home")) # Redirect to main classroom page
        
        return render_template("classroom.html", classroom=classes, teacher=userdata.teacher) # Load HTML of classroom page
    except Exception as e:
        return render_template("Error.html", error=e)
    
@classroom_bp.route("/<classid>", methods=['POST', 'GET'])
def classpage(classid):
    try:
        posts = client.collection('posts').get_full_list(query_params={ # Get list of posts that is children of the class
            "filter" : f'Owner.id="{classid}"',
            "sort": '-created'
        })
        userList = client.collection("users").get_full_list(query_params={ # Get list of users that is in the class
        'filter': f'Classes.id?="{classid}" && Teacher=false'
        })
        name = client.collection("Class").get_one(classid) # Get info of class
        quiz = client.collection("Quiz").get_one(classid) # Get info of quiz
            #posts = {}
        userdata = client.auth_store.base_model # Get info of current user

        if request.method == 'POST': # POST request from HTML

            if "create post" in request.form: # Create new post in classroom
                # Get all data for to create a post
                title = request.form.get('title')
                data = request.form.get('ckeditor')
                files = request.files.getlist('file')
                meetConfirm = request.form.get('MeetConfirm')
                meetConfirm = random.randint(0,100000) if meetConfirm else None # Create meeting id | ranges from 0 to 100000
                formatedList = []

                for i in files: # Create formatted list for uploading
                    formatedList.append((i.filename, i))

                formated = ((i[0], i[1]) for i in formatedList) # Turn list into arguements for function
                client.collection("posts").create({ # Create posts using fetched data
                    "Title": title,
                    "Text": data,
                    "Image": FileUpload(*formated),
                    "MeetID": meetConfirm,
                    "Owner": classid
                })

            elif "remove" in request.form:  # Remove class from user's list
                id = request.form['remove'] # Get id of class to be removed
                client.collection('Class').update(classid, { # remove user from class's students list
                    'Students-': id 
                })
                client.collection("users").update(id, { # Remove class from from user's list of class
                    'Classes-': classid
                })

            elif "remove post" in request.form: # Remove post from classroom
                id = request.form['remove post'] # Get id of post to be removed
                client.collection("posts").delete(id) # Delete post using its id

            return redirect(url_for('classroom.classpage', classid = classid)) #redirect to classroom page
        
        return render_template('classpage.html', teacher=userdata.teacher, Visible=quiz.visible, ClassName=name.title, post=posts, classid = classid, users=userList)
    except Exception as e:
        return render_template("Error.html", error=e)

@classroom_bp.route("/<classid>/<postid>", methods=['POST', 'GET'])
def postpage(classid, postid):
    try:
        info = client.collection("posts").get_one(postid) # Get post by id
        comments = client.collection("comments").get_full_list(query_params={ # Get list of comments of post
            'filter': f'Owner.id="{postid}"',
            "sort": '+created',
            'expand': 'Poster'
        })

        comments_filter = []

        for i in comments: # Format comments to display on HTML
            for j in [i.expand['Poster']]:
                if i.poster == j.id:
                    comments_filter.append(((j.id, j.username, i.message)))

        urls_for_file = []

        for i in info.image: # Get files of post and format it for HTML
            url = client.get_file_url(info, i, {})
            urls_for_file.append((i, url))
            
        if request.method == 'POST': # POST request from HTML

            if "comment" in request.form: # If user submitted a comment
                comment = request.form.get("comment-text") # Get comment
                client.collection('comments').create({ # Create comment as a child of post on database
                    "Owner": postid,
                    "Poster": client.auth_store.base_model.id,
                    "message": comment
                })

            # Pass data to html
            return redirect(url_for("classroom.postpage", classid=classid, postid=postid ,post=info, Urls=urls_for_file, comments=comments_filter, userid=client.auth_store.base_model.id))
        
        return render_template('classpost.html', post=info, Urls=urls_for_file, comments=comments_filter, userid=client.auth_store.base_model.id)
    
    except Exception as e:
        return render_template("Error.html", error=e)

@classroom_bp.route("/<postid>/meeting")
def join(postid):
    try:
        post = client.collection("posts").get_one(postid) # Get data of post by id
        userdata = client.auth_store.base_model # Get data of current user

        return render_template('meetjoin.html', user=userdata, post=post) # Pass data to html
    except Exception as e:
        return render_template("Error.html", error=e)
