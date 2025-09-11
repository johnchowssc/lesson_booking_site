import datetime
from sqlite3 import Date
from flask import render_template, request, flash, redirect, url_for, send_from_directory, abort
from app import app, db, mail
from app.forms import BookingClassForm, LoginForm, SlotForm, BookingForm, RegisterUserForm, SlotsForm, ClassForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Slot, ClassSlot, Student
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from functools import wraps
from sqlalchemy import and_
import os
from itertools import groupby
from flask_mail import Mail, Message
from smtplib import SMTP
from app.email import send_class_booking_email, send_password_reset_email, send_lesson_booking_email

SCAN_RANGE = 30
PAST_RANGE = 1
PREV_RANGE = 7
PREV_CLASS_RANGE = 70 #Use this so that you can see the previous term of classes. 

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

# Index route: show current date
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    date = datetime.date.today()
    date = datetime.datetime.strftime(date, '%Y-%m-%d')
    return redirect(url_for('show_date', date=date))

# Show dates outside of current date range +/- range
# @app.route('/date/<date>')
# def show_date(date):
#     date = datetime.datetime.strptime(date, '%Y-%m-%d')
#     date = date.date() # Strip hours from date
#     date_plus_range = date + datetime.timedelta(days=SCAN_RANGE)
#     date_minus_range = date - datetime.timedelta(days=PAST_RANGE)
#     date_prev_range = date - datetime.timedelta(days=PREV_RANGE)
#     # date_minus_range = date - datetime.timedelta(days=SCAN_RANGE)
#     slots = Slot.query.filter(and_(Slot.date < date_plus_range, Slot.date > date_minus_range)) #Show slots on current date +/- range days.
#     slots = sorted(slots, key=lambda slot: slot.time) # Sort by time
#     slots = sorted(slots, key=lambda slot: slot.date) # Then sort by date
#     slots_by_date = []
#     for k, g in groupby(slots, key=lambda slot: slot.date):
#         slots_by_date.append(list(g))
#     return render_template('index.html', all_slots=slots_by_date, today=date, next_date=date_plus_range, prev_date=date_minus_range, prior_date=date_prev_range)

# Show dates outside of current date range +/- range sorted by Instructor
@app.route('/date/<date>')
def show_date(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    date = date.date() # Strip hours from date
    date_plus_range = date + datetime.timedelta(days=SCAN_RANGE)
    date_minus_range = date - datetime.timedelta(days=PAST_RANGE)
    date_prev_range = date - datetime.timedelta(days=PREV_RANGE)
    # date_minus_range = date - datetime.timedelta(days=SCAN_RANGE)
    slots = Slot.query.filter(and_(Slot.date < date_plus_range, Slot.date > date_minus_range)) #Show slots on current date +/- range days.
    slots = sorted(slots, key=lambda slot: slot.time) # Sort by time
    slots = sorted(slots, key=lambda slot: slot.instructor) #Sort by instructor 
    slots = sorted(slots, key=lambda slot: slot.date) # Then sort by date
    slots_by_date = []
    for k, g in groupby(slots, key=lambda slot: slot.date):
        slots_by_date.append(list(g))
    slots_by_date_instructor = []
    for slots_in_date in slots_by_date:
        slots_by_instructor = []
        for k, g in groupby(slots_in_date, key= lambda slot_in_day: slot_in_day.instructor):
            slots_by_instructor.append(list(g))
        slots_by_date_instructor.append(slots_by_instructor)
    return render_template('index.html', all_slots=slots_by_date_instructor, today=date, next_date=date_plus_range, prev_date=date_minus_range, prior_date=date_prev_range)

## Show all lessons dates route
@app.route('/all_lessons', methods=['GET'])
def show_all_lessons():
    all_slots = Slot.query.all()
    all_slots = sorted(all_slots, key=lambda slot: slot.time)
    all_slots = sorted(all_slots, key=lambda slot: slot.date)
    slots_by_date = []
    for k, g in groupby(all_slots, key=lambda slot: slot.date):
        slots_by_date.append(list(g))
    return render_template('all_lessons.html', all_slots=slots_by_date)

## Register new user
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

## Login user
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

## Create slot
@app.route("/create", methods=["Get","POST"])
@admin_only
def create_slot():
    form = SlotForm()
    if form.validate_on_submit():
        new_slot = Slot(
            date = form.date.data,
            time = form.time.data,
            name = form.name.data,
            comment = form.comment.data,
            instructor = form.instructor.data,
            paid = form.paid.data
        )
        db.session.add(new_slot)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('slot.html', form=form)

## Book slot
@app.route("/book/<int:slot_id>", methods=["GET", "POST"])
def book_slot(slot_id):
    form = BookingForm()
    slot = Slot.query.get(slot_id)
    if form.validate_on_submit():
        slot.date = form.date.data
        slot.time = form.time.data
        slot.name = form.name.data
        slot.comment = form.comment.data
        slot.instructor = form.instructor.data
        slot.paid = form.paid.data
        db.session.commit()
        if current_user.is_authenticated:
            send_lesson_booking_email(current_user, slot)
        return redirect(url_for('index'))
    form.date.data = slot.date # Pre-populate date
    form.time.data = slot.time # Pre-populate time
    if current_user.is_authenticated:
        if slot.name is None:
            form.name.data = current_user.name # Pre-populate current user name
        else:
            form.name.data = slot.name # Pre-populate name
    form.comment.data = slot.comment # Pre-populate comment
    form.instructor.data = slot.instructor # Pre-populate comment
    form.paid.data = slot.paid # Pre-populate paid
    return render_template('booking.html', form=form)

## Logout user
@app.route('/logout')
def logout():
    logout_user()
    return redirect (url_for('index'))

## Delete slot
@app.route('/delete_slot/<slot_id>')
@admin_only
def delete_slot(slot_id):
    slot = Slot.query.get(slot_id)
    db.session.delete(slot)
    db.session.commit()
    return redirect(url_for('show_date', date=slot.date))

## Create multiple slots
@app.route('/create_slots', methods=["Get","POST"])
@admin_only
def create_slots():
    form = SlotsForm()
    if form.validate_on_submit():
        start = int(form.start_time.data)
        end = int(form.end_time.data)
        interval = int(form.interval.data)
        for hour in range(start,end,interval):
            time = datetime.time(hour,0)
            new_slot = Slot(
                date = form.date.data,
                time = time,
                instructor = form.instructor.data
            )
            db.session.add(new_slot)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('slots.html', form=form)

## Slot Paid
@app.route('/toggle_paid_slot/<slot_id>')
@admin_only
def toggle_paid_slot(slot_id):
    slot = Slot.query.get(slot_id)
    slot.paid = not slot.paid
    db.session.commit()
    return redirect(url_for('show_date', date=slot.date))

## Slot completed
@app.route('/toggle_complete_slot/<slot_id>')
@admin_only
def toggle_complete_slot(slot_id):
    slot = Slot.query.get(slot_id)
    slot.completed = not slot.completed
    db.session.commit()
    return redirect(url_for('show_date', date=slot.date))

## Slot clear
@app.route('/toggle_clear_slot/<slot_id>')
@admin_only
def toggle_clear_slot(slot_id):
    slot = Slot.query.get(slot_id)
    slot.name = None
    slot.comment = None
    slot.paid = None
    slot.complete = None
    # slot.user.id = None
    db.session.commit()
    return redirect(url_for('show_date', date=slot.date))

## Duplicate Slot for next week
@app.route('/toggle_duplicate_slot/<slot_id>')
@admin_only
def toggle_duplicate_slot(slot_id):
    slot_old = Slot.query.get(slot_id)
    # slot.user.id = None
    new_slot = Slot(
            date = slot_old.date + datetime.timedelta(days=7),
            time = slot_old.time,
            name = slot_old.name,
            instructor = slot_old.instructor,
        )
    db.session.add(new_slot)
    db.session.commit()
    return redirect(url_for('show_date', date=slot_old.date))

## Show All Classes
@app.route('/all_classes')
def show_all_classes():
    date = datetime.date.today()
    date = datetime.datetime.strftime(date, '%Y-%m-%d')
    classes = ClassSlot.query.all()
    classes = sorted(classes, key=lambda slot: slot.time) # Sort by time
    classes = sorted(classes, key=lambda slot: slot.date) # Then sort by date
    classes_by_date = []
    for k, g in groupby(classes, key=lambda slot: slot.date):
        classes_by_date.append(list(g))
    return render_template('classes.html', classes=classes_by_date)

## Show Classes
@app.route('/classes')
def show_classes():
    date = datetime.date.today()
    date_prev_range = date - datetime.timedelta(days=PREV_CLASS_RANGE)
    classes = ClassSlot.query.filter(ClassSlot.date > date_prev_range) #Show slots after previous range date.
    classes = sorted(classes, key=lambda slot: slot.time) # Sort by time
    classes = sorted(classes, key=lambda slot: slot.date) # Then sort by date
    classes_by_date = []
    for k, g in groupby(classes, key=lambda slot: slot.date):
        classes_by_date.append(list(g))
    return render_template('classes.html', classes=classes_by_date, today=date)

## Create Class
@app.route('/create_class', methods=['GET','POST'])
@admin_only
def create_class():
    form = ClassForm()
    if form.validate_on_submit():
        new_slot = ClassSlot(
            date = form.date.data,
            time = form.time.data,
            class_name = form.class_name.data,
            class_description = form.class_description.data,
            capacity = form.capacity.data
        )
        db.session.add(new_slot)
        db.session.commit()
        return redirect(url_for('show_classes'))
    return render_template('create_class.html', form=form)

## Edit Class
@app.route('/edit_class/<class_slot_id>', methods=['GET','POST'])
@admin_only
def edit_class(class_slot_id):
    form = ClassForm()
    class_slot = ClassSlot.query.get(class_slot_id)
    if form.validate_on_submit():
        new_slot = ClassSlot(
            date = form.date.data,
            time = form.time.data,
            class_name = form.class_name.data,
            class_description = form.class_description.data,
            capacity = form.capacity.data
        )
        class_slot.date = new_slot.date
        class_slot.time = new_slot.time
        class_slot.class_name = new_slot.class_name
        class_slot.class_description = new_slot.class_description
        class_slot.capacity = new_slot.capacity
        db.session.commit()
        return redirect(url_for('show_classes'))
    ## Prepopulate values in form
    form.date.data = class_slot.date
    form.time.data = class_slot.time
    form.class_name.data = class_slot.class_name
    form.class_description.data = class_slot.class_description
    form.capacity.data = class_slot.capacity
    return render_template('create_class.html', form=form)

## Delete Class
@app.route('/delete_class/<class_id>')
@admin_only
def delete_class(class_id):
    class_slot = ClassSlot.query.get(class_id)
    db.session.delete(class_slot)
    db.session.commit()
    return redirect(url_for('show_classes'))

## Class Completed
@app.route('/toggle_complete_class/<class_id>')
@admin_only
def toggle_complete_class(class_id):
    class_slot = ClassSlot.query.get(class_id)
    class_slot.completed = not class_slot.completed
    db.session.commit()
    return redirect(url_for('show_classes'))

## Show and Book Students in Single Class
@app.route('/classes/<class_slot_id>', methods=["GET", "POST"])
def book_class(class_slot_id):
    form = BookingClassForm()
    class_slot = ClassSlot.query.get(class_slot_id)
    if form.validate_on_submit():
        if class_slot.capacity - len(class_slot.students) > 0:
            new_student = Student(
                name = form.name.data,
                email = form.email.data,
                mobile = form.mobile.data,
                paid = form.paid.data,
                parent_id = class_slot_id,
                user_id = current_user.id
            )
            db.session.add(new_student)
            db.session.commit()
            send_class_booking_email(new_student.name, new_student.email, class_slot)
            flash('Check your email for booking request confirmation')
            return redirect(url_for('book_class', class_slot_id=class_slot_id))
        else:
            # Ideally this would be another page
            return redirect(url_for('book_class', class_slot_id=class_slot_id))
    if current_user.is_authenticated:
            if current_user.is_admin:
                pass
            else:
                form.name.data = current_user.name # Pre-populate current user name
                form.email.data = current_user.email # Pre-populate current user name
    return render_template('class_slot.html', current_class=class_slot, form=form)

## Edit Student
@app.route('/edit_student/<student_id>', methods=['GET','POST'])
@admin_only
def edit_student(student_id):
    form = BookingClassForm()
    student = Student.query.get(student_id)
    if form.validate_on_submit():
        new_student = Student(
            name = form.name.data,
            email = form.email.data,
            mobile = form.mobile.data,
            paid = form.paid.data,
            parent_id = student.parent_id,
            user_id = current_user.id
        )
        student.name = new_student.name
        student.email = new_student.email
        student.mobile = new_student.mobile
        student.paid = new_student.paid
        student.parent_id = new_student.parent_id
        #student.user_id = new_student.user_id
        db.session.commit()
        return redirect(url_for('book_class', class_slot_id=student.parent_id))
    ## Prepopulate values in form
    form.name.data = student.name
    form.email.data = student.email
    form.mobile.data = student.mobile
    form.paid.data = student.paid
    return render_template('edit_student.html', form=form)

## Delete student in class
@app.route('/delete_student/<student_id>')
@admin_only
def delete_student(student_id):
    student = Student.query.get(student_id)
    class_slot_id = student.parent_id
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('book_class', class_slot_id=class_slot_id))

## Reset Password Request
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

## Reset Password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your Password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

## Edit Student if Self
@app.route('/edit_student_self/<student_id>', methods=['GET','POST'])
def edit_student_self(student_id):
    form = BookingClassForm()
    student = Student.query.get(student_id)
    if form.validate_on_submit():
        new_student = Student(
            name = form.name.data,
            email = form.email.data,
            mobile = form.mobile.data,
            paid = student.paid.data,
            parent_id = student.parent_id,
            user_id = current_user.id
        )
        student.name = new_student.name
        student.email = new_student.email
        student.mobile = new_student.mobile
        student.paid = new_student.paid
        student.parent_id = new_student.parent_id
        #student.user_id = new_student.user_id
        #db.session.commit()
        return redirect(url_for('book_class', class_slot_id=student.parent_id))
    ## Prepopulate values in form
    form.name.data = student.name
    form.email.data = student.email
    form.mobile.data = student.mobile
    form.paid.data = student.paid
    return render_template('edit_student.html', form=form)

## Delete Student if Self in class
@app.route('/delete_student_self/<student_id>')
def delete_student_self(student_id):
    student = Student.query.get(student_id)
    class_slot_id = student.parent_id
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('book_class', class_slot_id=class_slot_id))