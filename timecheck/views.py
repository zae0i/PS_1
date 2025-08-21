from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import TimeCheckSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def record_time(request):
    """
    POST /api/timecheck/
    body: { "date": "YYYY-MM-DD", "study_time": "HH:MM:SS" }
    """
    ser = TimeCheckSerializer(data=request.data, context={"request": request})
    ser.is_valid(raise_exception=True)
    obj = ser.save()
    return Response(
        {"message": "측정 데이터 저장 완료!", "item": TimeCheckSerializer(obj).data},
        status=status.HTTP_201_CREATED
    )
