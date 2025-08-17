import math
import os
import requests
from django.conf import settings

def get_openweather(lat: float, lon: float):
    """Fetch current weather + simple derived rainfall from OpenWeather.
    Returns dict with keys: temp_c, humidity, wind_speed_ms, rainfall_mm_24h
    """
    key = settings.OPENWEATHER_API_KEY
    if not key:
        raise RuntimeError("OPENWEATHER_API_KEY is not set in .env")

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()

    temp_c = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    wind_speed_ms = data.get("wind", {}).get("speed")
    # Rain in last 1h/3h if available; approximate 24h (crude) by multiplying, else 0
    rain1h = data.get("rain", {}).get("1h", 0.0)
    rain3h = data.get("rain", {}).get("3h", 0.0)
    if rain1h:
        rainfall_mm_24h = float(rain1h) * 12  # rough approx
    elif rain3h:
        rainfall_mm_24h = float(rain3h) * 8   # rough approx
    else:
        rainfall_mm_24h = 0.0

    return {
        "temp_c": float(temp_c) if temp_c is not None else None,
        "humidity": float(humidity) if humidity is not None else None,
        "wind_speed_ms": float(wind_speed_ms) if wind_speed_ms is not None else None,
        "rainfall_mm_24h": float(rainfall_mm_24h),
    }

def get_recent_fires_count(lat: float, lon: float, radius_km: float = 25.0, days: int = 7):
    """Optional: Query NASA FIRMS API if API key is provided. Otherwise return 0.
    API docs: https://firms.modaps.eosdis.nasa.gov/
    For simplicity, this function returns 0 if no key is set.
    """
    key = settings.NASA_FIRMS_API_KEY
    if not key:
        return 0

    # Placeholder: you'd implement an API call here using your FIRMS key.
    # Because FIRMS requires registration and specific endpoints,
    # we'll return 0 by default to keep the app runnable.
    return 0

def get_ndvi(lat: float, lon: float):
    """Optional NDVI via GEE or any provider. For now we return None to keep it lightweight.
    You can integrate Google Earth Engine and replace this with real NDVI.
    """
    return None

def _norm_clip(x, lo, hi):
    if x is None:
        return None
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))

def compute_fire_risk(temp_c, humidity, wind_speed_ms, rainfall_mm_24h, ndvi=None, recent_fires=0):
    """Heuristic fire risk score in [0,1].
    Weights chosen to be simple and interpretable. Adjust as you gather data.
    """
    # Normalize indicators
    n_temp = _norm_clip(temp_c, 15, 40) if temp_c is not None else 0.5
    n_hum_rev = 1 - _norm_clip(humidity, 20, 80) if humidity is not None else 0.5  # lower humidity => higher risk
    n_wind = _norm_clip(wind_speed_ms, 0, 15) if wind_speed_ms is not None else 0.3
    n_rain_rev = 1 - _norm_clip(rainfall_mm_24h, 0, 20)  # more recent rain -> lower risk
    n_ndvi_rev = None
    if ndvi is not None:
        # green = 0.6-0.8 safe; dry < 0.3 risky
        n_ndvi_rev = 1 - _norm_clip(ndvi, 0.2, 0.7)
    else:
        n_ndvi_rev = 0.5

    n_recent_fires = 1.0 if recent_fires > 0 else 0.0

    # Weights (sum ~ 1.0)
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
    score = max(0.0, min(1.0, score))
    return score

def categorize_risk(score: float):
    if score < 0.3:
        return "LOW", "#16a34a"
    elif score < 0.6:
        return "MODERATE", "#eab308"
    elif score < 0.8:
        return "HIGH", "#f97316"
    else:
        return "EXTREME", "#dc2626"
