from django.urls import path
from reputation_app.views import IPCheckView

urlpatterns = [
    path('ips-scan/', IPCheckView.as_view(), name='check-ip-addresses')
]
