# -*- coding: utf-8 -*-
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('joni2back', 'joni2back@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        #USE: CREATE DATABASE dj_classifieds CHARACTER SET utf8;
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj_classifieds',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB;',
            'charset': 'utf8',
        },
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1', '*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

MAIN_PATH = os.path.dirname(os.path.realpath(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(MAIN_PATH, 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/assets/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(MAIN_PATH, 'assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '71_zi6o7*xw6#n#-2m=qkf#tdzezw79dj6)2s*u2m0f!jv_#zl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'classifieds.middleware.LocaleMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'classifieds.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'classifieds.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(MAIN_PATH, 'templates')
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'main',
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(levelname)s]: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(MAIN_PATH, 'classijango.log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'classijango': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@classijango'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

CLASSIFIED_LIST_MAX_ITEMS_QUERY = 100
CLASSIFIED_LIST_MAX_ITEMS_PER_PAGE = 4

CLASSIFIED_THUMBNAILS_CONVERSION_TYPE = 'JPEG'
CLASSIFIED_THUMBNAILS_EXT = 'jpg'
CLASSIFIED_THUMBNAILS = {
    'thumb150x150': {
        'width': 150,
        'height': 150,
        'quality': 95,
    },
    'thumb150x110': {
        'width': 150,
        'height': 110,
        'quality': 95,
    },
    'thumb270x195': {
        'width': 270,
        'height': 195,
        'quality': 80,
    },
    'thumb320x240': {
        'width': 320,
        'height': 240,
        'quality': 80,
    },
    'thumb500x400': {
        'width': 500,
        'height': 400,
        'quality': 80,
    },
    'thumb620x410': {
        'width': 620,
        'height': 410,
        'quality': 80,
    },
}
