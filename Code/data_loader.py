"""
Data Preprocessing and Loading Module
Handles data loading, cleaning, imputation, encoding, and scaling.
Supports both the Kaggle Food_Delivery_Times.csv and food_delivery_data.csv seamlessly.
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple, List
from linear_regression_scratch import StandardScalerScratch, train_test_split_scratch

def load_and_preprocess_data(
    file_path: str = None,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str], StandardScalerScratch, pd.DataFrame]:
    """
    Load food delivery dataset, clean, encode and standardize features.
    
    Returns:
    --------
    X_train_scaled, X_test_scaled, y_train, y_test, feature_names, scaler, raw_df
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    candidate_paths = [
        file_path,
        os.path.join(base_dir, file_path) if file_path else None,
        os.path.join(base_dir, "Food_Delivery_Times.csv"),
        os.path.join(base_dir, "food_delivery_data.csv"),
        os.path.join(base_dir, "dataset", "Food_Delivery_Times.csv"),
        "Food_Delivery_Times.csv",
        "food_delivery_data.csv"
    ]
    
    resolved_path = None
    for p in candidate_paths:
        if p and os.path.exists(p):
            resolved_path = p
            break
            
    if not resolved_path:
        raise FileNotFoundError(f"Could not locate dataset. Checked paths: {candidate_paths}")
        
    print(f"Loading dataset from: {resolved_path}")
    raw_df = pd.read_csv(resolved_path)
    df = raw_df.copy()
    
    # -------------------------------------------------------------------------
    # CASE 1: Kaggle Dataset (Food_Delivery_Times.csv)
    # -------------------------------------------------------------------------
    if 'Distance_km' in df.columns or 'Weather' in df.columns or 'Order_ID' in df.columns:
        if 'Order_ID' in df.columns:
            df = df.drop(columns=['Order_ID'])
            
        target_col = 'Delivery_Time_min'
        
        # Impute numerical features
        if 'Courier_Experience_yrs' in df.columns:
            df['Courier_Experience_yrs'] = pd.to_numeric(df['Courier_Experience_yrs'], errors='coerce')
            df['Courier_Experience_yrs'] = df['Courier_Experience_yrs'].fillna(df['Courier_Experience_yrs'].median())
            
        if 'Distance_km' in df.columns:
            df['Distance_km'] = pd.to_numeric(df['Distance_km'], errors='coerce')
            df['Distance_km'] = df['Distance_km'].fillna(df['Distance_km'].median())
            
        if 'Preparation_Time_min' in df.columns:
            df['Preparation_Time_min'] = pd.to_numeric(df['Preparation_Time_min'], errors='coerce')
            df['Preparation_Time_min'] = df['Preparation_Time_min'].fillna(df['Preparation_Time_min'].median())
            
        # Impute categorical features
        cat_cols = [c for c in ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type'] if c in df.columns]
        for c in cat_cols:
            df[c] = df[c].fillna(df[c].mode()[0])
            
        # One-hot encode categoricals
        if cat_cols:
            df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True, dtype=float)
        else:
            df_encoded = df.copy()
            
        feature_names = [c for c in df_encoded.columns if c != target_col]
        X = df_encoded[feature_names].values
        y = pd.to_numeric(df_encoded[target_col], errors='coerce').fillna(df_encoded[target_col].median()).values

    # -------------------------------------------------------------------------
    # CASE 2: food_delivery_data.csv (Physical simulated dataset)
    # -------------------------------------------------------------------------
    else:
        target_col = 'delivery_time_min'
        feature_names = [c for c in df.columns if c != target_col]
        for col in feature_names + [target_col]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median())
        X = df[feature_names].values
        y = df[target_col].values

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split_scratch(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Feature scaling (Standardization)
    scaler = StandardScalerScratch()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, feature_names, scaler, raw_df

if __name__ == '__main__':
    X_tr, X_te, y_tr, y_te, feats, scaler, df = load_and_preprocess_data()
    print("Features:", feats)
    print("Train shape:", X_tr.shape, "Test shape:", X_te.shape)
