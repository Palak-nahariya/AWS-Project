"""
Test script to verify the password hash fix
This script tests that users can authenticate successfully after the password hash fix
"""
import sys
sys.path.insert(0, r'C:\Users\khurai\OneDrive\Desktop\AWS Project')

from models.user import User

# Test cases for previously affected users
test_users = [
    ('ken@mail.com', 'password123'),
    ('admin@gmail.com', 'password123'),
    ('tushar@gmail.com', 'password123'),
    ('priyanshu@gmail.com', 'password123'),
    ('k@gmail.com', 'password123'),
    ('p@gmail.com', 'password123'),
    ('t@gmail.com', 'password123'),
]

# Test users that already had password hashes
existing_users = [
    'shivali@gmail.com',
    'priya@gmail.com',
    'ritu@gmail.com'
]

print("=" * 60)
print("Testing Password Hash Fix")
print("=" * 60)
print()

user_model = User()
all_passed = True

# Test previously affected users
print("1. Testing previously affected users (should now work):")
print("-" * 60)
for email, password in test_users:
    result = user_model.authenticate(email, password)
    if result['success']:
        print(f"✓ {email}: PASS - Login successful")
    else:
        print(f"✗ {email}: FAIL - {result['error']}")
        all_passed = False
print()

# Test existing users (should still work)
print("2. Verifying existing users still work:")
print("-" * 60)
for email in existing_users:
    user = user_model.get_user_by_email(email)
    if user and 'PasswordHash' in user:
        print(f"✓ {email}: PASS - PasswordHash exists")
    else:
        print(f"✗ {email}: FAIL - PasswordHash missing")
        all_passed = False
print()

# Summary
print("=" * 60)
if all_passed:
    print("✓ ALL TESTS PASSED - Password hash fix successful!")
else:
    print("✗ SOME TESTS FAILED - Review errors above")
print("=" * 60)
