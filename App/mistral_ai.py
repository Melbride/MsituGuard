import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class MistralAI:
    def __init__(self):
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        
    @property
    def api_key(self):
        """Get API key dynamically from settings"""
        return getattr(settings, 'MISTRAL_API_KEY', None)
        
    def _make_request(self, messages, max_tokens=400):
        """Make request to MISTRAL API"""
        if not self.api_key:
            logger.warning("MISTRAL API key not configured")
            return None
            
        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistral-small",
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                },
                timeout=15
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # Remove common AI response prefixes
                prefixes_to_remove = [
                    "Sure, I'd be happy to explain!",
                    "Sure, I'd be happy to help!",
                    "I'd be happy to explain!",
                    "I'd be happy to help!",
                    "Certainly!",
                    "Of course!"
                ]
                
                for prefix in prefixes_to_remove:
                    if content.startswith(prefix):
                        content = content[len(prefix):].strip()
                        break
                
                return content
            elif response.status_code == 401:
                logger.error("MISTRAL API: Invalid API key")
                return None
            elif response.status_code == 429:
                logger.error("MISTRAL API: Rate limit exceeded")
                return None
            else:
                logger.error(f"MISTRAL API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("MISTRAL API request timed out")
            return None
        except Exception as e:
            logger.error(f"MISTRAL API request failed: {str(e)}")
            return None
    
    def get_tree_recommendations(self, prediction_data, survival_rate):
        """Generate AI-powered tree planting recommendations"""
        
        if not self.api_key:
            return "Unable to generate recommendations."
        
        system_prompt = """You are a Kenyan forestry expert AI. Provide practical, actionable tree planting advice based on environmental data and survival predictions. Focus on specific, implementable recommendations."""
        
        user_prompt = f"""
        Tree Planting Analysis for Kenya:
        
        Location: {prediction_data.get('county', 'Unknown')}, {prediction_data.get('region', 'Unknown')}
        Species: {prediction_data.get('tree_species', 'Unknown')}
        Predicted Survival Rate: {survival_rate}%
        
        Environmental Conditions:
        - Soil Type: {prediction_data.get('soil_type', 'Unknown')} (pH {prediction_data.get('soil_ph', 'Unknown')})
        - Annual Rainfall: {prediction_data.get('rainfall_mm', 'Unknown')}mm
        - Average Temperature: {prediction_data.get('temperature_c', 'Unknown')}°C
        - Altitude: {prediction_data.get('altitude_m', 'Unknown')}m
        - Planting Season: {prediction_data.get('planting_season', 'Unknown')}
        - Planting Method: {prediction_data.get('planting_method', 'Unknown')}
        
        Provide exactly 3 specific, actionable recommendations to improve tree survival success. Format as numbered list.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        result = self._make_request(messages, max_tokens=300)
        return result if result else "Unable to generate recommendations."
    
    def get_alternative_species(self, prediction_data):
        """Get AI-recommended alternative tree species"""
        
        if not self.api_key:
            return "Unable to generate species suggestions."
        
        system_prompt = """You are a Kenyan forestry expert. Recommend native Kenyan tree species that would thrive in the given environmental conditions. Focus on indigenous and well-adapted species."""
        
        user_prompt = f"""
        Environmental Conditions in {prediction_data.get('county', 'Unknown')}, Kenya:
        
        - Soil Type: {prediction_data.get('soil_type', 'Unknown')} (pH {prediction_data.get('soil_ph', 'Unknown')})
        - Annual Rainfall: {prediction_data.get('rainfall_mm', 'Unknown')}mm
        - Average Temperature: {prediction_data.get('temperature_c', 'Unknown')}°C
        - Altitude: {prediction_data.get('altitude_m', 'Unknown')}m
        
        Recommend exactly 4 native Kenyan tree species that would have high survival rates in these conditions.
        
        Format each as: "Species Name - Expected Survival Rate - Key Benefit"
        Example: "Grevillea robusta - 85% - Fast growing, drought resistant"
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        result = self._make_request(messages, max_tokens=250)
        return result if result else "Unable to generate species suggestions."
    
    def explain_prediction_factors(self, prediction_data, survival_rate):
        """Explain why certain factors affect the prediction"""
        
        if not self.api_key:
            return "Unable to generate analysis."
        
        system_prompt = """You are a Kenyan forestry expert AI. Explain in simple terms why environmental factors affect tree survival rates. Be educational and easy to understand."""
        
        user_prompt = f"""
        Explain why this tree planting scenario has a {survival_rate}% survival rate:
        
        Species: {prediction_data.get('tree_species', 'Unknown')}
        Location: {prediction_data.get('county', 'Unknown')}, {prediction_data.get('region', 'Unknown')}
        Soil: {prediction_data.get('soil_type', 'Unknown')} (pH {prediction_data.get('soil_ph', 'Unknown')})
        Rainfall: {prediction_data.get('rainfall_mm', 'Unknown')}mm/year
        Temperature: {prediction_data.get('temperature_c', 'Unknown')}°C
        
        Explain in 2-3 sentences what factors are helping or hindering tree survival in this scenario.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        result = self._make_request(messages, max_tokens=200)
        return result if result else "Unable to generate analysis."

# Initialize global instance
mistral_ai = MistralAI()