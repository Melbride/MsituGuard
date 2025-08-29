import requests
import json
from django.conf import settings

def detect_soil_with_mistral(latitude, longitude):
    """Use MISTRAL AI to detect soil type based on GPS coordinates"""
    
    try:
        api_key = getattr(settings, 'MISTRAL_API_KEY', '4IgWzgaCc0NgxAkmbf9rjnZQfdxDP6lH')
        
        prompt = f"""Based on GPS coordinates {latitude}, {longitude} in Kenya, analyze the soil type.

Consider:
- Kenya's geological regions and soil formations
- Altitude and climate patterns
- Agricultural zones and soil surveys
- Volcanic activity and sedimentary deposits

Respond with ONLY the soil type from these options:
- Clay
- Loam  
- Sandy
- Rocky
- Volcanic

Location: {latitude}, {longitude}
Soil type:"""

        response = requests.post(
            'https://api.mistral.ai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'mistral-small',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 50,
                'temperature': 0.1
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            soil_type = result['choices'][0]['message']['content'].strip()
            
            # Validate response
            valid_soils = ['Clay', 'Loam', 'Sandy', 'Rocky', 'Volcanic']
            for soil in valid_soils:
                if soil.lower() in soil_type.lower():
                    return soil
            
            # Fallback based on coordinates
            return get_soil_fallback(latitude, longitude)
        else:
            return get_soil_fallback(latitude, longitude)
            
    except Exception as e:
        print(f"MISTRAL soil detection error: {e}")
        return get_soil_fallback(latitude, longitude)

def get_soil_fallback(latitude, longitude):
    """Fallback soil detection based on Kenya's geological zones"""
    
    # Central Kenya (volcanic soils)
    if -1.0 <= latitude <= 0.5 and 36.5 <= longitude <= 37.5:
        return 'Volcanic'
    
    # Coast region (sandy soils)
    elif -4.7 <= latitude <= -1.6 and 39.0 <= longitude <= 41.9:
        return 'Sandy'
    
    # Western Kenya (clay soils)
    elif -1.0 <= latitude <= 1.5 and 34.0 <= longitude <= 35.5:
        return 'Clay'
    
    # Eastern Kenya (rocky/sandy)
    elif -3.0 <= latitude <= 1.0 and 37.5 <= longitude <= 41.0:
        return 'Rocky'
    
    # Default to loam
    else:
        return 'Loam'

def detect_region_county(latitude, longitude):
    """Auto-detect region and county from GPS coordinates"""
    
    # Nairobi
    if -1.45 <= latitude <= -1.15 and 36.6 <= longitude <= 37.1:
        return 'Nairobi', 'Nairobi'
    
    # Central Kenya
    elif -1.0 <= latitude <= 0.5 and 36.5 <= longitude <= 37.5:
        if -1.3 <= latitude <= -0.9 and 36.7 <= longitude <= 37.2:
            return 'Central', 'Kiambu'
        else:
            return 'Central', 'Nyeri'
    
    # Coast
    elif -4.7 <= latitude <= -1.6 and 39.0 <= longitude <= 41.9:
        return 'Coast', 'Mombasa'
    
    # Western
    elif -1.0 <= latitude <= 1.5 and 34.0 <= longitude <= 35.5:
        return 'Western', 'Kakamega'
    
    # Eastern
    elif -3.0 <= latitude <= 1.0 and 37.5 <= longitude <= 41.0:
        return 'Eastern', 'Machakos'
    
    # Default
    else:
        return 'Central', 'Nyeri'