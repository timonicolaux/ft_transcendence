import os
from datetime import timedelta
from pathlib import Path

from decouple import config
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "10.13.12.1",
    "10.13.12.2",
    "10.13.12.3",
    "10.13.12.4",
    "10.12.11.7",
    "10.12.11.6",
    "10.13.11.3",
    "10.13.3.4",
    "10.13.3.2",
    "10.19.239.218",
    "192.168.1.30",
    "192.168.1.166",
    "192.168.1.80",
    "192.168.0.32",
    "10.19.234.197",
    "10.13.11.1",
]

INSTALLED_APPS = [
    "daphne",
    "channels",
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api",
    "game",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "sslserver",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "django_bleach",
]


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": ("api.authentication.CookieJWTAuthentication",),
}

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "api.middleware.UpdateLastSeenMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database pour le deploiement en utilisant docker
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT", default=5432, cast=int),
    }
}

# Database pour le developpement (sans passer par docker)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    # 'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    # 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    # 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Authentification standard Django
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "api.User"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/app/media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_CREDENTIALS = True  # Autoriser l'envoi des cookies avec CORS

CORS_ALLOWED_ORIGINS = [
    "http://frontend:3000",
    "http://backend:8000",
    "http://localhost:3000",
    "https://frontend:3000",
    "https://localhost:3000",
    "https://10.13.12.2:3000",
    "https://10.13.12.1:3000",
    "http://10.13.12.4:3000",
    "http://0.0.0.0:3000",
    "https://0.0.0.0:3000",
    "https://0.0.0.0:8000",
    "http://0.0.0.0:8000",
    "https://10.13.12.1:8443",
    "https://10.13.12.2:8443",
    "https://10.13.12.4:8443",
    "https://10.13.3.4:8443",
    "https://10.13.3.2:8443",
    "https://10.12.11.7:8443",
    "https://10.12.11.6:8443",
    "https://10.13.11.3:8443",
    "https://10.19.239.218:3000",
    "http://10.19.239.218:3000",
    "https://10.19.239.218:8443",
    "http://10.19.239.218:8443",
    "https://192.168.1.30:8443",
    "https://192.168.1.166:8443",
    "http://192.168.1.30:8443",
    "https://192.168.1.30:3000",
    "https://10.13.11.1:8443",
    "https://192.168.1.80:8443",
    "https://192.168.0.32:8443",
    "https://10.19.234.197:8443",
    "http://192.168.1.30:3000",
    "https://10.12.11.5:8443",
    "https://10.12.11.6:8443",
]

CSRF_TRUSTED_ORIGINS = [
    "http://frontend:3000",
    "http://localhost:3000",
    "https://localhost:3000",
    "https://frontend:3000",
    "http://0.0.0.0:3000",
    "http://0.0.0.0:8000",
    "https://10.13.12.1:3000",
    "http://10.13.12.4:3000",
    "https://10.13.12.1:8443",
    "https://10.13.12.2:8443",
    "https://10.13.12.4:8443",
    "https://10.12.11.7:8443",
    "https://10.12.11.6:8443",
    "https://10.13.3.4:8443",
    "https://10.13.3.2:8443",
    "https://10.13.11.1:8443",
    "https://10.13.11.3:8443",
    "https://10.19.239.218:3000",
    "https://10.19.239.218:8443",
    "http://10.19.239.218:3000",
    "http://10.19.239.218:8443",
    "https://192.168.1.30:8443",
    "http://192.168.1.30:8443",
    "https://192.168.1.30:3000",
    "http://192.168.1.30:3000",
    "https://192.168.1.80:8443",
    "https://192.168.0.32:8443",
    "https://10.19.234.197:8443",
    "https://192.168.1.166:8443",
]


ASGI_APPLICATION = "project.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": "ext://sys.stdout",  # Explicitly use stdout
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        # Add this for your consumers
        "project.game.consumers": {  # Replace with your actual consumer module path
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

OTP_TOTP_ISSUER = "YourAppName"
OTP_TOTP_DIGITS = 6  # Code à 6 chiffres
OTP_TOTP_INTERVAL = 30  # Code expire en 30 secondes

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"
