import pandas as pd
import numpy as np
import os

def create_tree_survival_dataset():
    """Create a sample tree survival dataset for Kenya"""
    
    os.makedirs('ml_data', exist_ok=True)
    
    # Expanded Kenya tree species and environmental factors
    tree_species = ['Eucalyptus', 'Pine', 'Cypress', 'Acacia', 'Indigenous Mix', 'Bamboo', 
                   'Grevillea', 'Casuarina', 'Wattle', 'Cedar', 'Jacaranda', 'Neem']
    regions = ['Central', 'Rift Valley', 'Western', 'Eastern', 'Coast', 'Northern', 
              'Nairobi', 'Nyanza', 'North Eastern']
    soil_types = ['Clay', 'Sandy', 'Loam', 'Rocky', 'Volcanic', 'Black Cotton', 'Red Soil']
    counties = ['Nairobi', 'Kiambu', 'Nakuru', 'Meru', 'Kakamega', 'Kisumu', 'Mombasa', 
               'Eldoret', 'Nyeri', 'Machakos', 'Kitui', 'Garissa', 'Turkana', 'Marsabit']
    
    # Generate 10,000 sample records for better ML training
    np.random.seed(42)
    n_samples = 10000
    
    data = []
    for i in range(n_samples):
        # Environmental factors
        rainfall = np.random.normal(800, 300)  # mm per year
        temperature = np.random.normal(22, 5)  # Celsius
        altitude = np.random.uniform(500, 3000)  # meters
        soil_ph = np.random.uniform(5.5, 8.0)
        
        # Tree characteristics
        species = np.random.choice(tree_species)
        region = np.random.choice(regions)
        county = np.random.choice(counties)
        soil_type = np.random.choice(soil_types)
        planting_season = np.random.choice(['Dry', 'Wet', 'Transition'])
        tree_age_months = np.random.randint(1, 120)  # Up to 10 years
        planting_method = np.random.choice(['Direct Seeding', 'Seedling', 'Cutting'])
        care_level = np.random.choice(['High', 'Medium', 'Low'])
        water_source = np.random.choice(['Rain-fed', 'Irrigation', 'Borehole', 'River'])
        
        # Calculate survival probability based on realistic factors
        survival_prob = 0.5  # Base survival rate
        
        # Species-specific adjustments (based on Kenya forestry data)
        species_bonus = {
            'Indigenous Mix': 0.35, 'Acacia': 0.30, 'Grevillea': 0.25,
            'Eucalyptus': 0.20, 'Casuarina': 0.22, 'Bamboo': 0.28,
            'Cedar': 0.18, 'Pine': 0.15, 'Cypress': 0.16,
            'Wattle': 0.24, 'Jacaranda': 0.12, 'Neem': 0.26
        }
        survival_prob += species_bonus.get(species, 0.1)
        
        # Climate adjustments
        if 600 <= rainfall <= 1200:  # Optimal rainfall
            survival_prob += 0.2
        elif rainfall < 400:  # Too dry
            survival_prob -= 0.3
        
        if 18 <= temperature <= 25:  # Optimal temperature
            survival_prob += 0.15
        elif temperature > 30:  # Too hot
            survival_prob -= 0.2
        
        # Soil adjustments
        soil_bonus = {
            'Loam': 0.20, 'Volcanic': 0.18, 'Red Soil': 0.15,
            'Clay': 0.05, 'Sandy': -0.10, 'Rocky': -0.25, 'Black Cotton': 0.08
        }
        survival_prob += soil_bonus.get(soil_type, 0)
        
        # Care and method adjustments
        if care_level == 'High':
            survival_prob += 0.25
        elif care_level == 'Medium':
            survival_prob += 0.10
        
        if planting_method == 'Seedling':
            survival_prob += 0.15
        elif planting_method == 'Cutting':
            survival_prob += 0.05
        
        if water_source in ['Irrigation', 'Borehole']:
            survival_prob += 0.20
        elif water_source == 'River':
            survival_prob += 0.10
        
        # Season adjustment
        if planting_season == 'Wet':
            survival_prob += 0.1
        
        # Age factor (younger trees more vulnerable)
        if tree_age_months < 6:
            survival_prob -= 0.1
        elif tree_age_months > 24:
            survival_prob += 0.1
        
        # Ensure probability is between 0 and 1
        survival_prob = max(0.1, min(0.95, survival_prob))
        
        # Generate binary survival outcome
        survived = 1 if np.random.random() < survival_prob else 0
        
        data.append({
            'tree_species': species,
            'region': region,
            'county': county,
            'soil_type': soil_type,
            'rainfall_mm': max(0, rainfall),
            'temperature_c': temperature,
            'altitude_m': altitude,
            'soil_ph': soil_ph,
            'planting_season': planting_season,
            'planting_method': planting_method,
            'care_level': care_level,
            'water_source': water_source,
            'tree_age_months': tree_age_months,
            'survival_probability': survival_prob,
            'survived': survived
        })
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv('ml_data/kenya_tree_survival_large_dataset.csv', index=False)
    
    print(f"Created dataset with {len(df)} records")
    print(f"Survival rate: {df['survived'].mean():.2%}")
    print(f"Species distribution:")
    print(df['tree_species'].value_counts())
    
    return df

if __name__ == "__main__":
    create_tree_survival_dataset()
    print("\nLarge dataset created! Use 'ml_data/kenya_tree_survival_large_dataset.csv' for training.")