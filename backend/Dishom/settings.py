"""
Django settings for Dishom project.
Production Ready Version
"""

from pathlib import Path
import os
from datetime import timedelta

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
# ============================================================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me-in-prod")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    'safalclasses.com',
    'www.safalclasses.com',
    '13.204.95.234',
]


# CORS
# ============================================================
CORS_ALLOWED_ORIGINS = [
    'https://safalclasses.com',
    'https://www.safalclasses.com',
]


# APPS
# ============================================================
INSTALLED_APPS = [
    'jazzmin',
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'django_browser_reload',

    'accounts',
    'batch',
    'study',
    'live_class',
]

AUTH_USER_MODEL = 'accounts.CustomUser'


# REST FRAMEWORK
# ============================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}


# MIDDLEWARE
# ============================================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'Dishom.urls'


# TEMPLATES / REACT BUILD SUPPORT
# ============================================================
REACT_APP_DIR = BASE_DIR / "frontend" / "dist"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [REACT_APP_DIR],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Dishom.wsgi.application'


# DATABASE
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# INTERNATIONALIZATION
# ============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# STATIC FILES (PRODUCTION)
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',      # Django static files
    REACT_APP_DIR,            # frontend/dist
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# MEDIA FILES
# ============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# JAZZMIN
# ============================================================
JAZZMIN_SETTINGS = {
    "site_title": "Dishom Classes",
    "site_header": "Dishom Classes",
    "site_brand": "Dishom Admin",
    "welcome_sign": "Welcome to the Dishom Admin Panel",
    "search_model": "accounts.CustomUser",
    "use_google_fonts_cdn": True,

    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "batch.Batch": "fas fa-layer-group",
        "batch.Subject": "fas fa-book",
        "study.Study": "fas fa-book-reader",
        "accounts.CustomUser": "fas fa-user",
        "live_class.YTClass": "fab fa-youtube",
        "live_class.LiveClass": "fas fa-video",
    },

    "changeform_format": "horizontal_tabs",

    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "icon": "tachometer-alt"},
    ],

    "hide_models": ["batch.Chapter", "batch.CourseCategory"],

    "order_with_respect_to": [
        "study",
        "live_class",
        "batch",
        "accounts",
        "auth",
    ],
}


# EMAIL
# ============================================================
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'no-reply@example.com'

FRONTEND_BASE_URL = 'http://localhost:5173'
