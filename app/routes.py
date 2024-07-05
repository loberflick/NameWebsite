from app import app
from flask import render_template, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from random import choices
from string import ascii_letters, digits



basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "classes.db")
app.secret_key = 'supersecretkey'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'evenmoresecretkey'
db.init_app(app)

# {"token": id}
login_sessions = {}
token_length = 16


import app.models as models
from app.forms import Add_Account

# Home Route
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Add_Account()
    if request.method == "GET":
        return render_template("login.html", form=form, login = True)
    else:
        password = form.password.data
        accounts = models.Account.query.filter_by(username=form.username.data).first()
        if str(password) == str(accounts.password):
            login_sessions.update({generate_token(): accounts.id}) 
            print(login_sessions)
            return redirect("/")
        else:
            return render_template("login.html", form=form, login=False)


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    print(request.method)
    form = Add_Account()
    if request.method == "GET":
        return render_template("login.html", form=form)
    else:
        new_account = models.Account()
        new_account.username = form.username.data
        new_account.password = form.password.data
        db.session.add(new_account)
        db.session.commit()
        return redirect("/")

def generate_token():
    token = choices(ascii_letters + digits, k=token_length)
    while str(token) in login_sessions:
        token = choices(ascii_letters + digits, k=token_length)
    return str("".join(token))



#@app.route('/add_pizza', methods = ["GET", "POST"])
#def add_pizza():
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