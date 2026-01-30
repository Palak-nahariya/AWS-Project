"""
Local Storage Module - Mock Database for Testing
This module provides in-memory storage for testing without AWS DynamoDB
"""

import json
import os
from datetime import datetime
from decimal import Decimal

class LocalStorage:
    def __init__(self, storage_file='local_data.json'):
        self.storage_file = storage_file
        self.data = self._load_data()
    
    def _load_data(self):
        """Load data from JSON file or create new storage"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Initialize empty storage
        return {
            'users': {},
            'accounts': {},
            'transactions': {}
        }
    
    def _save_data(self):
        """Save data to JSON file"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    # User operations
    def create_user(self, user_id, name, email, password_hash, role='customer'):
        """Create a new user"""
        timestamp = datetime.utcnow().isoformat()
        self.data['users'][user_id] = {
            'UserID': user_id,
            'Name': name,
            'Email': email,
            'PasswordHash': password_hash,
            'Role': role,
            'CreatedAt': timestamp,
            'UpdatedAt': timestamp
        }
        self._save_data()
        return True
    
    def get_user_by_email(self, email):
        """Get user by email"""
        for user in self.data['users'].values():
            if user['Email'] == email:
                return user
        return None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.data['users'].get(user_id)
    
    # Account operations
    def create_account(self, account_id, user_id, balance=0, account_type='CHECKING', status='ACTIVE'):
        """Create a new account"""
        timestamp = datetime.utcnow().isoformat()
        self.data['accounts'][account_id] = {
            'AccountID': account_id,
            'UserID': user_id,
            'Balance': float(balance),
            'AccountType': account_type,
            'Status': status,
            'CreatedAt': timestamp,
            'UpdatedAt': timestamp
        }
        self._save_data()
        return True
    
    def get_account(self, account_id):
        """Get account by ID"""
        return self.data['accounts'].get(account_id)
    
    def get_accounts_by_user(self, user_id):
        """Get all accounts for a user"""
        accounts = []
        for account in self.data['accounts'].values():
            if account['UserID'] == user_id:
                accounts.append(account)
        return accounts
    
    def update_balance(self, account_id, amount, operation='ADD'):
        """Update account balance"""
        account = self.data['accounts'].get(account_id)
        if not account:
            return {'success': False, 'error': 'Account not found'}
        
        if account['Status'] != 'ACTIVE':
            return {'success': False, 'error': 'Account is not active'}
        
        if operation == 'ADD':
            account['Balance'] = float(account['Balance']) + float(amount)
        elif operation == 'SUBTRACT':
            if float(account['Balance']) < float(amount):
                return {'success': False, 'error': 'Insufficient balance'}
            account['Balance'] = float(account['Balance']) - float(amount)
        
        account['UpdatedAt'] = datetime.utcnow().isoformat()
        self._save_data()
        return {'success': True, 'account': account}
    
    def freeze_account(self, account_id):
        """Freeze an account"""
        account = self.data['accounts'].get(account_id)
        if account:
            account['Status'] = 'FROZEN'
            account['UpdatedAt'] = datetime.utcnow().isoformat()
            self._save_data()
            return {'success': True}
        return {'success': False, 'error': 'Account not found'}
    
    def activate_account(self, account_id):
        """Activate an account"""
        account = self.data['accounts'].get(account_id)
        if account:
            account['Status'] = 'ACTIVE'
            account['UpdatedAt'] = datetime.utcnow().isoformat()
            self._save_data()
            return {'success': True}
        return {'success': False, 'error': 'Account not found'}
    
    # Transaction operations
    def create_transaction(self, transaction_id, account_id, transaction_type, amount, 
                          target_account_id=None, description='', fraud_score=0):
        """Create a new transaction"""
        timestamp = datetime.utcnow().isoformat()
        transaction = {
            'TransactionID': transaction_id,
            'AccountID': account_id,
            'TransactionType': transaction_type,
            'Amount': float(amount),
            'Date': timestamp,
            'Status': 'PENDING',
            'Description': description,
            'FraudScore': fraud_score
        }
        
        if target_account_id:
            transaction['TargetAccountID'] = target_account_id
        
        self.data['transactions'][transaction_id] = transaction
        self._save_data()
        return {'success': True, 'transaction_id': transaction_id, 'fraud_score': fraud_score}
    
    def update_transaction_status(self, transaction_id, status):
        """Update transaction status"""
        transaction = self.data['transactions'].get(transaction_id)
        if transaction:
            transaction['Status'] = status
            self._save_data()
            return {'success': True}
        return {'success': False, 'error': 'Transaction not found'}
    
    def get_account_transactions(self, account_id, limit=100):
        """Get transactions for an account"""
        transactions = []
        for txn in self.data['transactions'].values():
            if txn['AccountID'] == account_id or txn.get('TargetAccountID') == account_id:
                transactions.append(txn)
        
        # Sort by date descending
        transactions.sort(key=lambda x: x['Date'], reverse=True)
        return transactions[:limit]
    
    def get_high_fraud_transactions(self, threshold=70):
        """Get transactions above fraud threshold"""
        high_fraud = []
        for txn in self.data['transactions'].values():
            if txn['FraudScore'] >= threshold:
                high_fraud.append(txn)
        
        # Sort by fraud score descending
        high_fraud.sort(key=lambda x: x['FraudScore'], reverse=True)
        return high_fraud

# Global instance
local_db = LocalStorage()
