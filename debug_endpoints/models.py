from django.db import models

class DebugLog(models.Model):
    message = models.TextField()
    user = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Debug Log"
        verbose_name_plural = "Debug Logs"

    def __str__(self):
        return f"{self.timestamp} - {self.message[:50]}"
