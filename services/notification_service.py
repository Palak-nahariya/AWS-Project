import boto3
from config import Config

class NotificationService:
    """SNS notification service for alerts"""
    
    def __init__(self):
        self.sns_client = boto3.client(
            'sns',
            region_name=Config.AWS_REGION,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
    
    def send_transaction_alert(self, message, subject='Transaction Alert'):
        """Send transaction fraud alert via SNS"""
        try:
            if not Config.SNS_TRANSACTION_ALERTS_ARN:
                print("SNS Transaction Alerts ARN not configured")
                return {'success': False, 'error': 'SNS not configured'}
            
            response = self.sns_client.publish(
                TopicArn=Config.SNS_TRANSACTION_ALERTS_ARN,
                Message=message,
                Subject=subject
            )
            
            return {'success': True, 'message_id': response['MessageId']}
        except Exception as e:
            print(f"Error sending transaction alert: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_compliance_alert(self, message, subject='Compliance Alert'):
        """Send compliance threshold alert via SNS"""
        try:
            if not Config.SNS_COMPLIANCE_ALERTS_ARN:
                print("SNS Compliance Alerts ARN not configured")
                return {'success': False, 'error': 'SNS not configured'}
            
            response = self.sns_client.publish(
                TopicArn=Config.SNS_COMPLIANCE_ALERTS_ARN,
                Message=message,
                Subject=subject
            )
            
            return {'success': True, 'message_id': response['MessageId']}
        except Exception as e:
            print(f"Error sending compliance alert: {e}")
            return {'success': False, 'error': str(e)}
    
    def send_system_alert(self, message, subject='System Alert'):
        """Send system alert via SNS"""
        try:
            if not Config.SNS_SYSTEM_ALERTS_ARN:
                print("SNS System Alerts ARN not configured")
                return {'success': False, 'error': 'SNS not configured'}
            
            response = self.sns_client.publish(
                TopicArn=Config.SNS_SYSTEM_ALERTS_ARN,
                Message=message,
                Subject=subject
            )
            
            return {'success': True, 'message_id': response['MessageId']}
        except Exception as e:
            print(f"Error sending system alert: {e}")
            return {'success': False, 'error': str(e)}
    
    def notify_high_fraud_transaction(self, transaction_id, account_id, amount, fraud_score):
        """Send notification for high fraud score transaction"""
        message = f"""
High Fraud Score Transaction Detected!

Transaction ID: {transaction_id}
Account ID: {account_id}
Amount: ${amount:.2f}
Fraud Score: {fraud_score}/100

Please review this transaction immediately.
        """
        
        return self.send_transaction_alert(
            message,
            subject=f'High Fraud Alert - Score {fraud_score}'
        )
    
    def notify_account_frozen(self, account_id, reason='Suspicious activity detected'):
        """Send notification when account is frozen"""
        message = f"""
Account Frozen Alert!

Account ID: {account_id}
Reason: {reason}

The account has been automatically frozen. Please review and take appropriate action.
        """
        
        return self.send_transaction_alert(
            message,
            subject='Account Frozen - Immediate Action Required'
        )
