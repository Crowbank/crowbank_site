"""
Django settings for crowbank_site project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3-atf&yi@$06^#g1d!uv5x$-aneuw42%8opsy5)trrl5-fa5v1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'widget_tweaks',
    'petadmin.apps.PetadminConfig',
    'intranet.apps.IntranetConfig',
    'messaging.apps.MessagingConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crowbank_site.urls'

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
        },
    },
]

WSGI_APPLICATION = 'crowbank_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

if os.name == 'nt':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '192.168.1.109',
            'NAME': 'petadmin_data',
            'USER': 'pa',
            'PASSWORD': 'petadmin',
            'PORT': '3306'
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'crowbank$petadmin',
            'USER': 'crowbank',
            'PASSWORD': 'petadmin',
            'HOST': 'crowbank.mysql.pythonanywhere-services.com',
            'PORT': '3306'
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

if os.name == 'nt':
    STATIC_ROOT = 'static/'
else:
    STATIC_ROOT = '/home/crowbank/crowbank_site/static'

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'staticfiles'), # if your static files folder is named "staticfiles"
#)

EMAIL_HOST = 'ned.enixns.com'
EMAIL_HOST_PASSWORD = 'Crowb@nk454!'
EMAIL_HOST_USER = 'info@crowbank.co.uk'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'info@crowbank.co.uk'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'normal': {
            'format': '[%(levelname)5s] %(asctime)s %(module)s %(message)100s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'when': 'W0',
            'filename': os.path.join(os.path.dirname(__file__), 'django.log')
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'when': 'W0',
            'filename': os.path.join(os.path.dirname(__file__), 'debug.log')
        },
        'important': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(os.path.dirname(__file__), 'important.log')
        },
        'email': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html': True,
        }
    },
    'loggers': {
        'crowbank': {
            'handlers': ['debug', 'email', 'important'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['django'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

ADMINS = [('Eran', 'crowbank.partners@gmail.com')]
