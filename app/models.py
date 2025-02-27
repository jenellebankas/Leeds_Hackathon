from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Task(db.Model):
    id  =  db.Column(db.Integer, primary_key = True)
    task_title = db.Column(db.String(50), nullable = False)
    task_description = db.Column(db.String(200), nullable = False)
    deadline_date = db.Column(db.DateTime, nullable = False)
    status = db.Column(db.Boolean, default = False)
    progress = db.Columnn(db.Integer, default = False)
    colour = db.Column(db.Boolean, default = False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)