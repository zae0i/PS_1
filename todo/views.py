from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Todo

def _parse_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def todo_list_or_create(request):
    """
    GET  /api/todo/?date=YYYY-MM-DD  -> 해당 날짜의 Todo 목록
    POST /api/todo/ {content, date:'YYYY-MM-DD', status?} -> 새 Todo 생성
    """
    user = request.user

    if request.method == "GET":
        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"message": "날짜(date) 파라미터가 필요합니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        date = _parse_date(date_str)
        if not date:
            return Response({"message": "날짜 형식이 잘못되었습니다. 예: 2025-05-02"},
                            status=status.HTTP_400_BAD_REQUEST)

        todos = Todo.objects.filter(user=user, date=date)
        data = [{
            "id": t.id,
            "content": t.content,
            "status": t.status,
            "status_label": t.get_status_display() if hasattr(t, "get_status_display") else t.status,
            "date": t.date
        } for t in todos]
        return Response({"todos": data}, status=status.HTTP_200_OK)

    # POST
    data = request.data or {}
    content = data.get("content")
    status_value = data.get("status", "not_started")
    date_str = data.get("date")

    if not all([content, date_str]):
        return Response({"message": "내용과 날짜는 필수입니다."},
                        status=status.HTTP_400_BAD_REQUEST)

    date = _parse_date(date_str)
    if not date:
        return Response({"message": "날짜 형식이 잘못되었습니다. 예: 2025-05-02"},
                        status=status.HTTP_400_BAD_REQUEST)

    Todo.objects.create(user=user, content=content, status=status_value, date=date)
    return Response({"message": "할 일 추가 완료!"}, status=status.HTTP_201_CREATED)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def update_or_delete_todo(request, todo_id: int):
    """
    PUT    /api/todo/<id>/ {content?, status?} -> 수정
    DELETE /api/todo/<id>/                     -> 삭제
    """
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
    except Todo.DoesNotExist:
        return Response({"message": "해당 할 일이 존재하지 않습니다."},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = request.data or {}
        content = data.get("content")
        status_value = data.get("status")

        if content is not None:
            todo.content = content
        if status_value is not None:
            todo.status = status_value

        todo.save()
        return Response({"message": "할 일 수정 완료!"}, status=status.HTTP_200_OK)

    # DELETE
    todo.delete()
    return Response({"message": "할 일 삭제 완료!"}, status=status.HTTP_200_OK)
