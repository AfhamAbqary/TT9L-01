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
    Class_data = client.collection("Quiz").get_one(classid)
    Questions = client.collection("Questions").get_full_list(query_params={
        "filter" : f'Owner.id = "{classid}"',
        'sort': '+created'
    })
    print(Questions)


    if request.method == "POST":
        print(request.form)

        title = request.form.get('question_text')
        classid2 = request.form.get('option1') 
        classid3 = request.form.get('option2')
        classid4 = request.form.get('option3')
        classid5 = request.form.get('option4')
        answer =  request.form.get('Correct_Answer')
        
        if 'submit_button' in request.form:
            correct__answer = 0
            for i in Questions:
                user_answer=request.form[f'answer{i}']
                if user_answer == i.correct__answer:
                    print(True)
                    correct__answer += 1
                    client.collection("Questions").update(i.id,{
                        "Correct_Students+": client.auth_store.base_model.id 
                    })
                
                else:
                    print(False)
                    client.collection("Questions").update(i.id,{
                        "Wrong_Students+": client.auth_store.base_model.id 
                    })
            return redirect(url_for("quiz.quizpage", classid=classid))

            print(correct__answer)
          
    
        elif 'remove' in request.form:
            aish = request.form.get("remove")
            client.collection('Questions').delete(aish)
            return redirect(url_for("quiz.quizpage", classid=classid))

      
        elif "addquestion" in request.form:
            client.collection("Questions").create({
                "Title": title,
                "Option1": classid2,
                "Option2": classid3,
                "Option3": classid4,
                "Option4": classid5,
                "Correct_Answer": answer, 
                "Owner": classid

            }) 
        return redirect(url_for("quiz.quizpage", classid=classid))



    # render quizpage
    return render_template("quizpage.html", class_data=Questions, Class=Class_data)

@quiz_bp.route("/<classid>/resultquiz", methods=['POST', 'GET'])
def resultquiz(classid):
    Questions = client.collection("Questions").get_full_list(query_params={
        "filter" : f'Owner.id ="{classid}" && Correct_Students~"{client.auth_store.base_model.id }"'
    })
    print(Questions)
    return '<h1> correct ans</h1>' 
