from app import app
from flask import render_template, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "classes.db")
app.secret_key = 'supersecretkey'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'evenmoresecretkey'
db.init_app(app)

#import app.models as models
#from app.forms import Add_Pizza

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup")
def sign_up():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("index.html")

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