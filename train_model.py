"""
=============================================================================
Food Delivery Time Prediction System Using Linear Regression
Script: train_model.py
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
    Load food delivery dataset, clean missing values, and remove duplicates.
    
    Parameters:
        filepath (str): Path to the CSV dataset file.
        
    Returns:
        pd.DataFrame: Cleaned dataframe ready for modeling.
    """
    print("=" * 70)
    print("STEP 1: LOADING AND INSPECTING DATASET")
    print("=" * 70)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}. Please verify path.")

    df = pd.read_csv(filepath)
    print(f"Dataset loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.\n")

    print("Initial Dataset Information:")
    print("-" * 40)
    print(df.info())
    print("\nInitial Missing Values:")
    print(df.isnull().sum())
    print(f"\nInitial Duplicate Rows: {df.duplicated().sum()}")

    print("\n" + "=" * 70)
    print("STEP 2: DATA CLEANING & PREPROCESSING")
    print("=" * 70)

    # 1. Remove duplicate records
    initial_len = len(df)
    df = df.drop_duplicates()
    dropped_duplicates = initial_len - len(df)
    print(f"-> Removed {dropped_duplicates} duplicate records.")

    # 2. Impute missing numerical values using median
    median_experience = df['Partner_Experience_years'].median()
    df['Partner_Experience_years'] = df['Partner_Experience_years'].fillna(median_experience)
    print(f"-> Imputed missing 'Partner_Experience_years' with median ({median_experience:.1f} years).")

    # 3. Impute missing categorical values using mode (most frequent value)
    mode_weather = df['Weather'].mode()[0]
    df['Weather'] = df['Weather'].fillna(mode_weather)
    print(f"-> Imputed missing 'Weather' with mode ('{mode_weather}').")

    # Verify no missing values remain
    remaining_nulls = df.isnull().sum().sum()
    print(f"-> Remaining missing values: {remaining_nulls}")
    print(f"-> Cleaned dataset contains {df.shape[0]} rows.\n")

    return df


def train_simple_linear_regression(df: pd.DataFrame):
    """
    Train a Simple Linear Regression model (1 independent variable: Distance).
    Serves as an educational baseline to demonstrate y = mx + c.
    """
    print("=" * 70)
    print("STEP 3: SIMPLE LINEAR REGRESSION (Baseline Model)")
    print("=" * 70)

    # Feature and Target
    X_simple = df[['Delivery_Distance_km']]
    y = df['Delivery_Time_min']

    # 80-20 Train-Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_simple, y, test_size=0.2, random_state=42
    )

    slr_model = LinearRegression()
    slr_model.fit(X_train, y_train)

    # Predictions
    y_pred = slr_model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_test, y_pred)

    slope = float(slr_model.coef_[0])
    intercept = float(slr_model.intercept_)

    print("Simple Linear Regression Formula:")
    print(f"   Delivery_Time = ({slope:.2f} * Delivery_Distance_km) + {intercept:.2f}\n")
    print(f"Performance Metrics (Distance only):")
    print(f"   - Mean Absolute Error (MAE) : {mae:.2f} minutes")
    print(f"   - Mean Squared Error (MSE)  : {mse:.2f}")
    print(f"   - Root Mean Sq. Error (RMSE): {rmse:.2f} minutes")
    print(f"   - R-squared (R2) Score      : {r2:.4f} ({r2*100:.1f}% variance explained)")
    print("Interpretation: Distance explains only a fraction of total delivery time.")
    print("Traffic, weather, prep time, and vehicle type are needed for high accuracy.\n")

    return {
        'model': slr_model,
        'slope': slope,
        'intercept': intercept,
        'mae': float(mae),
        'mse': float(mse),
        'rmse': rmse,
        'r2': float(r2)
    }


def train_multiple_linear_regression(df: pd.DataFrame):
    """
    Train Multiple Linear Regression using all features with One-Hot Encoding.
    Evaluates MAE, MSE, RMSE, R2 and extracts feature coefficients.
    """
    print("=" * 70)
    print("STEP 4: MULTIPLE LINEAR REGRESSION (Primary Model)")
    print("=" * 70)

    num_cols = ['Delivery_Distance_km', 'Preparation_Time_min', 'Partner_Experience_years']
    cat_cols = ['Traffic_Level', 'Weather', 'Time_of_Day', 'Vehicle_Type']
    feature_cols = num_cols + cat_cols

    X = df[feature_cols]
    y = df['Delivery_Time_min']

    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Testing set : {X_test.shape[0]} samples\n")

    # ColumnTransformer: pass numerical features as-is, one-hot encode categoricals
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', num_cols),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_cols)
        ]
    )

    # Scikit-Learn Pipeline combining Preprocessor and Linear Regression
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Fit pipeline
    pipeline.fit(X_train, y_train)

    # Predict on test set
    y_pred = pipeline.predict(X_test)
    y_train_pred = pipeline.predict(X_train)

    # Metrics computation
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = float(np.sqrt(mse))
    r2_test = r2_score(y_test, y_pred)
    r2_train = r2_score(y_train, y_train_pred)

    print("Multiple Linear Regression Performance:")
    print("-" * 45)
    print(f"   - Mean Absolute Error (MAE) : {mae:.2f} minutes")
    print(f"   - Mean Squared Error (MSE)  : {mse:.2f}")
    print(f"   - Root Mean Sq. Error (RMSE): {rmse:.2f} minutes")
    print(f"   - Test R2 Score             : {r2_test:.4f} ({r2_test*100:.1f}%)")
    print(f"   - Train R2 Score            : {r2_train:.4f} ({r2_train*100:.1f}%)")

    # Extract transformed feature names and coefficients
    regressor = pipeline.named_steps['regressor']
    cat_encoder = pipeline.named_steps['preprocessor'].named_transformers_['cat']
    encoded_cat_features = list(cat_encoder.get_feature_names_out(cat_cols))
    all_feature_names = num_cols + encoded_cat_features

    coef_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Coefficient': regressor.coef_
    }).sort_values(by='Coefficient', ascending=False)

    print("\nFeature Coefficients (Impact on Delivery Time in minutes):")
    print("-" * 60)
    for _, row in coef_df.iterrows():
        sign = "+" if row['Coefficient'] >= 0 else ""
        print(f"   {row['Feature']:<35} : {sign}{row['Coefficient']:.3f} min")
    print(f"   {'[Intercept/Baseline Constant]':<35} : {regressor.intercept_:.3f} min")

    metrics = {
        'mae': float(mae),
        'mse': float(mse),
        'rmse': rmse,
        'r2': float(r2_test),
        'r2_train': float(r2_train),
        'n_train': int(len(X_train)),
        'n_test': int(len(X_test))
    }

    return pipeline, metrics, coef_df, float(regressor.intercept_), all_feature_names, X_test, y_test, y_pred


def save_artifacts(pipeline, mlr_metrics, slr_metrics, coef_df, intercept, all_feature_names, df, out_path):
    """
    Save the trained model pipeline, evaluation metrics, and metadata to disk.
    """
    print("\n" + "=" * 70)
    print("STEP 5: SAVING TRAINED MODEL ARTIFACTS")
    print("=" * 70)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Categories dictionary for UI dropdowns
    categories = {
        'Traffic_Level': ['Low', 'Medium', 'High', 'Jam'],
        'Weather': ['Clear', 'Windy', 'Foggy', 'Rainy', 'Stormy'],
        'Time_of_Day': ['Morning', 'Afternoon', 'Evening', 'Night'],
        'Vehicle_Type': ['Motorcycle', 'Scooter', 'Electric Bike', 'Bicycle']
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
            'distance_mean': float(df['Delivery_Distance_km'].mean()),
            'distance_min': float(df['Delivery_Distance_km'].min()),
            'distance_max': float(df['Delivery_Distance_km'].max()),
            'prep_time_mean': float(df['Preparation_Time_min'].mean()),
            'delivery_time_mean': float(df['Delivery_Time_min'].mean())
        }
    }

    joblib.dump(model_bundle, out_path)
    print(f"Model bundle successfully saved to: {out_path}")

    # Self-test the saved bundle
    print("\nVerifying saved model with a test prediction:")
    loaded_bundle = joblib.load(out_path)
    sample_input = pd.DataFrame([{
        'Delivery_Distance_km': 5.5,
        'Preparation_Time_min': 15.0,
        'Partner_Experience_years': 3.0,
        'Traffic_Level': 'Medium',
        'Weather': 'Clear',
        'Time_of_Day': 'Evening',
        'Vehicle_Type': 'Motorcycle'
    }])
    sample_prediction = loaded_bundle['pipeline'].predict(sample_input)[0]
    print(f"Input: 5.5 km, 15 min prep, 3 yrs exp, Med traffic, Clear weather, Evening, Motorcycle")
    print(f"Predicted Delivery Time: {sample_prediction:.1f} minutes")
    print("=" * 70)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'dataset', 'delivery_data.csv')
    model_output_path = os.path.join(base_dir, 'models', 'linear_regression.pkl')

    # 1. Load and clean
    df = load_and_preprocess_data(dataset_path)

    # 2. Simple Linear Regression
    slr_results = train_simple_linear_regression(df)

    # 3. Multiple Linear Regression
    pipeline, mlr_metrics, coef_df, intercept, feature_names, X_test, y_test, y_pred = (
        train_multiple_linear_regression(df)
    )

    # 4. Save model bundle
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
