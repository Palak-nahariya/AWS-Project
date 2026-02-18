import boto3
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError
from config import Config

class Account:
    """Account model for managing bank accounts in DynamoDB"""
    
    def __init__(self):
        # Check if using local storage
        if Config.USE_LOCAL_STORAGE:
            from local_storage import local_db
            self.storage = local_db
            self.use_local = True
        else:
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=Config.AWS_REGION,
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
            )
            self.table = self.dynamodb.Table(Config.DYNAMODB_ACCOUNTS_TABLE)
            self.use_local = False
    
    def create_account(self, account_id, user_id, initial_balance=0, account_type='SAVINGS'):
        """Create a new bank account"""
        if self.use_local:
            # Use local storage
            try:
                self.storage.create_account(account_id, user_id, initial_balance, account_type)
                return {'success': True, 'account_id': account_id}
            except Exception as e:
                return {'success': False, 'error': str(e)}
        else:
            # Use DynamoDB
            try:
                timestamp = datetime.utcnow().isoformat()
                
                self.table.put_item(
                    Item={
                        'AccountID': account_id,
                        'UserID': user_id,
                        'Balance': Decimal(str(initial_balance)),
                        'AccountType': account_type,
                        'Status': 'ACTIVE',
                        'CreatedAt': timestamp,
                        'UpdatedAt': timestamp
                    },
                    ConditionExpression='attribute_not_exists(AccountID)'
                )
                
                return {'success': True, 'account_id': account_id}
            except ClientError as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    return {'success': False, 'error': 'Account already exists'}
                return {'success': False, 'error': str(e)}
    
    def get_account(self, account_id):
        """Retrieve account by AccountID"""
        if self.use_local:
            # Use local storage
            return self.storage.get_account(account_id)
        else:
            # Use DynamoDB
            try:
                response = self.table.get_item(Key={'AccountID': account_id})
                account = response.get('Item')
                if account and 'Balance' in account:
                    account['Balance'] = float(account['Balance'])
                return account
            except ClientError as e:
                print(f"Error retrieving account: {e}")
                return None
    
    def get_accounts_by_user(self, user_id):
        """Retrieve all accounts for a user"""
        if self.use_local:
            # Use local storage
            return self.storage.get_accounts_by_user(user_id)
        else:
            # Use DynamoDB
            try:
                response = self.table.query(
                    IndexName='UserIDIndex',
                    KeyConditionExpression='UserID = :user_id',
                    ExpressionAttributeValues={':user_id': user_id}
                )
                accounts = response.get('Items', [])
                
                # Convert Decimal to float for JSON serialization
                for account in accounts:
                    if 'Balance' in account:
                        account['Balance'] = float(account['Balance'])
                
                return accounts
            except ClientError as e:
                print(f"Error retrieving accounts by user: {e}")
                return []
    
    def update_balance(self, account_id, amount, operation='ADD'):
        """Update account balance (ADD or SUBTRACT)"""
        if self.use_local:
            # Use local storage
            return self.storage.update_balance(account_id, amount, operation)
        else:
            # Use DynamoDB
            try:
                if operation == 'ADD':
                    update_expression = "SET Balance = Balance + :amount, UpdatedAt = :timestamp"
                elif operation == 'SUBTRACT':
                    update_expression = "SET Balance = Balance - :amount, UpdatedAt = :timestamp"
                else:
                    return {'success': False, 'error': 'Invalid operation'}
                
                # For SUBTRACT, ensure sufficient balance
                condition_expression = 'attribute_exists(AccountID) AND #status = :status'
                if operation == 'SUBTRACT':
                    condition_expression += ' AND Balance >= :amount'
                
                response = self.table.update_item(
                    Key={'AccountID': account_id},
                    UpdateExpression=update_expression,
                    ConditionExpression=condition_expression,
                    ExpressionAttributeNames={'#status': 'Status'},
                    ExpressionAttributeValues={
                        ':amount': Decimal(str(amount)),
                        ':timestamp': datetime.utcnow().isoformat(),
                        ':status': 'ACTIVE'
                    },
                    ReturnValues='ALL_NEW'
                )
                
                account = response['Attributes']
                account['Balance'] = float(account['Balance'])
                return {'success': True, 'account': account}
                
            except ClientError as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    return {'success': False, 'error': 'Insufficient balance or account inactive'}
                return {'success': False, 'error': str(e)}
    
    def freeze_account(self, account_id):
        """Freeze an account (fraud prevention)"""
        if self.use_local:
            # Use local storage
            return self.storage.freeze_account(account_id)
        else:
            # Use DynamoDB
            try:
                response = self.table.update_item(
                    Key={'AccountID': account_id},
                    UpdateExpression="SET #status = :status, UpdatedAt = :timestamp",
                    ExpressionAttributeNames={'#status': 'Status'},
                    ExpressionAttributeValues={
                        ':status': 'FROZEN',
                        ':timestamp': datetime.utcnow().isoformat()
                    },
                    ReturnValues='ALL_NEW'
                )
                return {'success': True, 'account': response['Attributes']}
            except ClientError as e:
                return {'success': False, 'error': str(e)}
    
    def activate_account(self, account_id):
        """Activate a frozen account"""
        if self.use_local:
            # Use local storage
            return self.storage.activate_account(account_id)
        else:
            # Use DynamoDB
            try:
                response = self.table.update_item(
                    Key={'AccountID': account_id},
                    UpdateExpression="SET #status = :status, UpdatedAt = :timestamp",
                    ExpressionAttributeNames={'#status': 'Status'},
                    ExpressionAttributeValues={
                        ':status': 'ACTIVE',
                        ':timestamp': datetime.utcnow().isoformat()
                    },
                    ReturnValues='ALL_NEW'
                )
                return {'success': True, 'account': response['Attributes']}
            except ClientError as e:
                return {'success': False, 'error': str(e)}
