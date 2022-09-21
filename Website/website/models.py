from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    gender = db.Column(db.String(150))
    birthday = db.Column(db.Date())
    password = db.Column(db.String(150))
    plan = db.Column(db.String(150))
