# Cloud Bank Analytics - Phase Implementation Guide

This guide provides a step-by-step approach to building the Cloud Banking Application in manageable phases. Follow these phases sequentially to build the complete system.

---

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.8+ installed
- AWS account with admin access
- Code editor (VS Code, PyCharm, etc.)
- Basic knowledge of Flask and AWS services
- Git (optional, for version control)

---

## Phase 1: Project Foundation (Est. Time: 1-2 hours)

### Step 1.1: Project Setup
```bash
# Create project directory
mkdir cloud-bank-analytics
cd cloud-bank-analytics

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 1.2: Install Core Dependencies
Create `requirements.txt`:
```
Flask==3.0.0
boto3==1.34.0
bcrypt==4.1.2
python-dotenv==1.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

Install:
```bash
pip install -r requirements.txt
```

### Step 1.3: Create Project Structure
```bash
# Create directories
mkdir models services routes templates static
mkdir templates/analytics static/css
```

### Step 1.4: Configuration Setup
Create `config.py`:
- Load environment variables
- Configure Flask settings
- Set AWS credentials
- Define security parameters

Create `.env.example`:
- Template for AWS credentials
- DynamoDB table names
- SNS topic ARNs
- Security settings

### Step 1.5: Basic Flask App
Create `app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Cloud Bank - Coming Soon"

if __name__ == '__main__':
    app.run(debug=True)
```

**Test**: Run `python app.py` and visit `http://localhost:5000`

---

## Phase 2: AWS Infrastructure Setup (Est. Time: 2-3 hours)

### Step 2.1: Create DynamoDB Tables

**Users Table:**
1. AWS Console → DynamoDB → Create table
2. Table name: `CloudBank_Users`
3. Partition key: `UserID` (String)
4. Add GSI: `EmailIndex` with `Email` as partition key

**Accounts Table:**
1. Table name: `CloudBank_Accounts`
2. Partition key: `AccountID` (String)
3. Add GSI: `UserIDIndex` with `UserID` as partition key

**Transactions Table:**
1. Table name: `CloudBank_Transactions`
2. Partition key: `TransactionID` (String)
3. Sort key: `Date` (String)
4. Add GSIs:
   - `AccountIDIndex`: AccountID (PK), Date (SK)
   - `DateIndex`: Date (PK)
   - `FraudScoreIndex`: FraudScore (Number, PK)

### Step 2.2: Configure SNS Topics
Create three topics:
- `TransactionAlerts`
- `ComplianceAlerts`
- `SystemAlerts`

Subscribe your email to each topic and confirm subscriptions.

### Step 2.3: Set up IAM
Create IAM user with policies:
- `AmazonDynamoDBFullAccess`
- `AmazonSNSFullAccess`

Save access keys for `.env` file.

### Step 2.4: Update Environment
Copy `.env.example` to `.env` and fill in:
- AWS credentials
- Table names
- SNS ARNs

**Test**: Run a simple boto3 script to verify DynamoDB connection

---

## Phase 3: Data Models (Est. Time: 3-4 hours)

### Step 3.1: User Model
Create `models/user.py`:
- `create_user()` - Hash password with bcrypt
- `get_user_by_id()` - Retrieve by UserID
- `get_user_by_email()` - Query EmailIndex
- `verify_password()` - bcrypt comparison
- `authenticate()` - Email/password login
- `update_user()` - Profile updates

**Test**: Create test script to register and login a user

### Step 3.2: Account Model
Create `models/account.py`:
- `create_account()` - Initialize with balance
- `get_account()` - Retrieve by AccountID
- `get_accounts_by_user()` - Query UserIDIndex
- `update_balance()` - Atomic ADD/SUBTRACT
- `freeze_account()` - Set status to FROZEN
- `activate_account()` - Set status to ACTIVE

**Test**: Create account and test balance operations

### Step 3.3: Transaction Model
Create `models/transaction.py`:
- `create_transaction()` - Record with fraud scoring
- `get_transaction()` - Retrieve by ID
- `get_account_transactions()` - Query AccountIDIndex
- `get_high_fraud_transactions()` - Query FraudScoreIndex
- `get_transactions_by_date_range()` - Query DateIndex
- `_calculate_fraud_score()` - Scoring algorithm

**Fraud Scoring Implementation:**
1. Implement amount anomaly detection (40 pts max)
2. Add frequency analysis (30 pts max)
3. Add large transaction risk (30 pts max)

**Test**: Create transactions and verify fraud scores

### Step 3.4: Models Package
Create `models/__init__.py` to export all models.

---

## Phase 4: Business Logic Services (Est. Time: 3-4 hours)

### Step 4.1: Authentication Service
Create `services/auth_service.py`:
- `register()` - Validate input, create user
- `login()` - Authenticate credentials
- `get_user()` - Session validation
- `update_profile()` - Safe profile updates

**Test**: Register users with different roles

### Step 4.2: Banking Service
Create `services/banking_service.py`:
- `create_account()` - Account creation
- `get_user_accounts()` - User's accounts
- `deposit()` - Add funds with transaction tracking
- `withdraw()` - Deduct funds with fraud check
- `transfer()` - Account-to-account with rollback
- `get_transaction_history()` - Transaction list

**Key Features:**
- Automatic account freeze for fraud score ≥90
- Transaction status tracking (PENDING → COMPLETED/FAILED)
- Rollback mechanism for failed transfers

**Test**: Perform all banking operations

### Step 4.3: Notification Service
Create `services/notification_service.py`:
- `send_transaction_alert()` - Fraud notifications
- `send_compliance_alert()` - Threshold warnings
- `send_system_alert()` - System health
- `notify_high_fraud_transaction()` - Specific fraud alert
- `notify_account_frozen()` - Account freeze notice

**Test**: Trigger notifications and check email

### Step 4.4: Analytics Service
Create `services/analytics_service.py`:

**Scenario 1 Methods:**
- `get_fraud_monitoring_dashboard()` - Categorized alerts
- `get_recent_transactions_feed()` - Live feed
- `investigate_transaction()` - Detailed view

**Scenario 2 Methods:**
- `generate_financial_report()` - Comprehensive metrics
- `get_deposit_growth_trends()` - Trend analysis
- `get_transaction_volume_analysis()` - Volume patterns

**Scenario 3 Methods:**
- `get_compliance_dashboard()` - Regulatory metrics
- `drill_down_compliance_metric()` - Investigation

**Test**: Generate reports with sample data

### Step 4.5: Services Package
Create `services/__init__.py` to export all services.

---

## Phase 5: Frontend Design System (Est. Time: 2-3 hours)

### Step 5.1: CSS Design System
Create `static/css/style.css`:

**Color Palette:**
- Define CSS variables for colors
- Primary, secondary, warning, danger themes
- Dark mode backgrounds

**Components:**
- Typography system
- Grid layouts (2, 3, 4 columns)
- Form controls with focus states
- Button variants
- Cards with glassmorphism
- Tables with hover effects
- Alerts and badges
- Stat cards

**Animations:**
- Fade-in effects
- Hover transitions
- Loading spinner

**Test**: Create HTML test page to preview components

### Step 5.2: Base Template
Create `templates/base.html`:
- HTML structure with head/body
- Google Fonts import (Inter)
- Navigation bar (conditional on login)
- Flash message display
- Content block
- Footer

**Navigation Features:**
- Role-based menu items
- Customer: Dashboard, Deposit, Withdraw, Transfer, History
- Analyst: + Fraud Monitoring
- Manager: + Reports
- Compliance: + Compliance

---

## Phase 6: Authentication Routes & Templates (Est. Time: 2-3 hours)

### Step 6.1: Authentication Routes
Create `routes/auth_routes.py`:
- `@login_required` decorator
- `@role_required(role)` decorator
- `/` - Index route
- `/register` - GET: form, POST: create user
- `/login` - GET: form, POST: authenticate
- `/logout` - Clear session

**Key Implementation:**
- Auto-create account with $1000 on registration
- Store user data in session
- Set permanent session (30 min timeout)

### Step 6.2: Authentication Templates

**`templates/index.html`:**
- Landing page with branding
- Call-to-action buttons
- Feature highlights (Security, Speed, Protection)

**`templates/login.html`:**
- Email and password form
- Link to registration
- Error message display

**`templates/register.html`:**
- Name, email, password fields
- Role dropdown (customer, analyst, manager, compliance)
- Password validation (min 8 chars)

**Test**: Register, login, logout flow

---

## Phase 7: Customer Banking Features (Est. Time: 3-4 hours)

### Step 7.1: Account Routes
Create `routes/account_routes.py`:
- `/dashboard` - Account overview
- `/accounts` - Account list (if multiple)

### Step 7.2: Transaction Routes
Create `routes/transaction_routes.py`:
- `/deposit` - GET: form, POST: process
- `/withdraw` - GET: form, POST: process
- `/transfer` - GET: form, POST: process
- `/history` - Transaction list

**Implementation Details:**
- Check fraud score after withdraw/transfer
- Send SNS alert if score ≥70
- Display fraud warnings to user
- Handle account freeze scenarios

### Step 7.3: Customer Templates

**`templates/dashboard.html`:**
- Account balance stat card
- Account status badge
- Quick action buttons
- Recent transactions table (limit 10)

**`templates/deposit.html`:**
- Account selector dropdown
- Amount input
- Description field
- Submit/Cancel buttons

**`templates/withdraw.html`:**
- Similar to deposit
- Add fraud detection warning alert

**`templates/transfer.html`:**
- Source account dropdown
- Target account ID input
- Amount and description fields
- Transfer confirmation info

**`templates/history.html`:**
- Account selector (if multiple accounts)
- Full transaction table
- Columns: Date, Type, Amount, Description, Status, Fraud Score
- Color-coded badges for status and fraud scores

**Test**: Complete banking workflow (deposit → withdraw → transfer)

---

## Phase 8: Analytics Dashboard - Scenario 1 (Est. Time: 2-3 hours)

### Step 8.1: Fraud Monitoring Routes
In `routes/analytics_routes.py`:
- `/analytics/fraud-monitoring` - Main dashboard
- `/analytics/api/recent-transactions` - JSON endpoint
- `/analytics/api/investigate/<id>` - Investigation data
- `/analytics/api/approve-transaction` - POST endpoint
- `/analytics/api/freeze-account` - POST endpoint

Add `@role_required('analyst')` decorator.

### Step 8.2: Fraud Monitoring Template
Create `templates/analytics/fraud_monitoring.html`:

**Dashboard Sections:**
1. **Summary Cards:**
   - Critical Risk count (score ≥90)
   - High Risk count (80-89)
   - Medium Risk count (70-79)
   - Total Flagged count

2. **Critical Alerts Section:**
   - Red transaction cards
   - Transaction details
   - Action buttons: Investigate, Freeze, Approve

3. **High Risk Section:**
   - Yellow/orange cards
   - Condensed view

4. **Medium Risk Section:**
   - Count display

**JavaScript Features:**
- `investigateTransaction()` - Show details
- `freezeAccount()` - POST to API
- `approveTransaction()` - POST to API

**Test**: Create high-value transactions, verify alerts appear

---

## Phase 9: Analytics Dashboard - Scenario 2 (Est. Time: 2-3 hours)

### Step 9.1: Reports Routes
In `routes/analytics_routes.py`:
- `/analytics/reports` - Main dashboard
- `/analytics/api/financial-report` - POST: generate report
- `/analytics/api/deposit-trends` - GET: trends data
- `/analytics/api/transaction-volume` - GET: volume data

Add `@role_required('manager')` decorator.

### Step 9.2: Reports Template
Create `templates/analytics/reports.html`:

**Dashboard Sections:**
1. **Report Generator:**
   - Start date picker
   - End date picker
   - Generate button

2. **Summary Metrics:**
   - Total transactions
   - Deposit volume
   - Withdrawal volume
   - Transfer volume

3. **Visualizations:**
   - Transaction breakdown (Chart.js doughnut)
   - Daily volume trend (Chart.js line)

4. **Quick Analysis Tools:**
   - 30-day deposit trends button
   - 24-hour volume analysis button

**JavaScript Features:**
- Include Chart.js CDN
- `generateReport()` - Fetch and display data
- `createTransactionChart()` - Doughnut chart
- `createVolumeChart()` - Line chart
- `analyzeDepositTrends()` - Fetch trends
- `analyzeTransactionVolume()` - Fetch volume

**Test**: Generate reports with various date ranges

---

## Phase 10: Analytics Dashboard - Scenario 3 (Est. Time: 2-3 hours)

### Step 10.1: Compliance Routes
In `routes/analytics_routes.py`:
- `/analytics/compliance` - Main dashboard
- `/analytics/api/compliance-drilldown` - Investigation

Add `@role_required('compliance')` decorator.

### Step 10.2: Compliance Template
Create `templates/analytics/compliance.html`:

**Dashboard Sections:**
1. **Overview:**
   - Total transactions (30 days)
   - Overall compliance status badge
   - Last updated timestamp

2. **Three Compliance Meters:**
   
   **Large Transactions (>$10,000):**
   - Count vs. threshold (100)
   - Progress bar (green/yellow/red)
   - Investigate button

   **Suspicious Activity:**
   - Fraud score ≥70 count vs. threshold (50)
   - Progress bar
   - Investigate button

   **Transaction Failure Rate:**
   - Percentage vs. target (<5%)
   - Progress bar
   - Investigate button

3. **Drill-down Results:**
   - Hidden section
   - Transaction table
   - Close button

**CSS Features:**
- Custom `.compliance-meter` class
- `.progress-bar` with color states
- `.progress-fill` animations

**JavaScript Features:**
- `drillDown(metricType)` - Fetch data
- `displayDrilldown()` - Show table
- `closeDrilldown()` - Hide section

**Test**: Trigger thresholds, verify warnings

---

## Phase 11: Routes Integration (Est. Time: 1 hour)

### Step 11.1: Routes Package
Create `routes/__init__.py`:
- Import all blueprints
- Export for app.py

### Step 11.2: Update Main App
In `app.py`:
- Import all blueprints
- Register with app
- Configure session timeout
- Add error handlers (404, 500)

**Test**: All routes accessible, navigation works

---

## Phase 12: Testing & Validation (Est. Time: 3-4 hours)

### Step 12.1: Create Test Users
Register users for each role:
1. Customer: `customer@test.com`
2. Analyst: `analyst@test.com`
3. Manager: `manager@test.com`
4. Compliance: `compliance@test.com`

### Step 12.2: Test User Workflows

**Customer Tests:**
- [ ] Register and auto-create account
- [ ] Login and view dashboard
- [ ] Make deposit ($500)
- [ ] Make withdrawal ($100)
- [ ] Transfer to another account ($50)
- [ ] View transaction history
- [ ] Logout

**Fraud Detection Tests:**
- [ ] Make large withdrawal ($5000) - check fraud score
- [ ] Make multiple rapid transactions - check frequency scoring
- [ ] Make transaction 3x average - check anomaly detection
- [ ] Verify SNS email received for score ≥70
- [ ] Verify account frozen for score ≥90

**Analyst Tests:**
- [ ] Login as analyst
- [ ] View fraud monitoring dashboard
- [ ] See all critical/high/medium alerts
- [ ] Investigate a transaction
- [ ] Freeze an account
- [ ] Approve a transaction

**Manager Tests:**
- [ ] Login as manager
- [ ] Generate financial report
- [ ] View transaction breakdown chart
- [ ] Analyze deposit trends
- [ ] Analyze transaction volume

**Compliance Tests:**
- [ ] Login as compliance officer
- [ ] View compliance dashboard
- [ ] Check all three meters
- [ ] Drill down into large transactions
- [ ] Drill down into suspicious activity
- [ ] Verify threshold warnings

### Step 12.3: Security Testing
- [ ] Verify passwords are hashed (check DynamoDB)
- [ ] Test session timeout (wait 30 min)
- [ ] Try accessing protected routes without login
- [ ] Try accessing analyst routes as customer
- [ ] Verify CSRF protection
- [ ] Test input validation on all forms

### Step 12.4: Edge Cases
- [ ] Insufficient balance withdrawal
- [ ] Transfer to non-existent account
- [ ] Invalid account ID format
- [ ] Negative amounts
- [ ] Very large amounts (fraud detection)
- [ ] Concurrent transactions

---

## Phase 13: Documentation (Est. Time: 2 hours)

### Step 13.1: Create README.md
Include:
- Project overview
- Features list
- Architecture diagram (text-based)
- Installation instructions
- Usage guide
- Testing account credentials

### Step 13.2: Create AWS_SETUP_GUIDE.md
Step-by-step AWS configuration:
- DynamoDB tables with exact specifications
- SNS topics setup
- IAM configuration
- Cost estimates

### Step 13.3: Code Documentation
Add docstrings to:
- All model methods
- All service methods
- Complex route handlers

---

## Phase 14: Production Deployment (Est. Time: 4-5 hours)

### Step 14.1: EC2 Instance Setup
1. Launch t2.small instance
2. Security group: SSH (your IP), HTTP (0.0.0.0/0), HTTPS (0.0.0.0/0)
3. Attach IAM role with DynamoDB and SNS permissions

### Step 14.2: Server Configuration
```bash
# Connect to EC2
ssh -i key.pem ec2-user@instance-ip

# Update system
sudo yum update -y

# Install Python
sudo yum install python3 python3-pip -y

# Create app directory
mkdir ~/cloud-bank
cd ~/cloud-bank
```

### Step 14.3: Deploy Application
```bash
# Upload code (scp or git)
# Install dependencies
pip3 install -r requirements.txt

# Create .env file
nano .env
# Add production credentials

# Test run
python3 app.py
```

### Step 14.4: Production Server (Gunicorn + Nginx)

**Install Nginx:**
```bash
sudo yum install nginx -y
```

**Configure Nginx** (`/etc/nginx/conf.d/cloudbank.conf`):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Systemd Service** (`/etc/systemd/system/cloudbank.service`):
```ini
[Unit]
Description=Cloud Bank Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/cloud-bank
ExecStart=/usr/local/bin/gunicorn -w 4 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

**Start Services:**
```bash
sudo systemctl enable cloudbank
sudo systemctl start cloudbank
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Step 14.5: SSL Certificate (HTTPS)
```bash
# Install certbot
sudo yum install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot-renew.timer
```

### Step 14.6: Monitoring
- Enable CloudWatch logs
- Set up billing alerts
- Create health check endpoint
- Monitor DynamoDB metrics

---

## Phase 15: Post-Deployment (Est. Time: 1-2 hours)

### Step 15.1: Final Testing
Test all features in production:
- [ ] Registration working
- [ ] All banking operations
- [ ] All analytics dashboards
- [ ] SNS emails received
- [ ] HTTPS enabled
- [ ] Performance acceptable

### Step 15.2: Backup Strategy
- Enable DynamoDB point-in-time recovery
- Schedule regular backups
- Document recovery procedures

### Step 15.3: User Onboarding
- Create admin user credentials
- Document user role assignment process
- Prepare user guide

---

## Estimated Total Time

| Phase | Time | Cumulative |
|-------|------|------------|
| 1. Foundation | 1-2 hrs | 2 hrs |
| 2. AWS Setup | 2-3 hrs | 5 hrs |
| 3. Data Models | 3-4 hrs | 9 hrs |
| 4. Services | 3-4 hrs | 13 hrs |
| 5. Design System | 2-3 hrs | 16 hrs |
| 6. Auth | 2-3 hrs | 19 hrs |
| 7. Banking | 3-4 hrs | 23 hrs |
| 8. Fraud Dashboard | 2-3 hrs | 26 hrs |
| 9. Reports Dashboard | 2-3 hrs | 29 hrs |
| 10. Compliance Dashboard | 2-3 hrs | 32 hrs |
| 11. Integration | 1 hr | 33 hrs |
| 12. Testing | 3-4 hrs | 37 hrs |
| 13. Documentation | 2 hrs | 39 hrs |
| 14. Deployment | 4-5 hrs | 44 hrs |
| 15. Post-Deploy | 1-2 hrs | **46 hrs** |

**Total: 40-50 hours** (1-2 weeks full-time, 4-6 weeks part-time)

---

## Tips for Success

1. **Work Sequentially**: Don't skip phases
2. **Test Continuously**: Test after each step
3. **Commit Often**: Use git for version control
4. **Ask Questions**: Use AWS documentation
5. **Monitor Costs**: Check AWS billing daily
6. **Take Breaks**: Complex project, pace yourself
7. **Document Issues**: Keep notes of problems and solutions

---

## Common Pitfalls to Avoid

❌ **Forgetting to activate virtual environment**  
✅ Always activate before installing packages

❌ **Hardcoding AWS credentials**  
✅ Use .env file, never commit credentials

❌ **Skipping GSI creation on DynamoDB**  
✅ Indexes are critical for performance

❌ **Not testing fraud detection thoroughly**  
✅ Create varied test scenarios

❌ **Deploying without testing locally**  
✅ Complete local testing first

❌ **Ignoring security best practices**  
✅ Use HTTPS, secure sessions, validate input

---

## Support Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **AWS DynamoDB**: https://docs.aws.amazon.com/dynamodb/
- **AWS SNS**: https://docs.aws.amazon.com/sns/
- **boto3**: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- **Chart.js**: https://www.chartjs.org/docs/

---

## Next Steps After Completion

1. **Enhance Features**:
   - Add transaction receipts
   - Implement password reset
   - Add email verification
   - Create admin panel

2. **Scale Infrastructure**:
   - Add load balancer
   - Implement Redis caching
   - Use Lambda for processing
   - Set up auto-scaling

3. **Improve Analytics**:
   - Machine learning for fraud detection
   - Predictive analytics
   - Customer behavior analysis
   - Advanced visualizations

4. **Mobile App**:
   - Create REST API
   - Build React Native app
   - Implement push notifications

Good luck building your Cloud Bank Analytics application! 🚀
