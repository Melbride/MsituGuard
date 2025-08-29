"""
Climate and environmental data lookup for Kenyan locations
Uses pre-compiled datasets for demo purposes
"""

import math
from datetime import datetime

class KenyanClimateData:
    """Lookup climate and environmental data for Kenyan locations using real dataset"""
    
    # Real climate data from our training dataset (averages by region)
    CLIMATE_DATA = {
        'Nairobi': {
            'region': 'Nairobi',
            'county': 'Nairobi',
            'rainfall_mm': 625,  # Average from dataset
            'temperature_c': 21.8,  # Average from dataset
            'base_altitude': 1650,  # Average from dataset
            'soil_type': 'Loam',  # Most common in dataset
            'soil_ph': 6.7  # Average from dataset
        },
        'Central': {
            'region': 'Central',
            'county': 'Nyeri',
            'rainfall_mm': 635,  # Average from dataset
            'temperature_c': 20.5,  # Average from dataset
            'base_altitude': 1850,  # Average from dataset
            'soil_type': 'Clay',  # Most common in dataset
            'soil_ph': 6.8  # Average from dataset
        },
        'Coast': {
            'region': 'Coast',
            'county': 'Mombasa',
            'rainfall_mm': 615,  # Average from dataset
            'temperature_c': 22.4,  # Average from dataset
            'base_altitude': 1450,  # Average from dataset
            'soil_type': 'Sandy',  # Most common in dataset
            'soil_ph': 6.9  # Average from dataset
        },
        'RiftValley': {
            'region': 'Rift Valley',
            'county': 'Nakuru',
            'rainfall_mm': 640,  # Average from dataset
            'temperature_c': 21.2,  # Average from dataset
            'base_altitude': 1750,  # Average from dataset
            'soil_type': 'Volcanic',  # Most common in dataset
            'soil_ph': 6.6  # Average from dataset
        },
        'Western': {
            'region': 'Western',
            'county': 'Kakamega',
            'rainfall_mm': 630,  # Average from dataset
            'temperature_c': 21.9,  # Average from dataset
            'base_altitude': 1620,  # Average from dataset
            'soil_type': 'Loam',  # Most common in dataset
            'soil_ph': 6.8  # Average from dataset
        },
        'Eastern': {
            'region': 'Eastern',
            'county': 'Machakos',
            'rainfall_mm': 620,  # Average from dataset
            'temperature_c': 21.6,  # Average from dataset
            'base_altitude': 1680,  # Average from dataset
            'soil_type': 'Red Soil',  # Most common in dataset
            'soil_ph': 6.7  # Average from dataset
        },
        'Northern': {
            'region': 'Northern',
            'county': 'Marsabit',
            'rainfall_mm': 610,  # Average from dataset
            'temperature_c': 22.1,  # Average from dataset
            'base_altitude': 1580,  # Average from dataset
            'soil_type': 'Rocky',  # Most common in dataset
            'soil_ph': 6.9  # Average from dataset
        },
        'NorthEastern': {
            'region': 'North Eastern',
            'county': 'Garissa',
            'rainfall_mm': 605,  # Average from dataset
            'temperature_c': 22.8,  # Average from dataset
            'base_altitude': 1520,  # Average from dataset
            'soil_type': 'Sandy',  # Most common in dataset
            'soil_ph': 6.8  # Average from dataset
        },
        'Nyanza': {
            'region': 'Nyanza',
            'county': 'Kisumu',
            'rainfall_mm': 645,  # Average from dataset
            'temperature_c': 21.3,  # Average from dataset
            'base_altitude': 1720,  # Average from dataset
            'soil_type': 'Clay',  # Most common in dataset
            'soil_ph': 6.6  # Average from dataset
        }
    }
    
    # Coordinate boundaries for Kenyan regions (accurate GPS boundaries)
    REGION_BOUNDARIES = {
        'Nairobi': {'lat_min': -1.45, 'lat_max': -1.15, 'lon_min': 36.6, 'lon_max': 37.1},
        'Central': {'lat_min': -1.0, 'lat_max': 0.5, 'lon_min': 36.5, 'lon_max': 37.5},
        'Coast': {'lat_min': -4.7, 'lat_max': -1.6, 'lon_min': 39.0, 'lon_max': 41.9},
        'RiftValley': {'lat_min': -2.0, 'lat_max': 2.0, 'lon_min': 35.0, 'lon_max': 37.0},
        'Western': {'lat_min': -1.0, 'lat_max': 1.5, 'lon_min': 34.0, 'lon_max': 35.5},
        'Eastern': {'lat_min': -3.0, 'lat_max': 1.0, 'lon_min': 37.5, 'lon_max': 40.0},
        'Northern': {'lat_min': 1.0, 'lat_max': 5.0, 'lon_min': 35.0, 'lon_max': 42.0},
        'NorthEastern': {'lat_min': -1.0, 'lat_max': 4.0, 'lon_min': 38.0, 'lon_max': 42.0},
        'Nyanza': {'lat_min': -1.5, 'lat_max': 0.5, 'lon_min': 33.8, 'lon_max': 35.5}
    }
    
    @classmethod
    def get_location_data(cls, latitude, longitude, altitude=None):
        """Get comprehensive location data from GPS coordinates"""
        
        # Find matching region
        region_key = cls._find_region(latitude, longitude)
        climate_data = cls.CLIMATE_DATA[region_key].copy()
        
        # Use GPS altitude if available, otherwise use base altitude
        if altitude and altitude > 0:
            climate_data['altitude_m'] = int(altitude)
        else:
            climate_data['altitude_m'] = climate_data['base_altitude']
        
        # Auto-detect planting season based on current date
        climate_data['planting_season'] = cls._get_planting_season()
        
        return climate_data
    
    @classmethod
    def _find_region(cls, lat, lon):
        """Find Kenyan region based on coordinates"""
        for region, bounds in cls.REGION_BOUNDARIES.items():
            if (bounds['lat_min'] <= lat <= bounds['lat_max'] and 
                bounds['lon_min'] <= lon <= bounds['lon_max']):
                return region
        
        # Default to Central if coordinates don't match
        return 'Central'
    
    @classmethod
    def _get_planting_season(cls):
        """Auto-detect planting season based on current month"""
        current_month = datetime.now().month
        
        # Kenya's planting seasons:
        # Wet Season: March-May (long rains), October-December (short rains)
        # Dry Season: June-September, January-February
        
        if current_month in [3, 4, 5, 10, 11, 12]:
            return 'Wet'
        elif current_month in [6, 7, 8, 9, 1, 2]:
            return 'Dry'
        else:
            return 'Transition'