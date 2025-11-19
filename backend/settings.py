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

from os import environ, getenv
from pathlib import Path
from datetime import date
import dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_ROOT = BASE_DIR / 'staticfiles'

dotenv.load_dotenv()

DEFAULT_COUNTRY = "Brasil"
DEFAULT_STATE = "SP"
DEFAULT_CITY = "São Caetano do Sul"
DEFAULT_BIRTHDATE = date(date.today().year - 15, 1, 1)

SCHOOL_NAME = "ETEC Jorge Street"
SCHOOL_CODE = 11
EMAIL_PATTERN = "{}.{}@etec.sp.gov.br"
SECURITY_KEY = getenv("MASTER_KEY")

STORAGE_BUCKET = getenv("STORAGE_URL")

# MAYBE: add these as a course attribute
LESSON_DURATION = 50 
TURNS = {"M": "7:00", "E": "13:00", "N": "19:00"}

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / "user_media"

SECRET_KEY = getenv("CSRF_KEY", "DEMZER-INSECURE-KEY")

WEEKDAYS = [
    "Segunda",
    "Terça",
    "Quarta",
    "Quinta",
    "Sexta",
    "Sábado",
    "Domingo",
]

MONTHS = [
    "janeiro",
    "fevereiro",
    "março",
    "abril",
    "março",
    "maio",
    "junho",
    "julho",
    "agosto",
    "setembro",
    "outubro",
    "novembro",
    "outubro",
]

DEBUG = True

SECURE_SSL_REDIRECT = False

ALLOWED_HOSTS = ['*']

STATICFILES_DIRS = [
    BASE_DIR / "static",
    # "/var/www/static/",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "rolepermissions",
    "core",
    "management",
    "grades",
    "communication",
    "captcha",
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        #"NAME": BASE_DIR / "db.sqlite3",
        "NAME": getenv("DB_NAME", "dev_demzer"),
        "USER": getenv("DB_USER", "root"),
        "PASSWORD": getenv("DB_PASSWORD", "root"),
        "HOST": getenv("DB_HOST", "localhost"),
        "PORT": "3306",
        "OPTIONS": {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
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

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "auth.User"

LOGIN_URL = "/login/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'socialdemzer@gmail.com'
EMAIL_HOST_PASSWORD = 'dozoitjwtkpjasfm'

ROLEPERMISSIONS_MODULE = "core.roles"
ROLEPERMISSIONS_SUPERUSER_SUPERPOWERS = False


# --- Configuração do AWS S3 ---
AWS_ACCESS_KEY_ID = 'AKIA6D6JBM4GQWGHCPSW'
AWS_SECRET_ACCESS_KEY = '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'

# 2. Configurações do Bucket
AWS_STORAGE_BUCKET_NAME = 'projeto-demzer-midia'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_FILE_OVERWRITE = False

AWS_S3_REGION_NAME = 'us-east-1'

AWS_S3_BASE_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

STORAGES = {
	"default": {
		"BACKEND": "storages.backends.s3boto3.S3StaticStorage",
	},

	"staticfiles": {
		"BACKEND": "storages.backends.s3boto3.S3StaticStorage",
	},
}

#Settings captcha

CAPTCHA_IMAGE_SIZE = (200,60)
CAPTCHA_FONT_SIZE = 48
CAPTCHA_LETTER_ROTATION = (-35, 35)
CAPTCHA_TIMEOUT = 5  # minutos
