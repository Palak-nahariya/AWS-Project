# AWS Infrastructure Setup Guide

This guide provides step-by-step instructions for setting up the AWS infrastructure required for the Cloud Bank Analytics application.

## Prerequisites

- AWS Account with admin access
- AWS CLI installed and configured (optional but recommended)
- Basic understanding of AWS services

## Table of Contents

1. [DynamoDB Tables Setup](#1-dynamodb-tables-setup)
2. [SNS Topics Setup](#2-sns-topics-setup)
3. [IAM Configuration](#3-iam-configuration)
4. [EC2 Instance Setup](#4-ec2-instance-setup)
5. [Environment Configuration](#5-environment-configuration)

---

## 1. DynamoDB Tables Setup

### Users Table

1. Navigate to DynamoDB in AWS Console
2. Click "Create table"
3. Configure:
   - **Table name**: `CloudBank_Users`
   - **Partition key**: `UserID` (String)
   - Leave default settings (On-demand or Provisioned capacity)
4. Click "Create table"
5. After creation, add Global Secondary Index:
   - Click on the table → "Indexes" tab → "Create index"
   - **Partition key**: `Email` (String)
   - **Index name**: `EmailIndex`
   - Click "Create index"

### Accounts Table

1. Click "Create table"
2. Configure:
   - **Table name**: `CloudBank_Accounts`
   - **Partition key**: `AccountID` (String)
3. Click "Create table"
4. Add Global Secondary Index:
   - **Partition key**: `UserID` (String)
   - **Index name**: `UserIDIndex`

### Transactions Table

1. Click "Create table"
2. Configure:
   - **Table name**: `CloudBank_Transactions`
   - **Partition key**: `TransactionID` (String)
   - **Sort key**: `Date` (String)
3. Click "Create table"
4. Add three Global Secondary Indexes:
   
   **Index 1: AccountIDIndex**
   - Partition key: `AccountID` (String)
   - Sort key: `Date` (String)
   - Index name: `AccountIDIndex`
   
   **Index 2: DateIndex**
   - Partition key: `Date` (String)
   - Index name: `DateIndex`
   
   **Index 3: FraudScoreIndex**
   - Partition key: `FraudScore` (Number)
   - Index name: `FraudScoreIndex`

---

## 2. SNS Topics Setup

### Create Topics

1. Navigate to SNS (Simple Notification Service) in AWS Console
2. Click "Topics" → "Create topic"

Create **three topics**:

**Topic 1: TransactionAlerts**
- Type: Standard
- Name: `TransactionAlerts`
- Display name: `Cloud Bank Transaction Alerts`

**Topic 2: ComplianceAlerts**
- Type: Standard
- Name: `ComplianceAlerts`
- Display name: `Cloud Bank Compliance Alerts`

**Topic 3: SystemAlerts**
- Type: Standard
- Name: `SystemAlerts`
- Display name: `Cloud Bank System Alerts`

### Subscribe to Topics

For each topic:
1. Click on the topic
2. Click "Create subscription"
3. Select Protocol: `Email`
4. Enter your email address
5. Click "Create subscription"
6. Check your email and confirm the subscription

**Note**: Copy each topic ARN for the environment configuration later.

---

## 3. IAM Configuration

### Option A: EC2 Instance Role (Recommended for Production)

1. Navigate to IAM → Roles → "Create role"
2. Select "AWS service" → "EC2" → Click "Next"
3. Attach policies:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`
4. Name: `CloudBankEC2Role`
5. Click "Create role"
6. Attach this role to your EC2 instance when launching

### Option B: Access Keys (For Local Development)

1. Navigate to IAM → Users → "Create user"
2. Username: `CloudBankAppUser`
3. Select "Programmatic access"
4. Attach policies directly:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`
5. Click through and create user
6. **Important**: Save the Access Key ID and Secret Access Key
7. Use these in your `.env` file

---

## 4. EC2 Instance Setup

### Launch Instance

1. Navigate to EC2 → "Launch Instance"
2. Configure:
   - **Name**: `CloudBankServer`
   - **AMI**: Amazon Linux 2 or Ubuntu Server 22.04
   - **Instance type**: t2.micro (free tier) or t2.small
   - **Key pair**: Create new or use existing
   - **Network settings**:
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere (0.0.0.0/0)
     - Allow HTTPS (port 443) from anywhere (0.0.0.0/0)
     - Allow Custom TCP (port 5000) for Flask development
3. **IAM instance profile**: Select `CloudBankEC2Role` (if using)
4. Launch instance

### Connect to Instance

```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

### Install Dependencies

```bash
# Update system
sudo yum update -y  # For Amazon Linux
# OR
sudo apt update && sudo apt upgrade -y  # For Ubuntu

# Install Python 3 and pip
sudo yum install python3 python3-pip -y  # Amazon Linux
# OR
sudo apt install python3 python3-pip -y  # Ubuntu

# Install git (optional)
sudo yum install git -y
# OR
sudo apt install git -y
```

### Deploy Application

```bash
# Create application directory
mkdir ~/cloud-bank
cd ~/cloud-bank

# Upload your application files (or clone from git)
# You can use scp, git, or other methods

# Install Python dependencies
pip3 install -r requirements.txt

# Create .env file with your configuration
nano .env
```

### Run Application

```bash
# For development
python3 app.py

# For production with gunicorn
pip3 install gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

### Optional: Set up as System Service

Create `/etc/systemd/system/cloudbank.service`:
```ini
[Unit]
Description=Cloud Bank Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/cloud-bank
Environment="PATH=/usr/local/bin"
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable cloudbank
sudo systemctl start cloudbank
```

---

## 5. Environment Configuration

Create a `.env` file in your project root:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=AKIA...  # Only if using access keys
AWS_SECRET_ACCESS_KEY=...   # Only if using access keys

# DynamoDB Tables
DYNAMODB_USERS_TABLE=CloudBank_Users
DYNAMODB_ACCOUNTS_TABLE=CloudBank_Accounts
DYNAMODB_TRANSACTIONS_TABLE=CloudBank_Transactions

# SNS Topics (Copy ARNs from SNS console)
SNS_TRANSACTION_ALERTS_ARN=arn:aws:sns:us-east-1:123456789012:TransactionAlerts
SNS_COMPLIANCE_ALERTS_ARN=arn:aws:sns:us-east-1:123456789012:ComplianceAlerts
SNS_SYSTEM_ALERTS_ARN=arn:aws:sns:us-east-1:123456789012:SystemAlerts

# Flask Configuration
FLASK_SECRET_KEY=your-very-secret-key-change-this-in-production
FLASK_ENV=production
DEBUG=False

# Security
SESSION_TIMEOUT=1800
BCRYPT_ROUNDS=12

# Fraud Detection Thresholds
FRAUD_ALERT_THRESHOLD=70
FRAUD_FREEZE_THRESHOLD=90
```

---

## Verification Steps

### Test DynamoDB Access

```python
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('CloudBank_Users')
print(table.table_status)  # Should print 'ACTIVE'
```

### Test SNS Access

```python
import boto3

sns = boto3.client('sns', region_name='us-east-1')
response = sns.publish(
    TopicArn='your-topic-arn',
    Message='Test message',
    Subject='Test'
)
print(response)  # Should return MessageId
```

---

## Costs Estimation

**DynamoDB**: 
- Free tier: 25 GB storage, 25 WCU, 25 RCU
- On-demand pricing after free tier

**SNS**:
- Free tier: 1,000 email notifications/month
- $2 per 100,000 notifications after

**EC2**:
- t2.micro: Free tier eligible (750 hours/month)
- t2.small: ~$17/month

**Estimated monthly cost**: $0-30 depending on usage and free tier eligibility

---

## Security Best Practices

1. **Enable DynamoDB encryption at rest** (default enabled)
2. **Use IAM roles instead of access keys** when possible
3. **Restrict security group rules** to minimum required ports
4. **Enable CloudWatch logging** for monitoring
5. **Use HTTPS in production** with SSL certificate
6. **Rotate credentials regularly**
7. **Enable MFA** for AWS account
8. **Use VPC** for network isolation (optional)

---

## Troubleshooting

### DynamoDB Connection Issues
- Verify IAM permissions
- Check AWS credentials in .env file
- Ensure table names match exactly
- Verify region configuration

### SNS Not Sending Emails
- Confirm email subscription
- Check spam folder
- Verify SNS topic ARN
- Check IAM permissions

### EC2 Connection Issues
- Verify security group allows inbound traffic
- Check instance is running
- Verify key pair permissions (chmod 400)
- Check public IP address

---

## Next Steps

After infrastructure setup:
1. Test the application locally
2. Create initial test users with different roles
3. Test all banking operations
4. Test fraud detection with high-value transactions
5. Verify SNS notifications are received
6. Test analytics dashboards for each role
7. Deploy to production EC2 instance
8. Set up monitoring and alerting

---

## Support Resources

- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
- [AWS SNS Documentation](https://docs.aws.amazon.com/sns/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
