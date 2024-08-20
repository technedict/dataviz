from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    email = StringField(('Email'), validators=[DataRequired(), Email()], render_kw={"placeholder": "email@example.com", "id": "login-form-email"})
    password = PasswordField(('Password'), validators=[DataRequired()], render_kw={"placeholder": "Password", "id": "login-form-password"})
    remember_me = BooleanField(('Remember Me'))
    submit = SubmitField(('Sign In'))


class RegistrationForm(FlaskForm):
    firstname = StringField(('First Name'), validators=[DataRequired()], render_kw={"placeholder": "John", "id": "signup-form-fname"})
    lastname = StringField(('Last Name'), validators=[DataRequired()], render_kw={"placeholder": "Doe", "id": "signup-form-lname"})
    email = StringField(('Email'), validators=[DataRequired(), Email()], render_kw={"placeholder": "email@example.com", "id": "signup-form-email"})
    password = PasswordField(('Password'), validators=[DataRequired()], render_kw={"placeholder": "Password", "id": "signup-form-password"})
    password2 = PasswordField(
        ('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')], render_kw={"placeholder": "Repeat Password", "id": "signup-form-confirm_password"})
    TC = BooleanField(('Remember Me'), validators=[DataRequired()], render_kw={"id": "signup-form-accept_terms"})
    submit = SubmitField(('Register'))

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError(('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        ('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(('Request Password Reset'))
