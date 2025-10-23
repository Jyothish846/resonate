import dj_database_url
import os
from pathlib import Path
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------------------------------------------------------
# ENVIRONMENT & SECURITY CONFIGURATION (CRITICAL FOR RENDER DEPLOYMENT)
# ----------------------------------------------------------------------

# SECRET_KEY MUST be set as an environment variable on Render
SECRET_KEY = config('SECRET_KEY')

# DEBUG must be set to False on Render
DEBUG = config('DEBUG', default=True, cast=bool)


if DEBUG:
    # Local Development: Allow localhost and standard IP addresses
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '::1']
    # CSRF settings are only critical in production, but good practice locally
    CSRF_TRUSTED_ORIGINS = []
else:
    # Production: Get the ALLOWED_HOSTS string from the environment.
    ALLOWED_HOSTS_STRING = config('ALLOWED_HOSTS', default='')
    
    # Manually split the string by commas and strip spaces (more reliable than Csv() for single values)
    # This creates the required Python list: ['resonate-33s5.onrender.com']
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STRING.split(',') if host.strip()]

    # 💥 CRITICAL CHECK: Define CSRF_TRUSTED_ORIGINS
    # CSRF_TRUSTED_ORIGINS requires the 'https://' prefix.
    
    # Create the list of trusted origins from the host list
    CSRF_TRUSTED_ORIGINS = ['https://' + host for host in ALLOWED_HOSTS]
    
    # Add RENDER_EXTERNAL_URL for robustness on Render, if it exists
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

# dj_database_url.config() will automatically read from the DATABASE_URL 
# environment variable if it exists.
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True, # Critical for Render's PostgreSQL connection
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
# STATIC FILES CONFIGURATION (FOR WHITENOISE/RENDER)
# ----------------------------------------------------------------------

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