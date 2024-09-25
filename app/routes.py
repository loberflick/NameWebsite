from app import app
from flask import render_template, request, redirect, make_response
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from random import choices
from string import ascii_letters, digits
from random import shuffle
from hashlib import sha256

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "classes.db")
app.config['SECRET_KEY'] = 'supersecretkey'
app.config["UPLOAD_FOLDER"] = 'static/images'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'evenmoresecretkey'
db.init_app(app)

# {"token": id}
login_sessions = {}
token_length = 16
# {id: quiz()}
current_quizzes = {}

overflow_lim = 9223372036854775807

hasher = sha256()


class Question():
    question_num = 0
    correct = 0

    option1 = ""
    picture1 = ""
    option2 = ""
    option3 = ""
    option4 = ""

    answer = ""

    def rand_ans(self):
        self.answer = choices(
            [self.option1,
                self.option2,
                self.option3,
                self.option],
            k=1)[0]


import app.models as models
from app.forms import Add_Account, Add_Class, Add_Student, Quiz


def check_overflow(num):
    if num > overflow_lim:
        return True
    else:
        return False


# Home Route
@app.route("/")
def home():
    user = find_login(request.cookies.get("login_token"))
    if user:
        classes = models.Class.query.filter_by(teacher=user)
        classes_length = 0
        for i in classes:
            classes_length += 1
        return render_template(
            "index.html",
            logedin=user,
            classes=classes,
            classes_length=classes_length)
    else:
        return redirect("/login")


# login to an account and store a cookie corresponding to the account
@app.route("/login", methods=["GET", "POST"])
def login():
    user = find_login(request.cookies.get("login_token"))
    form = Add_Account()
    valid_login = True
    if request.method == "POST":
        password = form.password.data
        accounts = models.Account.query.filter_by(username=form.username.data).first()
        print()
        if accounts is not None:
            hasher.update(password.encode(encoding="utf-8"))
            password = hasher.hexdigest()
            if str(password) == str(accounts.password):
                return sign_in(accounts)
            else:
                valid_login = False
        else:
            valid_login = False
    return render_template(
        "login.html",
        form=form,
        login=valid_login,
        logedin=user,
        accexist=False)


# Add a new account too the database
@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = Add_Account()
    acc_exist = False
    if request.method == "POST":
        if models.Account.query.filter_by(username=form.username.data).first() is None:
            # Create Account
            new_account = models.Account()
            new_account.username = form.username.data
            hasher.update(form.password.data.encode(encoding="utf-8"))
            new_account.password = hasher.hexdigest()
            db.session.add(new_account)
            db.session.commit()
            # Login
            return sign_in(new_account)
        else:
            acc_exist = True
    return render_template(
        "login.html",
        form=form,
        login=True,
        accexist=acc_exist)


def sign_in(account):
    gen_token = generate_token()
    resp = make_response(redirect("/"))
    resp.set_cookie("login_token", gen_token)
    login_sessions.update({gen_token: account.id})
    return resp


@app.route("/logout")
def logout():
    cookie = request.cookies.get("login_token")
    user = find_login(cookie)
    if user is None:
        return render_template("restricted.html", logedin=user)
    elif cookie in login_sessions:
        login_sessions.pop(cookie)
    return redirect("/")


# Generate a unique token and return it
def generate_token():
    token = choices(ascii_letters + digits, k=token_length)
    while str(token) in login_sessions:
        token = choices(ascii_letters + digits, k=token_length)
    return str("".join(token))


def find_login(token):
    id = login_sessions.get(token)
    if id is None:
        return False
    else:
        return id


@app.route("/add_class", methods=["GET", "POST"])
def add_class():
    form = Add_Class()
    user = find_login(request.cookies.get("login_token"))
    valid_file = True
    if user is None:
        return redirect("/login")
    elif request.method == "POST":
        f = form.picture.data
        filename, fileextension = os.path.splitext(f.filename)
        if fileextension == ".png" or fileextension == ".jpg":
            basedir = os.path.abspath(os.path.dirname(__file__))
            filepath = os.path.join(basedir, app.config["UPLOAD_FOLDER"] + '/class', secure_filename(str(user) + form.name.data + f.filename))
            f.save(filepath)

            new_class = models.Class()
            new_class.name = form.name.data
            new_class.description = form.description.data
            new_class.picture = "images/class/" + str(user) + form.name.data + f.filename
            new_class.teacher = user
            db.session.add(new_class)
            db.session.commit()
            return redirect("/")
        else:
            valid_file = False
    return render_template(
        "add_class.html",
        form=form,
        logedin=user,
        valid_file=valid_file)


@app.route('/classes')
def classes():
    user = find_login(request.cookies.get("login_token"))
    classes = models.Class.query.filter_by(teacher=user)
    return render_template('classes.html', logedin=user, classes=classes)


@app.route("/class/<int:id>", methods=["GET", "POST"])
def view_class(id):
    user = find_login(request.cookies.get("login_token"))
    if check_overflow(id):
        return render_template("restricted.html", logedin=user)
    form = Add_Student()
    quiz = current_quizzes.get(id)
    quiz_exist = False if quiz is None else True
    message = ""
    _class = models.Class.query.filter_by(id=id).first()
    if request.method == "GET":
        if _class is None or _class.teacher != user:
            return render_template("restricted.html", logedin=user)
        elif quiz_exist and quiz.question_num >= 10:
            current_quizzes.pop(id)
            quiz_exist = False
    elif request.method == "POST":
        if check_overflow(form.student_id.data):
            message += "Enter a lower student id "
        else:
            student = models.Student.query.filter_by(student_id=form.student_id.data).first()
            if student is None:
                f = form.picture.data
                filename, fileextension = os.path.splitext(f.filename)
                print(fileextension)
                if fileextension == ".png" or fileextension == ".jpg":
                    basedir = os.path.abspath(os.path.dirname(__file__))
                    filepath = os.path.join(basedir, app.config["UPLOAD_FOLDER"] + '/student', secure_filename(str(user) + _class.name + str(form.student_id.data) + fileextension))
                    f.save(filepath)
                    new_student = models.Student()
                    new_student.name = form.name.data
                    new_student.picture = "images/student/" + str(user) + _class.name + str(form.student_id.data) + fileextension
                    new_student.student_id = form.student_id.data
                    new_student.classes.append(_class)
                    db.session.add(new_student)
                    db.session.commit()
                else:
                    message += "Please use a valid file type "
            else:
                student.classes.append(_class)
                db.session.commit()
    return render_template(
        "class.html",
        message=message,
        logedin=user,
        _class=_class,
        form=form,
        id=id,
        quiz_exist=quiz_exist)


@app.route("/new_quiz/<int:id>/<int:new>/<int:correct>", methods=["GET", "POST"])
def new_quiz(id, new, correct):
    user = find_login(request.cookies.get("login_token"))
    if check_overflow(id):
        return render_template("overflow.html", logedin=user)
    elif user is None:
        return redirect("/login")
    _class = models.Class.query.filter_by(id=id).first()
    students = []
    for student in _class.students:
        students.append(student)
    shuffle(students)
    if request.method == "GET":
        quiz_exist = current_quizzes.get(id)
        if new == 1:
            new_quiz = Question()
        else:
            new_quiz = quiz_exist
            if correct == 1:
                new_quiz.correct += 1
            new_quiz.question_num += 1
        new_quiz.option1 = students[0].name
        new_quiz.option2 = students[1].name
        new_quiz.option3 = students[2].name
        new_quiz.option4 = students[3].name
        new_quiz.rand_ans()

        current_quizzes.update({id: new_quiz})
        return redirect("/quiz/1/" + str(id))


@app.route("/quiz/1/<int:id>", methods=["GET", "POST"])
def quiz(id):
    user = find_login(request.cookies.get("login_token"))
    if user is None:
        return redirect("/login")
    if check_overflow(id):
        return render_template("overflow.html", logedin=user)
    form = Quiz()
    _class = models.Class.query.filter_by(id=id).first()
    quiz = current_quizzes[id]
    form.guess.choices = [
        quiz.option1,
        quiz.option2,
        quiz.option3,
        quiz.option4]
    picture = ""
    correct = True
    answered = True
    for i in _class.students:
        if i.name == quiz.answer:
            picture = i.picture
    if request.method == "GET":
        if _class.teacher == user:
            pass
        else:
            return render_template("restricted.html", logedin=user)
        correct = False
        answered = False
    elif request.method == "POST":
        if form.guess.data != quiz.answer:
            correct = False
    return render_template(
        "quiz1.html",
        logedin=user,
        form=form,
        _class=_class,
        correct=correct,
        quiz=quiz,
        picture=picture,
        answered=answered)


@app.errorhandler(404)
def page_not_found(i):
    user = find_login(request.cookies.get("login_token"))
    return render_template("404.html", logedin=user), 404

# @app.errorhandler(6)
# def page_not_found(i):
#     user = find_login(request.cookies.get("login_token"))
#     return render_template("6.html", logedin=user), 6
