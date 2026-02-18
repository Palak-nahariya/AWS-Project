import boto3
import bcrypt
from boto3.dynamodb.conditions import Key
from config import Config
from datetime import datetime
from botocore.exceptions import ClientError

class User:
    """User model for authentication and user management"""
    
    def __init__(self):
        # Check if using local storage
        if Config.USE_LOCAL_STORAGE:
            from local_storage import local_db
            self.storage = local_db
            self.use_local = True
        else:
            self.dynamodb = boto3.resource('dynamodb',
                region_name=Config.AWS_REGION,
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
            )
            self.table = self.dynamodb.Table(Config.DYNAMODB_USERS_TABLE)
            self.use_local = False
    
    def create_user(self, user_id, name, email, password, role='customer'):
        """Create a new user with hashed password"""
        # Hash password
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(rounds=Config.BCRYPT_ROUNDS)
        ).decode('utf-8')
        
        if self.use_local:
            # Use local storage
            try:
                self.storage.create_user(user_id, name, email, password_hash, role)
                return {'success': True, 'user_id': user_id}
            except Exception as e:
                return {'success': False, 'error': str(e)}
        else:
            # Use DynamoDB
            timestamp = datetime.utcnow().isoformat()
            
            try:
                self.table.put_item(
                    Item={
                        'UserID': user_id,
                        'Name': name,
                        'Email': email,
                        'PasswordHash': password_hash,
                        'Role': role,
                        'CreatedAt': timestamp,
                        'UpdatedAt': timestamp
                    },
                    ConditionExpression='attribute_not_exists(UserID)'
                )
                return {'success': True, 'user_id': user_id}
            except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
                return {'success': False, 'error': 'User already exists'}
            except Exception as e:
                return {'success': False, 'error': str(e)}
    
    def get_user_by_id(self, user_id):
        """Get user by UserID"""
        if self.use_local:
            # Use local storage
            return self.storage.get_user_by_id(user_id)
        else:
            # Use DynamoDB
            try:
                response = self.table.get_item(Key={'UserID': user_id})
                return response.get('Item')
            except Exception as e:
                print(f"Error getting user by ID: {e}")
                return None
    
    def get_user_by_email(self, email):
        """Get user by email address"""
        if self.use_local:
            # Use local storage
            return self.storage.get_user_by_email(email)
        else:
            # Use DynamoDB
            try:
                response = self.table.query(
                    IndexName='EmailIndex',
                    KeyConditionExpression=Key('Email').eq(email)
                )
                
                if response['Items']:
                    return response['Items'][0]
                return None
            except Exception as e:
                print(f"Error getting user by email: {e}")
                return None
    
    def verify_password(self, password, password_hash):
        """Verify a password against its hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    
    def authenticate(self, email, password):
        """Authenticate user with email and password"""
        user = self.get_user_by_email(email)
        if not user:
            return {'success': False, 'error': 'Invalid credentials'}
        
        # Check if password hash exists
        if 'PasswordHash' not in user:
            return {'success': False, 'error': 'Account not properly configured. Please contact support.'}
        
        if self.verify_password(password, user['PasswordHash']):
            # Remove password hash before returning
            user.pop('PasswordHash', None)
            return {'success': True, 'user': user}
        else:
            return {'success': False, 'error': 'Invalid credentials'}
    
    def update_user(self, user_id, updates):
        """Update user attributes"""
        try:
            update_expression = "SET UpdatedAt = :timestamp"
            expression_values = {':timestamp': datetime.utcnow().isoformat()}
            expression_names = {}
            
            for key, value in updates.items():
                if key not in ['UserID', 'PasswordHash']:  # Prevent updating ID and direct password
                    placeholder = f":{key}"
                    update_expression += f", {key} = {placeholder}"
                    expression_values[placeholder] = value
            
            response = self.table.update_item(
                Key={'UserID': user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues='ALL_NEW'
            )
            
            return {'success': True, 'user': response['Attributes']}
        except ClientError as e:
            return {'success': False, 'error': str(e)}
