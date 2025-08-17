# MsituGuard Tree Survival Model - Data Provenance Report

## Dataset: combined_real_synthetic_dataset.csv

### REAL DATA COMPONENTS:
[VERIFIED] **Climate Data (Precipitation)**
- Source: World Bank Climate API
- Indicator: Average precipitation in depth (mm per year)
- Country: Kenya (KE)
- Years: 1960-2021 (60+ years of historical data)
- Values: 630mm average, range 630-692mm
- Status: VERIFIED REAL DATA from official World Bank API

### SYNTHETIC DATA COMPONENTS:
[SYNTHETIC] **Tree Survival Records**
- Source: Generated based on Kenya forestry research parameters
- Records: 10,000 simulated tree planting outcomes
- Features: 15 environmental and management factors
- Survival Rate: 93.69% (realistic for Kenya conditions)
- Status: SYNTHETIC but based on research literature

### DATA INTEGRATION METHOD:
1. Downloaded real precipitation data from World Bank API
2. Used real data distribution to generate realistic rainfall values
3. Combined with synthetic tree survival outcomes
4. Maintained realistic correlations between climate and survival

### VALIDATION STRATEGY:
1. **Immediate**: Model demonstrates prediction capability
2. **Short-term**: Validate against Kenya Forest Service data
3. **Long-term**: Collect real data through MsituGuard platform
4. **Continuous**: Update model with field observations

### RESEARCH REFERENCES:
- World Bank Climate Data Portal
- Kenya Forest Service Annual Reports
- ICRAF Tree Survival Studies
- FAO Forest Resource Assessment 2020

### TRANSPARENCY STATEMENT:
This dataset combines:
- Real climate data (World Bank verified)
- Synthetic tree survival data (research-based)
- Realistic environmental correlations
- Ready for real data integration

### NEXT STEPS:
1. Contact Kenya Forest Service for historical tree survival data
2. Validate model predictions against known outcomes
3. Integrate real field data as it becomes available
4. Continuous model improvement with platform data collection
