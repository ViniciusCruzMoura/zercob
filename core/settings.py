from pathlib import Path
import os
from decouple import config
from import_export.formats.base_formats import XLSX, CSV

CONFIG_ENVIRONMENT = config("CONFIG_ENVIRONMENT", default="PROD").upper()
CONFIG_DEBUG = config("CONFIG_DEBUG", default="True")
CONFIG_ALLOWED_HOSTS = config("CONFIG_ALLOWED_HOSTS", default="*")
CONFIG_CSRF_TRUSTED_ORIGINS = config('CONFIG_CSRF_TRUSTED_ORIGINS', default='http://127.0.0.1:8000')

CONFIG_DATABASE_ENGINE = config("CONFIG_DATABASE_ENGINE", "sqlite")
CONFIG_DATABASE_HOSTNAME = config("CONFIG_DATABASE_HOSTNAME", None)
CONFIG_DATABASE_PORT = config("CONFIG_DATABASE_PORT", None)
CONFIG_DATABASE_NAME = config("CONFIG_DATABASE_NAME", None)
CONFIG_DATABASE_USER = config("CONFIG_DATABASE_USER", None)
CONFIG_DATABASE_PASSWD = config("CONFIG_DATABASE_PASSWD", None)

CONFIG_REDIS_URL = config("CONFIG_REDIS_URL", "")

CONFIG_DROPBOX_APP_KEY = config("CONFIG_DROPBOX_APP_KEY", None)
CONFIG_DROPBOX_APP_SECRET = config("CONFIG_DROPBOX_APP_SECRET", None)
CONFIG_DROPBOX_REFRESH_TOKEN = config("CONFIG_DROPBOX_REFRESH_TOKEN", None)
CONFIG_DROPBOX_INTEGRATION_ENABLED = config("CONFIG_DROPBOX_INTEGRATION_ENABLED", "True") == 'True'

BASE_DIR = Path(__file__).resolve().parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'django-insecure-o&cp!1mjza263%zb)nk2q()cwnj7tw&9=bvyp)mkg34z@lvaf('
DEBUG = CONFIG_DEBUG == 'True'
IS_PRODUCTION = "PROD" in CONFIG_ENVIRONMENT
ASSETS_ROOT = "/static/assets"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", CONFIG_ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]
if CONFIG_CSRF_TRUSTED_ORIGINS:
    for domain in CONFIG_CSRF_TRUSTED_ORIGINS.split(","):
        if not domain.startswith(("http://", "https://")):
            print(f"Warning: Invalid domain format - {domain}. Skipping.")
            continue
        CSRF_TRUSTED_ORIGINS.append(domain)
CORS_ALLOW_ALL_ORIGINS = True
X_FRAME_OPTIONS = "SAMEORIGIN"
INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "unfold.contrib.location_field",  # optional, if django-location-field package is used
    "unfold.contrib.constance",  # optional, if django-constance package is used
    "unfold.contrib.hijack",  # optional, if django-hijack package is used
    'django.contrib.humanize',  # Required for django-daisy
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#     'rest_framework',
#     'post_office',
    'import_export',
    #"import_export_extensions",
    'celery',
    'django_celery_beat',
    'django_celery_results',
    'auditlog',
    'apps.user_admin',
    'apps.cobranca',
]
AUDITLOG_INCLUDE_ALL_MODELS = True
AUDITLOG_EXCLUDE_TRACKING_MODELS = (
    "django_celery_beat",
    "django_celery_results",
    "post_office",
    "auth",
#     "apps_processuais.BaseProdutivaNotificacao",
)
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = "import"
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = "export"
IMPORT_EXPORT_FORMATS = [XLSX]#, CSV]
IMPORT_EXPORT_SKIP_ADMIN_LOG = False
IMPORT_EXPORT_ESCAPE_FORMULAE_ON_EXPORT = True
IMPORT_EXPORT_SKIP_ADMIN_EXPORT_UI = True
# DATA_UPLOAD_MAX_NUMBER_FILES = 100 # Default is 100
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "auditlog.middleware.AuditlogMiddleware",
]
ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "admin:index"
LOGOUT_REDIRECT_URL = "admin:login"
TEMPLATE_DIR = os.path.join(CORE_DIR, "templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [TEMPLATE_DIR],
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
WSGI_APPLICATION = 'core.wsgi.application'
DATABASES = {}
if CONFIG_DATABASE_USER and CONFIG_DATABASE_PASSWD:
    if CONFIG_DATABASE_ENGINE.upper() == "ORACLE":
        DATABASES.update({
            "default": {
                'ENGINE': 'django.db.backends.oracle',
                'OPTIONS': {
                    'pool': {"min": 1, "max": 400, "increment": 1, "cclass": "cc1"}
                    },
                'NAME': f'{CONFIG_DATABASE_HOSTNAME}:{CONFIG_DATABASE_PORT}/{CONFIG_DATABASE_NAME}',
                'USER': f'{CONFIG_DATABASE_USER}',
                'PASSWORD': f'{CONFIG_DATABASE_PASSWD}',
                },
            })
    elif CONFIG_DATABASE_ENGINE.upper() == "POSTGRES":
        DATABASES.update(
            {
                "default": {
                    "OPTIONS": {"options": "-c search_path=public"},
                    "ENGINE": "django.db.backends.postgresql_psycopg2",
                    "NAME": f"{CONFIG_DATABASE_NAME}",
                    "USER": f"{CONFIG_DATABASE_USER}",
                    "PASSWORD": f"{CONFIG_DATABASE_PASSWD}",
                    "HOST": f"{CONFIG_DATABASE_HOSTNAME}",
                    "PORT": f"{CONFIG_DATABASE_PORT}",
                },
            }
        )
else:
    if CONFIG_DATABASE_ENGINE.upper() == "SQLITE":
        DATABASES.update(
            {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": BASE_DIR / "db.sqlite3",
                }
            }
        )
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
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Campo_Grande"
USE_I18N = True
USE_L10N = True
USE_TZ = False
NAMESPACE = 'zercob' if IS_PRODUCTION else 'zercob/hml'
STATIC_URL = NAMESPACE+'/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_URL = NAMESPACE+'/media/'
MEDIA_ROOT = os.path.join(CORE_DIR, "media")
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 'SITE_LOGO': '/static/admin/img/sebrae-blue.svg',  

CELERY_TASK_TIME_LIMIT = 10
CELERY_TASK_SOFT_TIME_LIMIT = 10
CELERY_TIMEZONE = "America/Campo_Grande"
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
if CONFIG_REDIS_URL:
    CELERY_BROKER_URL = f'redis://{CONFIG_REDIS_URL}:6379/0'
else:
    CELERY_BROKER_URL = 'redis://localhost:6379/1'





from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "Zerou Cobrança",
    "SITE_HEADER": "Appears in sidebar at the top",
    "SITE_SUBHEADER": "Appears under SITE_HEADER",
    "SITE_VERSION": "26.08.01",
#     "SITE_DROPDOWN": [
#         {
#             "icon": "diamond",
#             "title": _("My site"),
#             "link": "https://example.com",
#         },
#     ],
    "SITE_URL": "/",
#     "SITE_VIEWS": [
#         ("some-path-to-view", "name_of_view_1", "path.to.view_itself_1"),
#         ("other-path-to-view", "another_name_of_view_2", "path.to.view_itself_2"),
#     ],
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    "SITE_ICON": {
        "light": lambda request: static("icon-light.svg"),  # light mode
        "dark": lambda request: static("icon-dark.svg"),  # dark mode
    },
    #"SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    "SITE_LOGO": lambda request: static("logo.png"),
#     "SITE_LOGO": {
#         "light": lambda request: static("logo-light.svg"),  # light mode
#         "dark": lambda request: static("logo-dark.svg"),  # dark mode
#     },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.png"),
            #"href": lambda request: static("favicon.svg"),
        },
    ],
    "SHOW_HISTORY": True, # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True, # show/hide "View on site" button, default: True
    "SHOW_BACK_BUTTON": False, # show/hide "Back" button on changeform in header, default: False
    "SHOW_UI_WARNINGS": False, # show/hide warnings in UI, default: False
#     "ENVIRONMENT": "sample_app.environment_callback", # environment name in header
#     "ENVIRONMENT_TITLE_PREFIX": "sample_app.environment_title_prefix_callback", # environment name prefix in title tag
#     "DASHBOARD_CALLBACK": "sample_app.dashboard_callback",
    "THEME": "light", # Force theme: "dark" or "light". Will disable theme switcher
#     "LOGIN": {
#         "image": lambda request: static("login.png"),
# #         "redirect_after": lambda request: reverse_lazy("admin:APP_MODEL_changelist"),
#         # Inherits from `unfold.forms.AuthenticationForm`
# #         "form": "app.forms.CustomLoginForm",
#     },
#     "STYLES": [
#         lambda request: static("css/style.css"),
#     ],
#     "SCRIPTS": [
#         lambda request: static("js/script.js"),
#     ],
#     "BORDER_RADIUS": "6px",
    "BORDER_RADIUS": "8px",
#     "COLORS": {
#         "base": {
#             "50": "oklch(98.5% .002 247.839)",
#             "100": "oklch(96.7% .003 264.542)",
#             "200": "oklch(92.8% .006 264.531)",
#             "300": "oklch(87.2% .01 258.338)",
#             "400": "oklch(70.7% .022 261.325)",
#             "500": "oklch(55.1% .027 264.364)",
#             "600": "oklch(44.6% .03 256.802)",
#             "700": "oklch(37.3% .034 259.733)",
#             "800": "oklch(27.8% .033 256.848)",
#             "900": "oklch(21% .034 264.665)",
#             "950": "oklch(13% .028 261.692)",
#         },
#         "primary": {
#             "50": "oklch(97.7% .014 308.299)",
#             "100": "oklch(94.6% .033 307.174)",
#             "200": "oklch(90.2% .063 306.703)",
#             "300": "oklch(82.7% .119 306.383)",
#             "400": "oklch(71.4% .203 305.504)",
#             "500": "oklch(62.7% .265 303.9)",
#             #"600": "#35A77A",
#             "600": "oklch(55.8% .288 302.321)",
#             "700": "oklch(49.6% .265 301.924)",
#             "800": "oklch(43.8% .218 303.724)",
#             "900": "oklch(38.1% .176 304.987)",
#             "950": "oklch(29.1% .149 302.717)",
#         },
#         "font": {
#             "subtle-light": "var(--color-base-500)",  # text-base-500
#             "subtle-dark": "var(--color-base-400)",  # text-base-400
#             "default-light": "var(--color-base-600)",  # text-base-600
#             "default-dark": "var(--color-base-300)",  # text-base-300
#             "important-light": "var(--color-base-900)",  # text-base-900
#             "important-dark": "var(--color-base-100)",  # text-base-100
#         },
#     },
    "COLORS": {
        # Neutral / structural palette
        # Based on:
        # #F5F7F6 - Off-white
        # #263238 - Grafite
        "base": {
            "50": "oklch(97.4% 0.002 165.076)",   # #F5F7F6 - Off-white
            "100": "oklch(94.5% 0.006 170.442)",
            "200": "oklch(89.4% 0.010 171.771)",
            "300": "oklch(81.0% 0.014 174.064)",
            "400": "oklch(66.9% 0.023 174.617)",
            "500": "oklch(53.8% 0.024 174.277)",
            "600": "oklch(45.4% 0.024 176.476)",
            "700": "oklch(38.2% 0.023 170.222)",
            "800": "oklch(30.9% 0.019 229.784)",  # #263238 - Grafite
            "900": "oklch(26.9% 0.018 227.452)",
            "950": "oklch(19.9% 0.012 225.894)",
        },

        # Main ZEROU interface palette
        #
        # 600 = #247BA0 Azul Solução
        # 900 = #123B5D Azul Profundo
        #
        # This makes navigation/buttons/interface elements use
        # Azul Solução while stronger/darker states use Azul Profundo.
        "primary": {
            "50": "oklch(97.5% 0.007 219.559)",
            "100": "oklch(94.6% 0.016 221.080)",
            "200": "oklch(89.5% 0.033 221.305)",
            "300": "oklch(80.7% 0.061 219.293)",
            "400": "oklch(69.4% 0.088 222.384)",
            "500": "oklch(60.5% 0.101 227.891)",
            "600": "oklch(54.9% 0.098 231.147)",  # #247BA0
            "700": "oklch(47.2% 0.085 232.775)",
            "800": "oklch(40.4% 0.076 238.017)",
            "900": "oklch(34.2% 0.075 247.409)",  # #123B5D
            "950": "oklch(24.9% 0.050 247.036)",
        },

        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",

            # Grafite-oriented body text
            "default-light": "var(--color-base-800)",
            "default-dark": "var(--color-base-200)",

            "important-light": "var(--color-base-950)",
            "important-dark": "var(--color-base-50)",
        },
    },
    "SIDEBAR": {
#         "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Visão Geral"),
                "separator": False,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },

            {
                "title": _("Cobrança"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Devedores"),
                        "icon": "person",
                        "link": reverse_lazy("admin:apps_cobranca_devedores_changelist"),
                    },
                    {
                        "title": _("Propostas"),
                        "icon": "request_quote",
                        "link": reverse_lazy("admin:apps_cobranca_propostas_changelist"),
                    },
                    {
                        "title": _("Contratos"),
                        "icon": "contract",
                        "link": reverse_lazy("admin:apps_cobranca_contratos_changelist"),
                    },
                    {
                        "title": _("Acordos"),
                        "icon": "handshake",
                        "link": reverse_lazy("admin:apps_cobranca_acordos_changelist"),
                    },
                ],
            },

            {
                "title": _("Carteiras"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Carteiras"),
                        "icon": "account_balance_wallet",
                        "link": reverse_lazy("admin:apps_cobranca_carteiras_changelist"),
                    },
#                     {
#                         "title": _("Regras de Negociação"),
#                         "icon": "percent",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_carteirasregrasnegociacao_changelist"
#                         ),
#                     },
                ],
            },

            {
                "title": _("Organizações"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Organizações"),
                        "icon": "business",
                        "link": reverse_lazy("admin:apps_cobranca_organizacao_changelist"),
                    },
#                     {
#                         "title": _("Regras de Cobrança"),
#                         "icon": "rule",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_organizacaoregrascobranca_changelist"
#                         ),
#                     },
#                     {
#                         "title": _("Usuários da Organização"),
#                         "icon": "manage_accounts",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_usuarioorganizacao_changelist"
#                         ),
#                     },
                ],
            },

            {
                "title": _("Dados Auxiliares"),
                "separator": True,
                "collapsible": True,
                "items": [
#                     {
#                         "title": _("Contatos dos Devedores"),
#                         "icon": "contact_phone",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_devedorescontatos_changelist"
#                         ),
#                     },
#                     {
#                         "title": _("Endereços dos Devedores"),
#                         "icon": "location_on",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_devedoresenderecos_changelist"
#                         ),
#                     },
#                     {
#                         "title": _("Parcelas dos Contratos"),
#                         "icon": "receipt_long",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_contratosparcelas_changelist"
#                         ),
#                     },
#                     {
#                         "title": _("Contratos das Propostas"),
#                         "icon": "link",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_propostacontrato_changelist"
#                         ),
#                     },
#                     {
#                         "title": _("Parcelas das Propostas"),
#                         "icon": "payments",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_propostasparcelas_changelist"
#                         ),
#                     },
#                     {
#                         "title": _("Parcelas dos Acordos"),
#                         "icon": "calendar_month",
#                         "link": reverse_lazy(
#                             "admin:apps_cobranca_acordosparcelas_changelist"
#                         ),
#                     },
                ],
            },

            {
                "title": _("Administração"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Usuários"),
                        "icon": "group",
                        "link": reverse_lazy(
                            "admin:auth_user_changelist"
                        ),
                    },
                    {
                        "title": _("Grupos"),
                        "icon": "groups",
                        "link": reverse_lazy(
                            "admin:auth_group_changelist"
                        ),
                    },
                ],
            },

            {
                "title": _("Orquestrador"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Tarefas Agendadas"),
                        "icon": "schedule",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_periodictask_changelist"
                        ),
                    },
                    {
                        "title": _("Resultado das Tarefas"),
                        "icon": "task_alt",
                        "link": reverse_lazy(
                            "admin:django_celery_results_taskresult_changelist"
                        ),
                    },
                ],
            },

            {
                "title": _("Sistema"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Auditoria"),
                        "icon": "history",
                        "link": reverse_lazy(
                            "admin:auditlog_logentry_changelist"
                        ),
                    },
                ],
            },
        ],
    },
#     "SIDEBAR": {
#         "show_search": False,  # Search in applications and models names
#         "show_all_applications": False,  # Dropdown with all applications and models
#         "navigation": [
#             {
#                 "title": _("Navigation"),
#                 "separator": True,  # Top border
#                 "collapsible": True,  # Collapsible group of links
#                 "items": [
#                     {
#                         "title": _("Dashboard"),
#                         "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
#                         "icon_template": "helpers/icon/dashboard.svg",
#                         "link": reverse_lazy("admin:index"),
#                         "link_attrs": {
#                             "title": "Example title",
#                             "target": "_blank",
#                         },
#                         "badge": "sample_app.badge_callback",
#                         "badge_variant": "info", # info, success, warning, primary, danger
#                         "badge_style": "solid", # background fill style
#                         "badge_class": "ml-auto", # additional class for badge
#                         "permission": lambda request: request.user.is_superuser,
#                     },
#                     {
#                         "title": _("Users"),
#                         "icon": "people",
#                         "link": reverse_lazy("admin:auth_user_changelist"),
#                     },
#                 ],
#             },
#         ],
#     },
#     "TABS": [
#         {
#             "models": [
#                 "app_label.model_name_in_lowercase",
#             ],
#             "items": [
#                 {
#                     "title": _("Your custom title"),
#                     "link": reverse_lazy("admin:app_label_model_name_changelist"),
#                     "permission": "sample_app.permission_callback",
#                 },
#             ],
#         },
#     ],
}


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            "sample": "example",  # this will be injected into templates/admin/index.html
        }
    )
    return context


def environment_callback(request):
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    return ["Production", "danger"] # info, danger, warning, success


def badge_callback(request):
    return 3

def permission_callback(request):
    return request.user.has_perm("sample_app.change_model")
