from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from services.banking_service import BankingService
from services.notification_service import NotificationService
from routes.auth_routes import login_required
from config import Config

transaction_bp = Blueprint('transaction', __name__)
banking_service = BankingService()
notification_service = NotificationService()

@transaction_bp.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    """Deposit money"""
    user_id = session.get('user_id')
    
    # Get user accounts
    accounts_result = banking_service.get_user_accounts(user_id)
    accounts = accounts_result.get('accounts', [])
    
    if request.method == 'POST':
        account_id = request.form.get('account_id')
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description', 'Deposit')
        
        result = banking_service.deposit(account_id, amount, description)
        
        if result['success']:
            flash(f'Deposit successful! New balance: ${result["new_balance"]:.2f}', 'success')
            return redirect(url_for('account.dashboard'))
        else:
            flash(result['error'], 'danger')
    
    return render_template('deposit.html', accounts=accounts)

@transaction_bp.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    """Withdraw money"""
    user_id = session.get('user_id')
    
    # Get user accounts
    accounts_result = banking_service.get_user_accounts(user_id)
    accounts = accounts_result.get('accounts', [])
    
    if request.method == 'POST':
        account_id = request.form.get('account_id')
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description', 'Withdrawal')
        
        result = banking_service.withdraw(account_id, amount, description)
        
        if result['success']:
            fraud_score = result.get('fraud_score', 0)
            
            # Send alert if fraud score is high
            if fraud_score >= Config.FRAUD_ALERT_THRESHOLD:
                notification_service.notify_high_fraud_transaction(
                    result['transaction_id'], account_id, amount, fraud_score
                )
            
            flash(f'Withdrawal successful! New balance: ${result["new_balance"]:.2f}', 'success')
            if fraud_score >= Config.FRAUD_ALERT_THRESHOLD:
                flash(f'Note: This transaction was flagged (Fraud Score: {fraud_score})', 'warning')
            
            return redirect(url_for('account.dashboard'))
        else:
            flash(result['error'], 'danger')
    
    return render_template('withdraw.html', accounts=accounts)

@transaction_bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    """Transfer money between accounts"""
    user_id = session.get('user_id')
    
    # Get user accounts
    accounts_result = banking_service.get_user_accounts(user_id)
    accounts = accounts_result.get('accounts', [])
    
    if request.method == 'POST':
        source_account_id = request.form.get('source_account_id')
        target_account_id = request.form.get('target_account_id')
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description', 'Transfer')
        
        result = banking_service.transfer(
            source_account_id, target_account_id, amount, description
        )
        
        if result['success']:
            fraud_score = result.get('fraud_score', 0)
            
            # Send alert if fraud score is high
            if fraud_score >= Config.FRAUD_ALERT_THRESHOLD:
                notification_service.notify_high_fraud_transaction(
                    result['transaction_id'], source_account_id, amount, fraud_score
                )
            
            flash(f'Transfer successful! New balance: ${result["new_balance"]:.2f}', 'success')
            if fraud_score >= Config.FRAUD_ALERT_THRESHOLD:
                flash(f'Note: This transaction was flagged (Fraud Score: {fraud_score})', 'warning')
            
            return redirect(url_for('account.dashboard'))
        else:
            flash(result['error'], 'danger')
    
    return render_template('transfer.html', accounts=accounts)

@transaction_bp.route('/history')
@login_required
def history():
    """View transaction history"""
    user_id = session.get('user_id')
    
    # Get user accounts
    accounts_result = banking_service.get_user_accounts(user_id)
    accounts = accounts_result.get('accounts', [])
    
    # Get account_id from query params or use first account
    account_id = request.args.get('account_id')
    if not account_id and accounts:
        account_id = accounts[0]['AccountID']
    
    transactions = []
    if account_id:
        txn_result = banking_service.get_transaction_history(account_id, limit=100)
        transactions = txn_result.get('transactions', [])
    
    return render_template(
        'history.html',
        accounts=accounts,
        selected_account_id=account_id,
        transactions=transactions
    )
