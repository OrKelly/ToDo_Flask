from datetime import datetime

from flask import current_app

from todo import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    image_file = db.Column(db.String(), nullable=False, default='default.jpg')
    todos = db.relationship('Todo', backref='creator', lazy=True)

class Todo(db.Model):

    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    body = db.Column(db.Text)
    date_of_create = db.Column(db.DateTime, nullable=False, default=datetime.now)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String, nullable=False, default='Начато')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
