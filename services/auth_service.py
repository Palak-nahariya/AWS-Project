from models.user import User
import uuid

class AuthService:
    """Authentication service for user login, registration, and session management"""
    
    def __init__(self):
        self.user_model = User()
    
    def register(self, name, email, password, role='customer'):
        """Register a new user"""
        # Validate input
        if not name or not email or not password:
            return {'success': False, 'error': 'All fields are required'}
        
        if len(password) < 8:
            return {'success': False, 'error': 'Password must be at least 8 characters'}
        
        # Check if email already exists
        existing_user = self.user_model.get_user_by_email(email)
        if existing_user:
            return {'success': False, 'error': 'Email already registered'}
        
        # Create user with unique ID
        user_id = str(uuid.uuid4())
        result = self.user_model.create_user(user_id, name, email, password, role)
        
        return result
    
    def login(self, email, password):
        """Authenticate user and return user data"""
        # Validate input
        if not email or not password:
            return {'success': False, 'error': 'Email and password are required'}
        
        # Authenticate
        result = self.user_model.authenticate(email, password)
        
        return result
    
    def get_user(self, user_id):
        """Get user by ID (for session validation)"""
        user = self.user_model.get_user_by_id(user_id)
        if user:
            # Remove sensitive data
            user.pop('PasswordHash', None)
            return {'success': True, 'user': user}
        return {'success': False, 'error': 'User not found'}
    
    def update_profile(self, user_id, updates):
        """Update user profile"""
        # Prevent updating sensitive fields
        sensitive_fields = ['UserID', 'PasswordHash', 'CreatedAt']
        filtered_updates = {k: v for k, v in updates.items() if k not in sensitive_fields}
        
        if not filtered_updates:
            return {'success': False, 'error': 'No valid fields to update'}
        
        return self.user_model.update_user(user_id, filtered_updates)
