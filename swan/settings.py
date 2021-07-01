"""
Django settings for swan project.
Generated by 'django-admin startproject' using Django 3.1.7.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""


import os
from datetime import timedelta
from pathlib import Path


from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
#test to check cicd
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY","koshtamshepesh")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


#ALLOWED_HOSTS = []


load_dotenv()

ALLOWED_HOSTS = ['anatidaephobia.pythonanywhere.com', 'localhost', '127.0.0.1']
allowed_hosts_string = os.getenv("ALLOWED_HOSTS")

if allowed_hosts_string != None and len(allowed_hosts_string) != 0:
    allowed_host_list = allowed_hosts_string.split(", ")

    for allowed_host in allowed_host_list:
        if len(allowed_host) != 0:
            ALLOWED_HOSTS.append(str(allowed_host).strip())


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    "django_prometheus",
    'rest_framework',
    'django_minio_backend',
    'users',
    'team',
    'request_checker',
    'corsheaders',
    'socialmedia',
    'post',
    'scheduler',
    'filestorage',
    'postideas',
    'notification',
]
CORS_ORIGIN_ALLOW_ALL = True

MINIO_CONSISTENCY_CHECK_ON_START = True

MINIO_ENDPOINT="stage-minio:9000"
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin"
MINIO_USE_HTTPS = False
MINIO_URL_EXPIRY_HOURS = timedelta(days=1)
MINIO_CONSISTENCY_CHECK_ON_START = True
MINIO_PRIVATE_BUCKETS = [
    'django-backend-dev-private',
]

MINIO_PUBLIC_BUCKETS = [
    'django-backend-dev-public',
]


MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware'
]

ROOT_URLCONF = 'swan.urls'

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

WSGI_APPLICATION = 'swan.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'postgres'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

HOST = "http://localhost:8000/"
STATIC_URL = '/static/'
STATIC_ROOT = '/static/',
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", '')
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", '')
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")

# user models
AUTH_USER_MODEL = 'users.User'
ACCESS_TOKEN_EXPIRE_TIME = timedelta(days=0, hours=5, minutes=0)
REFRESH_TOKEN_EXPIRE_TIME = timedelta(days=2, hours=0, minutes=0)
# REST framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authenticators.JWTAuthenticator',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

#Crons
CRONJOBS = [
    ('* * * * *', 'scheduler.cron.Queue_jobs', '>>'+os.path.join(BASE_DIR,'scheduler/logs/queue_jobs.log')),
    ('* * * * *', 'scheduler.cron.Dequeue_Jobs', '>>'+os.path.join(BASE_DIR,'scheduler/logs/dequeue_jobs.log'))
]
CRONTAB_COMMAND_SUFFIX = '2>&1'