# ussdapp/africastalking_init.py

import africastalking
from django.conf import settings

# Initialize Africa's Talking API
africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)

