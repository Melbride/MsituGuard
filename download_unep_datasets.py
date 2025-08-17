import requests
import pandas as pd
import os
from io import StringIO

def download_unep_datasets():
    """Download key UNEP datasets for tree survival model enhancement"""
    
    os.makedirs('ml_data/unep_datasets', exist_ok=True)
    
    datasets_downloaded = []
    
    print("Downloading UNEP datasets for MsituGuard enhancement...")
    
    # 1. World Bank PM2.5 Air Pollution Data for Kenya
    try:
        print("\n1. Downloading World Bank PM2.5 data...")
        url = "https://api.worldbank.org/v2/country/KE/indicator/EN.ATM.PM25.MC.M3?format=json&per_page=100"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1])
                df.to_csv('ml_data/unep_datasets/worldbank_pm25_kenya.csv', index=False)
                print("[SUCCESS] PM2.5 air pollution data downloaded")
                datasets_downloaded.append("PM2.5 Air Pollution (World Bank)")
    except Exception as e:
        print(f"[FAILED] PM2.5 data: {e}")
    
    # 2. World Bank Urban Population Data
    try:
        print("\n2. Downloading World Bank urban population data...")
        url = "https://api.worldbank.org/v2/country/KE/indicator/SP.URB.TOTL.IN.ZS?format=json&per_page=100"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1])
                df.to_csv('ml_data/unep_datasets/worldbank_urban_population_kenya.csv', index=False)
                print("[SUCCESS] Urban population data downloaded")
                datasets_downloaded.append("Urban Population (World Bank)")
    except Exception as e:
        print(f"[FAILED] Urban population data: {e}")
    
    # 3. Carbon Pricing Dashboard (World Bank Excel)
    try:
        print("\n3. Downloading Carbon Pricing data...")
        url = "https://carbonpricingdashboard.worldbank.org/sites/default/files/data-latest.xlsx"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open('ml_data/unep_datasets/carbon_pricing_dashboard.xlsx', 'wb') as f:
                f.write(response.content)
            print("[SUCCESS] Carbon pricing data downloaded")
            datasets_downloaded.append("Carbon Pricing Dashboard (World Bank)")
    except Exception as e:
        print(f"[FAILED] Carbon pricing data: {e}")
    
    # 4. Kenya Economic Survey (KNBS Excel)
    try:
        print("\n4. Downloading Kenya Economic Survey...")
        url = "https://www.knbs.or.ke/wp-content/uploads/2024/04/2023-Economic-Survey-Kenya-Environment-and-Natural-Resources.xlsx"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            with open('ml_data/unep_datasets/kenya_economic_survey_environment.xlsx', 'wb') as f:
                f.write(response.content)
            print("[SUCCESS] Kenya Economic Survey downloaded")
            datasets_downloaded.append("Kenya Economic Survey - Environment (KNBS)")
    except Exception as e:
        print(f"[FAILED] Kenya Economic Survey: {e}")
    
    # 5. Try to get some climate data from IMF
    try:
        print("\n5. Attempting IMF climate data...")
        # This might require specific API access
        print("[INFO] IMF climate data requires specific API access - manual download needed")
    except Exception as e:
        print(f"[INFO] IMF data needs manual access: {e}")
    
    return datasets_downloaded

def create_integration_plan(downloaded_datasets):
    """Create plan for integrating UNEP data with tree survival model"""
    
    plan = f"""# UNEP Dataset Integration Plan for MsituGuard

## Successfully Downloaded Datasets:
{chr(10).join([f"- {dataset}" for dataset in downloaded_datasets])}

## Integration Strategy:

### 1. Air Quality Enhancement (PM2.5 data):
```python
# Add to tree survival model
features += ['pm25_exposure']  # Air pollution affects tree health
# Higher PM2.5 → lower tree survival probability
```

### 2. Urbanization Pressure (Urban population data):
```python
# Add urbanization context
features += ['urban_pressure']  # Urban areas have different survival rates
# Higher urbanization → different planting success rates
```

### 3. Carbon Context (Carbon pricing data):
```python
# Add economic environmental value
features += ['carbon_value']  # Trees have carbon sequestration value
# Links tree survival to economic environmental benefits
```

### 4. Environmental Economics (Kenya Economic Survey):
```python
# Add national environmental context
features += ['env_investment']  # Government environmental spending
# Policy support affects tree planting success
```

## Enhanced Model Features:
```python
# Original 13 features + UNEP enhancements
enhanced_features = [
    # Original features
    'tree_species', 'rainfall_mm', 'temperature_c', 'altitude_m',
    'soil_ph', 'planting_season', 'care_level', 'water_source',
    
    # UNEP dataset enhancements
    'pm25_exposure',      # Air quality impact on trees
    'urban_pressure',     # Urbanization effects
    'carbon_value',       # Economic environmental value
    'env_policy_support'  # Government environmental investment
]
```

## UNEP Competition Positioning:
"MsituGuard integrates official UNEP-recommended datasets:
- World Bank air quality data → environmental health impact
- Urban population trends → development pressure analysis  
- Carbon pricing data → economic environmental valuation
- Kenya national environmental data → policy alignment

This creates a comprehensive environmental prediction model that addresses multiple UNEP sustainability metrics."

## Next Steps:
1. Process downloaded datasets
2. Extract relevant variables for tree survival
3. Integrate with existing model
4. Validate enhanced predictions
5. Document UNEP dataset usage for competition
"""
    
    with open('ml_data/unep_datasets/INTEGRATION_PLAN.md', 'w', encoding='utf-8') as f:
        f.write(plan)
    
    print(f"\n[SUCCESS] Integration plan created")

if __name__ == "__main__":
    downloaded = download_unep_datasets()
    create_integration_plan(downloaded)
    
    print(f"\n=== SUMMARY ===")
    print(f"Downloaded {len(downloaded)} UNEP datasets")
    print(f"Files saved in: ml_data/unep_datasets/")
    print(f"Integration plan: INTEGRATION_PLAN.md")
    print(f"\nYour model can now use official UNEP-recommended data!")