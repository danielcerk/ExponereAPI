# Para local, windows: python -m celery -A core worker -l info -P solo
# Para produção, linux: python -m celery -A core worker


import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()