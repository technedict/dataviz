from flask import render_template, current_app, request, redirect, url_for, flash, session, send_file
from flask_login import login_required, current_user
import pandas as pd
import os, uuid
from app.data import bp
from app.utils.data_cleaning import clean_data, save_json_to_csv
from app.utils.eda import generate_summary_statistics, generate_visualization
from app.utils.report_generation import generate_pdf_report, generate_excel_report



@bp.route('/cleaning', methods=['GET', 'POST'])
@login_required
def cleaning():
    filepath = session.get('uploaded_file')
    # Now read the file from the saved path
    try:
        df = pd.read_csv(filepath)
    except:
        flash(f'File is Unavailable, Please upload', category='info')
        return redirect(url_for('upload.main'))
    if request.method == 'POST':
        # Retrieve the uploaded data from session (or database if stored)
        if df is None:
            flash('No data uploaded', 'danger')
            return redirect(url_for('upload.main'))
        
        # Retrieve selected cleaning options from form
        remove_na = 'remove_na' in request.form
        remove_duplicates = 'remove_duplicates' in request.form
        normalize_data = 'normalize_data' in request.form
        
        # Clean the data using the selected options
        cleaned_df = clean_data(df, remove_na, remove_duplicates, normalize_data)

        # Generate a unique filename to avoid collisions
        filename = f'{os.path.splitext(os.path.basename(filepath))[0]}(cleaned){os.path.splitext(os.path.basename(filepath))[1]}'
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        print(cleaned_df)
        save_json_to_csv(cleaned_df, filepath)
        # Store cleaned data back in session (or database)
        session['cleaned_data'] = filepath
        
        flash('Data cleaned successfully!', 'success')
        return redirect(url_for('data.eda'))
    return render_template('data/cleaning.html', filepath=os.path.basename(filepath))

@bp.route('/eda', methods=['GET', 'POST'])
@login_required
def eda():
    filepath = session.get('cleaned_data')
    try:
        df = pd.read_csv(filepath)
    except:
        flash(f'Please clean the file to avoid redundancy', category='danger')
        return redirect(url_for('data.cleaning'))
    if df is None:
        flash('No data available for analysis', 'danger')
        return redirect(url_for('upload.main'))

    if request.method == 'POST':
        analysis_type = request.form.get('analysis_type')
        
        if analysis_type == 'summary_statistics':
            summary_stats = generate_summary_statistics(df)
            return render_template('data/summary_statistics.html', summary_stats=summary_stats)
        
        elif analysis_type == 'visualization':
            chart_type = request.form.get('chart_type')
            column_x = request.form.get('column_x')
            column_y = request.form.get('column_y', None)
            visualization = generate_visualization(df, chart_type, column_x, column_y)
            return render_template('data/visualization.html', columns=df.columns, visualization=visualization)

    return render_template('data/visualization.html', columns=df.columns)

@bp.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    filepath = session.get('cleaned_data')
    # Now read the file from the saved path
    try:
        df = pd.read_csv(filepath)
    except:
        flash(f'File is Unavailable, Please upload', category='info')
        return redirect(url_for('upload.main'))
    if df is None:
        flash('No data available for generating reports', 'danger')
        return redirect(url_for('upload.main'))

    if request.method == 'POST':
        report_type = request.form.get('report_type')
        
        if report_type == 'pdf':
            pdf_path = generate_pdf_report(df, current_app.config['REPORTS_FOLDER'])
            return send_file(pdf_path, as_attachment=True)
        
        elif report_type == 'excel':
            excel_path = generate_excel_report(df, current_app.config['REPORTS_FOLDER'])
            return send_file(excel_path, as_attachment=True)

    return render_template('data/report.html')


@bp.route('/clear_session')
def clear_session():
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    for file in files:
        if f'[{current_user.id}]' in file:
            file = os.path.join(current_app.config['UPLOAD_FOLDER'], file)
            os.remove(file)

    session.pop('uploaded_file', None)
    session.pop('cleaned_data', None)
    flash('Session cleared!', 'success')
    return redirect(url_for('upload.main'))

