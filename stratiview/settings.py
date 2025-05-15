from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env') # Cargar variables de entorno desde el archivo .env


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DJANGO_DEBUG')

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'beautiful-einstein.51-79-98-210.plesk.page',
    'nice-satoshi'
]


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://beautiful-einstein.51-79-98-210.plesk.page",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fontawesomefree',
    'stratiview',
    'storages',
    'wfastcgi',
    'stratiview.templatetags',
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
    'stratiview.middleware.force_password_change.ForcePasswordChangeMiddleware',
    'stratiview.middleware.force_redirect_home.ForceRedirectHomeMiddleware',
    'stratiview.middleware.auto_logout.AutoLogoutMiddleware',
]

ROOT_URLCONF = 'stratiview.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'stratiview.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'recorrido',
        'USER': os.getenv('DB_USER'),  # Nombre de usuario de la base de datos
        'PASSWORD': os.getenv('DB_PASSWORD'),  # Contraseña de la base de datos
        'HOST': os.getenv('DB_HOST'),  # o IP del servidor
        'PORT': '',  # normalmente vacío para el puerto por defecto
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

# Base de datos para pruebas locales
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': 'recorrido',
#         'USER': 'geovanny',
#         'PASSWORD': '2832455882',
#         'HOST': 'Dell\MSSQLSERVER01',  # o IP del servidor
#         'PORT': '', # Vacio para utilizar el puerto por defecto
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
# Requerida para producción

STATICFILES_DIRS = [
    BASE_DIR / 'stratiview' / 'static', 
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Use Whitenoise for static file serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'stratiview.User' 
LOGIN_URL = '/stratiview/auth/sign_in'
LOGOUT_REDIRECT_URL = '/stratiview/auth/sign_in'
LOGIN_REDIRECT_URL = '/stratiview/routes'

DATA_UPLOAD_MAX_NUMBER_FILES = 500  # Numero maximo de imagenes permitidos
DATA_UPLOAD_MAX_MEMORY_SIZE = 4 * 1024 * 1024 * 1024  # Numero maximo de gigas 5GB

# Usar S3 como backend para archivos estáticos y medios
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Datos de tu bucket
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')

# Opcionales
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

# Configuracion para el envio de correos
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = "czrz rfbw ohwb zazo"


X_FRAME_OPTIONS = 'ALLOW-FROM https://nice-satoshi.15-235-118-158.plesk.page'