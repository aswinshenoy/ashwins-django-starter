import os
from environs import Env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Env()
env.read_env()

SECRET_KEY = env.str('SECRET_KEY', default='@v(sr0a1eocvp9x=pndj(ff*ll_d2yn7e&t19t!%$(bx47brrl')

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

# DJANGO_TRUSTED_ORGINS = env.list('DJANGO_TRUSTED_ORIGINS', ['http://localhost', 'http://192.168.43.88/'])

SHARD_EPOCH = 1314220021721

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'graphene_django',

    'chowkidar',
    'user'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'user.User'
ROOT_URLCONF = 'framework.urls'
ASGI_APPLICATION = 'framework.routing.application'

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
            ],
        },
    },
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': '5432',
    }
}

# Authentication

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'framework.utils.auth.AuthEmailBackend',
]

# GraphQL
GRAPHENE = {
    'SCHEMA': 'framework.graphql.schema.schema',
    'MIDDLEWARE': [
        'chowkidar.auth.ChowkidarAuthMiddleware',
        'graphene_django.debug.DjangoDebugMiddleware'
    ],
}



# Static files (CSS, JavaScript, Images)
AWS_ACCESS_KEY_ID = env.str('S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env.str('S3_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.ap-south-1.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = False

STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATICFILES_STORAGE = 'framework.utils.storage.StaticStorage'

STATICFILES_DIRS = (os.path.join('static'),)    # List of static file directories
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 25  # Maximum allowed upload size  for any file


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True
