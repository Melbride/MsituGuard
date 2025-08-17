import math
import requests
from django.conf import settings

def get_openweather(lat: float, lon: float):
    """Fetch current weather from OpenWeather API"""
    # For now, return mock data - you can add real API key later
    return {
        "temp_c": 25.0,
        "humidity": 60.0,
        "wind_speed_ms": 5.0,
        "rainfall_mm_24h": 0.0,
    }

def get_recent_fires_count(lat: float, lon: float, radius_km: float = 25.0):
    """Get recent fires count - mock data for now"""
    return 0

def get_ndvi(lat: float, lon: float):
    """Get vegetation index - mock data for now"""
    return 0.5

def _norm_clip(x, lo, hi):
    """Normalize value to 0-1 range"""
    if x is None:
        return None
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))

def compute_fire_risk(temp_c, humidity, wind_speed_ms, rainfall_mm_24h, ndvi=None, recent_fires=0):
    """Calculate fire risk score (0-1)"""
    # Normalize indicators
    n_temp = _norm_clip(temp_c, 15, 40) if temp_c is not None else 0.5
    n_hum_rev = 1 - _norm_clip(humidity, 20, 80) if humidity is not None else 0.5
    n_wind = _norm_clip(wind_speed_ms, 0, 15) if wind_speed_ms is not None else 0.3
    n_rain_rev = 1 - _norm_clip(rainfall_mm_24h, 0, 20)
    n_ndvi_rev = 1 - _norm_clip(ndvi, 0.2, 0.7) if ndvi is not None else 0.5
    n_recent_fires = 1.0 if recent_fires > 0 else 0.0

    # Weights
    w_temp = 0.28
    w_hum = 0.22
    w_wind = 0.18
    w_rain = 0.16
    w_ndvi = 0.12
    w_memory = 0.04

    score = (
        w_temp * n_temp +
        w_hum * n_hum_rev +
        w_wind * n_wind +
        w_rain * n_rain_rev +
        w_ndvi * n_ndvi_rev +
        w_memory * n_recent_fires
    )
    return max(0.0, min(1.0, score))

def categorize_risk(score: float):
    """Convert risk score to level and color"""
    if score < 0.3:
        return "LOW", "#16a34a"
    elif score < 0.6:
        return "MODERATE", "#eab308"
    elif score < 0.8:
        return "HIGH", "#f97316"
    else:
        return "EXTREME", "#dc2626"