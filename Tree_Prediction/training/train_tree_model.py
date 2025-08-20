import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

def train_tree_survival_model():
    """Train tree survival prediction model"""
    
    # Load data
    print("Loading cleaned tree data...")
    df = pd.read_csv('cleaned_tree_data.csv')
    
    # Feature engineering
    print("Preparing features...")
    
    # Encode categorical variables
    le_species = LabelEncoder()
    le_region = LabelEncoder()
    le_county = LabelEncoder()
    le_soil = LabelEncoder()
    le_season = LabelEncoder()
    le_method = LabelEncoder()
    le_care = LabelEncoder()
    le_water = LabelEncoder()
    
    df['tree_species_encoded'] = le_species.fit_transform(df['tree_species'])
    df['region_encoded'] = le_region.fit_transform(df['region'])
    df['county_encoded'] = le_county.fit_transform(df['county'])
    df['soil_type_encoded'] = le_soil.fit_transform(df['soil_type'])
    df['planting_season_encoded'] = le_season.fit_transform(df['planting_season'])
    df['planting_method_encoded'] = le_method.fit_transform(df['planting_method'])
    df['care_level_encoded'] = le_care.fit_transform(df['care_level'])
    df['water_source_encoded'] = le_water.fit_transform(df['water_source'])
    
    # Select features for training
    feature_columns = [
        'tree_species_encoded', 'region_encoded', 'county_encoded',
        'soil_type_encoded', 'rainfall_mm', 'temperature_c', 'altitude_m',
        'soil_ph', 'planting_season_encoded', 'planting_method_encoded',
        'care_level_encoded', 'water_source_encoded', 'tree_age_months'
    ]
    
    X = df[feature_columns]
    y = df['survived']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced',
        n_jobs=1  # Avoid multiprocessing issues
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Performance:")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 5 Most Important Features:")
    print(feature_importance.head())
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save model and encoders
    print("\nSaving model and encoders...")
    joblib.dump(model, 'models/tree_survival_model.pkl')
    joblib.dump(scaler, 'models/tree_scaler.pkl')
    
    # Save encoders
    encoders = {
        'species': le_species,
        'region': le_region,
        'county': le_county,
        'soil_type': le_soil,
        'planting_season': le_season,
        'planting_method': le_method,
        'care_level': le_care,
        'water_source': le_water
    }
    
    joblib.dump(encoders, 'models/tree_encoders.pkl')
    joblib.dump(feature_columns, 'models/feature_columns.pkl')
    
    print("Model training completed successfully!")
    print("Files saved:")
    print("- models/tree_survival_model.pkl")
    print("- models/tree_scaler.pkl") 
    print("- models/tree_encoders.pkl")
    print("- models/feature_columns.pkl")
    
    return model, scaler, encoders, feature_columns

if __name__ == "__main__":
    train_tree_survival_model()