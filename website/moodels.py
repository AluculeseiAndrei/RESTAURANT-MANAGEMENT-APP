from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func



class User(db.Model,UserMixin):
    id =db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    tables=db.relationship('Table',backref='User')

class Table(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150))
    products=db.Column(db.String(1000))
    total=db.Column(db.Float)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))



class Admin_data(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    sells=db.Column(db.Integer)
    debts=db.Column(db.Integer)#19% of sells
    tips=db.Column(db.Integer)
    

