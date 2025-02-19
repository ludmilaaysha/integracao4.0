from django.urls import path
from data_monitoring.views import *

urlpatterns = [
    path('', index),
]