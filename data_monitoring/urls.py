from django.urls import path
from data_monitoring.views import charts, receive_sensor_data


urlpatterns = [
    path('', charts, name='charts'),
    path("receive-data/", receive_sensor_data, name="receive_sensor_data"),
]