from django.db import models

class PredictionLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lon = models.FloatField()
    temperature_c = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    wind_speed_ms = models.FloatField(null=True, blank=True)
    rainfall_mm_24h = models.FloatField(null=True, blank=True)
    ndvi = models.FloatField(null=True, blank=True)
    recent_fires = models.IntegerField(default=0)
    risk_score = models.FloatField()
    risk_level = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.timestamp} ({self.lat:.3f},{self.lon:.3f}) -> {self.risk_level}"

class CitizenReport(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    lat = models.FloatField()
    lon = models.FloatField()
    observation = models.CharField(max_length=64, choices=[
        ("smoke", "Smoke"),
        ("heat", "Heat"),
        ("flames", "Flames"),
        ("smell", "Burning smell"),
        ("other", "Other"),
    ])
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} {self.observation} @ ({self.lat:.3f},{self.lon:.3f})"
