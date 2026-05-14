import os
import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immogab.settings')

app = celery.Celery('immogab')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
