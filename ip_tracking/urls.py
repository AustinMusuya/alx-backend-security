from django.urls import path, include
from ip_tracking.views import TestGeoLocationView, RateLimitedLoginView

urlpatterns = [
    path("test-geo/", TestGeoLocationView.as_view(), name="test_geo"),
    path('login/', RateLimitedLoginView.as_view(), name='login'),
]
