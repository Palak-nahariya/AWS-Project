from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from services.auth_service import AuthService
from services.banking_service import BankingService
from functools import wraps

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
banking_service = BankingService()

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page', 'warning')
                return redirect(url_for('auth.login'))
            
            if session.get('role') != required_role and session.get('role') != 'admin':
                flash('Access denied. Insufficient permissions.', 'danger')
                return redirect(url_for('account.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('account.dashboard'))
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if 'user_id' in session:
        return redirect(url_for('account.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'customer')
        
        result = auth_service.register(name, email, password, role)
        
        if result['success']:
            # Auto-create account for new user
            banking_service.create_account(result['user_id'], initial_balance=1000)
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(result['error'], 'danger')
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if 'user_id' in session:
        return redirect(url_for('account.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        result = auth_service.login(email, password)
        
        if result['success']:
            user = result['user']
            session['user_id'] = user['UserID']
            session['name'] = user['Name']
            session['email'] = user['Email']
            session['role'] = user['Role']
            session.permanent = True
            
            flash(f'Welcome back, {user["Name"]}!', 'success')
            return redirect(url_for('account.dashboard'))
        else:
            flash(result['error'], 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
