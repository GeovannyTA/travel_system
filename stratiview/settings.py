from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s^shu%g(_g72ld(q6c@rq#r8%@s%mn$fuarcqp#20+k2ql)kuu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'beautiful-einstein.51-79-98-210.plesk.page']


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
        'USER': 'sa',
        'PASSWORD': '=JeFGm[jFd%J?7j',
        'HOST': '51.79.98.210',  # o IP del servidor
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
LOGIN_REDIRECT_URL = '/stratiview/home'

DATA_UPLOAD_MAX_NUMBER_FILES = 1000  # Numero maximo de imagenes permitidos
DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024 * 1024  # Numero maximo de gigas 50GB

# Usar S3 como backend para archivos estáticos y medios
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Datos de tu bucket
AWS_ACCESS_KEY_ID = 'AKIA4MTWLQ33LZ6HZOWE'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'prueba-recorrido'
AWS_S3_REGION_NAME = 'us-west-2'  # Ejemplo: us-east-1, us-west-2, etc.

# Opcionales
AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

# Configuracion para el envio de correos
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "trejogeovannyaraujo@gmail.com"
EMAIL_HOST_PASSWORD = "czrz rfbw ohwb zazo"

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['console'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }