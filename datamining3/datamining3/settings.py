"""
Django settings for datamining3 project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

try:

    env_file_path = os.path.join(BASE_DIR, 'env_files', '.env')
    load_dotenv(env_file_path)

    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ALLOWED_HOSTS = str(os.getenv('ALLOWED_HOSTS')).split(',')
    DB_ENGINE = os.getenv('DB_ENGINE')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')
    GOOGLE_API = os.getenv('GOOGLE_API')
    #EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
    #EMAIL_HOST = os.getenv('EMAIL_HOST')
    #EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
    #EMAIL_PORT = os.getenv('EMAIL_PORT')
    #EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    #EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    #DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

except Exception as e:
    print(f'The app was unable to run because environment variables were not loaded properly.')
    exit()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #'rest_framework',
    'huey.contrib.djhuey',
    'pages',
    'tasks',
    'internals',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'datamining3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'template_filters': 'datamining3.template_filters',
            }
        },
    },
]

WSGI_APPLICATION = 'datamining3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if DB_ENGINE == 'sqlite3':
    DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{DB_ENGINE}',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

elif DB_ENGINE == 'postgresql':

    DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{DB_ENGINE}',
        'NAME': DB_NAME,
	    'USER': DB_USER,
	    'PASSWORD': DB_PASSWORD,
	    'HOST': DB_HOST,
	    'PORT': DB_PORT,
        }
    }

else:
    raise Exception(f'Unsupported database engine. Check DB_ENGINE parameter in {env_file_path}.')


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_files')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


if DB_ENGINE == 'sqlite3':

    HUEY = {
    'huey_class': 'huey.SqliteHuey',
    'name': DATABASES['default']['NAME'],
    'results': True,  # Store return values of tasks.
    'store_none': False,  # If a task returns None, do not save to results.
    'immediate': False,
    'consumer': {
        'workers': 1,
        'worker_type': 'thread',
        'initial_delay': 0.1,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 10.0,  # Max possible polling interval, -m.
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 1,  # Check worker health every second.
        },
    }

elif DB_ENGINE == 'postgresql':

    HUEY = {
    'huey_class': 'huey.contrib.sql_huey.SqlHuey',
    'database': f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    'name': DATABASES['default']['NAME'],
    'results': True,  # Store return values of tasks.
    'store_none': False,  # If a task returns None, do not save to results.
    'immediate': False,
    'consumer': {
        'workers': 1,
        'worker_type': 'thread',
        'initial_delay': 0.1,  # Smallest polling interval, same as -d.
        'backoff': 1.15,  # Exponential backoff using this rate, -b.
        'max_delay': 10.0,  # Max possible polling interval, -m.
        'scheduler_interval': 1,  # Check schedule every second, -s.
        'periodic': True,  # Enable crontab feature.
        'check_worker_health': True,  # Enable worker health checks.
        'health_check_interval': 1,  # Check worker health every second.
        },
    } 

else:
    raise Exception(f'Unsupported Huey configuration. Check DB_ENGINE parameter in {env_file_path}.')
