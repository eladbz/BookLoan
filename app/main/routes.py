from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.main import bp
from app.strings import not_found_str, received_str, confirmation_str
from app.utils import get_student_data, save_distribution, get_all_distributions, check_distribution_status, \
    reset_distributions


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
            class_num = int(request.form['class_num'])
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
