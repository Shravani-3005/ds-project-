"""
Model Comparison Pipeline
Compares the New Model (custom implementation) against the Pre-existed Model (Scikit-Learn).
"""

import json
import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression as SklearnLinearRegression

from data_loader import load_and_preprocess_data
from linear_regression_scratch import (
    LinearRegressionScratch,
    mean_squared_error,
    root_mean_squared_error,
    mean_absolute_error,
    r2_score,
    adjusted_r2_score
)
from generate_plots import (
    setup_plot_style,
    plot_cost_convergence,
    plot_actual_vs_predicted,
    plot_residuals_distribution,
    plot_coefficients_comparison,
    plot_learning_rate_comparison
)

def run_comparison():
    print("=" * 80)
    print(" FOOD DELIVERY TIME PREDICTION: MODEL COMPARISON ")
    print("=" * 80)
    
    setup_plot_style()
    
    # 1. Load and preprocess data
    print("\n[Step 1/5] Loading & Preprocessing Food Delivery Dataset...")
    X_train, X_test, y_train, y_test, feature_names, scaler, raw_df = load_and_preprocess_data(
        file_path='Food_Delivery_Times.csv',
        test_size=0.2,
        random_state=42
    )
    n_features = len(feature_names)
    print(f"Loaded {len(raw_df)} total records.")
    print(f"Training set: {X_train.shape[0]} samples | Test set: {X_test.shape[0]} samples | Features: {n_features}")
    
    # 2. Train Models (New Model vs Pre-existed Model)
    print("\n[Step 2/5] Training Models...")
    
    # Model 1: New Model (Optimized Custom NumPy Implementation)
    print(" -> Training Model 1: New Model (Optimized Feature Selection & Analytical Solver)...")
    new_model = LinearRegressionScratch(
        method='normal_equation',
        optimize_features=True
    )
    new_model.fit(X_train, y_train)
    
    # Model 2: Pre-existed Model (Scikit-Learn LinearRegression Baseline)
    print(" -> Training Model 2: Pre-existed Model (Scikit-Learn LinearRegression)...")
    t0 = time.perf_counter()
    pre_model = SklearnLinearRegression(fit_intercept=True)
    pre_model.fit(X_train, y_train)
    pre_time = time.perf_counter() - t0
    
    # 3. Model Predictions
    print("\n[Step 3/5] Computing Predictions and Evaluating Metrics...")
    y_pred_new = new_model.predict(X_test)
    y_pred_pre = pre_model.predict(X_test)
    
    # 4. Metric Computation
    n_active_new = len(new_model.active_indices_) if new_model.active_indices_ is not None else n_features
    models_dict = {
        "New Model": {
            "pred": y_pred_new,
            "time": new_model.training_time_sec_,
            "p": n_active_new
        },
        "Pre-existed Model": {
            "pred": y_pred_pre,
            "time": pre_time,
            "p": n_features
        }
    }
    
    metrics_summary = []
    for name, item in models_dict.items():
        pred = item["pred"]
        mse = mean_squared_error(y_test, pred)
        rmse = root_mean_squared_error(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        r2 = r2_score(y_test, pred)
        adj_r2 = adjusted_r2_score(y_test, pred, item["p"])
        
        metrics_summary.append({
            "Model": name,
            "RMSE (min)": round(rmse, 4),
            "MAE (min)": round(mae, 4),
            "MSE": round(mse, 4),
            "R² Score": round(r2, 5),
            "Adjusted R²": round(adj_r2, 5),
            "Training Time (ms)": round(item["time"] * 1000, 2)
        })
        
    df_metrics = pd.DataFrame(metrics_summary)
    print("\n" + "=" * 45 + " PERFORMANCE COMPARISON " + "=" * 45)
    print(df_metrics.to_string(index=False))
    
    # 5. Parameter Level Detailed Comparison
    print("\n" + "=" * 45 + " PARAMETERS COMPARISON " + "=" * 45)
    param_records = []
    
    # Add Intercept
    param_records.append({
        "Parameter": "Intercept (b)",
        "New Model": round(float(new_model.intercept_), 5),
        "Pre-existed Model": round(float(pre_model.intercept_), 5),
        "Difference": round(abs(float(new_model.intercept_ - pre_model.intercept_)), 6),
        "Relative Error (%)": round(abs((float(new_model.intercept_) - float(pre_model.intercept_)) / float(pre_model.intercept_)) * 100, 4)
    })
    
    # Add Feature Weights
    for idx, feat in enumerate(feature_names):
        w_new = float(new_model.coef_[idx])
        w_pre = float(pre_model.coef_[idx])
        diff = abs(w_new - w_pre)
        pct_diff = abs(diff / w_pre) * 100 if w_pre != 0 else 0.0
        
        param_records.append({
            "Parameter": f"Weight: {feat}",
            "New Model": round(w_new, 5),
            "Pre-existed Model": round(w_pre, 5),
            "Difference": round(diff, 6),
            "Relative Error (%)": round(pct_diff, 4)
        })
        
    df_params = pd.DataFrame(param_records)
    print(df_params.to_string(index=False))
    
    # 6. Prediction Alignment Checks
    max_pred_diff = float(np.max(np.abs(y_pred_new - y_pred_pre)))
    mean_pred_diff = float(np.mean(np.abs(y_pred_new - y_pred_pre)))
    print("\n" + "-" * 70)
    print(f"Max Absolute Prediction Difference (New Model vs Pre-existed Model): {max_pred_diff:.6f} minutes")
    print(f"Mean Absolute Prediction Difference (New Model vs Pre-existed Model): {mean_pred_diff:.6f} minutes")
    print("-" * 70)
    
    # 7. Generate Diagnostic Plots
    print("\n[Step 4/5] Generating Diagnostic & Visual Comparison Plots...")
    plots_dir = 'plots'
    f1 = plot_cost_convergence(new_model.loss_history_, plots_dir)
    f2 = plot_actual_vs_predicted(y_test, y_pred_new, y_pred_pre, plots_dir)
    f3 = plot_residuals_distribution(y_test, y_pred_new, y_pred_pre, plots_dir)
    f4 = plot_coefficients_comparison(
        feature_names,
        new_model.coef_,
        pre_model.coef_,
        plots_dir
    )
    f5 = plot_learning_rate_comparison(X_train, y_train, [0.001, 0.01, 0.05, 0.1], plots_dir)
    print(f"Plots saved successfully in '{plots_dir}/':")
    for f in [f1, f2, f3, f4, f5]:
        print(f"  ✓ {f}")
        
    # 8. Export Results
    print("\n[Step 5/5] Exporting Benchmark Results...")
    df_metrics.to_csv('model_metrics_comparison.csv', index=False)
    df_params.to_csv('model_parameters_comparison.csv', index=False)
    
    results_json = {
        "dataset_info": {
            "total_samples": len(raw_df),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "features": feature_names
        },
        "metrics": metrics_summary,
        "max_pred_diff_new_vs_pre_existed": max_pred_diff,
        "mean_pred_diff_new_vs_pre_existed": mean_pred_diff
    }
    with open('benchmark_summary.json', 'w') as f:
        json.dump(results_json, f, indent=4)
        
    print("Saved 'model_metrics_comparison.csv', 'model_parameters_comparison.csv', and 'benchmark_summary.json'")
    print("\n" + "=" * 80)
    print(" ALL RUNS & COMPARISONS COMPLETED SUCCESSFULLY! ")
    print("=" * 80)
    
    return df_metrics, df_params

if __name__ == '__main__':
    run_comparison()
