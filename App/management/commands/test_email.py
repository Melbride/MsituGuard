from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email sending functionality'

    def handle(self, *args, **options):
        try:
            send_mail(
                subject='Test Email - MsituGuard',
                message='This is a test email to verify email functionality.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['melbrideb@gmail.com'],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS('Test email sent successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Email failed: {e}'))