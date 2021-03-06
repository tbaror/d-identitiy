"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config
from qr_code.qrcode import constants

import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion

AUTH_LDAP_SERVER_URI = config('AUTH_LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = config('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = config('AUTH_LDAP_BIND_PASSWORD')

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch("OU=Migrated,OU=Users,OU=BeerSheba,OU=Israel,OU=Asia,DC=dalet,DC=local", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("CN=Users,DC=dalet,DC=local", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
)            

AUTH_LDAP_USER_ATTR_MAP = {
            "username": "sAMAccountName",
                "first_name": "givenName",
                    "last_name": "sn",
                        "email": "mail",
}
from django_auth_ldap.config import ActiveDirectoryGroupType
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
            "OU=SecurityAccess,OU=BeerSheba,OU=Israel,OU=Asia,DC=dalet,DC=local", ldap.SCOPE_SUBTREE, "(objectCategory=Group)"
            )
AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType(name_attr="cn")
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
            "is_superuser": "CN=VPN_BSH_ACCESS,OU=SecurityAccess,OU=BeerSheba,OU=Israel,OU=Asia,DC=dalet,DC=local",
            "is_staff": "CN=VPN_BSH_ACCESS,OU=SecurityAccess,OU=BeerSheba,OU=Israel,OU=Asia,DC=dalet,DC=local",
            }
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 1  # 1 hour cache

AUTHENTICATION_BACKENDS = [
            'django_auth_ldap.backend.LDAPBackend',
            'django.contrib.auth.backends.ModelBackend',
            
]



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['212.143.237.19','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django_user_agents',
    'widget_tweaks',
    'captcha',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts.apps.AccountsConfig',
    'qr_code',
]


# Cache backend is optional, but recommended to speed up user agent parsing
""" CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
} """

# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
USER_AGENTS_CACHE = 'default'

MIDDLEWARE_CLASSES = (
    # other middlewares...
    'django_user_agents.middleware.UserAgentMiddleware',
)

SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'login' # new

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
#EMAIL_HOST_USER = config('EMAIL_HOST_USER')
#EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_HOST_TLS = True
#EMAIL_USE_SSL = True

RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


QR_CODE_URL_PROTECTION = {
    constants.TOKEN_LENGTH: 30,                         # Optional random token length for URL protection. Defaults to 20.
    constants.SIGNING_KEY: 'my-secret-signing-key',     # Optional signing key for URL token. Uses SECRET_KEY if not defined.
    constants.SIGNING_SALT: 'my-signing-salt',          # Optional signing salt for URL token.
    constants.ALLOWS_EXTERNAL_REQUESTS_FOR_REGISTERED_USER: False  # Tells whether a registered user can request the QR code URLs from outside a site that uses this app. It can be a boolean value used for any user or a callable that takes a user as parameter. Defaults to False (nobody can access the URL without the signature token).
}