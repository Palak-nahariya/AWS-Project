from models.account import Account
from models.transaction import Transaction
from config import Config
import uuid

class BankingService:
    """Banking service for core banking operations"""
    
    def __init__(self):
        self.account_model = Account()
        self.transaction_model = Transaction()
    
    def create_account(self, user_id, initial_balance=0, account_type='SAVINGS'):
        """Create a new bank account for a user"""
        account_id = str(uuid.uuid4())
        result = self.account_model.create_account(
            account_id, user_id, initial_balance, account_type
        )
        return result
    
    def get_user_accounts(self, user_id):
        """Get all accounts for a user"""
        accounts = self.account_model.get_accounts_by_user(user_id)
        return {'success': True, 'accounts': accounts}
    
    def get_account(self, account_id):
        """Get account details"""
        account = self.account_model.get_account(account_id)
        if account:
            return {'success': True, 'account': account}
        return {'success': False, 'error': 'Account not found'}
    
    def deposit(self, account_id, amount, description='Deposit'):
        """Deposit money into an account"""
        # Validate amount
        if amount <= 0:
            return {'success': False, 'error': 'Amount must be positive'}
        
        # Create transaction record
        transaction_id = str(uuid.uuid4())
        txn_result = self.transaction_model.create_transaction(
            transaction_id, account_id, 'DEPOSIT', amount, description=description
        )
        
        if not txn_result['success']:
            return txn_result
        
        # Update account balance
        balance_result = self.account_model.update_balance(account_id, amount, 'ADD')
        
        if balance_result['success']:
            # Mark transaction as completed
            self.transaction_model.update_transaction_status(transaction_id, 'COMPLETED')
            return {
                'success': True,
                'transaction_id': transaction_id,
                'new_balance': balance_result['account']['Balance'],
                'fraud_score': txn_result.get('fraud_score', 0)
            }
        else:
            # Mark transaction as failed
            self.transaction_model.update_transaction_status(transaction_id, 'FAILED')
            return balance_result
    
    def withdraw(self, account_id, amount, description='Withdrawal'):
        """Withdraw money from an account"""
        # Validate amount
        if amount <= 0:
            return {'success': False, 'error': 'Amount must be positive'}
        
        # Create transaction record
        transaction_id = str(uuid.uuid4())
        txn_result = self.transaction_model.create_transaction(
            transaction_id, account_id, 'WITHDRAW', amount, description=description
        )
        
        if not txn_result['success']:
            return txn_result
        
        fraud_score = txn_result.get('fraud_score', 0)
        
        # Check fraud score - freeze account if too high
        if fraud_score >= Config.FRAUD_FREEZE_THRESHOLD:
            self.account_model.freeze_account(account_id)
            self.transaction_model.update_transaction_status(transaction_id, 'FAILED')
            return {
                'success': False,
                'error': 'Transaction blocked due to suspicious activity. Account frozen.',
                'fraud_score': fraud_score
            }
        
        # Update account balance
        balance_result = self.account_model.update_balance(account_id, amount, 'SUBTRACT')
        
        if balance_result['success']:
            # Mark transaction as completed
            self.transaction_model.update_transaction_status(transaction_id, 'COMPLETED')
            return {
                'success': True,
                'transaction_id': transaction_id,
                'new_balance': balance_result['account']['Balance'],
                'fraud_score': fraud_score
            }
        else:
            # Mark transaction as failed
            self.transaction_model.update_transaction_status(transaction_id, 'FAILED')
            return balance_result
    
    def transfer(self, source_account_id, target_account_id, amount, description='Transfer'):
        """Transfer money between accounts"""
        # Validate amount
        if amount <= 0:
            return {'success': False, 'error': 'Amount must be positive'}
        
        # Validate target account exists
        target_account = self.account_model.get_account(target_account_id)
        if not target_account:
            return {'success': False, 'error': 'Target account not found'}
        
        # Create transaction record
        transaction_id = str(uuid.uuid4())
        txn_result = self.transaction_model.create_transaction(
            transaction_id, source_account_id, 'TRANSFER', amount,
            target_account_id=target_account_id, description=description
        )
        
        if not txn_result['success']:
            return txn_result
        
        fraud_score = txn_result.get('fraud_score', 0)
        
        # Check fraud score
        if fraud_score >= Config.FRAUD_FREEZE_THRESHOLD:
            self.account_model.freeze_account(source_account_id)
            self.transaction_model.update_transaction_status(transaction_id, 'FAILED')
            return {
                'success': False,
                'error': 'Transaction blocked due to suspicious activity. Account frozen.',
                'fraud_score': fraud_score
            }
        
        # Deduct from source account
        deduct_result = self.account_model.update_balance(source_account_id, amount, 'SUBTRACT')
        
        if not deduct_result['success']:
            self.transaction_model.update_transaction_status(transaction_id, 'FAILED')
            return deduct_result
        
        # Add to target account
        add_result = self.account_model.update_balance(target_account_id, amount, 'ADD')
        
        if add_result['success']:
            # Mark transaction as completed
            self.transaction_model.update_transaction_status(transaction_id, 'COMPLETED')
            return {
                'success': True,
                'transaction_id': transaction_id,
                'new_balance': deduct_result['account']['Balance'],
                'fraud_score': fraud_score
            }
        else:
            # Rollback - add back to source account
            self.account_model.update_balance(source_account_id, amount, 'ADD')
            self.transaction_model.update_transaction_status(transaction_id, 'FAILED')
            return {'success': False, 'error': 'Transfer failed - transaction rolled back'}
    
    def get_transaction_history(self, account_id, limit=50):
        """Get transaction history for an account"""
        transactions = self.transaction_model.get_account_transactions(account_id, limit)
        return {'success': True, 'transactions': transactions}
