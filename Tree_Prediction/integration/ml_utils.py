import joblib
import numpy as np
import pandas as pd
import os
from django.conf import settings

class TreeSurvivalPredictor:
    """Tree survival prediction utility for MsituGuard"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.encoders = None
        self.feature_columns = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and preprocessing components"""
        try:
            model_dir = os.path.join(settings.BASE_DIR, 'App', 'models')
            
            self.model = joblib.load(os.path.join(model_dir, 'tree_survival_model.pkl'))
            self.scaler = joblib.load(os.path.join(model_dir, 'tree_scaler.pkl'))
            self.encoders = joblib.load(os.path.join(model_dir, 'tree_encoders.pkl'))
            self.feature_columns = joblib.load(os.path.join(model_dir, 'feature_columns.pkl'))
            
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def predict_survival(self, tree_data):
        """
        Predict tree survival probability
        
        Args:
            tree_data (dict): Dictionary containing tree planting data
                - tree_species: str
                - region: str  
                - county: str
                - soil_type: str
                - rainfall_mm: float
                - temperature_c: float
                - altitude_m: float
                - soil_ph: float
                - planting_season: str
                - planting_method: str
                - care_level: str
                - water_source: str
                - tree_age_months: int
        
        Returns:
            dict: Prediction results with probability and recommendation
        """
        
        if not self.model:
            return {
                'success': False,
                'error': 'Model not loaded',
                'survival_probability': 0.5,
                'recommendation': 'Model unavailable - proceed with caution'
            }
        
        try:
            # Prepare input data
            input_data = pd.DataFrame([tree_data])
            
            # Encode categorical variables
            input_data['tree_species_encoded'] = self.encoders['species'].transform([tree_data['tree_species']])[0]
            input_data['region_encoded'] = self.encoders['region'].transform([tree_data['region']])[0]
            input_data['county_encoded'] = self.encoders['county'].transform([tree_data['county']])[0]
            input_data['soil_type_encoded'] = self.encoders['soil_type'].transform([tree_data['soil_type']])[0]
            input_data['planting_season_encoded'] = self.encoders['planting_season'].transform([tree_data['planting_season']])[0]
            input_data['planting_method_encoded'] = self.encoders['planting_method'].transform([tree_data['planting_method']])[0]
            input_data['care_level_encoded'] = self.encoders['care_level'].transform([tree_data['care_level']])[0]
            input_data['water_source_encoded'] = self.encoders['water_source'].transform([tree_data['water_source']])[0]
            
            # Select features
            X = input_data[self.feature_columns]
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Make prediction
            survival_prob = self.model.predict_proba(X_scaled)[0][1]  # Probability of survival
            
            # Generate recommendation
            recommendation = self.get_recommendation(survival_prob, tree_data)
            
            return {
                'success': True,
                'survival_probability': round(survival_prob, 3),
                'survival_percentage': round(survival_prob * 100, 1),
                'recommendation': recommendation,
                'risk_level': self.get_risk_level(survival_prob)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'survival_probability': 0.5,
                'recommendation': 'Error in prediction - proceed with standard care'
            }
    
    def get_recommendation(self, survival_prob, tree_data):
        """Generate planting recommendation based on survival probability"""
        
        if survival_prob >= 0.8:
            return f"Excellent conditions for {tree_data['tree_species']}! High survival expected with {tree_data['care_level'].lower()} care."
        elif survival_prob >= 0.6:
            return f"Good conditions for {tree_data['tree_species']}. Consider upgrading to high care level for better results."
        elif survival_prob >= 0.4:
            return f"Moderate risk for {tree_data['tree_species']}. Recommend high care level and consider alternative species."
        else:
            return f"High risk conditions. Consider different species, location, or wait for better season."
    
    def get_risk_level(self, survival_prob):
        """Get risk level based on survival probability"""
        if survival_prob >= 0.8:
            return "Low"
        elif survival_prob >= 0.6:
            return "Medium"
        elif survival_prob >= 0.4:
            return "High"
        else:
            return "Very High"
    
    def get_species_recommendations(self, location_data):
        """Get recommended species for a specific location"""
        
        species_list = ['Eucalyptus', 'Pine', 'Acacia', 'Cypress', 'Cedar', 
                       'Grevillea', 'Neem', 'Wattle', 'Bamboo', 'Casuarina', 
                       'Jacaranda', 'Indigenous Mix']
        
        recommendations = []
        
        for species in species_list:
            test_data = {
                **location_data,
                'tree_species': species,
                'tree_age_months': 12,  # Standard age for comparison
                'care_level': 'Medium',
                'planting_method': 'Seedling'
            }
            
            try:
                result = self.predict_survival(test_data)
                if result['success']:
                    recommendations.append({
                        'species': species,
                        'survival_probability': result['survival_probability'],
                        'risk_level': result['risk_level']
                    })
            except:
                continue
        
        # Sort by survival probability
        recommendations.sort(key=lambda x: x['survival_probability'], reverse=True)
        
        return recommendations[:5]  # Top 5 recommendations

# Global predictor instance
tree_predictor = TreeSurvivalPredictor()