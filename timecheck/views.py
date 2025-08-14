from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import TimeCheck

def _parse_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

def _parse_time(s: str):
    try:
        return datetime.strptime(s, "%H:%M:%S").time()
    except Exception:
        return None

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def record_time(request):
    """
    POST /api/timecheck/
    { "date": "2025-06-26", "study_time": "01:30:00" }
    """
    data = request.data or {}
    date_str = data.get("date")
    time_str = data.get("study_time")

    date = _parse_date(date_str) if date_str else None
    study_time = _parse_time(time_str) if time_str else None
    if not (date and study_time):
        return Response({"message": "날짜 또는 시간 형식이 잘못되었습니다."},
                        status=status.HTTP_400_BAD_REQUEST)

    TimeCheck.objects.create(user=request.user, date=date, study_time=study_time)
    return Response({"message": "측정 데이터 저장 완료!"}, status=status.HTTP_201_CREATED)
