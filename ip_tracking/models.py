from django.db import models
from django.utils import timezone

# Create your models here.


class RequestLog(models.Model):
    """
    Logs the client IP, request path, and timestamp 
    for auditing, debugging, and security monitoring.
    """

    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ip_address} - {self.path} @ {self.timestamp}"
