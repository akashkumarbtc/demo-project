from link_chatbot.settings.base import *


SECRET_KEY = env('SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = env('PRODUCTION_ALLOWED_HOST').split(',')


DATABASES = {
    'default': {
        'ENGINE'   : env('DATABASE_ENGINE'),
        'NAME'     : env('DATABASE_NAME'),
        'USER'     : env('DATABASE_USER'),
        'PASSWORD' : env('DATABASE_PASSWORD'),
        'HOST'     : env('DATABASE_HOST'),
        'PORT'     : env('DATABASE_PORT'),
    }
}

# S3 BUCKETS CONFIGURATION

AWS_ACCESS_KEY_ID       = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE   = False
AWS_DEFAULT_ACL         = None
AWS_QUERYSTRING_AUTH    = False

DEFAULT_FILE_STORAGE    = 'storages.backends.s3boto3.S3Boto3Storage'

INSTALLED_APPS +=['corsheaders',]

CSRF_TRUSTED_ORIGINS= ['https://idia-backend.linkintime.co.in']


FORGOT_PASSWORD_HOST = "https://idia-admin.linkintime.co.in"

# Django RestFramework settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [

    ],
    'DEFAULT_THROTTLE_RATES': {
        "banner_scope": '20/min',
        "main_menu_scope": '15/min',
        "branch_scope": "30/min",
        "rating_scope": '10/min',
        "feedback_scope": '25/min',
        "mail_selected": '5/min',
        "isin_scope": '10/min',
        "question-list-throttle": '10/min',
        'context-list-throttle': '5/min',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

# JWT token settings

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    "ROTATE_REFRESH_TOKENS" : True,
}