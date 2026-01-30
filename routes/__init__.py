"""Routes for the Cloud Banking application"""

from .auth_routes import auth_bp
from .account_routes import account_bp
from .transaction_routes import transaction_bp
from .analytics_routes import analytics_bp

__all__ = ['auth_bp', 'account_bp', 'transaction_bp', 'analytics_bp']
