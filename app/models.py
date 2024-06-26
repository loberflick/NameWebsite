from app.routes import db

# PizzaTopping = db.Table('PizzaTopping', db.Column('pid', db.Integer, db.ForeignKey('Pizza.id')), db.Column('tid', db.Integer, db.ForeignKey('Topping.id')))

class Account(db.Model):
    __tablename__ = "Teacher_Account"
    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.Text())
    password = db.Column(db.Text())

    def __repr__(self):
        return self.password

#class Base(db.Model):
#    __tablename__ = "Base"
#    id = db.Column(db.Integer, primary_key = True)
#    name = db.Column(db.Text())
#
#    def __repr__(self):
#        return self.name
#
#
#class Topping(db.Model):
#    __tablename__ = "Topping"
#    id = db.Column(db.Integer, primary_key = True)
#   name = db.Column(db.Text())
#
#    pizzas = db.relationship("Pizza", secondary="PizzaTopping", back_populates="toppings")
#
#    def __repr__(self):
#        return self.name