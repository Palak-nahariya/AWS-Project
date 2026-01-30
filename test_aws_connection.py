import boto3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("=" * 60)
print("Cloud Bank AWS Connection Test")
print("=" * 60)

# Test DynamoDB connection
print("\n📊 Testing DynamoDB Connection...")
dynamodb = boto3.resource('dynamodb',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

try:
    # Test Users table
    users_table = dynamodb.Table(os.getenv('DYNAMODB_USERS_TABLE'))
    print(f"✅ Users table: {users_table.table_status}")
    users_gsis = [idx['IndexName'] for idx in users_table.global_secondary_indexes or []]
    print(f"   GSIs: {users_gsis}")
    
    # Test Accounts table
    accounts_table = dynamodb.Table(os.getenv('DYNAMODB_ACCOUNTS_TABLE'))
    print(f"✅ Accounts table: {accounts_table.table_status}")
    accounts_gsis = [idx['IndexName'] for idx in accounts_table.global_secondary_indexes or []]
    print(f"   GSIs: {accounts_gsis}")
    
    # Test Transactions table
    transactions_table = dynamodb.Table(os.getenv('DYNAMODB_TRANSACTIONS_TABLE'))
    print(f"✅ Transactions table: {transactions_table.table_status}")
    transactions_gsis = [idx['IndexName'] for idx in transactions_table.global_secondary_indexes or []]
    print(f"   GSIs: {transactions_gsis}")
    
    print("\n🎉 All DynamoDB tables accessible!")
    
    # Verify required indexes
    print("\n🔍 Verifying Required Indexes...")
    errors = []
    
    if 'EmailIndex' not in users_gsis:
        errors.append("❌ Missing EmailIndex on Users table")
    else:
        print("✅ Users EmailIndex found")
    
    if 'UserIDIndex' not in accounts_gsis:
        errors.append("❌ Missing UserIDIndex on Accounts table")
    else:
        print("✅ Accounts UserIDIndex found")
    
    required_txn_indexes = ['AccountIDIndex', 'DateIndex', 'FraudScoreIndex']
    for idx in required_txn_indexes:
        if idx not in transactions_gsis:
            errors.append(f"❌ Missing {idx} on Transactions table")
        else:
            print(f"✅ Transactions {idx} found")
    
    if errors:
        print("\n⚠️  Index Issues Found:")
        for error in errors:
            print(f"  {error}")
    else:
        print("\n✅ All required indexes verified!")
    
except Exception as e:
    print(f"❌ DynamoDB Error: {e}")
    print("\n💡 Troubleshooting:")
    print("  1. Check AWS credentials in .env file")
    print("  2. Verify region is correct")
    print("  3. Ensure DynamoDB tables are created")
    print("  4. Confirm IAM permissions (DynamoDB access)")

# Test SNS connection
print("\n" + "=" * 60)
print("📧 Testing SNS Connection...")
sns = boto3.client('sns',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

try:
    # Check if topics exist
    topics = [
        ('Transaction Alerts', os.getenv('SNS_TRANSACTION_ALERTS_ARN')),
        ('Compliance Alerts', os.getenv('SNS_COMPLIANCE_ALERTS_ARN')),
        ('System Alerts', os.getenv('SNS_SYSTEM_ALERTS_ARN'))
    ]
    
    for topic_name, topic_arn in topics:
        if topic_arn and 'arn:aws:sns' in topic_arn:
            print(f"✅ {topic_name}: {topic_arn}")
        else:
            print(f"❌ {topic_name}: ARN not configured")
    
    # Send test message
    system_alerts_arn = os.getenv('SNS_SYSTEM_ALERTS_ARN')
    if system_alerts_arn and 'arn:aws:sns' in system_alerts_arn:
        response = sns.publish(
            TopicArn=system_alerts_arn,
            Message='🎉 AWS connection test successful! Your Cloud Bank application can now send notifications.',
            Subject='Cloud Bank - AWS Connection Test'
        )
        print(f"\n✅ Test notification sent! MessageId: {response['MessageId']}")
        print("📧 Check your email inbox (including spam folder)")
    else:
        print("\n⚠️  Skipping test notification (SNS ARN not configured)")
    
except Exception as e:
    print(f"❌ SNS Error: {e}")
    print("\n💡 Troubleshooting:")
    print("  1. Verify SNS topic ARNs in .env file")
    print("  2. Check email subscriptions are confirmed")
    print("  3. Ensure IAM permissions (SNS access)")

print("\n" + "=" * 60)
print("✅ Connection test complete!")
print("=" * 60)
