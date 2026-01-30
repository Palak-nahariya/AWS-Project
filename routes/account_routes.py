from flask import Blueprint, render_template, session, redirect, url_for, flash
from services.banking_service import BankingService
from routes.auth_routes import login_required

account_bp = Blueprint('account', __name__)
banking_service = BankingService()

@account_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    user_id = session.get('user_id')
    
    # Get user accounts
    accounts_result = banking_service.get_user_accounts(user_id)
    accounts = accounts_result.get('accounts', [])
    
    # Get primary account (first account)
    primary_account = accounts[0] if accounts else None
    
    # Get recent transactions for primary account
    recent_transactions = []
    if primary_account:
        txn_result = banking_service.get_transaction_history(
            primary_account['AccountID'], limit=10
        )
        recent_transactions = txn_result.get('transactions', [])
    
    return render_template(
        'dashboard.html',
        accounts=accounts,
        primary_account=primary_account,
        recent_transactions=recent_transactions
    )

@account_bp.route('/accounts')
@login_required
def list_accounts():
    """List all user accounts"""
    user_id = session.get('user_id')
    
    accounts_result = banking_service.get_user_accounts(user_id)
    accounts = accounts_result.get('accounts', [])
    
    return render_template('accounts.html', accounts=accounts)
