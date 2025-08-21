# accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class StudentSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "student_id", "name", "password")

    def validate_student_id(self, value):
        # unique=True라서 save 시에도 막히지만, 에러를 400으로 예쁘게
        if User.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("이미 존재하는 아이디입니다.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StudentMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "student_id", "name")
        read_only_fields = fields
