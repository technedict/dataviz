from flask import session, current_app, render_template, request, redirect, url_for, flash
from app.upload import bp
from flask_login import login_required, current_user
import pandas as pd
import os, uuid
from app.utils.data_validation import validate_file

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def main():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and validate_file(file):            
            try:

                file.seek(0)

                # Generate a unique filename to avoid collisions
                filename = f'{str(uuid.uuid4())}[{current_user.id}]{os.path.splitext(file.filename)[1]}'
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                
                # Save file to the specified directory
                file.save(filepath)

                # Optionally save the DataFrame in session or process further
                session['uploaded_file'] = filepath  # Save file path in session if needed

                # Further processing, such as saving to database, goes here
                
                flash('File successfully uploaded!', 'success')
                return redirect(url_for('data.cleaning'))
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
        else:
            flash('Invalid file format or data issues.', 'danger')
    
    return render_template('upload/upload.html')
