from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", 'django-insecure-0%h8gn3k^k+r=mzmgf=l%+mtfh#1g6*6li25vo(&bwj9pf%+w=')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

DEBUG_STATE = config('DEBUG', default=True, cast=bool)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG_STATE

# Email settings
if DEBUG_STATE != True:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')

    # Default "from" email address
    DEFAULT_FROM_EMAIL = 'noreply@eeveeemporium.com'
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
else:
    # Use console backend for development
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "eeveeemporium-a0b363641244.herokuapp.com/",
    ".herokuapp.com",
]
DOMAIN = "https://eeveeemporium-a0b363641244.herokuapp.com/"
SITE_NAME = "Eevee Emporium"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'store',  # Custom app for the store
    'cart',   # Custom app for the shopping cart
    'payment',  # Custom app for payment processing
    'controlpanel',  # Custom app for the admin control panel
    'contact',  # Custom app for contact forms
    'django_extensions',
]

# Add compressor only if not in DEBUG mode to avoid development issues
if not DEBUG:
    INSTALLED_APPS.append('compressor')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eeveeEmporium.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Always True - loaders handle optimization
        'OPTIONS': {
            'context_processors': [
                # Custom context processor for categories
                'store.utils.context_processors.categories_processor',
                # Custom context processor for sets
                'store.utils.context_processors.sets_processor',
                # Cart Processor
                'cart.context_processors.cart',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Template optimization - only set loaders if not in DEBUG mode
if not DEBUG:
    TEMPLATES[0]['APP_DIRS'] = False  # Disable APP_DIRS when using loaders
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

WSGI_APPLICATION = 'eeveeEmporium.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}

if not DEBUG:
    DATABASES['default']['CONN_MAX_AGE'] = 60

if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }


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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

USE_AWS = os.environ.get("USE_AWS", "False").lower() in ("true", "1", "yes")

if USE_AWS:
    print("Using S3")

    # cache control
    AWS_S3_OBJECT_PARAMETERS = {
        "Expires": "Thu, 31 Dec 2099 20:00:00 GMT",
        "CacheControl": "max-age=94608000",
    }

    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "eu-west-1")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    STATICFILES_LOCATION = "static"
    MEDIAFILES_LOCATION = "media"

    # Static and media files
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "location": MEDIAFILES_LOCATION,
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        },
    }

    # Override static and media URLs in production
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"

CSRF_TRUSTED_ORIGINS = [
    'https://eeveeemporium-a0b363641244.herokuapp.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Stripe settings
STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY")
STRIPE_PRIVATE_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WH_SECRET = os.environ.get("STRIPE_WH_SECRET")

# Cache configuration
if DEBUG:
    # Use local memory cache for development
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
            'TIMEOUT': 300,
        }
    }
    # Don't use cache for sessions in development
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
else:
    # Use Redis for production if available, fallback to database
    redis_url = config('REDIS_URL', default=None)
    if redis_url:
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.redis.RedisCache',
                'LOCATION': redis_url,
                'TIMEOUT': 300,
                'OPTIONS': {
                    'CONNECTION_POOL_KWARGS': {'max_connections': 50},
                }
            }
        }
        # Use cache for sessions in production
        SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
        SESSION_CACHE_ALIAS = 'default'
    else:
        # Fallback to database cache
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'cache_table',
            }
        }
        SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Cache time settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300  # Cache pages for 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'eevee_emporium'

# Django Compressor settings (only if compressor is installed)
if 'compressor' in INSTALLED_APPS:
    COMPRESS_ENABLED = not DEBUG
    COMPRESS_OFFLINE = True
    COMPRESS_CSS_FILTERS = [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter',
    ]
    COMPRESS_JS_FILTERS = [
        'compressor.filters.jsmin.JSMinFilter',
    ]
    
    # Static files optimization
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
    ]
else:
    # Default static files finders
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

# Production optimizations
if not DEBUG:
    # Security settings (non-SSL)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'
    
    # Performance settings
    USE_ETAGS = True
    
    # SSL settings - only apply in actual production (Heroku/deployment)
    # Check if we're running on Heroku or other production environment
    IS_HEROKU = 'DYNO' in os.environ
    if IS_HEROKU or config('FORCE_SSL', default=False, cast=bool):
        SECURE_SSL_REDIRECT = True
        SECURE_HSTS_SECONDS = 31536000
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True

# File upload settings for better performance
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5MB

# Django Extensions settings (for development)
if DEBUG:
    # Add django-extensions settings for graph_models
    GRAPH_MODELS = {
        'all_applications': True,
        'group_models': True,
    }