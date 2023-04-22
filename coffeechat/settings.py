"""
Django settings for coffeechat project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fwet4_u)b)1tv9my2^&vb+7v=byk*x3!n(-w+3-x=+!-m!cqy&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '192.168.50.188', 'localhost']
INTERNAL_IPS = ['172.20.0.1']

# Application definition

INSTALLED_APPS = [
    # django default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party packages
    'rest_framework',
    'django_filters',
    'debug_toolbar',
    'notifications',

    #project apps
    'accounts',
    'tweets',
    'friendships',
    'newsfeeds',
    'comments',
    'likes',
    'inbox',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS':[
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'coffeechat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'coffeechat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'twitter',
        'HOST': '192.168.50.188',
        #'HOST': 'mysql8',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456',
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# translate our steps into SQL query
# LOGGING = {
#     'version':1,
#     'disable_existing_loggers': False,
#     'handlers':{
#         'console':{
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'handler': ['console'],
#             'propagate': True,
#             'level': 'DEBUG',
#         },
#     }
# }
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# https://docs.djangoproject.com/en/3.1/topics/cache/
# use `pip install python-memcached`
# DO NOT pip install memcache or django-memcached
CACHES = {
    'default': {
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        #'LOCATION': '172.20.0.2:11211',
        'TIMEOUT': 86400,
    },
    'testing': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        #'LOCATION': '172.20.0.2:11211',
        'TIMEOUT': 86400,
        'KEY_PREFIX': 'testing',
    },
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# traditional way
# MEDIA_ROOT = '/media/'
# MEDIA_URL = '/media/'

# current way
# use cloud service
# currently use Amazon S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
TESTING = ((" ".join(sys.argv)).find('manage.py test') != -1)
if TESTING:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

AWS_STORAGE_BUCKET_NAME = 'django-coffeechat'
AWS_S3_REGION_NAME = 'us-east-1'

MEDIA_ROOT = 'media/'

# Redis
# install in docker and then install python server
# pip install redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0 if TESTING else 1
REDIS_KEY_EXPIRE_TIME = 7 * 86400

try:
    from .local_settings import *
except:
    pass
