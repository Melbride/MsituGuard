from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Automatically run migrations on production deployment'

    def handle(self, *args, **options):
        self.stdout.write('Starting production migration...')
        
        try:
            # Check if we're on Render
            if os.environ.get('RENDER') == 'true':
                self.stdout.write('Detected Render environment')
                
                # Run makemigrations
                self.stdout.write('Creating migrations...')
                call_command('makemigrations', 'App', verbosity=2)
                
                # Run migrate
                self.stdout.write('Applying migrations...')
                call_command('migrate', verbosity=2)
                
                self.stdout.write(self.style.SUCCESS('Production migration completed successfully!'))
            else:
                self.stdout.write('Not in production environment, skipping...')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration failed: {str(e)}'))
            # Don't raise exception to prevent deployment failure