import dj_database_url
import os
from pathlib import Path
from decouple import config, Csv 


BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------------------------------------------------------
# ENVIRONMENT CONFIGURATION (FIX FOR RENDER CRASH)
# ----------------------------------------------------------------------

# SECRET_KEY MUST be set as an environment variable on Render
SECRET_KEY = config('SECRET_KEY')

# DEBUG must be set to False on Render (in environment variables)
# We default to True for local development if not specified
DEBUG = config('DEBUG', default=True, cast=bool)


if DEBUG:
    # Local Development: Allow localhost and standard IP addresses
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '::1']
else:
    # Production: Require ALLOWED_HOSTS to be explicitly set on Render
    # e.g., 'resonate-33s5.onrender.com'
    # It will read the value from the environment variable set on Render.
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())
    # Ensure all your production configuration is applied when DEBUG is False:
    CSRF_TRUSTED_ORIGINS = ['https://' + host for host in ALLOWED_HOSTS if host]
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
# ----------------------------------------------------------------------
# END ENVIRONMENT CONFIGURATION
# ----------------------------------------------------------------------


# Application definition
INSTALLED_APPS = [
    # Static file serving optimization for production 
    'whitenoise.runserver_nostatic', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
]

MIDDLEWARE = [
    # 1. SECURITY MIDDLEWARE MUST BE FIRST FOR SECURITY HEADERS
    'django.middleware.security.SecurityMiddleware',
    
    # 2. WHITENOISE MUST COME AFTER SECURITY MIDDLEWARE
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
# DATABASES CONFIGURATION (FIX FOR RENDER CRASH)
# ----------------------------------------------------------------------

# This configuration checks for the DATABASE_URL environment variable 
# and correctly uses dj_database_url to configure PostgreSQL for Render.
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            # No 'default=config('DATABASE_URL')' needed; it reads from os.environ
            conn_max_age=600,
            ssl_require=True,
        )
    }
# Otherwise (e.g., local development), fall back to SQLite.
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
    # ... (Keep your original validators here)
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ----------------------------------------------------------------------
# STATIC FILES CONFIGURATION (FIX FOR CSS ISSUE)
# ----------------------------------------------------------------------
# WhiteNoise serves static files in production from STATIC_ROOT.

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") # Where collectstatic puts files

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # Where Django looks for static files locally
]

# Define the storage backend explicitly for WhiteNoise (modern practice)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ----------------------------------------------------------------------
# END STATIC FILES CONFIGURATION
# ----------------------------------------------------------------------


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = "accounts:profile"
LOGOUT_REDIRECT_URL = "accounts:login"
PASSWORD_CHANGE_REDIRECT_URL = 'accounts:edit_profile' 


EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)