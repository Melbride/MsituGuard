from django.core.management.base import BaseCommand
from App.models import Reward

class Command(BaseCommand):
    help = 'Create sample rewards for the tokenization system'

    def handle(self, *args, **options):
        rewards_data = [
            {
                'name': '1GB Data Bundle',
                'reward_type': 'data_bundle',
                'token_cost': 5,
                'description': 'Get 1GB of mobile data to stay connected while protecting the environment.',
                'is_active': True
            },
            {
                'name': '5GB Data Bundle',
                'reward_type': 'data_bundle',
                'token_cost': 20,
                'description': 'Premium 5GB data bundle for heavy environmental monitoring activities.',
                'is_active': True
            },
            {
                'name': 'Tree Planting Kit',
                'reward_type': 'tree_kit',
                'token_cost': 15,
                'description': 'Complete tree planting kit with seeds, tools, and planting guide for indigenous species.',
                'is_active': True
            },
            {
                'name': 'Advanced Tree Kit',
                'reward_type': 'tree_kit',
                'token_cost': 35,
                'description': 'Professional tree planting kit with 50 indigenous seedlings and advanced tools.',
                'is_active': True
            },
            {
                'name': 'Environmental Workshop Access',
                'reward_type': 'workshop',
                'token_cost': 25,
                'description': 'Access to online environmental protection workshops and training sessions.',
                'is_active': True
            },
            {
                'name': 'Conservation Leadership Workshop',
                'reward_type': 'workshop',
                'token_cost': 50,
                'description': 'Exclusive leadership workshop for environmental conservation champions.',
                'is_active': True
            },
            {
                'name': 'Environmental Guardian Certificate',
                'reward_type': 'certificate',
                'token_cost': 30,
                'description': 'Official certificate recognizing your contribution to environmental protection.',
                'is_active': True
            },
            {
                'name': 'Conservation Champion Certificate',
                'reward_type': 'certificate',
                'token_cost': 75,
                'description': 'Premium certificate for top environmental conservation champions with special recognition.',
                'is_active': True
            }
        ]

        created_count = 0
        for reward_data in rewards_data:
            reward, created = Reward.objects.get_or_create(
                name=reward_data['name'],
                defaults=reward_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created reward: {reward.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Reward already exists: {reward.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new rewards!')
        )