from django.db import models
from django.conf import settings

class Todo(models.Model):
    STATUS_CHOICES = [
        ('not_started', '시작 전'),
        ('in_progress', '진행 중'),
        ('completed', '완료'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return f"{self.date} - {self.content} ({self.get_status_display()})"
