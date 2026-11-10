"""
=============================================================================
Food Delivery Time Prediction System Using Linear Regression
Dataset: Kaggle Food Delivery Time Prediction (by denkuznetz)
File: train_model.py
Description: End-to-end data preprocessing, Simple Linear Regression,
             Multiple Linear Regression training, evaluation, and model serialization.
=============================================================================
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def load_and_preprocess_data(filepath: str):
    """
    Load the Kaggle Food Delivery Times dataset, inspect columns,
    handle missing values, remove duplicates, and drop Order_ID.
    
    Parameters:
        filepath (str): Path to Food_Delivery_Times.csv
        
    Returns:
        pd.DataFrame: Cleaned dataframe ready for training.
    """
    print("=" * 70)
    print("STEP 1: INSPECTING AND VERIFYING DATASET (Kaggle: denkuznetz)")
    print("=" * 70)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")

    df = pd.read_csv(filepath)
    print(f"Dataset successfully loaded: {df.shape[0]} rows, {df.shape[1]} columns.\n")

    print("Column Data Types:")
    print("-" * 35)
    for col, dtype in df.dtypes.items():
        print(f" - {col:<25} : {dtype}")

    print("\nMissing Values per Column:")
    print("-" * 35)
    print(df.isnull().sum())

    print(f"\nDuplicate Records Count: {df.duplicated().sum()}")

    print("\n" + "=" * 70)
    print("STEP 2: DATA CLEANING & PREPROCESSING")
    print("=" * 70)

    # 1. Remove duplicate rows if any exist
    init_rows = len(df)
    df = df.drop_duplicates()
    print(f"-> Removed {init_rows - len(df)} duplicate records.")

    # 2. Drop Order_ID (identifier, not a predictive feature)
    if 'Order_ID' in df.columns:
        df = df.drop(columns=['Order_ID'])
        print("-> Dropped 'Order_ID' from feature matrix.")

    # 3. Impute missing numerical feature (Courier_Experience_yrs) with median
    med_exp = float(df['Courier_Experience_yrs'].median())
    df['Courier_Experience_yrs'] = df['Courier_Experience_yrs'].fillna(med_exp)
    print(f"-> Imputed missing 'Courier_Experience_yrs' with median ({med_exp:.1f} years).")

    # 4. Impute missing categorical features with their mode (most frequent value)
    for cat_col in ['Weather', 'Traffic_Level', 'Time_of_Day']:
        mode_val = df[cat_col].mode()[0]
        df[cat_col] = df[cat_col].fillna(mode_val)
        print(f"-> Imputed missing '{cat_col}' with mode ('{mode_val}').")

    # Verify no missing values remain
    remaining_nans = df.isnull().sum().sum()
    print(f"\n-> Remaining missing values: {remaining_nans}")
    print(f"-> Cleaned dataset shape: {df.shape[0]} rows, {df.shape[1]} columns.\n")

    return df


def train_simple_linear_regression(df: pd.DataFrame):
    """
    Train a Simple Linear Regression model using Distance_km as the sole predictor.
    Demonstrates baseline y = mx + c.
    """
    print("=" * 70)
    print("STEP 3: SIMPLE LINEAR REGRESSION (Distance Only)")
    print("=" * 70)

    X_simple = df[['Distance_km']]
    y = df['Delivery_Time_min']

    # 80/20 train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_simple, y, test_size=0.2, random_state=42
    )

    slr = LinearRegression()
    slr.fit(X_train, y_train)

    y_pred = slr.predict(X_test)

    # Evaluation
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_test, y_pred)

    slope = float(slr.coef_[0])
    intercept = float(slr.intercept_)

    print("Simple Linear Regression Formula:")
    print(f"   Delivery_Time = ({slope:.4f} * Distance_km) + {intercept:.4f}\n")
    print("Performance Metrics (Test Set):")
    print(f"   - Mean Absolute Error (MAE) : {mae:.4f} minutes")
    print(f"   - Mean Squared Error (MSE)  : {mse:.4f}")
    print(f"   - Root Mean Sq. Error (RMSE): {rmse:.4f} minutes")
    print(f"   - R-squared (R2) Score      : {r2:.4f} ({r2*100:.1f}% variance explained)\n")

    return {
        'model': slr,
        'slope': slope,
        'intercept': intercept,
        'mae': float(mae),
        'mse': float(mse),
        'rmse': rmse,
        'r2': float(r2)
    }


def train_multiple_linear_regression(df: pd.DataFrame):
    """
    Train Multiple Linear Regression using all available input features.
    Evaluates MAE, MSE, RMSE, R2 and extracts feature coefficients.
    """
    print("=" * 70)
    print("STEP 4: MULTIPLE LINEAR REGRESSION (Primary Model)")
    print("=" * 70)

    num_features = ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']
    cat_features = ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']
    feature_cols = num_features + cat_features

    X = df[feature_cols]
    y = df['Delivery_Time_min']

    # 80/20 train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training instances: {X_train.shape[0]} (80%)")
    print(f"Testing instances : {X_test.shape[0]} (20%)\n")

    # ColumnTransformer with OneHotEncoder(drop='first')
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', num_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_features)
        ]
    )

    # Scikit-learn Pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    pipeline.fit(X_train, y_train)

    # Predictions
    y_pred_test = pipeline.predict(X_test)
    y_pred_train = pipeline.predict(X_train)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred_test)
    mse = mean_squared_error(y_test, y_pred_test)
    rmse = float(np.sqrt(mse))
    r2_test = r2_score(y_test, y_pred_test)
    r2_train = r2_score(y_train, y_pred_train)

    print("Multiple Linear Regression Performance:")
    print("-" * 45)
    print(f"   - Mean Absolute Error (MAE) : {mae:.4f} minutes")
    print(f"   - Mean Squared Error (MSE)  : {mse:.4f}")
    print(f"   - Root Mean Sq. Error (RMSE): {rmse:.4f} minutes")
    print(f"   - Test R2 Score             : {r2_test:.4f} ({r2_test*100:.1f}%)")
    print(f"   - Train R2 Score            : {r2_train:.4f} ({r2_train*100:.1f}%)")

    # Feature coefficients
    regressor = pipeline.named_steps['regressor']
    cat_encoder = pipeline.named_steps['preprocessor'].named_transformers_['cat']
    encoded_cat_features = list(cat_encoder.get_feature_names_out(cat_features))
    all_feature_names = num_features + encoded_cat_features

    coef_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Coefficient': regressor.coef_
    }).sort_values(by='Coefficient', ascending=False)

    print("\nLearned Feature Coefficients:")
    print("-" * 55)
    for _, row in coef_df.iterrows():
        sign = "+" if row['Coefficient'] >= 0 else ""
        print(f"   {row['Feature']:<30} : {sign}{row['Coefficient']:.4f} min")
    print(f"   {'[Intercept/Constant]':<30} : {regressor.intercept_:.4f} min")

    metrics = {
        'mae': float(mae),
        'mse': float(mse),
        'rmse': rmse,
        'r2': float(r2_test),
        'r2_train': float(r2_train),
        'n_train': int(len(X_train)),
        'n_test': int(len(X_test))
    }

    return pipeline, metrics, coef_df, float(regressor.intercept_), all_feature_names, X_test, y_test, y_pred_test


def save_artifacts(pipeline, mlr_metrics, slr_metrics, coef_df, intercept, all_feature_names, df, out_path):
    """
    Save the trained pipeline and metadata to models/linear_regression.pkl.
    """
    print("\n" + "=" * 70)
    print("STEP 5: SERIALIZING MODEL PIPELINE USING JOBLIB")
    print("=" * 70)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    categories = {
        'Weather': sorted(df['Weather'].unique().tolist()),
        'Traffic_Level': ['Low', 'Medium', 'High'],
        'Time_of_Day': ['Morning', 'Afternoon', 'Evening', 'Night'],
        'Vehicle_Type': sorted(df['Vehicle_Type'].unique().tolist())
    }

    model_bundle = {
        'pipeline': pipeline,
        'metrics': mlr_metrics,
        'simple_lr_metrics': slr_metrics,
        'coefficients': coef_df.to_dict(orient='records'),
        'intercept': intercept,
        'feature_names': all_feature_names,
        'categories': categories,
        'dataset_summary': {
            'total_rows': int(len(df)),
            'distance_mean': float(df['Distance_km'].mean()),
            'distance_min': float(df['Distance_km'].min()),
            'distance_max': float(df['Distance_km'].max()),
            'prep_time_mean': float(df['Preparation_Time_min'].mean()),
            'delivery_time_mean': float(df['Delivery_Time_min'].mean())
        }
    }

    joblib.dump(model_bundle, out_path)
    print(f"Model pipeline bundle successfully saved to: {out_path}")

    # Self-test prediction using exact dataset schema
    print("\nVerifying pipeline with a sample prediction:")
    sample_input = pd.DataFrame([{
        'Distance_km': 10.5,
        'Preparation_Time_min': 15,
        'Courier_Experience_yrs': 3.0,
        'Weather': 'Clear',
        'Traffic_Level': 'Medium',
        'Time_of_Day': 'Evening',
        'Vehicle_Type': 'Scooter'
    }])
    pred_val = pipeline.predict(sample_input)[0]
    print(f"Input: 10.5 km, 15 min prep, 3 yrs exp, Clear weather, Medium traffic, Evening, Scooter")
    print(f"Predicted Delivery Time: {pred_val:.2f} minutes")
    print("=" * 70)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'dataset', 'Food_Delivery_Times.csv')
    model_output_path = os.path.join(base_dir, 'models', 'linear_regression.pkl')

    # 1. Load and clean
    df = load_and_preprocess_data(dataset_path)

    # 2. Simple Linear Regression
    slr_results = train_simple_linear_regression(df)

    # 3. Multiple Linear Regression
    pipeline, mlr_metrics, coef_df, intercept, feature_names, X_test, y_test, y_pred = (
        train_multiple_linear_regression(df)
    )

    # 4. Save artifacts
    save_artifacts(
        pipeline=pipeline,
        mlr_metrics=mlr_metrics,
        slr_metrics=slr_results,
        coef_df=coef_df,
        intercept=intercept,
        all_feature_names=feature_names,
        df=df,
        out_path=model_output_path
    )

    print("\nModel training workflow completed successfully!")


if __name__ == '__main__':
    main()
