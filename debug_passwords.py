"""Quick debug script to check which passwords work for each user"""
import bcrypt
from local_storage import local_db

users = list(local_db.data['users'].values())
test_passwords = ['password123', 'Password123', 'admin123', 'Admin@123', 
                  '12345678', 'Password@123', 'password', 'Palak@123']

for u in users:
    email = u['Email']
    name = u['Name']
    h = u.get('PasswordHash', '')
    if not h:
        print(f"{email} ({name}) - NO PASSWORD HASH!")
        continue
    
    matching = [p for p in test_passwords if bcrypt.checkpw(p.encode(), h.encode())]
    if matching:
        print(f"{email} ({name}) - password: {matching[0]}")
    else:
        print(f"{email} ({name}) - NO MATCH found in test passwords")
