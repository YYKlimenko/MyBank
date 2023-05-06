DEBUG = True
if DEBUG:
    from dotenv import load_dotenv
    load_dotenv()

from .api import CURRENCIES_API_URL, MOEX_STOCK_API_URL
from .authentication import AUTH_PASSWORD_VALIDATORS, REST_FRAMEWORK, SIMPLE_JWT
from .celery import CELERY_BROKER_URL
from .database import DATABASES
from .logging import LOGGING
from .main import (
    BASE_DIR, SECRET_KEY, ALLOWED_HOSTS, INSTALLED_APPS, MIDDLEWARE, ROOT_URLCONF, WSGI_APPLICATION,
    LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ, STATIC_URL, STATIC_ROOT, CORS_ALLOW_HEADERS, CORS_ALLOW_ALL_ORIGINS,
    TEMPLATES,
)
if DEBUG:
    DATABASES['default'] = DATABASES['develop'] if DEBUG else DATABASES['production']
