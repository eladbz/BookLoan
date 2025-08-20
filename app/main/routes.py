from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user

from config import Config
from app.main import bp
from app.strings import not_found_str, received_str, confirmation_str
from app.utils import get_student_data, save_distribution, get_all_distributions, check_distribution_status, \
    reset_distributions
import io
import csv
import os
from tempfile import NamedTemporaryFile


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return redirect(url_for('main.receive_books'))

@bp.route('/receive-books', methods=['GET', 'POST'])
@login_required
def receive_books():
    if request.method == 'POST':
        student_id = int(request.form['student_id'])

        if not 'confirm' in request.form:
            #Submit the form to get student data
            grade = int(request.form['grade'] )
            class_num = int(request.form['class_num'] if grade != 0 else 0)
            student = get_student_data(student_id, grade, class_num)
            if not student:
                flash(not_found_str % student_id)
                return redirect(url_for('main.receive_books'))
            received, receiver = check_distribution_status(student_id)
            if received:
                flash((received_str % student_id )+ receiver)
                return redirect(url_for('main.receive_books'))
            return render_template('main/receive_books.html', student=student)

        #Confirm part
        student_name = request.form['student_name']
        receiver = request.form['receiver_name']
        save_distribution(student_id, student_name, receiver)
        flash(confirmation_str)
        return redirect(url_for('main.receive_books'))

    return render_template('main/receive_books.html', student=None)

@bp.route('/status')
@login_required
def status():
    distributions = get_all_distributions()
    return render_template('main/status.html', distributions=distributions)

@bp.route('/reset')
@login_required
def reset():
    """Reset the distributions data."""
    if current_user.id != 'elad':
        flash("You do not have permission to reset the distributions.")
        return redirect(url_for('main.status'))
    reset_distributions()
    flash("File reset successfully")
    return redirect(url_for('main.status'))

@bp.route('/upload-csv', methods=['GET', 'POST'])
@login_required
def upload_csv():
    """Overwrite the distributions data using a CSV sent in the request body."""
    if current_user.id != 'elad':
        if request.method == 'POST':
            return jsonify({"error": "You do not have permission to reset the distributions."}), 403
        flash("You do not have permission to reset the distributions.")
        return redirect(url_for('main.status'))

    if request.method == 'GET':
        flash("POST a CSV (text/csv) in the request body to overwrite the distributions.")
        return redirect(url_for('main.status'))

    # POST: accept CSV in body
    raw = request.get_data()
    if not raw:
        return jsonify({"error": "Empty request body. Send CSV data in the body with Content-Type: text/csv."}), 400

    try:
        text = raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        return jsonify({"error": "Could not decode body as UTF-8. Please send UTF-8 encoded CSV."}), 400

    # Basic CSV validation and row count
    sio = io.StringIO(text)
    reader = csv.reader(sio)
    try:
        header = next(reader)
    except StopIteration:
        return jsonify({"error": "CSV appears to be empty."}), 400

    expected_header = ['תעודת זהות', 'שם תלמיד', 'מקבל', 'זמן קבלה']
    normalized = [h.strip() for h in header]
    if normalized[:len(expected_header)] != expected_header:
        return jsonify({
            "error": "Unexpected CSV header. Expected first columns: " + ", ".join(expected_header)
        }), 400

    row_count = sum(1 for _ in reader)

    tmp_file = NamedTemporaryFile('w', encoding='utf-8', newline='', delete=False)
    try:
        tmp_file.write(text)
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
        tmp_name = tmp_file.name
    finally:
        tmp_file.close()
    os.replace(tmp_name, Config.DISTRIBUTIONS_FILE)

    return jsonify({"message": "File rewrite successfully", "rows": row_count})