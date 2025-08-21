from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer

def _parse_date(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def todo_list_or_create(request):
    """
    GET  /api/todo/?date=YYYY-MM-DD
        -> 해당 날짜의 Todo 목록 ({"todos":[...]})
    POST /api/todo/
        body: { "content": "...", "date": "YYYY-MM-DD", "status": "not_started|in_progress|completed" }
        -> 생성된 Todo 리턴
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

        todos = Todo.objects.filter(user=user, date=date).order_by("id")
        ser = TodoSerializer(todos, many=True)
        return Response({"todos": ser.data}, status=status.HTTP_200_OK)

    # POST
    ser = TodoSerializer(data=request.data, context={"request": request})
    ser.is_valid(raise_exception=True)
    todo = ser.save()
    return Response(ser.data, status=status.HTTP_201_CREATED)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def update_or_delete_todo(request, todo_id: int):
    """
    PUT    /api/todo/<id>/   body: {content?, status?, date?}
           -> 수정된 Todo 리턴
    DELETE /api/todo/<id>/   -> {"message":"할 일 삭제 완료!"}
    """
    try:
        todo = Todo.objects.get(id=todo_id, user=request.user)
    except Todo.DoesNotExist:
        return Response({"message": "해당 할 일이 존재하지 않습니다."},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        ser = TodoSerializer(todo, data=request.data, partial=True, context={"request": request})
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_200_OK)

    # DELETE
    todo.delete()
    return Response({"message": "할 일 삭제 완료!"}, status=status.HTTP_200_OK)
