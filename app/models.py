from app import db, login_manager
from flask import current_app
from hashlib import md5
from time import time
from typing import Optional
import jwt
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_verified: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=0)
    terms_condition: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=1)
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=0)


    def __repr__(self):
        return 'User: {}'.format(self.firstname + " " + self.lastname)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    def get_verification_token(self, expires_in=600):
        return jwt.encode(
            {'verify': self.email, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return db.session.get(User, id)

    @staticmethod
    def verify_verification_token(token):
        try:
            email = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['verify']
        except:
            return
        return email

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, int(id))