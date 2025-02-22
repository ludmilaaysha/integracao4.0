from django.db import models

# Create your models here.

from django.db import models

class SensorData(models.Model):
    distance = models.FloatField()  # Armazena a distância lida pelo sensor
    timestamp = models.DateTimeField(auto_now_add=True)  # Data e hora da leitura

