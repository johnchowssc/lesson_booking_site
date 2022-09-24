from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, unique=False, nullable=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    lesson_passes = db.Column(db.Integer, default=0)
    class_passes = db.Column(db.Integer, default=0)
    slots = db.relationship('Slot', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def make_admin(self):
        self.is_admin = True
    
    def remove_admin(self):
        self.is_admin = False

    def check_lesson_passes(self):
        return self.lesson_passes
    
    def check_class_passes(self):
        return self.class_passes

    def add_lesson_passes(self, lessons):
        self.lesson_passes += lessons
    
    def remove_lesson_passes(self, lessons):
        self.lesson_passes -= lessons
    
    def add_class_passes(self, classes):
        self.class_passes += classes
    
    def remove_class_passes(self, classes):
        self.class_passes -= classes

    # Tells Python how to print objects of this class.
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Slot(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    name = db.Column(db.String(250), nullable=True)
    comment = db.Column(db.String(500), nullable=True)
    paid = db.Column(db.Boolean, default=False, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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
    students = db.relationship("Student")

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    paid = db.Column(db.Boolean, default=False, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('class_slots.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))