"""
Routes and views for the flask application.
"""
from flask import Flask
from datetime import datetime
from flask import render_template
from flask import request, session, redirect, url_for, render_template, flash, json, Response
#from forms import LoginForm, RegisterForm
import os 



courseData = [{"courseID":"1111","title":" Introduction to JavaScript","description":"Intro to JavaScript","term":"Fall, Spring"}, 
              {"courseID":"2222","title":"Java ","description":"Introduction to Java Programming","term":"Spring"}, 
              {"courseID":"3333","title":"Python","description":"Python Programming","term":"Fall"}, 
              {"courseID":"4444","title":"Angular ","description":"Intro to Angular","term":"Fall, Spring"},
              {"courseID":"5555","title":"Java ","description":"Advanced Java Programming","term":"Fall"}]

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'skills.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/playground')
def playground():
    """Renders the agent."""
    return render_template(
        'index.html',
        title='agent',
        year=datetime.now().year,
    )

@app.route("/signup", methods=['POST','GET'])
def register():
     return render_template(
        "signupcopy.html",
        title="Login", 
        login=True )
   
    
@app.route("/login", methods=['GET','POST'])
def login():
    return render_template(
    "logincopy.html",
    title="login", 
    login=True )


@app.route("/codecourses/")
@app.route("/codecourses/<term>")
def codecourses(term = None):
   
    term = "Winter 2019"
   
    return render_template("codecourses.html", courseData=courseData, courses = True, term=term )


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term = None):
    if term is None:
        term = "Winter 2019"
        return render_template("courses.html", courseData=classes, courses = True, term=term )


@app.route("/enrollment", methods=["GET","POST"])
def enrollment():
    courseID = request.form.get('courseID')
    title = request.form.get('title')
    user_id = 2

    if courseID and title:
        #Avoid duplicate enrollment
        if Enrollment.objects(user_id=user_id,courseID=courseID):
            flash(f"Sorry, you are already enrolled in the course {title}.","danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id,courseID=courseID).save()
            flash(f"You are enrolled in {title}.","success")

    classes = list(User.objects.aggregate(*[
            {

                '$lookup': {
                    'from': 'enrollment', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.courseID', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))

    return render_template("enrollment.html", classes=classes, enrollment=True)    





@app.route("/api/")
@app.route("/api/<idx>")
def api(idx=None):
    if(idx == None):
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    
    return Response(json.dumps(jdata), mimetype="application/json")

if __name__ == "__main__":
	env = os.environ.get('APP_ENV', 'development')
	port = int(os.environ.get('PORT', 8000))
	debug = False if env == 'production' else True
	app.run(host='0.0.0.0', port=port, debug=debug)