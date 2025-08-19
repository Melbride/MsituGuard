# 🌳 Tree Survival Prediction System

This folder contains all files related to the AI-powered tree survival prediction feature for MsituGuard.

## 📁 Folder Structure

### `/training/` - Model Training Files
- `train_tree_model.py` - Script that trains the AI model
- `cleaned_tree_data.csv` - Training data (copy)

### `/models/` - Trained Model Files
- `tree_survival_model.pkl` - The trained AI model
- `tree_scaler.pkl` - Feature scaling component
- `tree_encoders.pkl` - Text-to-number converters
- `feature_columns.pkl` - List of expected features

### `/integration/` - Django Integration Files
- `ml_utils.py` - Smart helper class for predictions
- `views_ml.py` - Web API endpoints
- `tree_prediction.html` - User interface template

## 🚀 How to Use

### 1. Training (Already Done)
```bash
cd Tree_Prediction/training
python train_tree_model.py
```

### 2. Integration (Already Done)
The integration files are copied to the Django app structure:
- `ml_utils.py` → `App/ml_utils.py`
- `views_ml.py` → `App/views_ml.py`
- `tree_prediction.html` → `App/templates/App/tree_prediction.html`

### 3. Access Prediction Interface
```
http://localhost:8000/tree-prediction/
```

## 📊 Model Performance
- **Accuracy**: 93.2%
- **Top Features**: Temperature, Altitude, Rainfall, Soil pH, Tree Age

## 🔗 API Endpoints
- `POST /api/predict-tree-survival/` - Get survival prediction
- `POST /api/species-recommendations/` - Get species recommendations

## 📝 Notes
- Model trained on 10,000+ tree records from Kenya
- Uses Random Forest algorithm
- Integrates real climate data from World Bank
- Supports 12 tree species across 9 regions