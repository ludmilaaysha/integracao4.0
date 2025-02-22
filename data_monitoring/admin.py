from django.contrib import admin

# Register your models here.

from .models import SensorData

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ("id", "distance", "timestamp")  # Exibe essas colunas na tabela
    ordering = ("-timestamp",)  # Ordena do mais recente para o mais antigo

