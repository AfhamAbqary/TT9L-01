from flask import Blueprint, render_template, request, session, redirect, url_for
from pocketbase import PocketBase 
from pocketbase.client import FileUpload
from ..extensions import client

quiz_bp = Blueprint("quiz", __name__,)

@quiz_bp.route("/", methods=["POST", "GET"])
def home():
    try:
        quiz_classes = []
        userdata = client.auth_store.base_model
        if userdata.teacher:
            classes= client.collection("Class").get_full_list(query_params={
                'filter': f'Teachers.id~"{userdata.id}"'
            })
        else:
            classes= client.collection("Class").get_full_list(query_params={
                'filter': f'Students.id?~"{userdata.id}"'
            })
        for i in classes:
            quiz_classes.append({
                "id": i.id,
                "name": i.title,
                "visible": i.visible
            })
        return render_template("quiz.html", quiz=classes)
    except Exception as e:
        return render_template("Error.html", error=e)

@quiz_bp.route("/<classid>", methods=['POST', 'GET'])
def quizpage(classid):
    try:
        userdata = client.auth_store.base_model
        Quiz = client.collection("Quiz")
        Class_data = Quiz.get_one(classid)
        Visible = "Visible" if (Class_data.visible) else "Hidden"
        if userdata.id in Class_data.students:
            return redirect(url_for("quiz.resultquiz", classid=classid))
        else:
            if userdata.id in Class_data.students:
                return "<h1>Already Answered</h1>"
            Questions = client.collection("Questions").get_full_list(query_params={
                "filter" : f'Owner.id = "{classid}"',
                'sort': '+created'
            })

            for i in Questions:
                print(i)
                print(i.__dict__)
                print("\n")

            if request.method == "POST":

                if "change" in request.form:
                    if Class_data.visible:
                        Quiz.update(classid, {
                            "Visible": False
                        })
                    else:
                        Quiz.update(classid, {
                            "Visible": True
                        })

                if 'Add_Question' in request.form:
                    title = request.form.get('question_text')
                    classid2 = request.form.get('option1') 
                    classid3 = request.form.get('option2')
                    classid4 = request.form.get('option3')
                    classid5 = request.form.get('option4')
                    answer =  request.form.get('Correct_Answer')

                    client.collection("Questions").create({
                            "Title": title,
                            "Option1": classid2,
                            "Option2": classid3,
                            "Option3": classid4,
                            "Option4": classid5,
                            "Correct_Answer": answer, 
                            "Owner": classid
                    })

                    
                elif 'remove' in request.form:
                    question = request.form.get("remove")
                    client.collection('Questions').delete(question)
                    
                
                elif 'submit_button' in request.form:
                    if userdata.teacher:
                        return redirect(url_for("quiz.resultquiz", classid=classid))
                    else:
                        correct__answer = 0
                        
                        for i in Questions:      
                            user_answer = request.form[f'answer_{i.id}']
                            if user_answer.replace(" ","").upper() == i.correct__answer.replace(" ","").upper():
                                correct__answer += 1
                                client.collection("Questions").update(i.id,{
                                    "Correct_Students+": client.auth_store.base_model.id 
                                })
                            
                            else:
                                client.collection("Questions").update(i.id,{
                                    "Wrong_Students+": client.auth_store.base_model.id 
                                })

                        client.collection("Quiz").update(classid,{
                                    "Students+": client.auth_store.base_model.id 
                                })

                    return redirect(url_for("quiz.resultquiz", classid=classid))

                return redirect(url_for("quiz.quizpage", classid=classid))
            # render quizpage
            return render_template("quizpage.html", class_data=Questions, Class=Class_data, teacher=userdata.teacher, Visible=Visible)
    except Exception as e:
        return render_template("Error.html", error=e)

@quiz_bp.route("/<classid>/resultquiz", methods=['POST', 'GET'])
def resultquiz(classid):
    try:
        userdata = client.auth_store.base_model
        Quiz = client.collection("Quiz").get_one(classid, query_params={
            'expand': 'Students'
        })
        Student_data = []
        Questions = client.collection("Questions").get_full_list(query_params={
        "filter" : f'Owner.id ="{classid}"',
        'expand': 'Correct_Students, Wrong_Students'
        })
        correct_answer = 0
        wrong_answer = 0
        if userdata.teacher:
            Question_data = []

            for i in Questions:
                Question_data.append({
                    "name": i.title,
                    "Correct": len(i.correct__students),
                    "Wrong": len(i.wrong__students),
                    "Score": str((len(i.correct__students)/len(Quiz.students))*100).split(".")[0] + "%" if len(Quiz.students) != 0 else str(0) + "%"
                })

            try:
                for i in Quiz.expand["Students"]:
                    correct_answer = 0
                    wrong_answer = 0

                    for j in Questions:
                        if i.id in j.correct__students:
                            correct_answer += 1
                        else:
                            wrong_answer += 1

                    Student_data.append({
                        "id": i.id,
                        "name": i.username,
                        "correct_answer": correct_answer,
                        "wrong_answer": wrong_answer,
                        "score": str((correct_answer/len(Questions))*100).split(".")[0] + "%" if len(Questions) != 0 else str(0)
                    })
            except Exception as e:
                print(e)

            if request.method == "POST":
                if "clear" in request.form:
                    id = request.form['clear']
                    client.collection("Quiz").update(classid, {
                        "Students-": id
                    })
                    for i in Questions:
                        client.collection("Questions").update(i.id, {
                            "Correct_Students-": id,
                            "Wrong_Students-": id
                        })
                
                if "clearall" in request.form:
                    client.collection("Quiz").update(classid, {
                        "Students": []
                    })
                    for i in Questions:
                        client.collection("Questions").update(i.id, {
                            "Correct_Students": [],
                            "Wrong_Students": []
                        })

                return redirect(url_for("quiz.resultquiz", classid=classid))

            return render_template("resultquiz.html", Student_data=Student_data, teacher=True, Questions=Question_data)
        else:
            for i in Questions:
                if userdata.id in i.correct__students:
                    correct_answer += 1
                else:
                    wrong_answer += 1

            Student_data.append({
                    "name": userdata.name,
                    "correct_answer": correct_answer,
                    "wrong_answer": wrong_answer,
                    "score": str((correct_answer/len(Questions))*100).split(".")[0] + "%" if correct_answer != 0 else str(0) + "%"
            })
            return render_template("resultquiz.html", Student_data=Student_data, teacher=False)
    except Exception as e:
        return render_template("Error.html", error=e)

