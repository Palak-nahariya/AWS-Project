"""
Simple script to generate a bcrypt hash for 'password123'
"""
import bcrypt

password = "password123"
password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
print(f"Password: {password}")
print(f"Hash: {password_hash}")
