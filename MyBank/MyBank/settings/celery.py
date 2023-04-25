"""All settings for Celery."""
import os

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
