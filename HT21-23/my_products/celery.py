import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_products.settings')

app = Celery('my_products')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
