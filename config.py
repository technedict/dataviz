import os
from os import path

basedir = os.path.abspath(os.path.dirname(__file__))
dbroute = path.dirname(path.realpath(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + path.join(dbroute, "database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploaded_files')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    REPORTS_FOLDER = os.path.join(os.getcwd(), 'reports')
    if not os.path.exists(REPORTS_FOLDER ):
        os.makedirs(REPORTS_FOLDER )
