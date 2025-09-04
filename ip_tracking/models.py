from django.db import models
from django.utils import timezone
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.


class RequestLog(models.Model):
    """
    Logs the client IP, request path, and timestamp 
    for auditing, debugging, and security monitoring.
    """

    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} @ {self.timestamp}"

    @classmethod
    def get_geolocation_data(cls, ip_address):
        """Get geolocation data from cache or API"""
        cache_key = f"ip_geo_{ip_address}"
        geo_data = cache.get(cache_key)

        if geo_data is None:
            try:
                import requests

                # Using ip-api.com (free tier)
                response = requests.get(
                    f"http://ip-api.com/json/{ip_address}?fields=status,message,country,city,lat,lon"
                )
                data = response.json()

                if data.get("status") == "success":
                    geo_data = {
                        "country": data.get("country"),
                        "city": data.get("city"),
                        "latitude": data.get("lat"),
                        "longitude": data.get("lon"),
                    }
                    # Cache for 24 hours
                    cache.set(cache_key, geo_data, 60 * 60 * 24)
                else:
                    geo_data = {}

            except Exception as e:
                # Log error but don't fail the request
                import logging

                logger = logging.getLogger(__name__)
                logger.error(
                    f"Failed to get geolocation for {ip_address}: {str(e)}")
                geo_data = {}

        return geo_data


class BlockedIP(models.Model):
    """
    Stores IP addresses that are blocked from accessing the application.
    """

    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(
        blank=True, null=True, help_text="Reason for blocking this IP"
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this IP block is active"
    )

    class Meta:
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ip_address} (Blocked at: {self.created_at})"

    def save(self, *args, **kwargs):
        # Validate IP address
        try:
            self.full_clean()
        except ValidationError as e:
            raise ValidationError(
                _(f"Invalid IP address: {self.ip_address}")) from e
        super().save(*args, **kwargs)
