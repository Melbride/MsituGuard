from django.core.management.base import BaseCommand
from App.models import TreePlanting

class Command(BaseCommand):
    help = 'Award tokens for verified tree plantings that haven\'t received them yet'

    def handle(self, *args, **options):
        # Find verified tree plantings that haven't been awarded tokens
        verified_plantings = TreePlanting.objects.filter(
            status='verified',
            tokens_awarded=False
        )
        
        count = 0
        for planting in verified_plantings:
            if planting.award_tokens():
                count += 1
                self.stdout.write(f"Awarded tokens for: {planting.title}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully awarded tokens to {count} tree plantings')
        )