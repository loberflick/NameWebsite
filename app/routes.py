from app import app
from flask import render_template, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy # no more boring old SQL for us! *_*
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "pizza.db")
app.secret_key = 'supersecretkey'
WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'evenmoresecretkey'
db.init_app(app)

import app.models as models
from app.forms import Add_Pizza

@app.route("/")
def all_pizzas():
    # conn = sqlite3.connect('pizza.db')
    # cur = conn.cursor()
    # cur.execute('SELECT * FROM Pizza')
    # pizzas = cur.fetchall()

    pizzas = models.Pizza.query.all()
    return render_template("all_pizzas.html", pizzas=pizzas)


@app.route("/pizza/<int:id>")
def Pizza(id):
    pizza = models.Pizza.query.filter_by(id=id).first()
    return render_template('pizza.html', pizza=pizza)

@app.route('/add_pizza', methods = ["GET", "POST"])
def add_pizza():
    form = Add_Pizza()
    if request.method == "GET":
        new_pizza = models.Base()
        form.base.choices = models.Base.query.all()
        return render_template("add_pizza.html", form=form)
    else:
        if form.validate_on_submit():
            new_pizza = models.Pizza()
            new_pizza.name = form.name.data
            new_pizza.description = form.description.data
            new_pizza.base = form.base.data
            db.session.add(new_pizza)
            db.session.commit
            return redirect(url_for('pizza', id=new_pizza.id))
        else:
            return render_template("add_pizza.html", form=form)

    pass