from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login, app
from time import time
import jwt

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, unique=False, nullable=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    waiver_returned = db.Column(db.Boolean, default=False, nullable=True)
    slots = db.relationship('Slot', backref='student', lazy='dynamic')
    students = db.relationship('Student', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def make_admin(self):
        self.is_admin = True
    
    def remove_admin(self):
        self.is_admin = False

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    # Tells Python how to print objects of this class.
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Slot(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    name = db.Column(db.String(250), nullable=True)
    instructor = db.Column(db.String(250), nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    paid = db.Column(db.Boolean, default=False, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return '<Slot {}>'.format(self.name)

class ClassSlot(db.Model):
    __tablename__ = "class_slots"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    class_name = db.Column(db.String(250), nullable=True)
    class_description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=True)
    capacity = db.Column(db.Integer, default=6, nullable=True)
    students = db.relationship("Student")

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    mobile = db.Column(db.String(250), nullable=True)
    paid = db.Column(db.Boolean, default=False, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('class_slots.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
