"""
Django settings for camfeeder project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from fnmatch import fnmatch
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

DJANGO_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ""))
BASE_DIR = os.path.normpath(os.path.join(DJANGO_DIR, "../"))

AUTH_USER_MODEL = 'users.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9#q=fcs14z9i0(dwv#d8btxior=psx*@8y^!cjm=*ip%1neyhp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'camfeeder.users',
    'camfeeder.feeder',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'camfeeder.urls'

WSGI_APPLICATION = 'camfeeder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'camfeeder',
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '0.0.0.0',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/dashboard/'

STATICFILES_DIRS = (
    os.path.join(DJANGO_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "static")

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    os.path.join(DJANGO_DIR, "templates"),
)
