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
    start_time = IntegerField("Start Time", validators=[DataRequired()])
    end_time = IntegerField("End Time", validators=[DataRequired()])
    interval = IntegerField("Interval", validators=[DataRequired()])
    submit = SubmitField("Create")