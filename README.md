# Cloud Bank Analytics - AWS Banking Application

A comprehensive cloud-based banking application featuring secure account management, financial transactions, and advanced analytics powered by AWS services.

## 🌟 Features

### Core Banking Operations
- **User Authentication**: Secure registration and login with bcrypt password hashing
- **Account Management**: View balances, account status, and account information
- **Deposits**: Add funds to accounts with transaction tracking
- **Withdrawals**: Withdraw funds with fraud detection
- **Transfers**: Transfer money between accounts securely
- **Transaction History**: Complete audit trail of all transactions

### Advanced Analytics (Role-Based)

#### 1. Real-time Fraud Monitoring (Analyst Role)
Scenario: Sarah, a fraud detection analyst, monitors suspicious transactions
- Live transaction feed with fraud scoring
- Critical/High/Medium risk categorization
- Investigation tools and detailed transaction analysis
- Account freeze/approve actions
- Automatic SNS alerts for high-risk transactions

#### 2. Custom Report Generation (Manager Role)
Scenario: John, a financial manager, generates comprehensive reports
- Financial metrics dashboard
- Transaction volume analysis
- Deposit growth trends
- Interactive charts and visualizations
- Custom date range selection

#### 3. Regulatory Compliance Monitoring (Compliance Officer Role)
Scenario: Lisa, a compliance officer, tracks regulatory requirements
- Large transaction monitoring (>$10,000)
- Suspicious activity tracking
- Transaction failure rate metrics
- Progress meters with thresholds
- Drill-down investigation tools

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python Flask
- **Database**: AWS DynamoDB (NoSQL)
- **Notifications**: AWS SNS
- **Hosting**: AWS EC2
- **Authentication**: AWS IAM
- **Security**: bcrypt, Flask sessions

### Database Schema

**Users Table**
- UserID (PK), Name, Email, PasswordHash, Role, CreatedAt, UpdatedAt
- GSI: EmailIndex (for authentication)

**Accounts Table**
- AccountID (PK), UserID, Balance, AccountType, Status, CreatedAt, UpdatedAt
- GSI: UserIDIndex (for account lookup)

**Transactions Table**
- TransactionID (PK), Date (SK), AccountID, TargetAccountID, TransactionType, Amount, Status, FraudScore
- GSI: AccountIDIndex, DateIndex, FraudScoreIndex

## 📦 Installation

### Prerequisites
- Python 3.8+
- AWS Account with configured credentials
- pip package manager

### Local Setup

1. **Clone or navigate to the project directory**
```bash
cd "C:\Users\khurai\OneDrive\Desktop\AWS Project"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update AWS credentials and configuration
   - Set Flask secret key

4. **Set up AWS infrastructure** (See AWS Setup Guide below)

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
   - Open browser to `http://localhost:5000`

## ⚙️ AWS Setup Guide

### Step 1: Create DynamoDB Tables

**Users Table:**
```
Table Name: CloudBank_Users
Primary Key: UserID (String)
Global Secondary Index:
  - EmailIndex: Email (PK)
```

**Accounts Table:**
```
Table Name: CloudBank_Accounts
Primary Key: AccountID (String)
Global Secondary Index:
  - UserIDIndex: UserID (PK)
```

**Transactions Table:**
```
Table Name: CloudBank_Transactions
Primary Key: TransactionID (String)
Sort Key: Date (String)
Global Secondary Indexes:
  - AccountIDIndex: AccountID (PK), Date (SK)
  - DateIndex: Date (PK)
  - FraudScoreIndex: FraudScore (Number - PK)
```

### Step 2: Create SNS Topics

Create three SNS topics:
- `TransactionAlerts`: For fraud detection notifications
- `ComplianceAlerts`: For compliance threshold warnings
- `SystemAlerts`: For system health monitoring

Subscribe email addresses to receive notifications.

### Step 3: Configure IAM

Create IAM role with policies:
- `AmazonDynamoDBFullAccess`
- `AmazonSNSFullAccess`

Attach role to EC2 instance or create access keys for local development.

### Step 4: Update Environment Variables

Update `.env` file with your AWS configuration:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
DYNAMODB_USERS_TABLE=CloudBank_Users
DYNAMODB_ACCOUNTS_TABLE=CloudBank_Accounts
DYNAMODB_TRANSACTIONS_TABLE=CloudBank_Transactions
SNS_TRANSACTION_ALERTS_ARN=arn:aws:sns:...
SNS_COMPLIANCE_ALERTS_ARN=arn:aws:sns:...
SNS_SYSTEM_ALERTS_ARN=arn:aws:sns:...
```

## 👥 User Roles

The application supports four user roles:

1. **Customer**: Standard banking operations (deposit, withdraw, transfer)
2. **Analyst**: Fraud detection analyst with access to fraud monitoring dashboard
3. **Manager**: Financial manager with access to custom reports
4. **Compliance**: Compliance officer with access to regulatory monitoring

Register with different roles to access role-specific features.

## 🔒 Security Features

- **Password Hashing**: bcrypt with 12 rounds
- **Session Management**: Secure HTTP-only cookies with 30-minute timeout
- **Fraud Detection**: Real-time scoring algorithm based on:
  - Amount anomalies (compared to user history)
  - Transaction frequency patterns
  - Large withdrawal/transfer monitoring
- **Account Freezing**: Automatic freeze for fraud scores ≥ 90
- **SNS Alerts**: Real-time notifications for suspicious activity

## 🎨 Design Features

- **Modern Dark Theme**: Premium glassmorphism design
- **Responsive Layout**: Mobile-friendly interface
- **Smooth Animations**: Fade-in effects and hover transitions
- **Interactive Charts**: Chart.js visualizations for reports
- **Color-Coded Alerts**: Intuitive visual feedback for fraud levels

## 📊 Fraud Detection Algorithm

The system calculates a fraud score (0-100) based on:

1. **Amount Anomaly (40 points max)**
   - Compares transaction amount to user's average
   - >3x average: 40 points
   - >2x average: 25 points
   - >1.5x average: 15 points

2. **Transaction Frequency (30 points max)**
   - >20 transactions in 24h: 30 points
   - >10 transactions in 24h: 20 points
   - >5 transactions in 24h: 10 points

3. **Large Withdrawal/Transfer (30 points max)**
   - >$10,000: 30 points
   - >$5,000: 20 points
   - >$2,000: 10 points

**Actions Triggered:**
- Score ≥ 70: SNS alert sent
- Score ≥ 90: Account automatically frozen, transaction blocked

## 🚀 Deployment (Production)

### EC2 Deployment

1. Launch EC2 instance (t2.small or larger)
2. Install Python and dependencies
3. Configure environment variables
4. Set up gunicorn process manager
5. Configure nginx reverse proxy
6. Enable HTTPS with Let's Encrypt
7. Set up systemd service for auto-restart

### Security Checklist
- ✓ HTTPS enabled
- ✓ Secure session configuration
- ✓ CSRF protection
- ✓ Input validation
- ✓ DynamoDB encryption at rest
- ✓ Restricted IAM permissions
- ✓ Security groups configured
- ✓ CloudWatch logging enabled

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

This is an AWS demonstration project showcasing cloud architecture best practices.

## 📧 Support

For issues or questions, please refer to the AWS documentation for DynamoDB, SNS, and EC2 services.
