from .models import RequestLog
from django.utils.timezone import now
from ipware import get_client_ip   # safer IP extraction, works with proxies


class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract client IP
        ip, is_routable = get_client_ip(request)
        if ip is None:
            ip = "0.0.0.0"  # fallback if IP cannot be determined

        # Save request log asynchronously in DB
        RequestLog.objects.create(
            ip_address=ip,
            timestamp=now(),
            path=request.path
        )

        response = self.get_response(request)
        return response
