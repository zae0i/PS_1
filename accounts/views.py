# accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSignupSerializer, StudentMeSerializer

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    """회원가입"""
    ser = StudentSignupSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    user = ser.save()
    return Response({"message": "회원가입 성공!", "id": user.id}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])  # JWT 필요
def me(request):
    """JWT 인증 후 내 정보 확인"""
    return Response(StudentMeSerializer(request.user).data, status=status.HTTP_200_OK)
