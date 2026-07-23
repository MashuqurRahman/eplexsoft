import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^gytcz5br=e41gy*hg3i3o2f1$^4xxli_a_qyglp!mapa#xxyk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = [
#     'demo-ecommerce.odelltech.com',
#     'www.demo-ecommerce.odelltech.com',
#     '127.0.0.1',
#     'localhost',
# ]
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    
    'client_app',
    'admin_app',
    'accounts_app',
    'permission_app',
    'report_app',
]

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'client_app.context_processors.categories_context',
                'client_app.context_processors.site_settings',
                'admin_app.context_processors.theme_colors',
                'client_app.context_processors.theme_colors',
                'client_app.context_processors.auth_errors_processor',
            ],
        },
    },
]

# STEADFAST_API_KEY = config('STEADFAST_API_KEY')
# STEADFAST_SECRET_KEY = config('STEADFAST_SECRET_KEY')
# STEADFAST_BASE_URL = config('STEADFAST_BASE_URL', default='https://portal.steadfast.com.bd/api/v1')

WSGI_APPLICATION = 'ecommerce_project.wsgi.application'

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.mysql',

        'NAME': os.environ.get('DJANGO_DB_NAME', 'aliancebrothers_ecommerce_db'),
        'USER': os.environ.get('DJANGO_DB_USER', 'aliancebrothers_aliancebrothers'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', 'odelltech@54312'),
        'HOST': os.environ.get('DJANGO_DB_HOST','127.0.0.1'),

        'PORT': os.environ.get('PORT', '3306'),

        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",

        }


    }

}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'accounts_app.User'
"""
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# For real email:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'odelltechecommercebd@gmail.com'
EMAIL_HOST_PASSWORD = 'lveomivrpboyiijd'
DEFAULT_FROM_EMAIL = 'E-Commerce <noreply@mysite.com>'

"""


# For CPanel

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.odelltech.com'  # Usually 'mail.' followed by your domain
EMAIL_PORT = 465                    # cPanel usually prefers 465 for SSL
EMAIL_USE_SSL = True                # Change TLS to SSL for Port 465
EMAIL_USE_TLS = False
EMAIL_HOST_USER = 'eplex@odelltech.com'  # The email you created in cPanel
EMAIL_HOST_PASSWORD = 'r_GEt)AA{0qDw8a@'
DEFAULT_FROM_EMAIL = 'E-Commerce <info@yourdomain.com>'
    
 
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
