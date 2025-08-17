from django.contrib import admin
from .models import PredictionLog, CitizenReport

@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "lat", "lon", "risk_level", "risk_score")
    list_filter = ("risk_level", "timestamp")

@admin.register(CitizenReport)
class CitizenReportAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "observation", "lat", "lon")
    list_filter = ("observation", "timestamp")
