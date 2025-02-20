from django.urls import path
from data_monitoring.views import charts

urlpatterns = [
    path('', charts, name='charts'),
]