# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,   # /jwt/login/  (access, refresh)
    TokenRefreshView,      # /jwt/refresh/
    TokenVerifyView,       # /jwt/verify/
)
from .views import signup, me, logout

urlpatterns = [
    # 회원가입
    path("signup/", signup, name="signup"),

    # JWT
    path("jwt/login/", TokenObtainPairView.as_view(), name="jwt_login"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),

    # 로그아웃 (블랙리스트 사용 시 refresh 토큰 무효화)
    path("logout/", logout, name="logout"),

    # 인증 확인용
    path("me/", me, name="me"),

    # (옵션) 과거 경로 호환
    # path("login/", TokenObtainPairView.as_view(), name="jwt_login_alias"),
]
