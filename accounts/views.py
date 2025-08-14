# accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])  # 공개 엔드포인트, CSRF 미적용
def signup(request):
    """회원가입 (DRF)"""
    name = request.data.get('name')
    student_id = request.data.get('student_id')
    password = request.data.get('password')

    if not all([name, student_id, password]):
        return Response({'message': '필수 항목 누락'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(student_id=student_id).exists():
        return Response({'message': '이미 존재하는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(student_id=student_id, name=name, password=password)
    return Response({'message': '회원가입 성공!', 'id': user.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # JWT 필요
def me(request):
    """JWT 인증 후 내 정보 확인"""
    u = request.user
    return Response(
        {
            'id': u.id,
            'student_id': getattr(u, 'student_id', None),
            'name': getattr(u, 'name', None),
        },
        status=status.HTTP_200_OK
    )
