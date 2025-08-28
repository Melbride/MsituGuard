#!/usr/bin/env python
"""
Reset organization user password
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crisis_communication.settings')
django.setup()

from django.contrib.auth.models import User
from App.models import UserProfile

def reset_org_password():
    """Reset organization password"""
    try:
        # Find organization user
        org_user = User.objects.get(username='demo_org')
        
        # Reset password
        org_user.set_password('MsituGuard2024!')
        org_user.save()
        
        print("✅ Organization password reset successfully!")
        print("Username: demo_org")
        print("New Password: MsituGuard2024!")
        
    except User.DoesNotExist:
        print("❌ Organization user 'demo_org' not found")
        print("Creating new organization user...")
        
        # Create new organization user
        org_user = User.objects.create_user(
            username='demo_org',
            email='org@msituguard.co.ke',
            password='MsituGuard2024!',
            first_name='Demo',
            last_name='Organization'
        )
        
        # Create profile
        UserProfile.objects.create(
            user=org_user,
            user_type='organization',
            phone_number='0700000002',
            location='Nairobi, Kenya'
        )
        
        print("✅ New organization user created!")
        print("Username: demo_org")
        print("Password: MsituGuard2024!")

if __name__ == "__main__":
    reset_org_password()