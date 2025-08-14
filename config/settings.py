# settings.py
from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ── 기본 보안/환경설정 ───────────────────────────────────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv("DJANGO_ALLOWED_HOSTS", "3.27.119.238,localhost,127.0.0.1").split(",")
    if h.strip()
]

# ── 앱 ──────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",          # DRF
    "corsheaders",

    "accounts",
    "timecheck",
    "timetable",
    "todo",
    "calendar_memo",
]

# ── 미들웨어 ───────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",   # CORS는 CommonMiddleware보다 위
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

AUTH_USER_MODEL = "accounts.Student"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ── Static / Media (도커 볼륨 경로와 일치) ───────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"   # docker-compose의 /app/media에 매핑

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── DRF / JWT ───────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # 공개 엔드포인트도 있으니 기본은 AllowAny,
    # 보호가 필요한 뷰만 @permission_classes([IsAuthenticated]) 사용
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),   # Authorization: Bearer <token>
}

# ── CORS / CSRF ─────────────────────────────────────────────────
# 프론트 도메인: 쉼표(,)로 구분해 .env의 FRONTEND_ORIGINS로 관리
_frontenv = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000")
CORS_ALLOWED_ORIGINS = [o.strip() for o in _frontenv.split(",") if o.strip()]

# JWT는 쿠키를 쓰지 않으므로 credentials 불필요
CORS_ALLOW_CREDENTIALS = False

# Authorization 헤더 허용
from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = (*default_headers, "Authorization")

# 관리자/폼 페이지용 신뢰 출처(운영에서 필요한 값만 남겨도 됨)
# 프론트 주소에서 http/https 모두 생성
_csrf = []
for o in CORS_ALLOWED_ORIGINS:
    if o.startswith(("http://", "https://")):
        _csrf.append(o.replace("http://", "https://"))
        _csrf.append(o.replace("https://", "http://"))
CSRF_TRUSTED_ORIGINS = sorted(set(_csrf))

# 프록시/로드밸런서에서 SSL 종료 시 사용
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
