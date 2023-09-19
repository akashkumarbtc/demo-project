from link_chatbot.settings.base import *


SECRET_KEY = 'django-insecure-_i%y#dpq-guq4k=@z!28e$mqejnq3qxz%_o_5k+bmfk#9t6n_+'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS +=['debug_toolbar',]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware",]

INTERNAL_IPS = [
    '127.0.0.1',
]

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