"""All settings to connect to the Databases."""
import os


DATABASES = {
    'develop': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '../db.sqlite3',
    },
    'production': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_LOGIN'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
