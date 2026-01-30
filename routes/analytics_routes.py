from flask import Blueprint, render_template, request, jsonify
from services.analytics_service import AnalyticsService
from services.banking_service import BankingService
from routes.auth_routes import login_required, role_required
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')
analytics_service = AnalyticsService()
banking_service = BankingService()

# === Scenario 1: Real-time Transaction Monitoring (Fraud Detection Analyst) ===

@analytics_bp.route('/fraud-monitoring')
@login_required
@role_required('analyst')
def fraud_monitoring():
    """Fraud monitoring dashboard for analysts"""
    threshold = int(request.args.get('threshold', 70))
    
    dashboard_data = analytics_service.get_fraud_monitoring_dashboard(threshold)
    
    return render_template(
        'analytics/fraud_monitoring.html',
        data=dashboard_data,
        threshold=threshold
    )

@analytics_bp.route('/api/recent-transactions')
@login_required
@role_required('analyst')
def api_recent_transactions():
    """API endpoint for live transaction feed"""
    hours = int(request.args.get('hours', 24))
    limit = int(request.args.get('limit', 100))
    
    result = analytics_service.get_recent_transactions_feed(hours, limit)
    
    return jsonify(result)

@analytics_bp.route('/api/investigate/<transaction_id>')
@login_required
@role_required('analyst')
def api_investigate_transaction(transaction_id):
    """API endpoint for transaction investigation"""
    result = analytics_service.investigate_transaction(transaction_id)
    
    return jsonify(result)

@analytics_bp.route('/api/approve-transaction', methods=['POST'])
@login_required
@role_required('analyst')
def api_approve_transaction():
    """Approve a flagged transaction"""
    data = request.get_json()
    account_id = data.get('account_id')
    
    # Activate frozen account
    result = banking_service.account_model.activate_account(account_id)
    
    return jsonify(result)

@analytics_bp.route('/api/freeze-account', methods=['POST'])
@login_required
@role_required('analyst')
def api_freeze_account():
    """Freeze an account due to fraud"""
    data = request.get_json()
    account_id = data.get('account_id')
    
    result = banking_service.account_model.freeze_account(account_id)
    
    return jsonify(result)

# === Scenario 2: Custom Report Generation (Financial Manager) ===

@analytics_bp.route('/reports')
@login_required
@role_required('manager')
def reports():
    """Custom report generation dashboard for managers"""
    return render_template('analytics/reports.html')

@analytics_bp.route('/api/financial-report', methods=['POST'])
@login_required
@role_required('manager')
def api_financial_report():
    """Generate comprehensive financial report"""
    data = request.get_json()
    
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if not start_date or not end_date:
        # Default to last 30 days
        end_date = datetime.utcnow().isoformat()
        start_date = (datetime.utcnow() - timedelta(days=30)).isoformat()
    
    result = analytics_service.generate_financial_report(start_date, end_date)
    
    return jsonify(result)

@analytics_bp.route('/api/deposit-trends')
@login_required
@role_required('manager')
def api_deposit_trends():
    """Get deposit growth trends"""
    days = int(request.args.get('days', 30))
    
    result = analytics_service.get_deposit_growth_trends(days)
    
    return jsonify(result)

@analytics_bp.route('/api/transaction-volume')
@login_required
@role_required('manager')
def api_transaction_volume():
    """Get transaction volume analysis"""
    hours = int(request.args.get('hours', 24))
    
    result = analytics_service.get_transaction_volume_analysis(hours)
    
    return jsonify(result)

# === Scenario 3: Regulatory Compliance Monitoring (Compliance Officer) ===

@analytics_bp.route('/compliance')
@login_required
@role_required('compliance')
def compliance():
    """Compliance monitoring dashboard for compliance officers"""
    dashboard_data = analytics_service.get_compliance_dashboard()
    
    return render_template(
        'analytics/compliance.html',
        data=dashboard_data
    )

@analytics_bp.route('/api/compliance-drilldown')
@login_required
@role_required('compliance')
def api_compliance_drilldown():
    """Drill down into compliance metric"""
    metric_type = request.args.get('metric_type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    result = analytics_service.drill_down_compliance_metric(
        metric_type, start_date, end_date
    )
    
    return jsonify(result)
