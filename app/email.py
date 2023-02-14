from flask import render_template
from flask_mail import Message
from app import app, mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_class_booking_email(student, student_email, class_slot):
    send_email('Booking Requested for ' + student,
        sender=app.config['ADMINS'][0],
        recipients=[student_email, app.config['ADMINS'][0]],
        text_body=render_template('email/class_booking_request.txt', student=student, class_slot=class_slot),
        html_body=render_template('email/class_booking_request.html', student=student, class_slot=class_slot)
    )

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Reset Your Password',
        sender=app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token)
    )

def send_lesson_booking_email(user, slot):
    send_email('Booking Requested for ' + slot.name,
        sender=app.config['ADMINS'][0],
        recipients=[user.email, app.config['ADMINS'][0]],
        text_body=render_template('email/lesson_booking_request.txt', user=user.name, slot=slot),
        html_body=render_template('email/lesson_booking_request.html', user=user.name, slot=slot)
    )