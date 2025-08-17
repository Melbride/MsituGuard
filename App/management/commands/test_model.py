from django.core.management.base import BaseCommand
from App.views import load_classification_model, classify_alert_image
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Test the image classification model'

    def handle(self, *args, **options):
        self.stdout.write('Testing model loading...')
        
        # Test model loading
        model = load_classification_model()
        if model:
            self.stdout.write(self.style.SUCCESS('Model loaded successfully!'))
            self.stdout.write(f'Model input shape: {model.input_shape}')
        else:
            self.stdout.write(self.style.ERROR('Failed to load model'))
            
        # Check if model file exists
        model_path = os.path.join(settings.BASE_DIR, 'App', 'models', 'alert-image_classifier_model.keras')
        if os.path.exists(model_path):
            self.stdout.write(f'Model file found at: {model_path}')
        else:
            self.stdout.write(self.style.ERROR(f'Model file not found at: {model_path}'))