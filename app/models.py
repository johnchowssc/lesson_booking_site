from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    slots = db.relationship('Slot', backref='student', lazy='dynamic')

# Tells Python how to print objects of this class.
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Slot(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    name = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Slot {}>'.format(self.name)