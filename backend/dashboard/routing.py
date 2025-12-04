from django.urls import re_path
from .consumers import LiveFeedConsumer

websocket_urlpatterns = [
    re_path(r'^ws/dashboard/live-events/(?P<app>[^/]+)/$', LiveFeedConsumer.as_asgi()),
]

