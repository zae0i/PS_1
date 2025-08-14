from django.db import models
from django.conf import settings

class CalendarMemo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f"{self.date} - {self.title}"
