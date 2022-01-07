import flask_wtf
import wtforms
import wtforms.validators
import datetime

## Configure forms
class SlotForm(flask_wtf.FlaskForm):
    date = wtforms.DateField("Slot Date", format='%Y-%m-%d', default=datetime.datetime.now(), validators=[wtforms.validators.DataRequired()])
    time = wtforms.TimeField("Slot Time", format='%H:%M', default=datetime.datetime.now(), validators=[wtforms.validators.DataRequired()])
    submit = wtforms.SubmitField("Create")

class BookingForm(flask_wtf.FlaskForm):
    name = wtforms.StringField("Name")
    submit = wtforms.SubmitField("Book")