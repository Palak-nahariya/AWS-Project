from flask import Flask, session
from datetime import timedelta
from config import Config
from routes import auth_bp, account_bp, transaction_bp, analytics_bp

# Create Flask application
app = Flask(__name__)

# Configuration
app.config.from_object(Config)

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=Config.SESSION_TIMEOUT)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(analytics_bp)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404

@app.errorhandler(500)
def internal_error(error):
    return "Internal server error", 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
