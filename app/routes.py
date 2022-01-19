import datetime
from flask import render_template, flash, redirect, url_for, send_from_directory, abort
from app import app, db
from app.forms import LoginForm, SlotForm, BookingForm, RegisterUserForm, SlotsForm
from app.models import User, Slot
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from functools import wraps
import os

def admin_only(function):
    wraps(function)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.is_admin != True:
                print("Not an admin")
                return abort(403)
        except:
            print("Not logged in")
            return abort(403) #Not logged in
        else:
            return function(*args, **kwargs)
    decorated_function.__name__ = function.__name__
    return decorated_function        

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    slots = Slot.query.all()
    slots_by_time = sorted(slots, key=lambda slot: slot.time)
    slots_by_timedate = sorted(slots_by_time, key=lambda slot: slot.date)
    return render_template('index.html', all_slots=slots_by_timedate)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        try:
            new_user = User(
            name = form.name.data,
            email = form.email.data,
            is_admin = False,
            )
            new_user.set_password(password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            # If this is the first user, make admin
            if new_user.id == 1:
                new_user.make_admin()
                db.session.commit()

            login_user(new_user)
        except:
            flash("Email already exists")
            return redirect(url_for('login'))
        return redirect(url_for('index'))
        
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for email {}, remember_me={}'.format(
            form.email.data, form.remember_me.data
            )
        )
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("User doesn't exist")
        elif not user.check_password(password=form.password.data):
            flash("Password incorrect")
        else:
            login_user(user)
            return redirect(url_for('index'))

    return render_template("login.html", form=form)

@app.route("/create", methods=["Get","POST"])
@admin_only
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
    users = User.query.all()
    names = [ user.name for user in users]
    form.name.choices = names
    slot = Slot.query.get(slot_id)
    if form.validate_on_submit():
        slot.name = form.name.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('booking.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect (url_for('index'))

@app.route('/delete_slot/<slot_id>')
@admin_only
def delete_slot(slot_id):
    slot = Slot.query.get(slot_id)
    db.session.delete(slot)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/create_slots', methods=["Get","POST"])
@admin_only
def create_slots():
    form = SlotsForm()
    if form.validate_on_submit():
        start = form.start_time.data
        end = form.end_time.data
        interval = form.interval.data
        for hour in range(start,end,interval):
            time = datetime.time(hour,0)
            new_slot = Slot(
                date = form.date.data,
                time = time
            )
            db.session.add(new_slot)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('slots.html', form=form)