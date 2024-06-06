from flask import Blueprint, render_template, request, session, redirect, url_for
from pocketbase import PocketBase 
from pocketbase.client import FileUpload
from ..extensions import client

quiz_bp = Blueprint("quiz", __name__, static_folder="", template_folder="templates")

@quiz_bp.route("/", methods=["POST", "GET"])
def home():
    if client.auth_store.base_model is not None:
        userdata = client.auth_store.base_model
        classes = [client.collection("Class").get_one(f"{i}") for i in userdata.classes]
        for i in classes:
            print(i)
        return render_template("quiz.html", quiz=classes)
    else:
        return "<h1>PLEASE LOG IN</h1>"

@quiz_bp.route("/<classid>", methods=['POST', 'GET'])
def quizpage(classid):
    class_data = client.collection("Questions").get_full_list(query_params={
    "filter": f"Owner.id='{classid}'"
    })
    #print(class_data)


    Questions = client.collection("Questions").get_full_list(query_params={
        "filter" : f'Owner.id = "{classid}"',
        'sort': '+created'
    })
    print(Questions)

    if request.method == "POST":
        title = request.form.get('question_text')
        classid2 = request.form.get('option1') 
        classid3 = request.form.get('option2')


        
        print("Title", title)
        print("option 1:", classid2)
        print("option 2:", classid3)
        print("Class ID", classid)

        client.collection("Questions").create({
                "Title": title,
                "Option1": classid2,
                "Option2": classid3,
                "Owner": classid
        })
        return redirect(url_for("quiz.quizpage", classid=classid))



    # render quizpage
    return render_template("quizpage.html", class_data=Questions)

    #test without fetching database
    #return render_template("quizpage2.html", class_data=class_data)
