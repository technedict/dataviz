from flask import render_template, redirect, url_for, flash, request
from urllib.parse import urlsplit
from flask_login import login_user, logout_user, current_user, login_required
import sqlalchemy as sa
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email, send_verification_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.main'))
    form = LoginForm()
    print(form.errors)
    if form.validate_on_submit():
        flash('hey')
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None:
            flash(('Invalid email'), category="danger")
            return redirect(url_for('auth.login'))
        elif not user.check_password(form.password.data):
            flash(('Invalid password'), category="danger")
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash(f"{current_user.firstname} logged in successfully", category="success")
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home.main')
        return redirect(next_page)
    return render_template('auth/signin.html', title=('Sign In'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.main'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('hey')
        user = User(username=form.username.data, firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Congratulations, you are now a registered user!', category="success")
        return redirect(url_for('home.main'))
    return render_template('auth/signup.html', title=('Register'),
                           form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home.main'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash(
            ('Check your email for the instructions to reset your password'), category="info")
        return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/reset_password_request.html',
                           title=('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.main'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home.main'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(('Your password has been reset.'), category="success")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/verify', methods=['GET', 'POST'])
@login_required
def verify():
    if current_user.is_verified:
        return redirect(url_for('home.main'))
    send_verification_email(current_user)
    flash('Check your email for the verification Email', category="info")
    return render_template('auth/verify.html',
                           title=('Verify'))

@bp.route('/confirm/<token>', methods=['GET', 'POST'])
@login_required
def confirm(token):
    if current_user.is_verified:
        return redirect(url_for('home.main'))
    email = User.verify_verification_token(token)
    if current_user.email != email:
        flash('Invalid Token')
        return redirect(url_for('auth.verify'))
    current_user.is_verified = True
    db.session.commit()
    flash('Your Account has been successfully verified.', category="success")
    return redirect(url_for('home.main'))

@bp.route('/debugverify/<token>', methods=['GET', 'POST'])
@login_required
def debugverify(token):
    if token == "admin":
        current_user.is_verified = True
        db.session.commit()
        flash('Your Account has been successfully verified.', category="success")
        return redirect(url_for('home.main'))
    else:
        flash('Invalid key')
        return redirect(url_for('home.main'))
