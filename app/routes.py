from app import app
from flask import render_template, abort, request, redirect, url_for, make_response 
from flask_sqlalchemy import SQLAlchemy
import os
from random import choices
from string import ascii_letters, digits
from random import shuffle

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "classes.db")
app.config['SECRET_KEY'] = 'supersecretkey'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'evenmoresecretkey'
db.init_app(app)

# {"token": id}
login_sessions = {}
token_length = 16
# {id: quiz()}
current_quizzes = {}


import app.models as models
from app.forms import Add_Account, Add_Class, Add_Student, Quiz


# Home Route
@app.route("/")
def home():
    return render_template("index.html", logedin=find_login(request.cookies.get("login_token")))


# login to an account and store a cookie corresponding to the account
@app.route("/login", methods=["GET", "POST"])
def login():
    print(request.cookies)
    form = Add_Account()
    if request.method == "GET":
        return render_template("login.html", form=form, login=True, logedin=find_login(request.cookies.get("login_token")))
    else:
        password = form.password.data
        accounts = models.Account.query.filter_by(username=form.username.data).first()
        if str(password) == str(accounts.password):
            gen_token = generate_token()
            resp = make_response(redirect("/"))
            resp.set_cookie("login_token", gen_token)
            login_sessions.update({gen_token: accounts.id})
            return resp
        else:
            return render_template("login.html", form=form, login=False)


# Add a new account too the database
@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    print(request.method)
    form = Add_Account()
    if request.method == "GET":
        return render_template("login.html", form=form, login=True)
    else:
        new_account = models.Account()
        new_account.username = form.username.data
        new_account.password = form.password.data
        db.session.add(new_account)
        db.session.commit()
        return redirect("/")


# Generate a unique token and return it
def generate_token():
    token = choices(ascii_letters + digits, k=token_length)
    while str(token) in login_sessions:
        token = choices(ascii_letters + digits, k=token_length)
    return str("".join(token))


def find_login(token):
    print(login_sessions)
    id = login_sessions.get(token)
    print(id, token)
    if id is None:
        return False
    else:
        return id


@app.route("/add_class", methods=["GET","POST"])
def add_class():
    form = Add_Class()
    if request.method == "GET":
        return render_template("add_class.html", form=form, logedin=find_login(request.cookies.get("login_token")))
    elif request.method == "POST":
        new_class = models.Class()
        new_class.name = form.name.data
        new_class.image = form.picture.data
        new_class.teacher = find_login(request.cookies.get("login_token"))
        db.session.add(new_class)
        db.session.commit()
        return redirect("/")
    return render_template("add_class.html", form=form, logedin=find_login(request.cookies.get("login_token")))


@app.route('/classes')
def classes():
    id = find_login(request.cookies.get("login_token"))
    classes = models.Class.query.filter_by(teacher=id)
    return render_template('classes.html', logedin=find_login(request.cookies.get("login_token")), classes=classes)


@app.route("/class/<int:id>", methods=["GET", "POST"])
def view_class(id):
    form = Add_Student()
    _class = models.Class.query.filter_by(id=id).first()
    if request.method == "GET":
        if _class.teacher == find_login(request.cookies.get("login_token")):
            pass
        else:
            return render_template("restricted.html", _class=_class,logedin=find_login(request.cookies.get("login_token")))
    elif request.method == "POST":
        print("new studetn")
        new_student = models.Student()
        new_student.name = form.name.data
        new_student.picture = form.picture.data
        new_student.student_id = form.student_id.data
        new_student.classes.append(_class)
        db.session.add(new_student)
        db.session.commit()
    return render_template("class.html", logedin=find_login(request.cookies.get("login_token")), _class=_class, form=form, id=id)


class Question():
    option1 = ""
    picture1 = ""
    option2 = ""
    picture2 = ""
    option3 = ""
    picture3 = ""
    option4 = ""
    picture4 = ""

    anwser = ""

    def rand_ans():
        anwser = choices([quiz.option1, quiz.option2, quiz.option3, quiz.option4])

@app.route("/new_quiz/<int:id>", methods=["GET", "POST"])
def new_quiz(id):
    _class = models.Class.query.filter_by(id=id).first()
    students = []
    for student in _class.students:
        print(student.name)
        students.append(student)
    shuffle(students)
    if request.method == "GET":
        new_quiz = Question()
        new_quiz.option1 = students[0].name
        new_quiz.option2 = students[1].name
        new_quiz.option3 = students[2].name
        new_quiz.option4 = students[3].name

        new_quiz.anwser = students[3].name

        current_quizzes.update({find_login(request.cookies.get("login_token")): new_quiz})
        return redirect("/quiz/1/" + str(id))


@app.route("/quiz/1/<int:id>", methods=["GET", "POST"])
def quiz(id):
    form = Quiz()
    _class = models.Class.query.filter_by(id=id).first()
    quiz = current_quizzes[find_login(request.cookies.get("login_token"))]
    if request.method == "GET":
        if _class.teacher == find_login(request.cookies.get("login_token")):
            pass
        else:
            return render_template("restricted.html", _class=_class, logedin=find_login(request.cookies.get("login_token")))
        for i in _class.students:
            print(i.name)
        form.guess.choices = [quiz.option1, quiz.option2, quiz.option3, quiz.option4]
        return render_template("quiz1.html", logedin=find_login(request.cookies.get("login_token")), form=form, _class=_class, correct=False)
    elif request.method == "POST":
        if form.guess.data == quiz.anwser:
            return render_template("quiz1.html", logedin=find_login(request.cookies.get("login_token")), form=form, _class=_class, correct=True)
        else:
            form.guess.choices = [quiz.option1, quiz.option2, quiz.option3, quiz.option4]
            return render_template("quiz1.html", logedin=find_login(request.cookies.get("login_token")), form=form, _class=_class, correct=False)
            


def quick_template(page, form):
    return render_template(page, form, logedin=find_login(request.cookies.get("login_token")))


# @app.route('/add_pizza', methods = ["GET", "POST"])
# def add_pizza():
#    form = Add_Pizza()
#    if request.method == "GET":
#        new_pizza = models.Base()
#        form.base.choices = models.Base.query.all()
#        return render_template("add_pizza.html", form=form)
#    else:
#        if form.validate_on_submit():
#            new_pizza = models.Pizza()
#            new_pizza.name = form.name.data
#            new_pizza.description = form.description.data
#            new_pizza.base = form.base.data
#            db.session.add(new_pizza)
#            db.session.commit
#            return redirect(url_for('pizza', id=new_pizza.id))
#        else:
#            return render_template("add_pizza.html", form=form)