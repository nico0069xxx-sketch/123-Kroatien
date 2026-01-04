"""
VERBESSERTE Django settings.py
Mit Sicherheits-Best-Practices und Umgebungsvariablen

WICHTIG: Ersetzen Sie Ihre alte settings.py mit dieser Datei!
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Lesen aus Umgebungsvariable oder .env Datei
SECRET_KEY = os.environ.get('SECRET_KEY', '0(6e97v$fomarty^=ihz$7^qv3farukk9uc=1ayzz2hqww#t-jau%*n^5ui')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Nur spezifische Hosts erlauben (nicht '*')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages.apps.PagesConfig',
    'listings.apps.ListingsConfig',
    'realtors.apps.RealtorsConfig',
    'django.contrib.humanize',
    'accounts.apps.AccountsConfig',
    'contacts.apps.ContactsConfig',
    'crispy_forms',
    'bootstrap4',
    'ckeditor',
    'ckeditor_uploader',
    'django_cleanup.apps.CleanupConfig',
    'main',
]

CKEDITOR_UPLOAD_PATH = 'uploads/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'height': 'auto',
        'width': 'auto',
        'toolbar_Custom': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker', 'Undo'],
            ['Link', 'Unlink', 'Anchor', 'Italic', 'Underline', ],
            ['Image', 'Flash', 'Table', 'HorizontalRule'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'],
            ['Source'],
        ],
    },
    'special': {
        'toolbar': 'Custom',
        'width': 'auto',
        'height': 'auto',
        'toolbar_Special': [
            ['Bold', 'CodeSnippet', 'Youtube'],
        ],
        'extraPlugins': ','.join(['codesnippet', 'youtube']),
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise für Static Files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'realstate.urls'

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
                'main.context_processors.set_language',
                'main.context_processors.get_my_translations',
            ],
        },
    },
]

WSGI_APPLICATION = 'realstate.wsgi.application'

# Database
# Für Entwicklung: SQLite
# Für Produktion: PostgreSQL empfohlen
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Produktions-Datenbank (PostgreSQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'immobilien_kroatien'),
            'USER': os.environ.get('DB_USER', 'immobilien_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }

# Password validation
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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'ge'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Croatian English Polish Czech Russian Swedish Norway Slovak Dutch
LANGUAGES = [
    ('en', 'English'),
    ('ge', 'German'),
    ('fr', 'French'),
    ('gr', 'Greek'),
    ('hr', 'Croatian'),
    ('pl', 'Polish'),
    ('cz', 'Czech'),
    ('ru', 'Russian'),
    ('sw', 'Swedish'),
    ('no', 'Norway'),
    ('sk', 'Slovak'),
    ('nl', 'Dutch'),
]

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Whitenoise für bessere Static File Performance
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Folder Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Message Alerts
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

CRISPY_TEMPLATE_PACK = 'uni_form'

# Email Configuration - Aus Umgebungsvariablen
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'service.mahamudh472@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'pmjv woji jdsx kvns')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# SICHERHEITS-EINSTELLUNGEN (PRODUKTION)
# ============================================

if not DEBUG:
    # HTTPS erzwingen
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
    
    # Session & CSRF Cookies nur über HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 Jahr
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Content Security Policy Headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Referrer Policy
    SECURE_REFERRER_POLICY = 'same-origin'
    
    # Proxy-Header für HTTPS (bei Nutzung von Reverse Proxy)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ============================================
# ENTWICKLUNGS-EINSTELLUNGEN (DEBUG=True)
# ============================================

if DEBUG:
    # In Entwicklung: Weniger strenge Einstellungen
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    
    # Email in Konsole ausgeben (für Tests)
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ============================================
# LOGGING (FEHLER-PROTOKOLLIERUNG)
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_errors.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Logs-Ordner erstellen falls nicht vorhanden
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
