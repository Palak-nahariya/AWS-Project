# Local Storage Mode - Quick Start Guide

## ✅ What Changed

The application now supports **local JSON-based storage** so you can test all features without setting up AWS DynamoDB!

---

## 🎯 Current Status

### Enabled Features:
- ✅ User Registration (signup)
- ✅ User Login (signin)
- ✅ Account creation
- ✅ Deposits, Withdrawals, Transfers
- ✅ Transaction history
- ✅ Basic fraud detection
- ✅ All role-based dashboards

### Storage Location:
- All data is stored in: `local_data.json` (created automatically)
- This file persists between application restarts

---

## 🚀 How to Use

### 1. Server is Running! ✅
- **URL:** http://localhost:5000
- **Status:** Flask development server active

### 2. Open in Browser
Click here or copy to browser: **http://localhost:5000**

### 3. Create an Account
1. Click **"Register"**
2. Fill in:
   - Name: Your name
   - Email: test@example.com
   - Password: password123 (min 8 characters)
   - Role: Choose Customer, Analyst, Manager, or Compliance Officer
3. Click **"Create Account"**

### 4. Login
1. Use the email and password you registered with
2. Click **"Sign In"**

### 5. Test Banking Features
- **Deposit**: Add money to your account
- **Withdraw**: Remove money (will check balance)
- **Transfer**: Send to another account (need 2 accounts)
- **History**: View all transactions

---

## 📁 Files Created/Modified

### New Files:
1. **local_storage.py** - Local JSON database
2. **simple_models.py** - Model wrappers
3. **local_data.json** - Data storage (created on first use)

### Modified Files:
1. **config.py** - Added `USE_LOCAL_STORAGE` flag
2. **.env** - Set `USE_LOCAL_STORAGE=True`
3. **models/user.py** - Dual storage support
4. **models/account.py** - Dual storage support
5. **services/banking_service.py** - Adaptive models
6. **app.py** - Fixed config reference

---

## 🔄 Switching Between Local and AWS

### To Use Local Storage (Current):
```bash
# In .env file
USE_LOCAL_STORAGE=True
```

### To Use AWS DynamoDB:
```bash
# In .env file
USE_LOCAL_STORAGE=False

# Then configure AWS credentials
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

---

## 🎭 Testing Different Roles

Create users with different roles to test all dashboards:

### Customer Role:
- Default banking features
- Dashboard with balance
- Deposit, Withdraw, Transfer
- Transaction history

### Analyst Role:
- Access to `/analytics/fraud-monitoring`
- View high-risk transactions
- Investigate suspicious activity
- Freeze/approve accounts

### Manager Role:
- Access to `/analytics/reports`
- Financial metrics and charts
- Custom report generation
- Trend analysis

### Compliance Officer Role:
- Access to `/analytics/compliance`
- Regulatory threshold monitoring
- Large transaction tracking
- Drill-down investigations

---

## 🧪 Sample Test Data

### Create Test Accounts:
1. **Customer 1:**
   - Email: alice@test.com
   - Password: password123
   - Role: Customer

2. **Customer 2:**
   - Email: bob@test.com
   - Password: password123
   - Role: Customer

3. **Analyst:**
   - Email: analyst@bank.com
   - Password: password123
   - Role: Analyst

4. **Manager:**
   - Email: manager@bank.com
   - Password: password123
   - Role: Manager

5. **Compliance:**
   - Email: compliance@bank.com
   - Password: password123
   - Role: Compliance Officer

### Test Fraud Detection:
1. Login as Customer
2. Try to withdraw **$15,000** (triggers high fraud score)
3. Account may be frozen automatically
4. Login as Analyst to see the alert

---

## 📊 Data Persistence

### View Stored Data:
Open `local_data.json` to see all stored data:
- users: All registered users
- accounts: All bank accounts
- transactions: All transactions

### Reset Data:
Delete `local_data.json` and restart the server to start fresh

---

## ⚠️ Limitations of Local Mode

### No SNS Notifications:
- Email alerts won't be sent
- Fraud alerts logged to console only

### No AWS Features:
- No DynamoDB indexes
- No CloudWatch logging
- No distributed scalability

### For Demo/Testing Only:
- Not for production use
- Data stored in plain JSON file
- No distributed transactions

---

## 📝 Next Steps

1. ✅ **Try it now!** Open http://localhost:5000
2. ✅ Register and login
3. ✅ Test deposits, withdrawals, transfers
4. ✅ Try different user roles
5. ✅ View analytics dashboards

---

## 🛠️ Troubleshooting

### Server not responding?
```bash
# Check if server is running
# Look for "Running on http://127.0.0.1:5000"

# If not, restart:
. venv\Scripts\Activate.ps1
python app.py
```

### "local_data.json" errors?
- File will be created automatically
- If corrupted, delete it and restart

### Can't login after registration?
- Check `local_data.json` to verify user was created
- Ensure password is at least 8 characters

---

## 🎉 Ready to Test!

**Open your browser and go to:**
### 🌐 http://localhost:5000

Enjoy testing your Cloud Banking Application! 🏦✨
