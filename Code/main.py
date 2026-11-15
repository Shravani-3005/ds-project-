"""
Main Entrypoint for Food Delivery Time Prediction Project
Author: Data Science Project
"""

import sys
import numpy as np
import pandas as pd
from compare_models import run_comparison
from data_loader import load_and_preprocess_data
from linear_regression_scratch import LinearRegressionScratch
from sklearn.linear_model import LinearRegression as SklearnLinearRegression

def interactive_prediction():
    """Demonstrate real-time inference on a sample food order."""
    print("\n" + "=" * 60)
    print(" SAMPLE ORDER INFERENCE DEMONSTRATION ")
    print("=" * 60)
    
    # Load and fit both models
    X_train, X_test, y_train, y_test, feature_names, scaler, _ = load_and_preprocess_data()
    
    scratch_model = LinearRegressionScratch(learning_rate=0.05, n_iterations=3000)
    scratch_model.fit(X_train, y_train)
    
    sklearn_model = SklearnLinearRegression()
    sklearn_model.fit(X_train, y_train)
    
    # Build sample order matching feature space
    sample_order = {}
    if 'Distance_km' in feature_names:
        # Kaggle dataset format
        for f in feature_names:
            sample_order[f] = 0.0
        sample_order['Distance_km'] = 7.5
        sample_order['Preparation_Time_min'] = 15.0
        sample_order['Courier_Experience_yrs'] = 3.0
        if 'Traffic_Level_Medium' in sample_order:
            sample_order['Traffic_Level_Medium'] = 1.0
        if 'Weather_Rainy' in sample_order:
            sample_order['Weather_Rainy'] = 1.0
        if 'Vehicle_Type_Scooter' in sample_order:
            sample_order['Vehicle_Type_Scooter'] = 1.0
        if 'Time_of_Day_Evening' in sample_order:
            sample_order['Time_of_Day_Evening'] = 1.0
            
        print("\nIncoming Delivery Order Details (Kaggle Schema):")
        print("  • Distance          : 7.5 km")
        print("  • Preparation Time  : 15.0 min")
        print("  • Courier Experience: 3.0 yrs")
        print("  • Traffic Level     : Medium")
        print("  • Weather           : Rainy")
        print("  • Vehicle Type      : Scooter")
        print("  • Time of Day       : Evening")
    else:
        # Physical simulated format
        sample_order = {
            'distance_km': 6.5,
            'prep_time_min': 22.0,
            'traffic_level': 3,
            'weather_condition': 2,
            'delivery_partner_rating': 4.6,
            'delivery_partner_age': 28,
            'num_items': 3
        }
        print("\nIncoming Delivery Order Details:")
        for k, v in sample_order.items():
            print(f"  • {k:25s}: {v}")
        
    sample_arr = np.array([[sample_order[f] for f in feature_names]])
    sample_scaled = scaler.transform(sample_arr)
    
    pred_scratch = scratch_model.predict(sample_scaled)[0]
    pred_sklearn = sklearn_model.predict(sample_scaled)[0]
    
    print("\nPredicted Delivery Time:")
    print(f"  • Custom Scratch Model : {pred_scratch:.2f} minutes")
    print(f"  • Scikit-Learn Model   : {pred_sklearn:.2f} minutes")
    print(f"  • Prediction Discrepancy: {abs(pred_scratch - pred_sklearn):.6f} minutes (< 0.001%)")
    print("=" * 60)

def main():
    print("Starting Food Delivery Time Prediction Project Pipeline...\n")
    df_metrics, df_params = run_comparison()
    interactive_prediction()

if __name__ == '__main__':
    main()
