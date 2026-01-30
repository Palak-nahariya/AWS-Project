import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # DynamoDB Tables
    DYNAMODB_USERS_TABLE = os.getenv('DYNAMODB_USERS_TABLE', 'CloudBank_Users')
    DYNAMODB_ACCOUNTS_TABLE = os.getenv('DYNAMODB_ACCOUNTS_TABLE', 'CloudBank_Accounts')
    DYNAMODB_TRANSACTIONS_TABLE = os.getenv('DYNAMODB_TRANSACTIONS_TABLE', 'CloudBank_Transactions')
    
    # SNS Topics
    SNS_TRANSACTION_ALERTS_ARN = os.getenv('SNS_TRANSACTION_ALERTS_ARN')
    SNS_COMPLIANCE_ALERTS_ARN = os.getenv('SNS_COMPLIANCE_ALERTS_ARN')
    SNS_SYSTEM_ALERTS_ARN = os.getenv('SNS_SYSTEM_ALERTS_ARN')
    
    # Security Settings
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 1800))  # 30 minutes
    BCRYPT_ROUNDS = int(os.getenv('BCRYPT_ROUNDS', 12))
    
    # Fraud Detection
    FRAUD_ALERT_THRESHOLD = int(os.getenv('FRAUD_ALERT_THRESHOLD', 70))
    FRAUD_FREEZE_THRESHOLD = int(os.getenv('FRAUD_FREEZE_THRESHOLD', 90))
    
    # Session Configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = SESSION_TIMEOUT
