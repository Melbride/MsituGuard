from django.core.management.base import BaseCommand
from App.models import TreePlanting

class Command(BaseCommand):
    help = 'Check status of tree plantings and token awards'

    def handle(self, *args, **options):
        plantings = TreePlanting.objects.all().order_by('-planted_date')
        
        self.stdout.write("Tree Planting Status Report:")
        self.stdout.write("-" * 50)
        
        for planting in plantings:
            planter_name = planting.planter.username if planting.planter else "Unregistered"
            self.stdout.write(
                f"ID: {planting.id} | {planting.title} | "
                f"Planter: {planter_name} | Status: {planting.status} | "
                f"Tokens Awarded: {planting.tokens_awarded} | Trees: {planting.number_of_trees}"
            )
        
        # Summary
        total = plantings.count()
        verified = plantings.filter(status='verified').count()
        tokens_awarded = plantings.filter(tokens_awarded=True).count()
        
        self.stdout.write("-" * 50)
        self.stdout.write(f"Total: {total} | Verified: {verified} | Tokens Awarded: {tokens_awarded}")