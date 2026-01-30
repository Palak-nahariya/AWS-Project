from models.transaction import Transaction
from models.account import Account
from datetime import datetime, timedelta
from collections import defaultdict

class AnalyticsService:
    """Analytics service for fraud monitoring, reporting, and compliance"""
    
    def __init__(self):
        self.transaction_model = Transaction()
        self.account_model = Account()
    
    # === Scenario 1: Real-time Transaction Monitoring ===
    
    def get_fraud_monitoring_dashboard(self, threshold=70):
        """Get real-time fraud monitoring data for analysts"""
        # Get high-risk transactions
        high_fraud_txns = self.transaction_model.get_high_fraud_transactions(threshold)
        
        # Categorize by fraud level
        critical = [t for t in high_fraud_txns if t['FraudScore'] >= 90]
        high = [t for t in high_fraud_txns if 80 <= t['FraudScore'] < 90]
        medium = [t for t in high_fraud_txns if 70 <= t['FraudScore'] < 80]
        
        return {
            'success': True,
            'total_flagged': len(high_fraud_txns),
            'critical_count': len(critical),
            'high_count': len(high),
            'medium_count': len(medium),
            'transactions': {
                'critical': critical,
                'high': high,
                'medium': medium
            }
        }
    
    def get_recent_transactions_feed(self, hours=24, limit=100):
        """Get recent transactions for live monitoring"""
        start_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        end_time = datetime.utcnow().isoformat()
        
        transactions = self.transaction_model.get_transactions_by_date_range(
            start_time, end_time, limit
        )
        
        return {
            'success': True,
            'count': len(transactions),
            'transactions': transactions
        }
    
    def investigate_transaction(self, transaction_id):
        """Get detailed information for transaction investigation"""
        transaction = self.transaction_model.get_transaction(transaction_id)
        
        if not transaction:
            return {'success': False, 'error': 'Transaction not found'}
        
        # Get account details
        account = self.account_model.get_account(transaction['AccountID'])
        
        # Get recent transaction history for pattern analysis
        recent_txns = self.transaction_model.get_account_transactions(
            transaction['AccountID'], limit=20
        )
        
        return {
            'success': True,
            'transaction': transaction,
            'account': account,
            'recent_history': recent_txns
        }
    
    # === Scenario 2: Custom Report Generation ===
    
    def generate_financial_report(self, start_date, end_date):
        """Generate comprehensive financial report"""
        transactions = self.transaction_model.get_transactions_by_date_range(
            start_date, end_date
        )
        
        # Calculate metrics
        total_deposits = sum(t['Amount'] for t in transactions if t['TransactionType'] == 'DEPOSIT')
        total_withdrawals = sum(t['Amount'] for t in transactions if t['TransactionType'] == 'WITHDRAW')
        total_transfers = sum(t['Amount'] for t in transactions if t['TransactionType'] == 'TRANSFER')
        
        deposit_count = len([t for t in transactions if t['TransactionType'] == 'DEPOSIT'])
        withdrawal_count = len([t for t in transactions if t['TransactionType'] == 'WITHDRAW'])
        transfer_count = len([t for t in transactions if t['TransactionType'] == 'TRANSFER'])
        
        # Transaction volume by day
        daily_volume = defaultdict(float)
        for txn in transactions:
            date = txn['Date'][:10]  # Extract date part
            daily_volume[date] += txn['Amount']
        
        return {
            'success': True,
            'period': {'start': start_date, 'end': end_date},
            'summary': {
                'total_transactions': len(transactions),
                'deposit_volume': total_deposits,
                'withdrawal_volume': total_withdrawals,
                'transfer_volume': total_transfers,
                'deposit_count': deposit_count,
                'withdrawal_count': withdrawal_count,
                'transfer_count': transfer_count,
                'net_flow': total_deposits - total_withdrawals
            },
            'daily_volume': dict(daily_volume)
        }
    
    def get_deposit_growth_trends(self, days=30):
        """Analyze deposit growth trends"""
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
        end_date = datetime.utcnow().isoformat()
        
        transactions = self.transaction_model.get_transactions_by_date_range(
            start_date, end_date
        )
        
        deposits = [t for t in transactions if t['TransactionType'] == 'DEPOSIT']
        
        # Group by day
        daily_deposits = defaultdict(list)
        for dep in deposits:
            date = dep['Date'][:10]
            daily_deposits[date].append(dep['Amount'])
        
        # Calculate daily totals and averages
        trends = []
        for date in sorted(daily_deposits.keys()):
            amounts = daily_deposits[date]
            trends.append({
                'date': date,
                'count': len(amounts),
                'total': sum(amounts),
                'average': sum(amounts) / len(amounts)
            })
        
        return {
            'success': True,
            'period_days': days,
            'trends': trends,
            'total_deposits': sum(d['total'] for d in trends),
            'average_daily_deposits': sum(d['total'] for d in trends) / len(trends) if trends else 0
        }
    
    def get_transaction_volume_analysis(self, hours=24):
        """Analyze transaction volume patterns"""
        start_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
        end_time = datetime.utcnow().isoformat()
        
        transactions = self.transaction_model.get_transactions_by_date_range(
            start_time, end_time
        )
        
        # Hourly distribution
        hourly_volume = defaultdict(int)
        for txn in transactions:
            hour = txn['Date'][11:13]  # Extract hour
            hourly_volume[hour] += 1
        
        return {
            'success': True,
            'total_volume': len(transactions),
            'hourly_distribution': dict(hourly_volume),
            'peak_hour': max(hourly_volume.items(), key=lambda x: x[1])[0] if hourly_volume else None
        }
    
    # === Scenario 3: Regulatory Compliance Monitoring ===
    
    def get_compliance_dashboard(self):
        """Get regulatory compliance metrics"""
        # Get last 30 days of transactions
        start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        end_date = datetime.utcnow().isoformat()
        
        transactions = self.transaction_model.get_transactions_by_date_range(
            start_date, end_date, limit=10000
        )
        
        # Large transaction monitoring (>$10,000)
        large_transactions = [t for t in transactions if t['Amount'] > 10000]
        large_txn_threshold = 100  # Compliance limit
        large_txn_percentage = (len(large_transactions) / len(transactions) * 100) if transactions else 0
        
        # High fraud score transactions
        suspicious_transactions = [t for t in transactions if t.get('FraudScore', 0) >= 70]
        suspicious_txn_threshold = 50  # Max allowed suspicious transactions
        
        # Failed transaction rate
        failed_transactions = [t for t in transactions if t.get('Status') == 'FAILED']
        failed_rate = (len(failed_transactions) / len(transactions) * 100) if transactions else 0
        failed_rate_threshold = 5  # Max 5% failure rate
        
        return {
            'success': True,
            'metrics': {
                'large_transactions': {
                    'count': len(large_transactions),
                    'threshold': large_txn_threshold,
                    'status': 'compliant' if len(large_transactions) < large_txn_threshold else 'warning',
                    'percentage': large_txn_percentage
                },
                'suspicious_activity': {
                    'count': len(suspicious_transactions),
                    'threshold': suspicious_txn_threshold,
                    'status': 'compliant' if len(suspicious_transactions) < suspicious_txn_threshold else 'alert'
                },
                'transaction_failure_rate': {
                    'rate': failed_rate,
                    'threshold': failed_rate_threshold,
                    'status': 'compliant' if failed_rate < failed_rate_threshold else 'warning'
                },
                'total_transactions': len(transactions)
            }
        }
    
    def drill_down_compliance_metric(self, metric_type, start_date=None, end_date=None):
        """Drill down into specific compliance metric for root cause analysis"""
        if not start_date:
            start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
        if not end_date:
            end_date = datetime.utcnow().isoformat()
        
        transactions = self.transaction_model.get_transactions_by_date_range(
            start_date, end_date, limit=10000
        )
        
        if metric_type == 'large_transactions':
            filtered = [t for t in transactions if t['Amount'] > 10000]
        elif metric_type == 'suspicious_activity':
            filtered = [t for t in transactions if t.get('FraudScore', 0) >= 70]
        elif metric_type == 'failed_transactions':
            filtered = [t for t in transactions if t.get('Status') == 'FAILED']
        else:
            return {'success': False, 'error': 'Invalid metric type'}
        
        return {
            'success': True,
            'metric_type': metric_type,
            'count': len(filtered),
            'transactions': filtered
        }
