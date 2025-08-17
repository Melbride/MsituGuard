import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msituguard_fire_risk.settings')
application = get_asgi_application()
