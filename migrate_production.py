#!/usr/bin/env python
"""
Script to help with production database migration
Run this locally to generate the migration commands you need to run on Render
"""

import os
import django
from django.core.management import execute_from_command_line

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crisis_communication.settings')
django.setup()

print("=== PRODUCTION DATABASE MIGRATION GUIDE ===")
print()
print("Your production database is missing the new Profile model fields.")
print("You need to run these commands on your Render deployment:")
print()
print("1. SSH into your Render service or use Render's shell:")
print("   python manage.py makemigrations App")
print("   python manage.py migrate")
print()
print("2. If that doesn't work, try:")
print("   python manage.py makemigrations App --empty")
print("   # Then edit the migration file to add the missing fields")
print("   python manage.py migrate")
print()
print("3. Alternative - Reset database (WARNING: This will delete all data):")
print("   python manage.py flush")
print("   python manage.py migrate")
print()
print("=== MISSING FIELDS IN PRODUCTION ===")
print("The production database is missing these Profile fields:")
print("- phoneNumber")
print("- account_type") 
print("- donor_tier")
print("- monthly_contribution")
print("- total_donated")
print("- donor_since")
print()
print("Your local database has these fields, but production doesn't.")