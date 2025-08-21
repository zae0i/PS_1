# accounts/views.py
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, inline_serializer

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import StudentSignupSerializer, StudentMeSerializer

User = get_user_model()


@extend_schema(
    summary="회원가입",
    request=StudentSignupSerializer,
    responses={
        201: inline_serializer(
            name="SignupSuccess",
            fields={
                "message": serializers.CharField(),
                "id": serializers.IntegerField(),
            },
        )
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    """회원가입"""
    ser = StudentSignupSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    user = ser.save()
    return Response({"message": "회원가입 성공!", "id": user.id}, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="내 정보 조회",
    responses=StudentMeSerializer,
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])  # JWT 필요
def me(request):
    """JWT 인증 후 내 정보 확인"""
    return Response(StudentMeSerializer(request.user).data, status=status.HTTP_200_OK)


@extend_schema(
    summary="로그아웃",
    request=inline_serializer(
        name="LogoutRequest",
        fields={"refresh": serializers.CharField(required=False)},
    ),
    responses=inline_serializer(
        name="LogoutResponse",
        fields={"message": serializers.CharField()},
    ),
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    JWT 로그아웃
    - 블랙리스트 앱이 활성화된 경우(refresh 필요): 서버에서 토큰 무효화
    - 비활성화된 경우: 클라이언트가 보유한 access/refresh 토큰 삭제로 처리
    """
    use_blacklist = "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS

    if use_blacklist:
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"message": "refresh 토큰이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"message": "이미 로그아웃되었거나 유효하지 않은 토큰입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"message": "로그아웃 성공!"}, status=status.HTTP_200_OK)

    # 블랙리스트 미사용 시: FE에서 토큰 삭제로 처리
    return Response({"message": "로그아웃 성공!"}, status=status.HTTP_200_OK)
