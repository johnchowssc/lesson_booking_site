import flask
import flask_bootstrap
import flask_wtf
import wtforms
import wtforms.validators

import os
import dotenv
import flask_sqlalchemy
import datetime

## Import environment variables
dotenv.load_dotenv()

## Initialise Flask
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("APP_SECRET_KEY")

## Initialise Bootstrap
flask_bootstrap.Bootstrap(app)

## Initialise DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///bookings.db") ## Use Heroku Postgres, or if not found, e.g. local, SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)

## Configure tables
class Slot(db.Model):
    __tablename__ = "slots"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    name = db.Column(db.String(250), nullable=True)

db.create_all()


## Configure forms
class SlotForm(flask_wtf.FlaskForm):
    date = wtforms.DateField("Slot Date", format='%Y-%m-%d', default=datetime.datetime.now(), validators=[wtforms.validators.DataRequired()])
    time = wtforms.TimeField("Slot Time", format='%H:%M', default=datetime.datetime.now(), validators=[wtforms.validators.DataRequired()])
    name = wtforms.StringField("Name")
    submit = wtforms.SubmitField('Create')

## Routes
@app.route("/", methods=["Get","POST"])
def get_calendar():
    slots = Slot.query.all()
    form = SlotForm()
    if form.validate_on_submit():
        new_slot = Slot(
            date = form.date.data,
            time = form.time.data,
            name = form.name.data
        )
        db.session.add(new_slot)
        db.session.commit()
        return flask.redirect(flask.url_for("get_calendar"))
    return flask.render_template("index.html", form=form, all_slots=slots)

if __name__ == "__main__":
    app.run(debug=True)