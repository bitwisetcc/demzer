"""
More info: 
https://docs.djangoproject.com/en/4.2/topics/settings

Documentation:
https://docs.djangoproject.com/en/4.2/ref/settings

Pre-deployment:
https://docs.djangoproject.com/en/4.2/howto/deployment/checklist

Static files:
https://docs.djangoproject.com/en/4.2/howto/static-files

Database
https://docs.djangoproject.com/en/4.2/ref/settings/#databases

Password validation
https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

Internationalization
https://docs.djangoproject.com/en/4.1/topics/i18n
"""

from os import environ
from pathlib import Path
from datetime import date

DEFAULT_COUNTRY = "Brasil"
DEFAULT_STATE = "SP"
DEFAULT_CITY = "São Caetano do Sul"
DEFAULT_BIRTHDATE = date(date.today().year - 15, 1, 1)

SCHOOL_NAME = "ETEC Jorge Street"
EMAIL_PATTERN = "{}.{}@etec.sp.gov.br"


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-j*9=2)w4ojo9evy9yje0kc)3aysl^e!p1m9w)j6)sr2akot4j="

DEBUG = True

SECURE_SSL_REDIRECT = False

ALLOWED_HOSTS = []

STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

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
                "core.urls.school_info",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

DB_ENGINE = environ.get("DB_ENGINE", "sqlite3")


if DB_ENGINE == "sqlite3":
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.{}".format(DB_ENGINE),
            "NAME": environ.get("DB_NAME", "tcc"),
            "USER": environ.get("DB_USER", "root"),
            "PASSWORD": environ.get("DB_PASSWORD", "root"),
            "HOST": environ.get("DB_PASSWORD", "localhost"),
        }
    }


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

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "auth.User"

LOGIN_URL = "/login/"
