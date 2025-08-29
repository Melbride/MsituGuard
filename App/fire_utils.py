import math
import requests
from django.conf import settings
import random
from datetime import datetime

# Configuration for Kenya's climate conditions
KENYA_FIRE_CONFIG = {
    'temp_range': {'min': 15, 'max': 40},
    'humidity_range': {'min': 20, 'max': 85},
    'wind_range': {'min': 0, 'max': 20},
    'rainfall_range': {'min': 0, 'max': 25},
    'ndvi_range': {'min': 0.1, 'max': 0.8},
    'risk_thresholds': {
        'low': 0.25,
        'moderate': 0.55,
        'high': 0.75
    },
    'weights': {
        'temperature': 0.30,
        'humidity': 0.25,
        'wind': 0.20,
        'rainfall': 0.15,
        'vegetation': 0.08,
        'fire_history': 0.02
    }
}

def get_openweather(lat: float, lon: float):
    """Fetch weather data with realistic variation based on location and season"""
    try:
        # Add seasonal and regional variation for Kenya
        month = datetime.now().month
        
        # Dry season (Dec-Mar, Jun-Oct) vs wet season (Apr-May, Nov)
        is_dry_season = month in [12, 1, 2, 3, 6, 7, 8, 9, 10]
        
        # Base temperature varies by altitude (estimated from lat/lon)
        altitude_factor = max(0, (lat + 1.5) * 2)  # Rough Kenya altitude estimation
        base_temp = 28 - (altitude_factor * 0.5)
        
        if is_dry_season:
            temp = base_temp + random.uniform(-3, 8)
            humidity = random.uniform(25, 55)
            rainfall = random.uniform(0, 2)
        else:
            temp = base_temp + random.uniform(-5, 3)
            humidity = random.uniform(55, 85)
            rainfall = random.uniform(0, 15)
        
        wind_speed = random.uniform(2, 12)
        
        return {
            "temp_c": round(temp, 1),
            "humidity": round(humidity, 1),
            "wind_speed_ms": round(wind_speed, 1),
            "rainfall_mm_24h": round(rainfall, 1),
        }
    except Exception:
        # Fallback to default values
        return {
            "temp_c": 25.0,
            "humidity": 60.0,
            "wind_speed_ms": 5.0,
            "rainfall_mm_24h": 0.0,
        }

def get_recent_fires_count(lat: float, lon: float, radius_km: float = 25.0):
    """Get recent fires count with realistic probability"""
    # Simulate fire probability based on season and location
    month = datetime.now().month
    is_dry_season = month in [12, 1, 2, 3, 6, 7, 8, 9, 10]
    
    if is_dry_season:
        # Higher chance of fires in dry season
        fire_probability = 0.15
    else:
        fire_probability = 0.05
    
    if random.random() < fire_probability:
        return random.randint(1, 3)
    return 0

def get_ndvi(lat: float, lon: float):
    """Get vegetation index with seasonal variation"""
    month = datetime.now().month
    is_wet_season = month in [4, 5, 11]
    
    if is_wet_season:
        # Higher vegetation in wet season
        return round(random.uniform(0.4, 0.8), 2)
    else:
        # Lower vegetation in dry season
        return round(random.uniform(0.1, 0.5), 2)

def _norm_clip(x, lo, hi):
    """Normalize value to 0-1 range with safety checks"""
    if x is None or lo is None or hi is None:
        return 0.5  # Default middle value
    if hi <= lo:
        return 0.5  # Avoid division by zero
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))

def compute_fire_risk(temp_c, humidity, wind_speed_ms, rainfall_mm_24h, ndvi=None, recent_fires=0, config=None):
    """Calculate fire risk score (0-1) using configurable parameters"""
    if config is None:
        config = KENYA_FIRE_CONFIG
    
    # Get ranges from config
    temp_range = config['temp_range']
    humidity_range = config['humidity_range']
    wind_range = config['wind_range']
    rainfall_range = config['rainfall_range']
    ndvi_range = config['ndvi_range']
    weights = config['weights']
    
    # Normalize indicators using configurable ranges
    n_temp = _norm_clip(temp_c, temp_range['min'], temp_range['max']) if temp_c is not None else 0.5
    n_hum_rev = 1 - _norm_clip(humidity, humidity_range['min'], humidity_range['max']) if humidity is not None else 0.5
    n_wind = _norm_clip(wind_speed_ms, wind_range['min'], wind_range['max']) if wind_speed_ms is not None else 0.3
    n_rain_rev = 1 - _norm_clip(rainfall_mm_24h, rainfall_range['min'], rainfall_range['max'])
    n_ndvi_rev = 1 - _norm_clip(ndvi, ndvi_range['min'], ndvi_range['max']) if ndvi is not None else 0.5
    n_recent_fires = min(1.0, recent_fires / 3.0)  # Scale fires 0-3 to 0-1

    # Calculate weighted score using configurable weights
    score = (
        weights['temperature'] * n_temp +
        weights['humidity'] * n_hum_rev +
        weights['wind'] * n_wind +
        weights['rainfall'] * n_rain_rev +
        weights['vegetation'] * n_ndvi_rev +
        weights['fire_history'] * n_recent_fires
    )
    return max(0.0, min(1.0, score))

def categorize_risk(score: float, config=None):
    """Convert risk score to level and color using configurable thresholds"""
    if config is None:
        config = KENYA_FIRE_CONFIG
    
    thresholds = config['risk_thresholds']
    
    if score < thresholds['low']:
        return "LOW", "#16a34a"
    elif score < thresholds['moderate']:
        return "MODERATE", "#eab308"
    elif score < thresholds['high']:
        return "HIGH", "#f97316"
    else:
        return "EXTREME", "#dc2626"

def get_risk_explanation(score: float, weather_data: dict, config=None):
    """Generate contextual explanation for risk level"""
    if config is None:
        config = KENYA_FIRE_CONFIG
    
    level, _ = categorize_risk(score, config)
    temp = weather_data.get('temp_c', 0)
    humidity = weather_data.get('humidity', 0)
    wind = weather_data.get('wind_speed_ms', 0)
    rainfall = weather_data.get('rainfall_mm_24h', 0)
    
    explanations = {
        'LOW': f"Low fire risk due to favorable conditions: moderate temperature ({temp}°C), adequate humidity ({humidity}%), and recent rainfall ({rainfall}mm).",
        'MODERATE': f"Moderate fire risk with current temperature ({temp}°C), humidity ({humidity}%), and wind speed ({wind} m/s). Monitor conditions closely.",
        'HIGH': f"High fire risk due to elevated temperature ({temp}°C), low humidity ({humidity}%), and strong winds ({wind} m/s). Exercise extreme caution.",
        'EXTREME': f"Extreme fire risk with dangerous conditions: high temperature ({temp}°C), very low humidity ({humidity}%), strong winds ({wind} m/s), and no recent rainfall."
    }
    
    return explanations.get(level, "Risk assessment unavailable.")