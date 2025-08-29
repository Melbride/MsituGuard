from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
# Import the ML predictor
import os
import pandas as pd
from django.conf import settings

# Simple GPS to dataset mapping without ML model dependency
def get_climate_from_dataset(latitude, longitude, altitude=None):
    """Get climate data from GPS using our trained dataset"""
    try:
        # Load our actual training dataset
        dataset_path = os.path.join(settings.BASE_DIR, 'Tree_Prediction', 'training', 'cleaned_tree_data.csv')
        df = pd.read_csv(dataset_path)
        
        # Map GPS to region (same logic as our trained model)
        def map_gps_to_region(lat, lon):
            if -1.45 <= lat <= -1.15 and 36.6 <= lon <= 37.1:
                return 'Nairobi'
            elif -1.0 <= lat <= 0.5 and 36.5 <= lon <= 37.5:
                return 'Central'
            elif -4.7 <= lat <= -1.6 and 39.0 <= lon <= 41.9:
                return 'Coast'
            elif -1.0 <= lat <= 1.5 and 34.0 <= lon <= 35.5:
                return 'Western'
            elif -3.0 <= lat <= 1.0 and 37.5 <= lon <= 40.0:
                return 'Eastern'
            elif -2.0 <= lat <= 2.0 and 35.0 <= lon <= 37.0:
                return 'Rift Valley'
            elif 1.0 <= lat <= 5.0 and 35.0 <= lon <= 42.0:
                return 'Northern'
            elif -1.0 <= lat <= 4.0 and 38.0 <= lon <= 42.0:
                return 'North Eastern'
            elif -1.5 <= lat <= 0.5 and 33.8 <= lon <= 35.5:
                return 'Nyanza'
            else:
                return 'Central'
        
        region = map_gps_to_region(latitude, longitude)
        
        # Get real averages from our training data for this region
        region_data = df[df['region'] == region]
        
        if len(region_data) > 0:
            # Use actual dataset averages
            climate_data = {
                'region': region,
                'county': region_data['county'].mode().iloc[0],
                'rainfall_mm': int(region_data['rainfall_mm'].mean()),
                'temperature_c': round(region_data['temperature_c'].mean(), 1),
                'altitude_m': altitude if altitude and altitude > 0 else int(region_data['altitude_m'].mean()),
                'soil_type': region_data['soil_type'].mode().iloc[0],
                'soil_ph': round(region_data['soil_ph'].mean(), 1),
                'planting_season': 'Wet' if pd.Timestamp.now().month in [3,4,5,10,11,12] else 'Dry'
            }
        else:
            # Fallback to Central region data
            central_data = df[df['region'] == 'Central']
            climate_data = {
                'region': 'Central',
                'county': central_data['county'].mode().iloc[0],
                'rainfall_mm': int(central_data['rainfall_mm'].mean()),
                'temperature_c': round(central_data['temperature_c'].mean(), 1),
                'altitude_m': altitude if altitude and altitude > 0 else int(central_data['altitude_m'].mean()),
                'soil_type': central_data['soil_type'].mode().iloc[0],
                'soil_ph': round(central_data['soil_ph'].mean(), 1),
                'planting_season': 'Wet' if pd.Timestamp.now().month in [3,4,5,10,11,12] else 'Dry'
            }
        
        return climate_data
        
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return {
            'region': 'Central',
            'county': 'Nyeri',
            'rainfall_mm': 1200,
            'temperature_c': 20.5,
            'altitude_m': altitude if altitude and altitude > 0 else 1850,
            'soil_type': 'Clay',
            'soil_ph': 6.8,
            'planting_season': 'Wet'
        }

# Try to import ML predictor, but don't fail if it doesn't work
try:
    from .ml_utils import tree_predictor
    print("ML predictor imported successfully")
except Exception as e:
    print(f"ML predictor import failed: {e}")
    tree_predictor = None

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
        
        # Try to use trained ML model first
        if tree_predictor and hasattr(tree_predictor, 'model') and tree_predictor.model:
            try:
                result = tree_predictor.predict_survival(tree_data)
                if result.get('success'):
                    return JsonResponse(result)
            except Exception as e:
                print(f"ML prediction error: {e}")
        
        # Use our dataset-based prediction as backup
        try:
            dataset_path = os.path.join(settings.BASE_DIR, 'Tree_Prediction', 'training', 'cleaned_tree_data.csv')
            df = pd.read_csv(dataset_path)
            
            # Find similar conditions in our dataset
            similar_conditions = df[
                (df['tree_species'] == tree_data['tree_species']) &
                (df['region'] == tree_data['region']) &
                (df['planting_season'] == tree_data['planting_season'])
            ]
            
            if len(similar_conditions) > 0:
                # Calculate survival rate from actual data
                survival_rate = similar_conditions['survived'].mean()
                survival_percentage = round(survival_rate * 100, 1)
                
                def get_risk_level(rate):
                    if rate >= 0.8: return "Low"
                    elif rate >= 0.6: return "Medium"
                    elif rate >= 0.4: return "High"
                    else: return "Very High"
                
                risk = get_risk_level(survival_rate)
                recommendation = f"Based on {len(similar_conditions)} similar plantings in our dataset, {tree_data['tree_species']} has {survival_percentage}% survival rate in {tree_data['region']} region during {tree_data['planting_season'].lower()} season."
                
                return JsonResponse({
                    'success': True,
                    'survival_probability': round(survival_rate, 3),
                    'survival_percentage': survival_percentage,
                    'recommendation': recommendation,
                    'risk_level': risk
                })
            else:
                # General species success rate
                species_data = df[df['tree_species'] == tree_data['tree_species']]
                if len(species_data) > 0:
                    survival_rate = species_data['survived'].mean()
                    survival_percentage = round(survival_rate * 100, 1)
                    
                    survival_percentage = round(survival_rate * 100, 1)
                    
                    def get_risk_level(rate):
                        if rate >= 0.8: return "Low"
                        elif rate >= 0.6: return "Medium"
                        elif rate >= 0.4: return "High"
                        else: return "Very High"
                    
                    return JsonResponse({
                        'success': True,
                        'survival_probability': round(survival_rate, 3),
                        'survival_percentage': survival_percentage,
                        'recommendation': f"Based on our dataset, {tree_data['tree_species']} has {survival_percentage}% average survival rate across Kenya.",
                        'risk_level': get_risk_level(survival_rate)
                    })
                
        except Exception as e:
            print(f"Dataset prediction error: {e}")
        
        # Final fallback
        return JsonResponse({
            'success': False,
            'error': 'Unable to load prediction models or dataset',
            'survival_probability': 0.5,
            'recommendation': 'Please try again later'
        })
        
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
    """API endpoint for species recommendations using actual dataset"""
    
    try:
        data = json.loads(request.body)
        
        base_conditions = {
            'region': data.get('region', 'Central'),
            'county': data.get('county', 'Nairobi'),
            'soil_type': data.get('soil_type', 'Clay'),
            'rainfall_mm': float(data.get('rainfall_mm', 600)),
            'temperature_c': float(data.get('temperature_c', 20)),
            'altitude_m': float(data.get('altitude_m', 1500)),
            'soil_ph': float(data.get('soil_ph', 6.5)),
            'planting_season': data.get('planting_season', 'Wet'),
            'planting_method': data.get('planting_method', 'Seedling'),
            'care_level': 'Medium',
            'water_source': 'Rain-fed',
            'tree_age_months': 12
        }
        
        species_list = ['Indigenous Mix', 'Grevillea', 'Acacia', 'Pine', 'Eucalyptus', 'Cedar']
        recommendations = []
        
        dataset_path = os.path.join(settings.BASE_DIR, 'Tree_Prediction', 'training', 'cleaned_tree_data.csv')
        df = pd.read_csv(dataset_path)
        
        # Use actual trained ML model for predictions
        if tree_predictor and tree_predictor.model:
            for species in species_list:
                test_data = {
                    **base_conditions,
                    'tree_species': species
                }
                
                try:
                    result = tree_predictor.predict_survival(test_data)
                    if result['success']:
                        recommendations.append({
                            'species': species,
                            'survival_probability': result['survival_probability'],
                            'survival_percentage': int(result['survival_percentage']),
                            'risk_level': result['risk_level']
                        })
                except Exception as e:
                    print(f"Error predicting for {species}: {e}")
                    continue
        else:
            # Fallback to dataset statistics if model not available
            for species in species_list:
                similar_conditions = df[
                    (df['tree_species'] == species) &
                    (df['region'] == base_conditions['region']) &
                    (df['planting_season'] == base_conditions['planting_season'])
                ]
                
                if len(similar_conditions) > 0:
                    survival_rate = similar_conditions['survived'].mean()
                else:
                    species_data = df[df['tree_species'] == species]
                    survival_rate = species_data['survived'].mean() if len(species_data) > 0 else 0.5
                
                survival_percentage = int(round(survival_rate * 100))
                
                def get_risk_level(rate):
                    if rate >= 0.8: return "Low"
                    elif rate >= 0.6: return "Medium"
                    elif rate >= 0.4: return "High"
                    else: return "Very High"
                
                recommendations.append({
                    'species': species,
                    'survival_probability': round(survival_rate, 3),
                    'survival_percentage': survival_percentage,
                    'risk_level': get_risk_level(survival_rate)
                })
        
        recommendations.sort(key=lambda x: x['survival_probability'], reverse=True)
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations[:5]
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'recommendations': []
        })

@csrf_exempt
@require_http_methods(["POST"])
def get_climate_data(request):
    """API endpoint to get climate data from GPS coordinates using real dataset"""
    
    try:
        data = json.loads(request.body)
        
        latitude = float(data.get('latitude', -1.2921))
        longitude = float(data.get('longitude', 36.8219))
        altitude = data.get('altitude', 1500)
        
        # Get climate data from our actual training dataset
        location_data = get_climate_from_dataset(latitude, longitude, altitude)
        
        return JsonResponse({
            'success': True,
            'location_data': location_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'location_data': {}
        })