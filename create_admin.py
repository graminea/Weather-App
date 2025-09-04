#!/usr/bin/env python3
"""
Script to create an admin user for testing
"""

import hashlib
from database import Database
from user import User

def create_admin_user():
    db = Database()
    
    # Check if admin already exists
    existing_admin = db.find_one('users', {'is_admin': 'admin'})
    if existing_admin:
        print(f"Admin user already exists: {existing_admin['username']}")
        return
    
    # Create admin user
    username = input("Enter admin username (default: admin): ").strip() or "admin"
    password = input("Enter admin password (default: admin123): ").strip() or "admin123"
    
    # Hash password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Create admin user
    admin_user = User(username, hashed_password, 'admin')
    
    try:
        db.insert_one('users', admin_user.to_dict())
        print(f"✅ Admin user '{username}' created successfully!")
        print(f"Password: {password}")
        print("\nYou can now login with these credentials.")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")

if __name__ == "__main__":
    print("🔧 Weather App - Admin User Creator")
    print("=" * 40)
    create_admin_user()
