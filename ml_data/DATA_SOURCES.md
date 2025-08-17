# MsituGuard Tree Survival Dataset Documentation

## Data Sources Status

### Real Data (Successfully Downloaded):
1. **World Bank Climate Data**: Historical temperature data for Kenya
   - Source: World Bank Climate API
   - File: worldbank_temperature_kenya.csv
   - Status: REAL DATA - Verified from official World Bank API

### Synthetic Data (Generated for Development):
1. **Tree Survival Records**: 10,000 simulated records
   - Based on: Kenya forestry research parameters and literature
   - File: kenya_tree_survival_large_dataset.csv
   - Status: SYNTHETIC - Realistic but simulated for model development

## How to Get Real Tree Survival Data

### Immediate Actions:
1. **Kenya Forest Service**: Contact directly
   - Email: info@kenyaforestservice.org
   - Request: Historical tree planting success rates by species/region

2. **ICRAF (World Agroforestry Centre)**: Based in Nairobi
   - Website: worldagroforestry.org
   - They have extensive tree survival research data

3. **Manual FAO Download**:
   - Visit: https://fra-data.fao.org/KEN/fra2020/home/
   - Download Kenya Forest Resource Assessment Excel files

### Research Papers with Real Data:
- Search Google Scholar: "tree survival rates Kenya"
- Look for datasets in forestry journals
- Contact paper authors for data sharing

## Model Development Strategy

### Phase 1 (Current): Proof of Concept
- Use synthetic data for initial model development
- Validate model architecture and features
- Demonstrate prediction capability

### Phase 2 (Next): Real Data Integration
- Replace synthetic data with real field data
- Retrain model with actual survival rates
- Validate predictions against known outcomes

### Phase 3 (Future): Continuous Learning
- Collect data through MsituGuard platform
- Update model with new tree planting results
- Improve predictions over time

## Transparency for UNEP Competition

### What to Say:
"Our tree survival prediction model uses:
1. Real climate data from World Bank API
2. Synthetic training data based on Kenya forestry research
3. Model architecture ready for real data integration
4. Validation framework for field data collection"

### What NOT to Say:
- Don't claim synthetic data is real
- Don't hide the data generation process
- Don't present without mentioning data sources

## Validation Plan
1. Contact Kenya Forest Service for historical data
2. Partner with local organizations for field validation
3. Use MsituGuard platform to collect real survival data
4. Continuously improve model accuracy

## Technical Implementation
- Model trained on 15 environmental and management features
- 93.69% baseline survival rate (realistic for Kenya)
- Ready to integrate real data when available
- Scalable architecture for continuous learning