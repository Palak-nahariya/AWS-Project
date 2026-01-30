import boto3
import bcrypt
from datetime import datetime
from botocore.exceptions import ClientError
from config import Config

class User:
    """User model for managing user data in DynamoDB"""
    
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        self.table = self.dynamodb.Table(Config.DYNAMODB_USERS_TABLE)
    
    def create_user(self, user_id, name, email, password, role='customer'):
        """Create a new user with hashed password"""
        try:
            # Hash the password
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt(rounds=Config.BCRYPT_ROUNDS)
            ).decode('utf-8')
            
            timestamp = datetime.utcnow().isoformat()
            
            # Create user item
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
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                return {'success': False, 'error': 'User already exists'}
            return {'success': False, 'error': str(e)}
    
    def get_user_by_id(self, user_id):
        """Retrieve user by UserID"""
        try:
            response = self.table.get_item(Key={'UserID': user_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error retrieving user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Retrieve user by email using GSI"""
        try:
            response = self.table.query(
                IndexName='EmailIndex',
                KeyConditionExpression='Email = :email',
                ExpressionAttributeValues={':email': email}
            )
            items = response.get('Items', [])
            return items[0] if items else None
        except ClientError as e:
            print(f"Error retrieving user by email: {e}")
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
