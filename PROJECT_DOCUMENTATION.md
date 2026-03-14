# ☁️ Cloud Bank Analytics — Project Documentation

> **A comprehensive cloud-based banking application featuring secure account management, financial transactions, role-based analytics dashboards, and real-time fraud detection — powered by AWS services.**

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Project Structure](#3-project-structure)
4. [Architecture & Data Flow](#4-architecture--data-flow)
5. [Database Schema](#5-database-schema)
6. [Module-Level Documentation](#6-module-level-documentation)
7. [API Routes & Endpoints](#7-api-routes--endpoints)
8. [User Roles & Access Control](#8-user-roles--access-control)
9. [Fraud Detection System](#9-fraud-detection-system)
10. [Security Features](#10-security-features)
11. [Local Development Mode](#11-local-development-mode)
12. [Environment Configuration](#12-environment-configuration)
13. [AWS Infrastructure Setup](#13-aws-infrastructure-setup)
14. [Installation & Running](#14-installation--running)
15. [Production Deployment](#15-production-deployment)
16. [UI & Design](#16-ui--design)
17. [Testing](#17-testing)

---

## 1. Project Overview

**Cloud Bank Analytics** is a full-stack banking web application built with Python Flask that demonstrates the integration of multiple AWS services for a real-world financial application. It includes:

- **Core banking operations** — registration, login, deposits, withdrawals, transfers, and transaction history.
- **Role-based analytics dashboards** — real-time fraud monitoring, custom financial report generation, and regulatory compliance tracking.
- **Fraud detection engine** — an algorithm that scores every transaction (0–100) and can automatically freeze accounts.
- **AWS-native backend** — DynamoDB for data persistence, SNS for push notifications, EC2 for hosting, and IAM for access control.
- **Local development mode** — JSON-file-based storage that lets developers run and test the entire application without any AWS credentials.

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend Framework** | Flask 3.0.0 | Web server, routing, templating |
| **Database** | AWS DynamoDB | NoSQL data persistence |
| **Notifications** | AWS SNS | Email / SMS alerts for fraud and compliance |
| **Hosting** | AWS EC2 | Production server |
| **Authentication** | bcrypt 4.1.2 | Password hashing with 12 rounds |
| **Session Management** | Flask sessions | HTTP-only, SameSite cookies |
| **Environment Config** | python-dotenv 1.0.0 | `.env` file management |
| **HTTP Server** | Werkzeug 3.0.1 (dev), Gunicorn 21.2.0 (prod) | WSGI servers |
| **Cloud SDK** | boto3 1.34.0 | AWS service integration |
| **Frontend** | Jinja2 templates, CSS, Chart.js | UI rendering |

### Dependencies (`requirements.txt`)

```
Flask==3.0.0
boto3==1.34.0
bcrypt==4.1.2
python-dotenv==1.0.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

---

## 3. Project Structure

```
AWS Project/
│
├── app.py                    # Flask application entry point
├── config.py                 # Centralized configuration (Config class)
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (git-ignored)
├── .env.example              # Template for environment variables
├── .gitignore                # Git ignore rules
├── README.md                 # Quick-start README
├── PROJECT_DOCUMENTATION.md  # ◀ This document
│
├── models/                   # Data access layer (DynamoDB)
│   ├── __init__.py           # Exports User, Account, Transaction
│   ├── user.py               # User model — CRUD, auth, password hashing
│   ├── account.py            # Account model — balance, freeze/activate
│   └── transaction.py        # Transaction model — CRUD, fraud scoring
│
├── simple_models.py          # Lightweight wrappers for local-storage mode
├── local_storage.py          # JSON-file-based mock database
├── local_data.json           # Persisted local data file
│
├── services/                 # Business logic layer
│   ├── __init__.py           # Exports all services
│   ├── auth_service.py       # Registration, login, session management
│   ├── banking_service.py    # Deposit, withdraw, transfer, history
│   ├── analytics_service.py  # Fraud dashboard, reports, compliance
│   └── notification_service.py  # AWS SNS alert delivery
│
├── routes/                   # HTTP route handlers (Flask Blueprints)
│   ├── __init__.py           # Registers all blueprints
│   ├── auth_routes.py        # /, /register, /login, /logout
│   ├── account_routes.py     # /dashboard
│   ├── transaction_routes.py # /deposit, /withdraw, /transfer, /history
│   └── analytics_routes.py   # /analytics/* (fraud, reports, compliance)
│
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Master layout (navbar, footer, flash msgs)
│   ├── index.html            # Landing page
│   ├── login.html            # Login form
│   ├── register.html         # Registration form
│   ├── dashboard.html        # User dashboard with account overview
│   ├── deposit.html          # Deposit form
│   ├── withdraw.html         # Withdrawal form
│   ├── transfer.html         # Transfer form
│   ├── history.html          # Transaction history table
│   └── analytics/
│       ├── fraud_monitoring.html   # Analyst: fraud dashboard
│       ├── reports.html            # Manager: financial reports
│       └── compliance.html         # Compliance: regulatory dashboard
│
├── static/
│   └── css/
│       └── style.css         # Global stylesheet (dark glassmorphism theme)
│
├── test_aws_connection.py    # AWS connectivity test script
├── test_password_fix.py      # Password hashing verification script
├── debug_passwords.py        # Debug utility for password issues
├── generate_hash.py          # Standalone bcrypt hash generator
│
└── venv/                     # Python virtual environment (git-ignored)
```

---

## 4. Architecture & Data Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│                          CLIENT (Browser)                             │
│   index.html │ login │ register │ dashboard │ deposit │ withdraw │ …  │
└───────────────────────────────┬────────────────────────────────────────┘
                                │ HTTP
┌───────────────────────────────▼────────────────────────────────────────┐
│                        FLASK APP  (app.py)                            │
│  ┌──────────┐  ┌────────────┐  ┌─────────────┐  ┌───────────────┐    │
│  │ auth_bp  │  │ account_bp │  │transaction_bp│  │ analytics_bp  │    │
│  │ (routes) │  │  (routes)  │  │   (routes)   │  │   (routes)    │    │
│  └────┬─────┘  └─────┬──────┘  └──────┬───────┘  └──────┬────────┘   │
│       │              │               │                  │            │
│  ┌────▼──────────────▼───────────────▼──────────────────▼─────────┐  │
│  │                    SERVICE LAYER                                │  │
│  │  AuthService │ BankingService │ AnalyticsService │ Notification │  │
│  └────────────────────────────┬───────────────────────────────────┘  │
│                               │                                      │
│  ┌────────────────────────────▼───────────────────────────────────┐  │
│  │                     MODEL / DATA LAYER                         │  │
│  │      User │ Account │ Transaction │ LocalStorage (fallback)    │  │
│  └────────────────────────────┬───────────────────────────────────┘  │
└───────────────────────────────┼──────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                      │                        │
   ┌────▼─────┐         ┌─────▼──────┐          ┌──────▼──────┐
   │ DynamoDB │         │    SNS     │          │ local_data  │
   │ (3 tables)│         │ (3 topics) │          │   .json     │
   └──────────┘         └────────────┘          └─────────────┘
```

### Layered Architecture

| Layer | Files | Responsibility |
|---|---|---|
| **Routes** | `routes/*.py` | HTTP request handling, input validation, flash messages, template rendering |
| **Services** | `services/*.py` | Business logic, orchestration, fraud scoring decisions |
| **Models** | `models/*.py`, `simple_models.py` | Data access, DynamoDB / local-storage abstraction |
| **Storage** | `local_storage.py`, `local_data.json` | JSON-file mock database for local development |

---

## 5. Database Schema

### 5.1  Users Table (`CloudBank_Users`)

| Attribute | Type | Description |
|---|---|---|
| `UserID` | String (PK) | UUID, primary key |
| `Name` | String | Full name |
| `Email` | String | Unique email (GSI: `EmailIndex`) |
| `PasswordHash` | String | bcrypt hash |
| `Role` | String | `customer` · `analyst` · `manager` · `compliance` |
| `CreatedAt` | String (ISO 8601) | Timestamp |
| `UpdatedAt` | String (ISO 8601) | Timestamp |

**Global Secondary Index:** `EmailIndex` (PK: `Email`) — used for login lookups.

---

### 5.2  Accounts Table (`CloudBank_Accounts`)

| Attribute | Type | Description |
|---|---|---|
| `AccountID` | String (PK) | UUID |
| `UserID` | String | Owner reference |
| `Balance` | Number (Decimal) | Current balance |
| `AccountType` | String | `SAVINGS` · `CHECKING` |
| `Status` | String | `ACTIVE` · `FROZEN` |
| `CreatedAt` | String | Timestamp |
| `UpdatedAt` | String | Timestamp |

**Global Secondary Index:** `UserIDIndex` (PK: `UserID`) — used to fetch all accounts for a user.

---

### 5.3  Transactions Table (`CloudBank_Transactions`)

| Attribute | Type | Description |
|---|---|---|
| `TransactionID` | String (PK) | UUID |
| `Date` | String (SK) | ISO 8601 timestamp (sort key) |
| `AccountID` | String | Source account |
| `TargetAccountID` | String | Destination (transfers only) |
| `TransactionType` | String | `DEPOSIT` · `WITHDRAW` · `TRANSFER` |
| `Amount` | Number (Decimal) | Transaction amount |
| `Status` | String | `PENDING` · `COMPLETED` · `FAILED` |
| `FraudScore` | Number | 0–100 risk score |
| `Description` | String | User-provided note |

**Global Secondary Indexes:**
- `AccountIDIndex` (PK: `AccountID`, SK: `Date`)
- `DateIndex` (PK: `Date`)
- `FraudScoreIndex` (PK: `FraudScore`)

---

## 6. Module-Level Documentation

### 6.1  `app.py` — Application Entry Point

- Creates the Flask app and loads configuration from `Config`.
- Registers four blueprints: `auth_bp`, `account_bp`, `transaction_bp`, `analytics_bp`.
- Configures session lifetime (default 30 min).
- Defines `404` and `500` error handlers.
- Runs on `0.0.0.0:5000` in debug mode.

### 6.2  `config.py` — Configuration

Loads environment variables from `.env` via `python-dotenv` and exposes them through the `Config` class.

| Config Group | Key Settings |
|---|---|
| Flask | `SECRET_KEY`, `DEBUG` |
| Storage mode | `USE_LOCAL_STORAGE` (default `True`) |
| AWS | `AWS_REGION`, access keys |
| DynamoDB tables | `CloudBank_Users`, `CloudBank_Accounts`, `CloudBank_Transactions` |
| SNS ARNs | Transaction, Compliance, and System alert topics |
| Session | 30-min lifetime, HTTP-only cookies, SameSite=Lax |
| Security | `BCRYPT_ROUNDS` = 12 |
| Fraud thresholds | Alert ≥ 70, Freeze ≥ 90 |

### 6.3  `models/user.py` — User Model

| Method | Description |
|---|---|
| `create_user()` | Hashes password with bcrypt, stores in DynamoDB or local storage |
| `get_user_by_id()` | Fetch by primary key |
| `get_user_by_email()` | Fetch via `EmailIndex` GSI |
| `verify_password()` | Compare plaintext against bcrypt hash |
| `authenticate()` | Full login flow: lookup → verify → return sanitized user |
| `update_user()` | Partial update (prevents overwriting `UserID` and `PasswordHash`) |

### 6.4  `models/account.py` — Account Model

| Method | Description |
|---|---|
| `create_account()` | New account with conditional check for duplicates |
| `get_account()` | Fetch by `AccountID` |
| `get_accounts_by_user()` | Query `UserIDIndex` GSI |
| `update_balance()` | Atomic `ADD` / `SUBTRACT` with sufficient-balance check |
| `freeze_account()` | Set status to `FROZEN` |
| `activate_account()` | Restore status to `ACTIVE` |

### 6.5  `models/transaction.py` — Transaction Model

| Method | Description |
|---|---|
| `create_transaction()` | Records transaction with auto-calculated fraud score |
| `update_transaction_status()` | Mark as `COMPLETED` or `FAILED` |
| `get_transaction()` | Fetch single transaction |
| `get_account_transactions()` | History for an account (most recent first) |
| `get_high_fraud_transactions()` | Query by fraud score threshold |
| `get_transactions_by_date_range()` | Date-range query via `DateIndex` |
| `_calculate_fraud_score()` | Internal scoring algorithm (see §9) |

### 6.6  `services/auth_service.py` — AuthService

| Method | Description |
|---|---|
| `register()` | Validates input → checks duplicate email → creates user |
| `login()` | Validates input → authenticates → returns user data |
| `get_user()` | Session re-validation (strips `PasswordHash`) |
| `update_profile()` | Filters out sensitive fields before update |

### 6.7  `services/banking_service.py` — BankingService

- Automatically selects `simple_models` (local) or `models` (DynamoDB) based on `USE_LOCAL_STORAGE`.

| Method | Description |
|---|---|
| `create_account()` | Creates account with UUID |
| `get_user_accounts()` | Returns all accounts for a user |
| `deposit()` | Creates transaction → updates balance → marks complete |
| `withdraw()` | Creates transaction → checks fraud score → freezes if ≥ 90 → updates balance |
| `transfer()` | Validates target → creates transaction → deducts source → credits target → **rollback on failure** |
| `get_transaction_history()` | Delegates to transaction model |

### 6.8  `services/analytics_service.py` — AnalyticsService

**Scenario 1 — Fraud Monitoring (Analyst)**
| Method | Description |
|---|---|
| `get_fraud_monitoring_dashboard()` | Categorizes flagged transactions: Critical (≥90), High (80–89), Medium (70–79) |
| `get_recent_transactions_feed()` | Live feed of last N hours |
| `investigate_transaction()` | Deep dive: transaction + account + recent history |

**Scenario 2 — Reports (Manager)**
| Method | Description |
|---|---|
| `generate_financial_report()` | Aggregate metrics: deposit/withdrawal/transfer volumes, daily breakdown |
| `get_deposit_growth_trends()` | Daily deposit totals & averages over N days |
| `get_transaction_volume_analysis()` | Hourly volume distribution, peak hour detection |

**Scenario 3 — Compliance (Officer)**
| Method | Description |
|---|---|
| `get_compliance_dashboard()` | Monitors large txns (>$10K), suspicious activity, failure rate |
| `drill_down_compliance_metric()` | Filtered transaction lists per metric type |

### 6.9  `services/notification_service.py` — NotificationService

| Method | Description |
|---|---|
| `send_transaction_alert()` | Publishes to the Transaction Alerts SNS topic |
| `send_compliance_alert()` | Publishes to the Compliance Alerts SNS topic |
| `send_system_alert()` | Publishes to the System Alerts SNS topic |
| `notify_high_fraud_transaction()` | Formats and sends fraud alert with transaction details |
| `notify_account_frozen()` | Sends account-freeze notification |

### 6.10  `local_storage.py` — LocalStorage

A **JSON-file-based mock database** (`local_data.json`) that mirrors the DynamoDB API surface. Used when `USE_LOCAL_STORAGE=True`.

- In-memory dict backed by `local_data.json`.
- Implements all CRUD operations for users, accounts, and transactions.
- Auto-saves on every write.

### 6.11  `simple_models.py` — SimpleAccount / SimpleTransaction

Lightweight wrappers that delegate to `LocalStorage` while matching the `Account` / `Transaction` model interface. Includes a simplified fraud-score calculator (amount-based only).

---

## 7. API Routes & Endpoints

### 7.1  Authentication Routes (`auth_bp`)

| Method | URL | Auth | Description |
|---|---|---|---|
| GET | `/` | No | Landing page (redirects to dashboard if logged in) |
| GET/POST | `/register` | No | User registration form & handler |
| GET/POST | `/login` | No | Login form & handler |
| GET | `/logout` | Yes | Clears session, redirects to login |

### 7.2  Account Routes (`account_bp`)

| Method | URL | Auth | Description |
|---|---|---|---|
| GET | `/dashboard` | Yes | Shows all user accounts with balances |

### 7.3  Transaction Routes (`transaction_bp`)

| Method | URL | Auth | Description |
|---|---|---|---|
| GET/POST | `/deposit` | Yes | Deposit money into selected account |
| GET/POST | `/withdraw` | Yes | Withdraw money (triggers fraud check + SNS alert if score ≥ 70) |
| GET/POST | `/transfer` | Yes | Transfer between accounts (fraud check + rollback on failure) |
| GET | `/history` | Yes | View transaction history with account selector |

### 7.4  Analytics Routes (`analytics_bp`, prefix: `/analytics`)

| Method | URL | Role | Description |
|---|---|---|---|
| GET | `/analytics/fraud-monitoring` | Analyst | Fraud monitoring dashboard |
| GET | `/analytics/api/recent-transactions` | Analyst | JSON: live transaction feed |
| GET | `/analytics/api/investigate/<id>` | Analyst | JSON: transaction deep-dive |
| POST | `/analytics/api/approve-transaction` | Analyst | Activate a frozen account |
| POST | `/analytics/api/freeze-account` | Analyst | Freeze a suspicious account |
| GET | `/analytics/reports` | Manager | Report generation dashboard |
| POST | `/analytics/api/financial-report` | Manager | JSON: comprehensive financial metrics |
| GET | `/analytics/api/deposit-trends` | Manager | JSON: deposit growth trends |
| GET | `/analytics/api/transaction-volume` | Manager | JSON: hourly volume distribution |
| GET | `/analytics/compliance` | Compliance | Compliance monitoring dashboard |
| GET | `/analytics/api/compliance-drilldown` | Compliance | JSON: filtered compliance detail |

---

## 8. User Roles & Access Control

| Role | Access |
|---|---|
| **Customer** | Dashboard, Deposit, Withdraw, Transfer, History |
| **Analyst** | All Customer pages + Fraud Monitoring Dashboard (`/analytics/fraud-monitoring`) |
| **Manager** | All Customer pages + Custom Reports Dashboard (`/analytics/reports`) |
| **Compliance** | All Customer pages + Regulatory Compliance Dashboard (`/analytics/compliance`) |

### Access Control Implementation

- **`login_required`** decorator (in `auth_routes.py`): checks `session['user_id']`.
- **`role_required(role)`** decorator: checks `session['role']`; admin role bypasses all checks.
- Navbar dynamically shows role-specific links based on `session.role`.

---

## 9. Fraud Detection System

### 9.1  Scoring Algorithm (`_calculate_fraud_score`)

Every withdrawal and transfer is scored on a 0–100 scale:

| Factor | Condition | Points |
|---|---|---|
| **Amount Anomaly** (max 40) | > 3× user's average | 40 |
| | > 2× user's average | 25 |
| | > 1.5× user's average | 15 |
| **Frequency** (max 30) | > 20 txns in 24h | 30 |
| | > 10 txns in 24h | 20 |
| | > 5 txns in 24h | 10 |
| **Large Amount** (max 30) | > $10,000 | 30 |
| | > $5,000 | 20 |
| | > $2,000 | 10 |

### 9.2  Automated Actions

| Threshold | Action |
|---|---|
| Score ≥ 70 | SNS alert sent to Transaction Alerts topic |
| Score ≥ 90 | Account **automatically frozen**, transaction **blocked** |

### 9.3  Analyst Dashboard

Analysts can review flagged transactions categorized as:
- 🔴 **Critical** (score ≥ 90) — account frozen
- 🟠 **High** (80–89) — needs investigation
- 🟡 **Medium** (70–79) — flagged for review

Analysts can **freeze** or **approve/activate** accounts via API endpoints.

---

## 10. Security Features

| Feature | Implementation |
|---|---|
| **Password Hashing** | bcrypt with 12 rounds (configurable via `BCRYPT_ROUNDS`) |
| **Session Security** | HTTP-only cookies, SameSite=Lax, 30-min expiry |
| **Input Validation** | Server-side validation in services layer |
| **Sensitive Data Protection** | `PasswordHash` stripped from all API responses |
| **Fraud Prevention** | Real-time scoring, automatic account freezing |
| **SNS Alerts** | Immediate notification for high-risk transactions |
| **Account Freeze** | Frozen accounts cannot process transactions |
| **Transfer Rollback** | Automatic balance restoration if target credit fails |
| **Conditional Writes** | DynamoDB condition expressions prevent race conditions |

---

## 11. Local Development Mode

When `USE_LOCAL_STORAGE=True` (default), the application runs **entirely without AWS**:

| Component | Production | Local Mode |
|---|---|---|
| User data | DynamoDB `CloudBank_Users` | `local_data.json` |
| Account data | DynamoDB `CloudBank_Accounts` | `local_data.json` |
| Transaction data | DynamoDB `CloudBank_Transactions` | `local_data.json` |
| Models used | `models/` (full DynamoDB) | `simple_models.py` + `local_storage.py` |
| Fraud scoring | Full 3-factor algorithm | Simplified amount-only check |
| Notifications | SNS topics | Console print (no-op) |

### How It Works

1. `config.py` reads `USE_LOCAL_STORAGE` from `.env`.
2. Each model class checks this flag in `__init__()`.
3. If local mode, it imports `local_storage.local_db` (singleton instance).
4. `banking_service.py` switches between `simple_models` and `models` at import time.
5. All data persists to `local_data.json` via `json.dump()`.

---

## 12. Environment Configuration

### `.env` Variables

```bash
# ── Storage Mode ──────────────────────────────────────
USE_LOCAL_STORAGE=True            # Set to False for DynamoDB

# ── AWS Credentials ──────────────────────────────────
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# ── DynamoDB Tables ──────────────────────────────────
DYNAMODB_USERS_TABLE=CloudBank_Users
DYNAMODB_ACCOUNTS_TABLE=CloudBank_Accounts
DYNAMODB_TRANSACTIONS_TABLE=CloudBank_Transactions

# ── SNS Topics ───────────────────────────────────────
SNS_TRANSACTION_ALERTS_ARN=arn:aws:sns:us-east-1:ACCOUNT:TransactionAlerts
SNS_COMPLIANCE_ALERTS_ARN=arn:aws:sns:us-east-1:ACCOUNT:ComplianceAlerts
SNS_SYSTEM_ALERTS_ARN=arn:aws:sns:us-east-1:ACCOUNT:SystemAlerts

# ── Flask ────────────────────────────────────────────
FLASK_SECRET_KEY=your_secret_key_here
DEBUG=True

# ── Security ─────────────────────────────────────────
SESSION_TIMEOUT=1800              # 30 minutes
BCRYPT_ROUNDS=12

# ── Fraud Detection ──────────────────────────────────
FRAUD_ALERT_THRESHOLD=70
FRAUD_FREEZE_THRESHOLD=90
```

---

## 13. AWS Infrastructure Setup

### Step 1 — Create DynamoDB Tables

**Users Table:**
```
Table Name: CloudBank_Users
Primary Key: UserID (String)
GSI: EmailIndex → Email (PK)
```

**Accounts Table:**
```
Table Name: CloudBank_Accounts
Primary Key: AccountID (String)
GSI: UserIDIndex → UserID (PK)
```

**Transactions Table:**
```
Table Name: CloudBank_Transactions
Primary Key: TransactionID (String)
Sort Key: Date (String)
GSI: AccountIDIndex → AccountID (PK), Date (SK)
GSI: DateIndex → Date (PK)
GSI: FraudScoreIndex → FraudScore (Number PK)
```

### Step 2 — Create SNS Topics

| Topic Name | Purpose |
|---|---|
| `TransactionAlerts` | Fraud detection notifications |
| `ComplianceAlerts` | Compliance threshold warnings |
| `SystemAlerts` | System health monitoring |

Subscribe email addresses to each topic for notifications.

### Step 3 — Configure IAM

Create an IAM role/user with these policies:
- `AmazonDynamoDBFullAccess`
- `AmazonSNSFullAccess`

Attach to the EC2 instance or generate access keys for local development.

### Step 4 — Update `.env`

Set `USE_LOCAL_STORAGE=False` and fill in all AWS credentials and ARNs.

---

## 14. Installation & Running

### Prerequisites
- Python 3.8 or later
- pip package manager
- (Optional) AWS account with configured credentials

### Setup

```bash
# 1. Navigate to project directory
cd "C:\Users\khurai\OneDrive\Desktop\AWS Project"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
copy .env.example .env
# Edit .env with your settings

# 6. Run the application
python app.py
```

### Access

Open your browser at **http://localhost:5000**.

### First-Time Registration

1. Go to `/register`.
2. Fill in name, email, password (min 8 chars), and select a role.
3. A bank account with **$1,000 initial balance** is auto-created.
4. Log in at `/login`.

---

## 15. Production Deployment

### EC2 Deployment Steps

1. Launch an EC2 instance (`t2.small` or larger).
2. Install Python 3.8+, pip, and project dependencies.
3. Set `USE_LOCAL_STORAGE=False`, `DEBUG=False` in `.env`.
4. Set a strong `FLASK_SECRET_KEY`.
5. Run via Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
6. Configure Nginx as a reverse proxy.
7. Enable HTTPS with Let's Encrypt / ACM.
8. Set up a systemd service for auto-restart.

### Production Security Checklist

- [ ] HTTPS enabled
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] Strong `FLASK_SECRET_KEY`
- [ ] DynamoDB encryption at rest
- [ ] Restricted IAM permissions (least-privilege)
- [ ] Security groups: only ports 80/443 open
- [ ] CloudWatch logging enabled
- [ ] CSRF protection

---

## 16. UI & Design

- **Theme:** Modern dark glassmorphism with semi-transparent cards and gradient backgrounds.
- **Typography:** Inter (Google Fonts) — weights 300–700.
- **Animations:** CSS `fade-in` effects and hover transitions.
- **Charts:** Chart.js for analytics dashboards (deposit trends, volume distribution).
- **Responsive:** Mobile-friendly layout.
- **Alerts:** Color-coded flash messages (`success`, `warning`, `danger`, `info`).
- **Navbar:** Dynamic role-based links — shows Fraud Monitor / Reports / Compliance based on user role.

---

## 17. Testing

### Test Files

| File | Purpose |
|---|---|
| `test_aws_connection.py` | Verifies AWS DynamoDB and SNS connectivity |
| `test_password_fix.py` | Tests bcrypt password hashing and verification |
| `debug_passwords.py` | Inspects stored password hashes for debugging |
| `generate_hash.py` | Standalone bcrypt hash generator utility |

### Running Tests

```bash
python test_aws_connection.py    # Test AWS connectivity
python test_password_fix.py      # Verify password hashing
```

---

> **© 2026 Cloud Bank Analytics — Powered by AWS**
