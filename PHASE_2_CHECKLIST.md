# Phase 2: AWS Infrastructure Setup - Checklist

## Status: 🚧 In Progress

**Estimated Time:** 2-3 hours  
**Prerequisites:** AWS Account with admin access, Phase 1 completed

---

## Overview

Phase 2 focuses on setting up the AWS infrastructure required for the Cloud Banking Application:
- 3 DynamoDB tables with Global Secondary Indexes
- 3 SNS topics for notifications
- IAM user/role configuration
- Environment configuration

---

## Step 2.1: Create DynamoDB Tables

### Table 1: Users Table ⏳

**AWS Console Steps:**
1. Navigate to **DynamoDB** service
2. Click **"Create table"**
3. Configure table:
   - **Table name**: `CloudBank_Users`
   - **Partition key**: `UserID` (String)
   - **Table settings**: On-demand (recommended) or Provisioned
   - **Encryption**: Default (AWS owned key)
4. Click **"Create table"**
5. Wait for status: **ACTIVE** (~30 seconds)

**Add Global Secondary Index:**
1. Click on the `CloudBank_Users` table
2. Go to **"Indexes"** tab
3. Click **"Create index"**
4. Configure:
   - **Partition key**: `Email` (String)
   - **Index name**: `EmailIndex`
   - **Attributes to project**: All
5. Click **"Create index"**

**Verification:**
```bash
# Test using AWS CLI (optional)
aws dynamodb describe-table --table-name CloudBank_Users
```

**Checklist:**
- [ ] Table created with name `CloudBank_Users`
- [ ] Partition key: `UserID` (String)
- [ ] EmailIndex GSI created with `Email` as partition key
- [ ] Table status: ACTIVE

---

### Table 2: Accounts Table ⏳

**AWS Console Steps:**
1. Click **"Create table"**
2. Configure:
   - **Table name**: `CloudBank_Accounts`
   - **Partition key**: `AccountID` (String)
   - **Table settings**: On-demand
3. Click **"Create table"**

**Add Global Secondary Index:**
1. Click on `CloudBank_Accounts` table
2. **Indexes** → **"Create index"**
3. Configure:
   - **Partition key**: `UserID` (String)
   - **Index name**: `UserIDIndex`
   - **Attributes to project**: All
4. Create index

**Checklist:**
- [ ] Table created: `CloudBank_Accounts`
- [ ] Partition key: `AccountID` (String)
- [ ] UserIDIndex GSI created
- [ ] Table status: ACTIVE

---

### Table 3: Transactions Table ⏳

**AWS Console Steps:**
1. Click **"Create table"**
2. Configure:
   - **Table name**: `CloudBank_Transactions`
   - **Partition key**: `TransactionID` (String)
   - **Sort key**: `Date` (String)
   - **Table settings**: On-demand
3. Click **"Create table"**

**Add Global Secondary Indexes (3 total):**

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

**Checklist:**
- [ ] Table created: `CloudBank_Transactions`
- [ ] Partition key: `TransactionID`, Sort key: `Date`
- [ ] AccountIDIndex GSI created
- [ ] DateIndex GSI created
- [ ] FraudScoreIndex GSI created
- [ ] Table status: ACTIVE

---

## Step 2.2: Create SNS Topics

### Topic 1: TransactionAlerts ⏳

**AWS Console Steps:**
1. Navigate to **SNS** (Simple Notification Service)
2. Click **"Topics"** → **"Create topic"**
3. Configure:
   - **Type**: Standard
   - **Name**: `TransactionAlerts`
   - **Display name**: `Cloud Bank Transaction Alerts`
4. Click **"Create topic"**
5. **Copy the Topic ARN** (you'll need this for .env file)

**Subscribe to Topic:**
1. Click **"Create subscription"**
2. Configure:
   - **Protocol**: Email
   - **Endpoint**: your-email@example.com
3. Click **"Create subscription"**
4. **Check your email** and confirm subscription

**Checklist:**
- [ ] Topic created: `TransactionAlerts`
- [ ] Topic ARN copied
- [ ] Email subscription created
- [ ] Email confirmed (check inbox/spam)

---

### Topic 2: ComplianceAlerts ⏳

**Steps:**
1. **"Create topic"**
   - Type: Standard
   - Name: `ComplianceAlerts`
   - Display name: `Cloud Bank Compliance Alerts`
2. Copy ARN
3. Create email subscription
4. Confirm email

**Checklist:**
- [ ] Topic created: `ComplianceAlerts`
- [ ] Topic ARN copied
- [ ] Email subscription confirmed

---

### Topic 3: SystemAlerts ⏳

**Steps:**
1. **"Create topic"**
   - Type: Standard
   - Name: `SystemAlerts`
   - Display name: `Cloud Bank System Alerts`
2. Copy ARN
3. Create email subscription
4. Confirm email

**Checklist:**
- [ ] Topic created: `SystemAlerts`
- [ ] Topic ARN copied
- [ ] Email subscription confirmed

---

## Step 2.3: Configure IAM

### Option A: IAM User with Access Keys (For Development)

**Create IAM User:**
1. Navigate to **IAM** → **Users**
2. Click **"Create user"**
3. Configure:
   - **User name**: `CloudBankAppUser`
   - **Access type**: Programmatic access
4. Click **"Next: Permissions"**

**Attach Policies:**
1. Select **"Attach policies directly"**
2. Search and select:
   - ✅ `AmazonDynamoDBFullAccess`
   - ✅ `AmazonSNSFullAccess`
3. Click **"Next"** → **"Create user"**

**Get Access Keys:**
1. Click on the created user
2. Go to **"Security credentials"** tab
3. Click **"Create access key"**
4. Select use case: **"Application running outside AWS"**
5. **IMPORTANT: Save these credentials immediately**
   - Access Key ID
   - Secret Access Key
6. Download .csv file as backup

**Checklist:**
- [ ] IAM user created: `CloudBankAppUser`
- [ ] DynamoDB policy attached
- [ ] SNS policy attached
- [ ] Access keys generated
- [ ] Keys saved securely (do NOT commit to git)

---

### Option B: EC2 Instance Role (For Production)

**Create IAM Role:**
1. **IAM** → **Roles** → **"Create role"**
2. Select trusted entity: **AWS service**
3. Use case: **EC2**
4. Attach policies:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`
5. Role name: `CloudBankEC2Role`
6. Create role

**Note:** Attach this role when launching EC2 instance (Phase 14)

**Checklist:**
- [ ] Role created: `CloudBankEC2Role`
- [ ] Policies attached

---

## Step 2.4: Update Environment Configuration

### Edit .env File

Open `C:\Users\khurai\OneDrive\Desktop\AWS Project\.env` and update:

```bash
# AWS Configuration
AWS_REGION=us-east-1  # Change to your region
AWS_ACCESS_KEY_ID=AKIA...  # Your access key
AWS_SECRET_ACCESS_KEY=...   # Your secret key

# DynamoDB Tables
DYNAMODB_USERS_TABLE=CloudBank_Users
DYNAMODB_ACCOUNTS_TABLE=CloudBank_Accounts
DYNAMODB_TRANSACTIONS_TABLE=CloudBank_Transactions

# SNS Topics (paste your ARNs)
SNS_TRANSACTION_ALERTS_ARN=arn:aws:sns:us-east-1:123456789012:TransactionAlerts
SNS_COMPLIANCE_ALERTS_ARN=arn:aws:sns:us-east-1:123456789012:ComplianceAlerts
SNS_SYSTEM_ALERTS_ARN=arn:aws:sns:us-east-1:123456789012:SystemAlerts

# Flask Configuration
FLASK_SECRET_KEY=change-this-to-very-long-random-string-xyz123
FLASK_ENV=development
DEBUG=True

# Security
SESSION_TIMEOUT=1800
BCRYPT_ROUNDS=12

# Fraud Detection
FRAUD_ALERT_THRESHOLD=70
FRAUD_FREEZE_THRESHOLD=90
```

**Generate Secret Key:**
```bash
# In Python
python -c "import secrets; print(secrets.token_hex(32))"
```

**Checklist:**
- [ ] AWS_REGION set to your region
- [ ] AWS_ACCESS_KEY_ID added
- [ ] AWS_SECRET_ACCESS_KEY added
- [ ] All 3 DynamoDB table names verified
- [ ] All 3 SNS ARNs pasted
- [ ] FLASK_SECRET_KEY generated and set
- [ ] File saved

---

## Step 2.5: Test AWS Connection

### Test DynamoDB Connection

Create test file: `test_aws_connection.py`

```python
import boto3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Test DynamoDB connection
dynamodb = boto3.resource('dynamodb',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

try:
    # Test Users table
    users_table = dynamodb.Table(os.getenv('DYNAMODB_USERS_TABLE'))
    print(f"✅ Users table status: {users_table.table_status}")
    
    # Test Accounts table
    accounts_table = dynamodb.Table(os.getenv('DYNAMODB_ACCOUNTS_TABLE'))
    print(f"✅ Accounts table status: {accounts_table.table_status}")
    
    # Test Transactions table
    transactions_table = dynamodb.Table(os.getenv('DYNAMODB_TRANSACTIONS_TABLE'))
    print(f"✅ Transactions table status: {transactions_table.table_status}")
    
    print("\n🎉 All DynamoDB tables accessible!")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

**Run test:**
```bash
. venv\Scripts\Activate.ps1
python test_aws_connection.py
```

**Expected Output:**
```
✅ Users table status: ACTIVE
✅ Accounts table status: ACTIVE
✅ Transactions table status: ACTIVE

🎉 All DynamoDB tables accessible!
```

---

### Test SNS Connection

Add to `test_aws_connection.py`:

```python
# Test SNS connection
sns = boto3.client('sns',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

try:
    response = sns.publish(
        TopicArn=os.getenv('SNS_SYSTEM_ALERTS_ARN'),
        Message='Test message from Cloud Bank Application',
        Subject='AWS Connection Test'
    )
    print(f"\n✅ SNS message sent! MessageId: {response['MessageId']}")
    print("📧 Check your email for test notification")
    
except Exception as e:
    print(f"❌ SNS Error: {e}")
```

**Checklist:**
- [ ] test_aws_connection.py created
- [ ] DynamoDB test passes (all 3 tables ACTIVE)
- [ ] SNS test passes (email received)
- [ ] No credential errors

---

## Step 2.6: Verify Table Indexes

### Check Global Secondary Indexes

**For each table, verify GSIs exist:**

```python
# Verify indexes
def check_indexes():
    users_table = dynamodb.Table('CloudBank_Users')
    print("Users GSIs:", [idx['IndexName'] for idx in users_table.global_secondary_indexes or []])
    
    accounts_table = dynamodb.Table('CloudBank_Accounts')
    print("Accounts GSIs:", [idx['IndexName'] for idx in accounts_table.global_secondary_indexes or []])
    
    transactions_table = dynamodb.Table('CloudBank_Transactions')
    print("Transactions GSIs:", [idx['IndexName'] for idx in transactions_table.global_secondary_indexes or []])

check_indexes()
```

**Expected Output:**
```
Users GSIs: ['EmailIndex']
Accounts GSIs: ['UserIDIndex']
Transactions GSIs: ['AccountIDIndex', 'DateIndex', 'FraudScoreIndex']
```

**Checklist:**
- [ ] Users: EmailIndex exists
- [ ] Accounts: UserIDIndex exists
- [ ] Transactions: All 3 indexes exist

---

## Phase 2 Summary

### What You Created:

**DynamoDB Tables:**
- ✅ CloudBank_Users (with EmailIndex)
- ✅ CloudBank_Accounts (with UserIDIndex)
- ✅ CloudBank_Transactions (with 3 indexes)

**SNS Topics:**
- ✅ TransactionAlerts
- ✅ ComplianceAlerts
- ✅ SystemAlerts

**IAM Configuration:**
- ✅ User/Role with DynamoDB + SNS permissions
- ✅ Access keys secured

**Configuration:**
- ✅ .env file updated with all AWS details
- ✅ Connection tested successfully

---

## Cost Estimation

**DynamoDB (On-Demand):**
- Free tier: 25 GB storage, 25 WCU, 25 RCU
- After free tier: $1.25 per million write requests
- Estimated: $0-5/month for development

**SNS:**
- Free tier: 1,000 email notifications/month
- After free tier: $2 per 100,000 emails
- Estimated: $0-2/month

**IAM:**
- Free (no charges)

**Total Estimated Cost:** $0-10/month (likely $0 with free tier)

---

## Troubleshooting

### Issue: Table creation fails
**Solution:** Check AWS region, ensure sufficient permissions

### Issue: Can't create indexes
**Solution:** Wait for table to be ACTIVE before adding GSIs

### Issue: SNS email not received
**Solution:** Check spam folder, verify subscription confirmed

### Issue: Connection test fails
**Solution:** 
- Verify .env credentials are correct
- Check AWS region matches
- Ensure IAM policies attached
- Verify no typos in table/topic names

---

## Next Steps

Once Phase 2 is complete:
1. ✅ Proceed to **Phase 3: Test the Application**
2. Register a test user
3. Test banking operations
4. Verify fraud detection
5. Test analytics dashboards

**Ready to test?** Run: `python app.py` and visit `http://localhost:5000`

---

## Phase 2 Completion Checklist

- [ ] All 3 DynamoDB tables created with correct schemas
- [ ] All 6 Global Secondary Indexes created
- [ ] All 3 SNS topics created
- [ ] Email subscriptions confirmed
- [ ] IAM user/role configured
- [ ] .env file updated with all credentials and ARNs
- [ ] Connection test passes for DynamoDB
- [ ] Connection test passes for SNS
- [ ] Index verification successful

**Phase 2 Status:** ⏳ In Progress  
**Estimated Time Remaining:** 1.5-2.5 hours

---

**Need help?** Refer to [AWS_SETUP_GUIDE.md](file:///C:/Users/khurai/OneDrive/Desktop/AWS%20Project/AWS_SETUP_GUIDE.md) for detailed AWS instructions.
