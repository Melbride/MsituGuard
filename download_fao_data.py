import requests
import pandas as pd
import os

def download_fao_forest_data():
    """Download FAO forest data for Kenya"""
    
    # Create data directory
    os.makedirs('ml_data', exist_ok=True)
    
    # FAO FAOSTAT API endpoints
    urls = {
        'forest_area': 'https://fenixservices.fao.org/faostat/api/v1/en/data/FO?area=114&element=5110',
        'forest_production': 'https://fenixservices.fao.org/faostat/api/v1/en/data/FO?area=114&element=5516',
        'tree_cover': 'https://fenixservices.fao.org/faostat/api/v1/en/data/LC?area=114&element=6601'
    }
    
    for name, url in urls.items():
        try:
            print(f"Downloading {name}...")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data['data'])
                df.to_csv(f'ml_data/fao_{name}_kenya.csv', index=False)
                print(f"[OK] Saved fao_{name}_kenya.csv")
            else:
                print(f"[FAIL] Failed to download {name}: {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Error downloading {name}: {e}")

def download_climate_data():
    """Download World Bank climate data for Kenya"""
    
    # World Bank Climate API
    climate_indicators = {
        'precipitation': 'PR.PRC.TOTL.MM',
        'temperature': 'AG.LND.PRCP.MM'
    }
    
    for name, indicator in climate_indicators.items():
        try:
            url = f"https://api.worldbank.org/v2/country/KE/indicator/{indicator}?format=json&per_page=100"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1:
                    df = pd.DataFrame(data[1])
                    df.to_csv(f'ml_data/worldbank_{name}_kenya.csv', index=False)
                    print(f"[OK] Saved worldbank_{name}_kenya.csv")
                    
        except Exception as e:
            print(f"✗ Error downloading {name}: {e}")

if __name__ == "__main__":
    print("Downloading FAO and World Bank data for Kenya...")
    download_fao_forest_data()
    download_climate_data()
    print("\nDownload complete! Check 'ml_data' folder for files.")