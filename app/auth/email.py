from flask import render_template, current_app

from app.email import send_mail


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail(('[AlgotradeAI] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_verification_email(user):
    token = user.get_verification_token()
    send_mail('[AlgotradeAI] Verify Your Account',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/verification.txt',
                                         user=user, token=token),
               html_body=render_template('email/verification.html',
                                         user=user, token=token))
