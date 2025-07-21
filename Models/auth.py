from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from Models.models import db, User
from functools import wraps

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('home'))
        else:
            msg = 'Credenciales incorrectas'
    return render_template('login.html', msg=msg)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session or 'role' not in session:
                return redirect(url_for('auth.login'))
            if session['role'] not in roles:
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper
