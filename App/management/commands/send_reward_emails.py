from django.core.management.base import BaseCommand
from App.models import TreePlanting
from App.views import send_tree_verification_notification

class Command(BaseCommand):
    help = 'Send reward emails for recently verified tree plantings'

    def handle(self, *args, **options):
        # Find verified tree plantings with registered users
        verified_plantings = TreePlanting.objects.filter(
            status='verified',
            tokens_awarded=True,
            planter__isnull=False
        )
        
        count = 0
        for planting in verified_plantings:
            try:
                send_tree_verification_notification(planting)
                count += 1
                self.stdout.write(f"Sent reward email for: {planting.title}")
            except Exception as e:
                self.stdout.write(f"Failed to send email for {planting.title}: {e}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {count} reward emails')
        )