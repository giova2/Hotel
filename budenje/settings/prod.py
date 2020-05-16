from budenje.settings.base import *
import os
DEBUG = False
ALLOWED_HOSTS = ['giova.pythonanywhere.com']

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('BUD_DATABASE_NAME', 'budenje'),
        'USER': os.environ.get('BUD_DATABASE_USER', 'giova'),
        'PASSWORD': os.environ.get('BUD_DATABASE_PASSWORD', 'falacia4,'),
        'HOST': os.environ.get('BUD_DATABASE_HOST', 'localhost'),
        # 'PORT': 3306,
    }
}