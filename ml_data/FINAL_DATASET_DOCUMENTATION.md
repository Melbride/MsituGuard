# MsituGuard Final UNEP-Integrated Dataset

## Dataset: FINAL_UNEP_INTEGRATED_DATASET.csv

### Complete Data Sources:
✅ **Real Environmental Data (6 UNEP sources)**:
- PM2.5 Air Quality (World Bank verified)
- Urban Population (World Bank verified)
- Forest Cover (World Bank verified)
- Agricultural Land (World Bank verified)
- Enhanced Climate (World Bank verified)
- Carbon Pricing (World Bank verified)

✅ **Real Climate Foundation**:
- World Bank Precipitation: 61 years historical data
- Enhanced climate measurements

⚠️ **Synthetic Tree Survival Data**:
- 10,000 tree planting records
- Research-based survival parameters
- Realistic environmental correlations

### Final Feature Set (22 features):

#### Environmental Features (Real Data):
1. `rainfall_mm` - World Bank precipitation (61 years)
2. `pm25_exposure` - Air quality impact (30+ years)
3. `urban_pressure` - Urbanization effects
4. `forest_cover_trend` - Forest context
5. `agricultural_pressure` - Land use competition
6. `carbon_value` - Economic environmental value
7. `climate_enhanced` - Enhanced climate data

#### Tree & Management Features (Synthetic but Realistic):
8. `tree_species` - 12 Kenya tree species
9. `tree_age_months` - Tree age (1-120 months)
10. `planting_method` - Planting technique
11. `care_level` - Management intensity
12. `water_source` - Water supply type
13. `planting_season` - Seasonal timing

#### Location Features (Synthetic but Realistic):
14. `region` - Kenya regions
15. `county` - Kenya counties
16. `soil_type` - Soil characteristics
17. `altitude_m` - Elevation
18. `soil_ph` - Soil acidity
19. `temperature_c` - Temperature

#### Target Variable:
20. `survived` - Binary survival outcome (0/1)

#### Metadata:
21. `unep_datasets_integrated` - Number of UNEP sources
22. `dataset_version` - Version tracking

### Data Quality Notes:
- Missing values preserved for data cleaning phase
- All real environmental data from verified World Bank APIs
- Synthetic data based on Kenya forestry research parameters
- Ready for ML model training after cleaning

### UNEP Competition Positioning:
"MsituGuard integrates 6 official UNEP-recommended datasets with 60+ years of verified environmental data from World Bank APIs, creating a comprehensive tree survival prediction model that addresses multiple UNEP sustainability categories."

### Next Steps:
1. Data cleaning and preprocessing
2. Handle missing values appropriately
3. Feature engineering and scaling
4. ML model training and validation
5. Integration with MsituGuard platform
