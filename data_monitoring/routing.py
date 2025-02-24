from django.urls import re_path
from data_monitoring.consumers import SensorConsumer

websocket_urlpatterns = [
    re_path(r"ws/data_monitoring/", SensorConsumer.as_asgi()),
]
