import requests
import pandas as pd
import os

def try_alternative_sources():
    """Try to get real forestry data from alternative sources"""
    
    print("Trying alternative real data sources...")
    
    # 1. Try World Bank Forest Data
    try:
        url = "https://api.worldbank.org/v2/country/KE/indicator/AG.LND.FRST.ZS?format=json&per_page=100"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                df = pd.DataFrame(data[1])
                df.to_csv('ml_data/worldbank_forest_area_kenya.csv', index=False)
                print("✓ Downloaded World Bank forest area data")
    except Exception as e:
        print(f"World Bank forest data failed: {e}")
    
    # 2. Try UN FAO STAT (different endpoint)
    try:
        # Forest area data
        url = "http://fenixservices.fao.org/faostat/api/v1/en/data/FO?area=114&element=5110&year=2010,2015,2020"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                df = pd.DataFrame(data['data'])
                df.to_csv('ml_data/fao_forest_kenya_real.csv', index=False)
                print("✓ Downloaded real FAO forest data")
    except Exception as e:
        print(f"FAO STAT failed: {e}")
    
    # 3. Try Global Forest Watch API
    try:
        # This is a simplified example - real API requires more setup
        print("Note: Global Forest Watch requires API key registration")
        print("Visit: https://data.globalforestwatch.org/ to get real data")
    except Exception as e:
        print(f"GFW failed: {e}")

def create_documentation():
    """Create documentation about data sources"""
    
    doc = """
# MsituGuard Tree Survival Dataset Documentation

## Data Sources:

### Real Data (Downloaded):
1. **World Bank Climate Data**: Historical temperature and precipitation for Kenya
   - Source: World Bank Climate API
   - File: worldbank_temperature_kenya.csv
   - Status: ✓ Real data

### Synthetic Data (Generated):
1. **Tree Survival Records**: 10,000 simulated records
   - Based on: Kenya forestry research parameters
   - File: kenya_tree_survival_large_dataset.csv
   - Status: ⚠️ Synthetic (realistic but simulated)

## Validation Strategy:
1. Model trained on synthetic data with realistic parameters
2. Validation planned with real field data from:
   - Kenya Forest Service
   - Local tree planting organizations
   - ICRAF research data

## Research References:
- Kenya Forest Service Annual Reports
- ICRAF Tree Survival Studies
- World Bank Climate Data
- FAO Forest Resource Assessment 2020

## Next Steps:
1. Obtain real tree survival data from KFS
2. Validate model predictions against field data
3. Continuous model improvement with real data
"""
    
    with open('ml_data/DATA_SOURCES.md', 'w') as f:
        f.write(doc)
    
    print("✓ Created data documentation")

if __name__ == "__main__":
    try_alternative_sources()
    create_documentation()
    print("\nRecommendation: Contact Kenya Forest Service directly for real tree survival data")
    print("Email: info@kenyaforestservice.org")