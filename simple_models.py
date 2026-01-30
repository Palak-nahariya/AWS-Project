"""
Simplified models wrapper for local storage compatibility
This file provides simple wrappers that work with both DynamoDB and local storage
"""

from config import Config

if Config.USE_LOCAL_STORAGE:
    from local_storage import local_db
    
    # Simple Account wrapper
    class SimpleAccount:
        def __init__(self):
            self.storage = local_db
        
        def create_account(self, account_id, user_id, initial_balance=0, account_type='SAVINGS'):
            return {'success': self.storage.create_account(account_id, user_id, initial_balance, account_type, 'ACTIVE')}
        
        def get_account(self, account_id):
            return self.storage.get_account(account_id)
        
        def get_accounts_by_user(self, user_id):
            return self.storage.get_accounts_by_user(user_id)
        
        def update_balance(self, account_id, amount, operation='ADD'):
            return self.storage.update_balance(account_id, amount, operation)
        
        def freeze_account(self, account_id):
            return self.storage.freeze_account(account_id)
        
        def activate_account(self, account_id):
            return self.storage.activate_account(account_id)
    
    # Simple Transaction wrapper
    class SimpleTransaction:
        def __init__(self):
            self.storage = local_db
        
        def create_transaction(self, transaction_id, account_id, transaction_type, amount, target_account_id=None, description=''):
            # Simple fraud score calculation
            fraud_score = 0
            if amount > 5000:
                fraud_score = 30
            if amount > 10000:
                fraud_score = 50
            
            return self.storage.create_transaction(
                transaction_id, account_id, transaction_type, amount, 
                target_account_id, description, fraud_score
            )
        
        def update_transaction_status(self, transaction_id, status):
            return self.storage.update_transaction_status(transaction_id, status)
        
        def get_account_transactions(self, account_id, limit=100):
            return self.storage.get_account_transactions(account_id, limit)
        
        def get_high_fraud_transactions(self, threshold=70):
            return self.storage.get_high_fraud_transactions(threshold)
    
    Account = SimpleAccount
    Transaction = SimpleTransaction
    
else:
    # Use original DynamoDB models
    from models.account import Account as DynamoAccount
    from models.transaction import Transaction as DynamoTransaction
    
    Account = DynamoAccount
    Transaction = DynamoTransaction
