from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Project(db.Model):
    name = db.Column(db.String(150))
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    subject = db.Column(db.String(150))
    notebook = db.Column(db.Integer)
    todo = db.Column(db.Integer)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    pictureData = db.Column(db.LargeBinary)

class Friend(db.Model):
    name = db.Column(db.String(150))
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    friendId = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userId = db.Column(db.Integer)