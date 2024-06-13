from app.routes import db

PizzaTopping = db.Table('PizzaTopping', db.Column('pid', db.Integer, db.ForeignKey('Pizza.id')), db.Column('tid', db.Integer, db.ForeignKey('Topping.id')))

class Pizza(db.Model):
    __tablename__ = "Pizza"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text())
    description = db.Column(db.Text())
    
    base = db.Column(db.Integer, db.ForeignKey("Base.id"))
    base_desc = db.relationship('Base', backref = "pizza")

    toppings = db.relationship("Topping", secondary="PizzaTopping", back_populates="pizzas")

    def __repr__(self):
        return self.name

class Base(db.Model):
    __tablename__ = "Base"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text())

    def __repr__(self):
        return self.name


class Topping(db.Model):
    __tablename__ = "Topping"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text())

    pizzas = db.relationship("Pizza", secondary="PizzaTopping", back_populates="toppings")

    def __repr__(self):
        return self.name