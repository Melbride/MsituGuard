from django.core.management.base import BaseCommand
from App.models import Reward

class Command(BaseCommand):
    help = 'Add special certificate for 15 billion trees initiative participants'

    def handle(self, *args, **options):
        certificate, created = Reward.objects.get_or_create(
            name='15 Billion Trees Initiative Certificate',
            defaults={
                'reward_type': 'certificate',
                'token_cost': 10,
                'description': 'Official certificate recognizing your participation in Kenya\'s 15 Billion Trees Initiative. Show the world you\'re helping restore Kenya\'s forests!',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created 15 Billion Trees Initiative Certificate!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('15 Billion Trees Initiative Certificate already exists')
            )