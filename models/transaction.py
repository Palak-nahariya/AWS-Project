import boto3
from datetime import datetime, timedelta
from decimal import Decimal
from botocore.exceptions import ClientError
from config import Config
import statistics

class Transaction:
    """Transaction model for managing financial transactions in DynamoDB"""
    
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        self.table = self.dynamodb.Table(Config.DYNAMODB_TRANSACTIONS_TABLE)
    
    def create_transaction(self, transaction_id, account_id, transaction_type, 
                          amount, target_account_id=None, description=''):
        """Create a new transaction with fraud scoring"""
        try:
            timestamp = datetime.utcnow().isoformat()
            
            # Calculate fraud score
            fraud_score = self._calculate_fraud_score(account_id, amount, transaction_type)
            
            transaction_item = {
                'TransactionID': transaction_id,
                'AccountID': account_id,
                'TransactionType': transaction_type,
                'Amount': Decimal(str(amount)),
                'Date': timestamp,
                'Status': 'PENDING',
                'Description': description,
                'FraudScore': fraud_score
            }
            
            if target_account_id:
                transaction_item['TargetAccountID'] = target_account_id
            
            self.table.put_item(Item=transaction_item)
            
            return {
                'success': True,
                'transaction_id': transaction_id,
                'fraud_score': fraud_score
            }
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def update_transaction_status(self, transaction_id, status):
        """Update transaction status (COMPLETED, FAILED)"""
        try:
            response = self.table.update_item(
                Key={'TransactionID': transaction_id},
                UpdateExpression="SET #status = :status",
                ExpressionAttributeNames={'#status': 'Status'},
                ExpressionAttributeValues={':status': status},
                ReturnValues='ALL_NEW'
            )
            return {'success': True, 'transaction': response['Attributes']}
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def get_transaction(self, transaction_id):
        """Retrieve transaction by TransactionID"""
        try:
            response = self.table.get_item(Key={'TransactionID': transaction_id})
            transaction = response.get('Item')
            if transaction and 'Amount' in transaction:
                transaction['Amount'] = float(transaction['Amount'])
            return transaction
        except ClientError as e:
            print(f"Error retrieving transaction: {e}")
            return None
    
    def get_account_transactions(self, account_id, limit=50):
        """Retrieve transactions for an account"""
        try:
            response = self.table.query(
                IndexName='AccountIDIndex',
                KeyConditionExpression='AccountID = :account_id',
                ExpressionAttributeValues={':account_id': account_id},
                Limit=limit,
                ScanIndexForward=False  # Most recent first
            )
            
            transactions = response.get('Items', [])
            
            # Convert Decimal to float
            for txn in transactions:
                if 'Amount' in txn:
                    txn['Amount'] = float(txn['Amount'])
            
            return transactions
        except ClientError as e:
            print(f"Error retrieving transactions: {e}")
            return []
    
    def get_high_fraud_transactions(self, threshold=70, limit=100):
        """Retrieve transactions with high fraud scores"""
        try:
            response = self.table.query(
                IndexName='FraudScoreIndex',
                KeyConditionExpression='FraudScore >= :threshold',
                ExpressionAttributeValues={':threshold': threshold},
                Limit=limit,
                ScanIndexForward=False
            )
            
            transactions = response.get('Items', [])
            
            # Convert Decimal to float
            for txn in transactions:
                if 'Amount' in txn:
                    txn['Amount'] = float(txn['Amount'])
            
            return transactions
        except ClientError as e:
            print(f"Error retrieving high fraud transactions: {e}")
            return []
    
    def get_transactions_by_date_range(self, start_date, end_date, limit=1000):
        """Retrieve transactions within a date range"""
        try:
            response = self.table.query(
                IndexName='DateIndex',
                KeyConditionExpression='#date BETWEEN :start_date AND :end_date',
                ExpressionAttributeNames={'#date': 'Date'},
                ExpressionAttributeValues={
                    ':start_date': start_date,
                    ':end_date': end_date
                },
                Limit=limit
            )
            
            transactions = response.get('Items', [])
            
            # Convert Decimal to float
            for txn in transactions:
                if 'Amount' in txn:
                    txn['Amount'] = float(txn['Amount'])
            
            return transactions
        except ClientError as e:
            print(f"Error retrieving transactions by date: {e}")
            return []
    
    def _calculate_fraud_score(self, account_id, amount, transaction_type):
        """Calculate fraud score based on transaction patterns"""
        score = 0
        
        try:
            # Get recent transactions (last 24 hours)
            yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat()
            today = datetime.utcnow().isoformat()
            
            recent_txns = self.get_account_transactions(account_id, limit=100)
            recent_txns = [t for t in recent_txns if t.get('Date', '') >= yesterday]
            
            if not recent_txns:
                return 10  # Low score for first transaction
            
            # Factor 1: Amount anomaly (40 points max)
            amounts = [float(t['Amount']) for t in recent_txns if 'Amount' in t]
            if amounts:
                avg_amount = statistics.mean(amounts)
                if amount > avg_amount * 3:  # 3x average
                    score += 40
                elif amount > avg_amount * 2:
                    score += 25
                elif amount > avg_amount * 1.5:
                    score += 15
            
            # Factor 2: Transaction frequency (30 points max)
            txn_count_24h = len(recent_txns)
            if txn_count_24h > 20:
                score += 30
            elif txn_count_24h > 10:
                score += 20
            elif txn_count_24h > 5:
                score += 10
            
            # Factor 3: Large withdrawal/transfer (30 points max)
            if transaction_type in ['WITHDRAW', 'TRANSFER']:
                if amount > 10000:
                    score += 30
                elif amount > 5000:
                    score += 20
                elif amount > 2000:
                    score += 10
            
            # Cap score at 100
            return min(score, 100)
            
        except Exception as e:
            print(f"Error calculating fraud score: {e}")
            return 50  # Default moderate score on error
