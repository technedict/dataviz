from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
import os
from app.home import bp
from flask_login import login_required, current_user
import pandas as pd
from app.utils.data_validation import validate_file


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    return render_template('home/main.html')

@bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    user_files = []
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    for file in files:
        if f'[{current_user.id}]' in file:
            user_files.append(file)
    return render_template('home/home.html', files=user_files)


