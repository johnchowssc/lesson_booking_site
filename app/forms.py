from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TimeField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired 
from datetime import datetime

## Configure forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SlotForm(FlaskForm):
    date = DateField("Slot Date", format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    time = TimeField("Slot Time", format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    submit = SubmitField("Create")

class BookingForm(FlaskForm):
    date = DateField("Slot Date", format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    time = TimeField("Slot Time", format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    comment = TextAreaField("Comment", validators=[])
    paid = BooleanField("Paid", default=False, validators=[])
    completed = BooleanField("Completed", default=False, validators=[])
    submit = SubmitField("Book")

class RegisterUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class SlotsForm(FlaskForm):
    date = DateField("Slot Date", format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    start_time = SelectField("Start Time (24H)", choices=range(24), validators=[DataRequired()])
    end_time = SelectField("End Time (24H)", choices=range(24), validators=[DataRequired()])
    interval = SelectField("Interval (Hours)", choices=range(1,5), validators=[DataRequired()])
    submit = SubmitField("Create")

class ClassForm(FlaskForm):
    date = DateField("Slot Date", format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    time = TimeField("Slot Time", format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    class_name = StringField("Class Name", validators=[])
    class_description = TextAreaField("Description", validators=[])
    capacity = IntegerField("Class Capacity", default=6, validators=[DataRequired()])
    submit = SubmitField("Create")

class BookingClassForm(FlaskForm):
    name = StringField("Student Name", validators=[DataRequired()])
    email = StringField("Student Email", validators=[DataRequired()])
    mobile = StringField("Student Mobile", validators=[DataRequired()])
    submit = SubmitField("Add Student")