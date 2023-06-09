import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyBank.settings')
app = Celery('MyBank')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'add-every-120-seconds': {
        'task': 'app.tasks.update',
        'schedule': 300,
    },
}
