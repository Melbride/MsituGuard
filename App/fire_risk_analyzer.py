import requests
import json
from typing import Dict, Any, Optional

class FireRiskAnalyzer:
    """MISTRAL AI integration for enhanced fire risk analysis"""
    
    def __init__(self, api_key: str = "4IgWzgaCc0NgxAkmbf9rjnZQfdxDP6lH"):
        self.api_key = api_key
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        
    def analyze_fire_risk(self, weather_data: Dict[str, Any], location_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Analyze fire risk using MISTRAL AI with weather and location data
        """
        try:
            # Prepare context for AI analysis
            context = self._prepare_fire_context(weather_data, location_data)
            
            # Create contextual prompt based on risk level
            risk_level = weather_data.get('risk_level', 'MODERATE')
            
            if risk_level in ['LOW']:
                focus = "maintaining current good conditions and basic fire safety"
                tone = "reassuring but vigilant"
            elif risk_level in ['MODERATE']:
                focus = "preventing escalation and maintaining awareness"
                tone = "balanced caution with practical advice"
            elif risk_level in ['HIGH', 'EXTREME']:
                focus = "immediate action and emergency preparedness"
                tone = "urgent but clear guidance"
            else:
                focus = "general fire safety awareness"
                tone = "informative"
            
            if risk_level in ['LOW', 'MODERATE']:
                prompt = f"""
                You are a fire safety expert for Kenya. Current fire risk is {risk_level}.

                Current conditions:
                {context}

                Provide a BRIEF summary in plain language (no markdown):
                1. RISK_EXPLANATION: (1-2 sentences) Why is the risk {risk_level}?
                2. PREVENTION_TIPS: (2-3 key actions) Most important prevention steps.
                3. EMERGENCY_ACTIONS: (1-2 actions) What to do if fire is spotted.
                4. SEASONAL_OUTLOOK: (1-2 sentences) What to expect and one key action.

                Keep each section short and practical.
                """
            else:
                prompt = f"""
                You are a fire safety expert for Kenya. Current fire risk is {risk_level} - this requires attention.

                Current conditions:
                {context}

                Provide focused advice in plain language (no markdown):
                1. RISK_EXPLANATION: (2-3 sentences) Why is the risk {risk_level}?
                2. PREVENTION_TIPS: (3-4 key actions) Essential prevention steps.
                3. EMERGENCY_ACTIONS: (2-3 actions) Key emergency response steps.
                4. SEASONAL_OUTLOOK: (2-3 sentences) What to expect and actions needed.

                Keep responses urgent but concise.
                """

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "model": "mistral-large-latest",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 400,
                "temperature": 0.3
            }

            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_content = result['choices'][0]['message']['content']
                return self._parse_ai_response(ai_content)
            else:
                return self._get_fallback_analysis(weather_data)
                
        except Exception as e:
            print(f"MISTRAL AI error: {e}")
            return self._get_fallback_analysis(weather_data)
    
    def _prepare_fire_context(self, weather_data: Dict[str, Any], location_data: Dict[str, Any]) -> str:
        """Prepare context string for AI analysis"""
        context = f"""
        LOCATION: {location_data.get('region', 'Kenya')}, {location_data.get('county', 'Unknown County')}
        COORDINATES: {location_data.get('lat', 0):.3f}, {location_data.get('lon', 0):.3f}
        
        CURRENT WEATHER:
        - Temperature: {weather_data.get('temp_c', 'N/A')}°C
        - Humidity: {weather_data.get('humidity', 'N/A')}%
        - Wind Speed: {weather_data.get('wind_speed_ms', 'N/A')} m/s
        - Recent Rainfall: {weather_data.get('rainfall_mm_24h', 'N/A')} mm (24h)
        
        RISK FACTORS:
        - Current Risk Level: {weather_data.get('risk_level', 'UNKNOWN')}
        - Risk Score: {weather_data.get('risk_score', 'N/A')}
        - Recent Fires: {weather_data.get('recent_fires', 0)} within 25km
        - Vegetation Index: {weather_data.get('ndvi', 'N/A')}
        """
        return context
    
    def _parse_ai_response(self, ai_content: str) -> Dict[str, str]:
        """Parse AI response into structured format and clean markdown"""
        sections = {
            'risk_explanation': '',
            'prevention_tips': '',
            'emergency_actions': '',
            'seasonal_outlook': ''
        }
        
        # Simple parsing - look for key sections
        lines = ai_content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if 'RISK_EXPLANATION' in line.upper():
                current_section = 'risk_explanation'
            elif 'PREVENTION_TIPS' in line.upper():
                current_section = 'prevention_tips'
            elif 'EMERGENCY_ACTIONS' in line.upper():
                current_section = 'emergency_actions'
            elif 'SEASONAL_OUTLOOK' in line.upper():
                current_section = 'seasonal_outlook'
            elif line and current_section:
                # Clean markdown formatting
                cleaned_line = self._clean_markdown(line)
                if cleaned_line:
                    if sections[current_section]:
                        sections[current_section] += ' ' + cleaned_line
                    else:
                        sections[current_section] = cleaned_line
        
        # If parsing failed, put everything in risk_explanation
        if not any(sections.values()):
            sections['risk_explanation'] = self._clean_markdown(ai_content)
        
        return sections
    
    def _clean_markdown(self, text: str) -> str:
        """Remove markdown formatting for clean display"""
        import re
        # Remove markdown headers
        text = re.sub(r'^#{1,6}\s*', '', text)
        # Remove bold/italic markers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        # Remove checkmarks and bullet points
        text = re.sub(r'^[✅❌•\-\*]\s*', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _get_fallback_analysis(self, weather_data: Dict[str, Any]) -> Dict[str, str]:
        """Fallback analysis when AI is unavailable"""
        risk_level = weather_data.get('risk_level', 'MODERATE')
        temp = weather_data.get('temp_c', 25)
        humidity = weather_data.get('humidity', 50)
        
        if risk_level == 'HIGH' or risk_level == 'EXTREME':
            explanation = f"High fire risk due to temperature ({temp}°C) and low humidity ({humidity}%). Dry conditions increase fire spread potential."
            tips = "Avoid outdoor burning, clear vegetation around buildings, have water/sand ready for emergencies."
        elif risk_level == 'MODERATE':
            explanation = f"Moderate fire risk with current temperature ({temp}°C) and humidity ({humidity}%). Monitor conditions closely."
            tips = "Exercise caution with fire use, maintain firebreaks, monitor weather updates."
        else:
            explanation = f"Low fire risk with favorable conditions. Temperature: {temp}°C, Humidity: {humidity}%."
            tips = "Normal fire safety precautions apply. Good time for controlled burns if needed."
        
        return {
            'risk_explanation': explanation,
            'prevention_tips': tips,
            'emergency_actions': "Call 999 for fire emergencies. Evacuate if instructed by authorities.",
            'seasonal_outlook': "Monitor weather forecasts for changing conditions."
        }

def get_fire_risk_analysis(weather_data: Dict[str, Any], location_data: Dict[str, Any]) -> Dict[str, str]:
    """Main function to get fire risk analysis"""
    analyzer = FireRiskAnalyzer()
    return analyzer.analyze_fire_risk(weather_data, location_data)