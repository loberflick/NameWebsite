from app.routes import db
from sqlalchemy_utils import EncryptedType
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

encryption_key = urlsafe_b64encode(b"Supersecurekeynoonewilleverknow")

StudentClass = db.Table(
    'StudentClass',
    db.Column('sid', db.Integer, db.ForeignKey('Student.id')),
    db.Column('cid', db.Integer, db.ForeignKey('Class.id')))


class Account(db.Model):
    __tablename__ = "Teacher_Account"
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Text())
    password = db.Column(db.Text())

    def __repr__(self):
        return self


class Class(db.Model):
    __tablename__ = "Class"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(EncryptedType(db.Text(), encryption_key))
    description = db.Column(EncryptedType(db.Text(), encryption_key))
    picture = db.Column(EncryptedType(db.Text(), encryption_key))
    teacher = db.Column(db.Integer())

    students = db.relationship("Student", secondary="StudentClass", back_populates="classes")

    def __repr__(self):
        return self


class Student(db.Model):
    __tablename__ = "Student"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(EncryptedType(db.Text(), encryption_key))
    picture = db.Column(EncryptedType(db.Text(), encryption_key))
    student_id = db.Column(db.Text())

    classes = db.relationship("Class", secondary="StudentClass", back_populates="students")

    def __repr__(self):
        return self


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