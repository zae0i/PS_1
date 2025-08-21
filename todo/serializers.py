# todo/serializers.py
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    # 상태 라벨 함께 제공
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    # 날짜 입력 포맷 고정 (YYYY-MM-DD)
    date = serializers.DateField(input_formats=["%Y-%m-%d"])

    class Meta:
        model = Todo
        fields = ("id", "content", "date", "status", "status_label")
        read_only_fields = ("id", "status_label")

    def create(self, validated_data):
        # FE는 user를 보내지 않음: 로그인 사용자로 자동 주입
        user = self.context["request"].user
        return Todo.objects.create(user=user, **validated_data)
