from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TimeField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from datetime import datetime
import pytz

def get_sydney_now():
    sydney_tz = pytz.timezone('Australia/Sydney')
    return datetime.now(sydney_tz)

## Configure forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SlotForm(FlaskForm):
    date = DateField("Slot Date",format='%Y-%m-%d',default=lambda: get_sydney_now().date(),validators=[DataRequired()])
    time = TimeField("Slot Time", format='%H:%M',default=lambda: get_sydney_now().time(),validators=[DataRequired()])
    name = StringField("Name", validators=[])
    comment = TextAreaField("Comment", validators=[])
    instructor = StringField("Instructor", validators=[DataRequired()])
    paid = BooleanField("Paid", default=False, validators=[])
    completed = BooleanField("Completed", default=False, validators=[])
    submit = SubmitField("Create")

class SlotsForm(FlaskForm):
    date = DateField("Slot Date",format='%Y-%m-%d',default=lambda: get_sydney_now().date(),validators=[DataRequired()])
    start_time = SelectField("Start Time (24H)", choices=range(24), validators=[DataRequired()])
    end_time = SelectField("End Time (24H)", choices=range(24), validators=[DataRequired()])
    interval = SelectField("Interval (Hours)", choices=range(1,5), validators=[DataRequired()])
    instructor = StringField("Instructor", validators=[DataRequired()])
    submit = SubmitField("Create")    

class BookingForm(FlaskForm):
    date = DateField("Slot Date",format='%Y-%m-%d',default=lambda: get_sydney_now().date(),validators=[DataRequired()])
    time = TimeField("Slot Time", format='%H:%M',default=lambda: get_sydney_now().time(),validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    optional_email = StringField("Optional Email", validators=[])
    comment = TextAreaField("Comment", validators=[])
    instructor = StringField("Instructor", validators=[DataRequired()])
    paid = BooleanField("Paid", default=False, validators=[])
    completed = BooleanField("Completed", default=False, validators=[])
    submit = SubmitField("Book")

class RegisterUserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class ClassForm(FlaskForm):
    date = DateField("Slot Date",format='%Y-%m-%d',default=lambda: get_sydney_now().date(),validators=[DataRequired()])
    time = TimeField("Slot Time", format='%H:%M',default=lambda: get_sydney_now().time(),validators=[DataRequired()])
    class_name = StringField("Class Name", validators=[])
    class_description = TextAreaField("Description", validators=[])
    capacity = IntegerField("Class Capacity", default=6, validators=[DataRequired()])
    submit = SubmitField("Create")

class BookingClassForm(FlaskForm):
    name = StringField("Student Name", validators=[DataRequired()])
    email = StringField("Student Email", validators=[])
    mobile = StringField("Student Mobile", validators=[])
    paid = BooleanField("Paid", default=False, validators=[])
    submit = SubmitField("Add Student")

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')