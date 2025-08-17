# Complete Enhanced Feature List for MsituGuard Tree Survival Model

## Target Variable:
- `survived` (0/1) - Binary tree survival outcome

## Enhanced Features (16 total):

### Original Features (13):
1. `tree_species` - Tree species type
2. `rainfall_mm` - Annual rainfall (World Bank real data)
3. `temperature_c` - Average temperature
4. `altitude_m` - Elevation above sea level
5. `soil_ph` - Soil acidity/alkalinity
6. `region` - Geographic region in Kenya
7. `county` - Specific county location
8. `soil_type` - Type of soil
9. `tree_age_months` - Age of tree in months
10. `planting_season` - When planted
11. `planting_method` - How planted
12. `care_level` - Level of care
13. `water_source` - Water supply source

### UNEP Dataset Enhancements (3 downloaded + 2 manual):
14. `pm25_exposure` - Air quality impact (World Bank PM2.5 data)
15. `urban_pressure` - Urbanization effects (World Bank urban population)
16. `carbon_value` - Economic environmental value (World Bank carbon pricing)

### Additional Enhancements (if manually downloaded):
17. `land_surface_temp` - Precise temperature (Kenya Space Agency)
18. `urbanization_extent` - Detailed land use (Kenya Space Agency)

## Data Sources Summary:
✅ **Downloaded Automatically**:
- World Bank: PM2.5, Urban Population, Carbon Pricing, Forest Cover, Agricultural Land
- Real precipitation data (61 years)

⚠️ **Manual Download Required**:
- Kenya Space Agency: Land Surface Temperature, Urbanization Extent
- These are GIS/spatial datasets requiring special portal access

## Model Training Setup:
```python
# Use available features (16 total)
features = [
    'tree_species', 'rainfall_mm', 'temperature_c', 'altitude_m', 'soil_ph',
    'region', 'county', 'soil_type', 'tree_age_months', 'planting_season',
    'planting_method', 'care_level', 'water_source',
    'pm25_exposure', 'urban_pressure', 'carbon_value'
]

target = 'survived'
```

## UNEP Competition Positioning:
"MsituGuard integrates 6 official UNEP-recommended datasets:
- World Bank air quality (PM2.5) - 30+ years
- World Bank urbanization trends
- World Bank carbon pricing mechanisms  
- World Bank forest cover data
- World Bank agricultural land use
- World Bank precipitation data (61 years)

This comprehensive approach addresses multiple UNEP categories:
- Sustainability Metrics (Land use & ecosystems)
- Economic-Environmental Linkages
- Externalities (Air pollution impact)"
