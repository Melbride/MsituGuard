from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .ml_utils import tree_predictor

@csrf_exempt
@require_http_methods(["POST"])
def predict_tree_survival(request):
    """API endpoint for tree survival prediction"""
    
    try:
        data = json.loads(request.body)
        
        # Extract required fields
        tree_data = {
            'tree_species': data.get('tree_species', 'Eucalyptus'),
            'region': data.get('region', 'Central'),
            'county': data.get('county', 'Nairobi'),
            'soil_type': data.get('soil_type', 'Loam'),
            'rainfall_mm': float(data.get('rainfall_mm', 600)),
            'temperature_c': float(data.get('temperature_c', 20)),
            'altitude_m': float(data.get('altitude_m', 1500)),
            'soil_ph': float(data.get('soil_ph', 6.5)),
            'planting_season': data.get('planting_season', 'Wet'),
            'planting_method': data.get('planting_method', 'Seedling'),
            'care_level': data.get('care_level', 'Medium'),
            'water_source': data.get('water_source', 'Rain-fed'),
            'tree_age_months': int(data.get('tree_age_months', 12))
        }
        
        # Get prediction
        result = tree_predictor.predict_survival(tree_data)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'survival_probability': 0.5,
            'recommendation': 'Error in prediction'
        })

@csrf_exempt
@require_http_methods(["POST"])
def get_species_recommendations(request):
    """API endpoint for species recommendations based on location"""
    
    try:
        data = json.loads(request.body)
        
        location_data = {
            'region': data.get('region', 'Central'),
            'county': data.get('county', 'Nairobi'),
            'soil_type': data.get('soil_type', 'Loam'),
            'rainfall_mm': float(data.get('rainfall_mm', 600)),
            'temperature_c': float(data.get('temperature_c', 20)),
            'altitude_m': float(data.get('altitude_m', 1500)),
            'soil_ph': float(data.get('soil_ph', 6.5)),
            'planting_season': data.get('planting_season', 'Wet'),
            'water_source': data.get('water_source', 'Rain-fed')
        }
        
        recommendations = tree_predictor.get_species_recommendations(location_data)
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'recommendations': []
        })