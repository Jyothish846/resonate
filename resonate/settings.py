import dj_database_url
import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------------------------------------------------------
# ENVIRONMENT & SECURITY CONFIGURATION
# ----------------------------------------------------------------------

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

if DEBUG:
    # Local Development: Allow localhost and standard IP addresses
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '::1']
    CSRF_TRUSTED_ORIGINS = []
else:
    # Production configuration
    ALLOWED_HOSTS_STRING = config('ALLOWED_HOSTS', default='')
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STRING.split(',') if host.strip()]
    CSRF_TRUSTED_ORIGINS = ['https://' + host for host in ALLOWED_HOSTS]
    RENDER_URL = os.environ.get('RENDER_EXTERNAL_URL')
    if RENDER_URL and 'https://' + RENDER_URL not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append('https://' + RENDER_URL)
        
    # Force connection over HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    DEBUG_PROPAGATE_EXCEPTIONS = True

# ----------------------------------------------------------------------
# END ENVIRONMENT & SECURITY CONFIGURATION
# ----------------------------------------------------------------------


# Application definition
INSTALLED_APPS = [ 
    'whitenoise.runserver_nostatic', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Removed 'storages' as it is not needed for FileSystemStorage.
    
    # Project Apps
    'accounts',
    'channels',
    'chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'resonate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'resonate.wsgi.application'

# ----------------------------------------------------------------------
# DATABASES CONFIGURATION
# ----------------------------------------------------------------------

if 'DATABASE_URL' in os.environ:
    DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ----------------------------------------------------------------------
# END DATABASES CONFIGURATION
# ----------------------------------------------------------------------


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ----------------------------------------------------------------------
# STATIC & MEDIA FILES CONFIGURATION (MINI-PROJECT/EPHEMERAL MEDIA)
# ----------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles" 

STATICFILES_DIRS = [
    BASE_DIR / 'static', 
]


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media" 

# FIX: Simple, universal storage configuration.
# WARNING: Media files (user uploads) will be lost on deployment/restart on Render.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ----------------------------------------------------------------------
# END STATIC & MEDIA FILES CONFIGURATION
# ----------------------------------------------------------------------


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = "accounts:my_profile" 
LOGOUT_REDIRECT_URL = "accounts:login" 
PASSWORD_CHANGE_REDIRECT_URL = 'accounts:edit_profile' 
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
ASGI_APPLICATION = 'resonate.asgi.application'