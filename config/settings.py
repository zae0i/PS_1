# settings.py
from pathlib import Path
from datetime import timedelta
import os
from corsheaders.defaults import default_headers  # ← 그대로 OK

BASE_DIR = Path(__file__).resolve().parent.parent

# ── 기본 보안/환경설정 ───────────────────────────────────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "3.27.119.238,localhost,127.0.0.1"
    ).split(",")
    if h.strip()
]

# ── 앱 ──────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",  # ← collectstatic/whitenoise 사용

    # 3rd-party
    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_spectacular",

    # 도메인 앱
    "accounts",
    "timecheck",
    "timetable",
    "todo",
    "calendar_memo",
]

# ── 미들웨어 ───────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # ★ 추가: SecurityMiddleware 바로 아래
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",        # CORS는 CommonMiddleware보다 위
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ── DB (ENV로 전환: DB_ENGINE=postgresql 이면 Postgres, 아니면 SQLite) ──
if os.getenv("DB_ENGINE", "sqlite").lower() == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "todolist"),
            "USER": os.getenv("DB_USER", "ps123"),
            "PASSWORD": os.getenv("DB_PASSWORD", "ps123"),
            "HOST": os.getenv("DB_HOST", "db"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ── 사용자 모델 ─────────────────────────────────────────────────
AUTH_USER_MODEL = "accounts.Student"

# ── 비밀번호 정책 ───────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── 로캘/타임존 ─────────────────────────────────────────────────
LANGUAGE_CODE = os.getenv("DJANGO_LANGUAGE_CODE", "ko-kr")
TIME_ZONE = os.getenv("DJANGO_TIME_ZONE", "Asia/Seoul")
USE_I18N = True
USE_TZ = True

# ── Static / Media (정적 서빙: Whitenoise) ─────────────────────
STATIC_URL = "/static/"                     # ★ 슬래시로 시작하도록 수정 권장
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # ★ 추가

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── DRF / JWT ───────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ── drf-spectacular ─────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    "TITLE": "PS_1 API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ── CORS / CSRF ─────────────────────────────────────────────────
_frontenv = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"
)
CORS_ALLOWED_ORIGINS = [o.strip() for o in _frontenv.split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_HEADERS = (*default_headers, "Authorization")

_csrf = []
for o in CORS_ALLOWED_ORIGINS:
    if o.startswith(("http://", "https://")):
        _csrf.append(o.replace("http://", "https://"))
        _csrf.append(o.replace("https://", "http://"))
CSRF_TRUSTED_ORIGINS = sorted(set(_csrf))

# 프록시/로드밸런서에서 SSL 종료 시 사용 (필요 시 주석 해제)
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
