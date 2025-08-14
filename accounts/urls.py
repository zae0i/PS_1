from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # /jwt/login/  (access, refresh)
    TokenRefreshView,     # /jwt/refresh/
    TokenVerifyView,      # /jwt/verify/
)
from .views import signup, me

urlpatterns = [
    # 회원가입
    path('signup/', signup),

    # JWT
    path('jwt/login/', TokenObtainPairView.as_view(), name='jwt_login'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

    # 인증 확인용
    path('me/', me),
]
