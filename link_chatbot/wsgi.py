import os
import environ

env = environ.Env()
base = environ.Path(__file__) - 2
environ.Env.read_env(env_file=base('.env'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env('DJANGO_SETTINGS_MODULE'))

application = get_wsgi_application()

