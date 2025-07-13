# Fix Production Database Issue

## Problem
Your production database on Render is missing the new Profile model fields that you added locally.

## Quick Fix Options

### Option 1: Run Migrations on Render (Recommended)
1. Go to your Render dashboard
2. Open your web service
3. Go to "Shell" tab
4. Run these commands:
```bash
python manage.py makemigrations App
python manage.py migrate
```

### Option 2: Reset Database (Will Delete All Data)
If Option 1 doesn't work:
```bash
python manage.py flush
python manage.py migrate
```

### Option 3: Manual Migration
Create a new migration file:
```bash
python manage.py makemigrations App --empty
```
Then edit the migration to add missing fields.

## Missing Fields in Production
Your production Profile table is missing:
- phoneNumber
- account_type
- donor_tier  
- monthly_contribution
- total_donated
- donor_since

## Prevention
Always run migrations on production after model changes:
```bash
git push  # Deploy to Render
# Then in Render shell:
python manage.py migrate
```