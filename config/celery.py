import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app.conf.broker_url = REDIS_URL

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
