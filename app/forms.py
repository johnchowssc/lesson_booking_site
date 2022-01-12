from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TimeField
from wtforms.validators import DataRequired 
from datetime import datetime

## Configure forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SlotForm(FlaskForm):
    date = DateField("Slot Date", format='%Y-%m-%d', default=datetime.now(), validators=[DataRequired()])
    time = TimeField("Slot Time", format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    submit = SubmitField("Create")

class BookingForm(FlaskForm):
    name = StringField("Name")
    submit = SubmitField("Book")