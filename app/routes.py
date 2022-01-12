from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, SlotForm, BookingForm
from app.models import User, Slot

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    slots = Slot.query.all()
    return render_template('index.html', all_slots=slots)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
            )
        )
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route("/create", methods=["Get","POST"])
def create_slot():
    form = SlotForm()
    if form.validate_on_submit():
        new_slot = Slot(
            date = form.date.data,
            time = form.time.data
        )
        db.session.add(new_slot)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('slot.html', form=form)

@app.route("/book/<int:slot_id>", methods=["GET", "POST"])
def book_slot(slot_id):
    form = BookingForm()
    slot = Slot.query.get(slot_id)
    if form.validate_on_submit():
        slot.name = form.name.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('booking.html', form=form)

# def get_calendar():
#     slots = Slot.query.all()
#     return flask.render_template("index.html", all_slots=slots)





# @app.route("/delete/<int:slot_id>")
# def delete_slot(slot_id):
#     slot = Slot.query.get(slot_id)
#     db.session.delete(slot)
#     db.session.commit()
#     return flask.redirect(flask.url_for('get_calendar'))