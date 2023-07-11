"""
Django settings for api project.

Generated by "django-admin startproject" using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-m5m=f9*0u9sa_2@71_oxwxtne+5byr(g@d1wuky4oour^kf(f2"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = "RENDER" not in os.environ

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = []
ALLOWED_HOSTS = []
INTERNAL_IPS = [
    "127.0.0.1",
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

if DEBUG:
    ALLOWED_HOSTS += [
        "localhost",
        "127.0.0.1",
        "localhost:3000",
        "127.0.0.1:8000",
    ]

    CORS_ALLOWED_ORIGIN_REGEXES += [
        r"^http(s)?://localhost:3000$",
        r"^http(s)?://127.0.0.1:3000$",
    ]


# Application definition

INSTALLED_APPS = [
    "daphne",

    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "corsheaders",

    "oauth2_provider",
    "social_django",
    "drf_social_oauth2",

    "django_filters",
    "rest_framework",
    "graphene_django",
    "drf_spectacular",

    "channels",

    "authentication.apps.AuthenticationConfig",
    "common.apps.CommonConfig",
    "shop.apps.ShopConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

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

                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"
ASGI_APPLICATION = "api.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

GRAPHENE = {
    "SCHEMA": "api.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "drf_social_oauth2.authentication.SocialAuthentication",
    ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}


# User & Authentication

AUTH_USER_MODEL = "authentication.User"

AUTHENTICATION_BACKENDS = (
    # Google  OAuth2
    "social_core.backends.google.GoogleOAuth2",
    # drf-social-oauth2
    "drf_social_oauth2.backends.DjangoOAuth2",
    # graphql-jwt
    "graphql_jwt.backends.JSONWebTokenBackend",
    # Django
    "django.contrib.auth.backends.ModelBackend",
)


ACTIVATE_JWT = True

SOCIAL_AUTH_JSONFIELD_ENABLED = True

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "authentication.pipeline.get_avatar",
)

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("GOOGLE_OAUTH2_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("GOOGLE_OAUTH2_SECRET")

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://postgres:postgres@localhost:5432/postgres",
        conn_max_age=600,
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# UNFOLD SETTINGS
# =====================

UNFOLD = {
    "SITE_TITLE": "Shoplist",
    "SITE_HEADER": "Shoplist",
    "SITE_URL": "/",
    "LOGIN": {
        "image": lambda r: static("common/images/pexels-pixabay-316149.jpg"),
        "redirect_after": lambda r: reverse_lazy("admin:index"),
    },
    "STYLES": [],
    "SCRIPTS": [],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Shop"),
                        "icon": "shopping_bag",
                        "link": reverse_lazy("admin:shop_list_changelist"),
                    },
                    {
                        "title": _("Shop Choices"),
                        "icon": "shopping_bag",
                        "link": reverse_lazy("admin:shop_listcategory_changelist"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "group",
                        "link": reverse_lazy("admin:authentication_user_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "authentication.user",
                "auth.group",
                "social_django.usersocialauth",
            ],
            "items": [
                {
                    "title": _("All Users"),
                    "link": reverse_lazy("admin:authentication_user_changelist"),
                },
                {
                    "title": _("All Groups"),
                    "link": reverse_lazy("admin:auth_group_changelist"),
                },
                {
                    "title": _("All Social Accounts"),
                    "link": reverse_lazy(
                        "admin:social_django_usersocialauth_changelist"
                    ),
                },
            ],
        },
        {
            "models": [
                "shop.list",
                "shop.product",
                "shop.store",
                "shop.storeproduct",
                "shop.listproduct",
            ],
            "items": [
                {
                    "title": _("All Lists"),
                    "link": reverse_lazy("admin:shop_list_changelist"),
                },
                {
                    "title": _("All Products"),
                    "link": reverse_lazy("admin:shop_product_changelist"),
                },
                {
                    "title": _("All Stores"),
                    "link": reverse_lazy("admin:shop_store_changelist"),
                },
            ],
        },
        {
            "models": [
                "shop.listcategory",
                "shop.storecategory",
                "shop.productcategory",
                "shop.productunit",
            ],
            "items": [
                {
                    "title": _("List Categories"),
                    "link": reverse_lazy("admin:shop_listcategory_changelist"),
                },
                {
                    "title": _("Store Categories"),
                    "link": reverse_lazy("admin:shop_storecategory_changelist"),
                },
                {
                    "title": _("Product Categories"),
                    "link": reverse_lazy("admin:shop_productcategory_changelist"),
                },
                {
                    "title": _("Product Units"),
                    "link": reverse_lazy("admin:shop_productunit_changelist"),
                },
            ],
        },
    ],
}
