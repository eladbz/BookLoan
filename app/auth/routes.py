from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from app.auth import bp
from app.auth.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user(username)
        
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
