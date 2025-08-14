from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import TimetableEntry

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_timetable_entry(request):
    """
    POST /api/timetable/
    { "weekday": "월", "period": 1, "subject": "물리", "teacher": "김철수" }
    """
    data = request.data or {}
    weekday = data.get("weekday")
    period = data.get("period")
    subject = data.get("subject")
    teacher = data.get("teacher")

    if not all([weekday, period, subject, teacher]):
        return Response({"message": "모든 필드를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    if TimetableEntry.objects.filter(user=request.user, weekday=weekday, period=period).exists():
        return Response({"message": "해당 요일과 교시에 이미 등록된 항목이 있습니다."},
                        status=status.HTTP_400_BAD_REQUEST)

    TimetableEntry.objects.create(
        user=request.user, weekday=weekday, period=period, subject=subject, teacher=teacher
    )
    return Response({"message": "시간표 저장 완료!"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_timetable(request):
    """
    GET /api/timetable/
    """
    entries = TimetableEntry.objects.filter(user=request.user).order_by("weekday", "period")
    data = [{
        "id": e.id, "weekday": e.weekday, "period": e.period,
        "subject": e.subject, "teacher": e.teacher
    } for e in entries]
    return Response({"timetable": data}, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_timetable_entry(request, entry_id: int):
    """
    PUT /api/timetable/<id>/
    { "subject": "...", "teacher": "..." }
    """
    try:
        entry = TimetableEntry.objects.get(id=entry_id, user=request.user)
    except TimetableEntry.DoesNotExist:
        return Response({"message": "해당 시간표 항목을 찾을 수 없습니다."},
                        status=status.HTTP_404_NOT_FOUND)

    data = request.data or {}
    subject = data.get("subject")
    teacher = data.get("teacher")
    if not all([subject, teacher]):
        return Response({"message": "수정할 과목명과 교사명을 입력해주세요."},
                        status=status.HTTP_400_BAD_REQUEST)

    entry.subject = subject
    entry.teacher = teacher
    entry.save()
    return Response({"message": "시간표 수정 완료!"}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_timetable_entry(request, entry_id: int):
    """
    DELETE /api/timetable/<id>/
    """
    try:
        entry = TimetableEntry.objects.get(id=entry_id, user=request.user)
    except TimetableEntry.DoesNotExist:
        return Response({"message": "해당 항목이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    entry.delete()
    return Response({"message": "시간표 삭제 완료!"}, status=status.HTTP_200_OK)
