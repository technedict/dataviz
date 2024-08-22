from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User


class LoginForm(FlaskForm):
    email = StringField(('Email'), validators=[DataRequired(), Email()], render_kw={"class":"form-control", "aria-label": "Email", "id": "validationCustomEmail","aria-describedby":"inputGroupPrepend"})
    password = PasswordField(('Password'), validators=[DataRequired()], render_kw={"placeholder": "Password", "class":"form-control", "id": "validationCustomPassword", "aria-describedby":"inputGroupPrepend"})
    submit = SubmitField(('Sign In'), render_kw={"class":"btn btn-primary"})


class RegistrationForm(FlaskForm):
    firstname = StringField(('First Name'), validators=[DataRequired()], render_kw={"class":"form-control", "id": "validationCustom01", "value":"John"})
    lastname = StringField(('Last Name'), validators=[DataRequired()], render_kw={ "class":"form-control", "id": "validationCustom02", "value":"Doe"})
    username = StringField(('Username'), validators=[DataRequired()], render_kw={ "class":"form-control", "id": "validationCustomUsername", "aria-describedby":"inputGroupPrepend"})
    email = StringField(('Email'), validators=[DataRequired(), Email()], render_kw={"class":"form-control", "aria-label": "Email", "id": "validationCustomEmail","aria-describedby":"basic-addon2"})
    password = PasswordField(('Password'), validators=[DataRequired()], render_kw={"placeholder": "Password", "class":"form-control", "id": "validationCustomPassword", "aria-describedby":"inputGroupPrepend"})
    password2 = PasswordField(
        ('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')], render_kw={"placeholder": "Confirm Password","class":"form-control", "id": "validationCustomPassword", "aria-describedby":"inputGroupPrepend"})
    terms = BooleanField(('Remember Me'), validators=[DataRequired()], render_kw={"id": "invalidCheck", "class":"form-check-input"})
    submit = SubmitField(('Register'), render_kw={"class":"btn btn-primary"})

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
