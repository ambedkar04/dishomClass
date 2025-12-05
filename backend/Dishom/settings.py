"""
Django settings for Dishom project.
Production Ready Version with Security Best Practices
"""

from pathlib import Path
import os
from datetime import timedelta
from typing import Any, Dict, List
from typing import TYPE_CHECKING, Any

import importlib
try:
    load_dotenv = importlib.import_module('dotenv').load_dotenv  # type: ignore[attr-defined]
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
# ============================================================
SECRET_KEY = os.getenv("SECRET_KEY") or (
    "django-insecure-dev-key-only" if os.getenv("DEBUG", "False") == "True" else None
)
if SECRET_KEY is None:
    raise ValueError("SECRET_KEY environment variable must be set in production")

DEBUG = os.getenv("DEBUG", "False") == "True"

# Parse ALLOWED_HOSTS from environment variable (comma-separated)
allowed_hosts_str = os.getenv(
    "ALLOWED_HOSTS",
    "safalclasses.com,www.safalclasses.com,127.0.0.1,localhost,13.200.248.251"
)
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(",")]


# CORS
# ============================================================
cors_origins = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,https://safalclasses.com,https://www.safalclasses.com"
)
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(",")]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = [
    'http://safalclasses.com',
    'https://safalclasses.com',
    'http://www.safalclasses.com',
    'https://www.safalclasses.com',
]


# APPS
# ============================================================
INSTALLED_APPS = [
    'unfold',
    'crispy_forms',
    'crispy_bootstrap5',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',

    'theme',
    'tailwind',
    'django_browser_reload',

    'accounts',
    'batch',

    'live_class',
    'dashboard',
]

AUTH_USER_MODEL = 'accounts.CustomUser'
AUTH_GROUP_MODEL = 'accounts.CustomGroup'


# REST FRAMEWORK
# ============================================================
REST_FRAMEWORK: Dict[str, Any] = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ) if not DEBUG else (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

SIMPLE_JWT: Dict[str, Any] = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
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
]

if DEBUG:
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

ROOT_URLCONF = 'Dishom.urls'


# TEMPLATES / REACT BUILD SUPPORT
# ============================================================
REACT_APP_DIR = BASE_DIR / "frontend" / "dist"

TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            REACT_APP_DIR,
            BASE_DIR / 'templates',
        ],  
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


# settings.py

# Postgres Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}



# Cache Configuration
_caches_cfg: Dict[str, Dict[str, Any]]
if os.getenv('REDIS_URL'):
    _caches_cfg = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'dishom',
            'TIMEOUT': 300,
        }
    }
else:
    _caches_cfg = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
CACHES: Dict[str, Dict[str, Any]] = _caches_cfg

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'


# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS: List[Dict[str, Any]] = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# INTERNATIONALIZATION
# ============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # Indian Standard Time
USE_I18N = True
USE_TZ = True


# STATIC FILES (PRODUCTION)
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',      # Django static files
]

# Only add React build directory if it exists
if REACT_APP_DIR.exists():
    STATICFILES_DIRS.append(REACT_APP_DIR)

STATICFILES_STORAGE = (
    'django.contrib.staticfiles.storage.StaticFilesStorage'
    if DEBUG
    else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

# WhiteNoise Configuration
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_MANIFEST_STRICT = False


# MEDIA FILES
# ============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SECURITY SETTINGS (PRODUCTION)
# ============================================================
if not DEBUG:
    # HTTPS/SSL
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Security Headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Additional Security Headers
    SECURE_REFERRER_POLICY = 'same-origin'
    
    # Proxy Headers (for Nginx)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True





# EMAIL CONFIGURATION
# ============================================================
EMAIL_BACKEND = (
    'django.core.mail.backends.console.EmailBackend'
    if DEBUG
    else 'django.core.mail.backends.smtp.EmailBackend'
)
if not DEBUG:
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False') == 'True'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    EMAIL_TIMEOUT = 30

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@safalclasses.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Frontend URL
FRONTEND_BASE_URL = os.getenv('FRONTEND_BASE_URL', 'https://safalclasses.com')


# LOGGING
# ============================================================
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django_errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django_info.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file_error', 'file_info'] if not DEBUG else ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_error'] if not DEBUG else ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file_error', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_error'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# ADDITIONAL SETTINGS
# ============================================================

# Admin Site Configuration
ADMIN_SITE_HEADER = "Safal Classes Administration"
ADMIN_SITE_TITLE = "Safal Classes Admin Portal"
ADMIN_INDEX_TITLE = "Welcome to Safal Classes Admin Portal"


def site_logo(request: Any) -> str:
    static = importlib.import_module('django.templatetags.static').static  # type: ignore[attr-defined]
    return static("images/logo.png")

# Django Unfold Theme Configuration
UNFOLD: Dict[str, Any] = {
    "SITE_TITLE": "Safal Classes Admin Portal",
    "SITE_HEADER": "Safal Classes",
    "SITE_URL": "https://www.safalclasses.com",
    "SITE_NAME": "safalclasses.com",
    "SITE_LOGO": site_logo,
    
    # Sidebar Configuration
    "SIDEBAR": {
        "show_search": False,  
        "command_search": False,  
        "show_all_applications": False,  
        "navigation": [
            {
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": "/admin/"
                    },
                ]
            },
            {
                "title": "Live Classes",
                "separator": True,
                "items": [
                    {
                        "title": "YT Classes",
                        "icon": "video_library",
                        "link": "/admin/live_class/ytclass/"
                    },
                    {
                        "title": "Live Classes",
                        "icon": "video_call",
                        "link": "/admin/live_class/liveclass/"
                    }
                ]
            },
            {
                "title": "Batch",
                "separator": True, 
                "items": [
                    {
                        "title": "Batches",
                        "icon": "school",
                        "link": "/admin/batch/batch/"
                    },
                    {
                        "title": "Subjects",
                        "icon": "menu_book",
                        "link": "/admin/batch/subject/"
                    }
                ]
            },
            {
                "title": "Authentication",  
                "separator": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "people",
                        "link": "/admin/accounts/customuser/"
                    },
                    {
                        "title": "Groups",
                        "icon": "groups",
                        "link": "/admin/accounts/customgroup/"
                    },
                    {
                        "title": "Audit Logs",
                        "icon": "history",
                        "link": "/admin/dashboard/auditlog/"
                    },
                    {
                        "title": "Incidents",
                        "icon": "report",
                        "link": "/admin/dashboard/incident/"
                    },
                    {
                        "title": "Alert Rules",
                        "icon": "notifications_active",
                        "link": "/admin/dashboard/alertrule/"
                    },
                ],
            }
        ]
    },
    # Theme and Styling
    "THEME": "dark",  # Options: "light", "dark", "auto"
    "THEME_COLORS": {
        "primary": "#2563eb",
        "secondary": "#64748b", 
        "success": "#16a34a",
        "warning": "#f59e0b",
        "error": "#dc2626",
        "info": "#0ea5e9",
    },
    
    # Display Settings
    "LIST_PER_PAGE": 20,
    "LIST_SHOW_FULL_DATE_POPUP": True,
    "SHOW_FIELDSETS_IN_TABBED_FORM": True,
    "SHOW_VIEW_NEXT_CHANGE_LINK": True,
    "SHOW_HISTORY_LINK": True,
}

# Date and Time Formats
DATE_FORMAT = 'd M Y'
DATETIME_FORMAT = 'd M Y, h:i A'
SHORT_DATE_FORMAT = 'd/m/Y'

ADMIN_RELATED_WIDGETS = False

# Error Pages (create these templates)
# CSRF_FAILURE_VIEW = 'your_app.views.csrf_failure'
# HANDLER404 = 'your_app.views.handler404'
# HANDLER500 = 'your_app.views.handler500'
# Trigger reload

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Tailwind CSS Configuration
TAILWIND_APP_NAME = 'theme'

# NPM Binary Path (optional, but recommended for production)
# If you have npm installed globally, you can leave this commented
# NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"  # Windows
# NPM_BIN_PATH = "/usr/local/bin/npm"  # Linux/Mac

# Internal IPs for django-browser-reload
INTERNAL_IPS = [
    "127.0.0.1",
]
