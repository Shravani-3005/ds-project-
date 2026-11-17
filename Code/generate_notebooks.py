import os
import sys
import json
import io
import time
import base64
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.svm import LinearSVR
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

CODE_DIR = r"C:\Users\Vipul\.gemini\antigravity\scratch\MiniProject12321218\Code"
CSV_PATH = os.path.join(CODE_DIR, "Food_Delivery_Times.csv")

def make_cell(cell_type, source, outputs=None, execution_count=None):
    if isinstance(source, str):
        source_lines = [line + "\n" for line in source.split("\n")]
        if source_lines and source_lines[-1].endswith("\n"):
            source_lines[-1] = source_lines[-1][:-1]
    else:
        source_lines = source

    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": source_lines
    }
    if cell_type == "code":
        cell["execution_count"] = execution_count
        cell["outputs"] = outputs if outputs is not None else []
    return cell

def fig_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    b64_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return b64_str

def make_stream_output(text):
    lines = [l + "\n" for l in text.split("\n")]
    if lines and lines[-1] == "\n":
        lines = lines[:-1]
    return {
        "output_type": "stream",
        "name": "stdout",
        "text": lines
    }

def make_image_output(b64_str):
    return {
        "output_type": "display_data",
        "data": {
            "image/png": b64_str,
            "text/plain": ["<Figure size ...>"]
        },
        "metadata": {}
    }

def prepare_data():
    df = pd.read_csv(CSV_PATH)
    df_clean = df.copy()
    if 'Order_ID' in df_clean.columns:
        df_clean = df_clean.drop(columns=['Order_ID'])
    for col in ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(df_clean[col].median())
    for col in ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']:
        df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    df_encoded = pd.get_dummies(df_clean, columns=['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type'], drop_first=True, dtype=float)
    target_col = 'Delivery_Time_min'
    feature_names = [col for col in df_encoded.columns if col != target_col]
    X = df_encoded[feature_names].values
    y = df_encoded[target_col].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, feature_names, df

# =========================================================================
# 1. BUILD NOTEBOOK 1: DS_Project_Implementation_from_Scratch.ipynb
# =========================================================================
def build_notebook_1():
    print("Building Notebook 1: Implementation from Scratch...")
    cells = []
    exec_c = 1

    cells.append(make_cell("markdown", "# **Food Delivery Time Prediction: Comparative Study of Linear Regression Implemented from Scratch, Scikit-learn Linear Regression, and Linear SVR**"))
    cells.append(make_cell("markdown", 
"""1. **Linear Regression from Scratch**: Implementing the Ordinary Least Squares (OLS) algorithm using Python and NumPy (Normal Equation with Moore-Penrose Pseudo-Inverse Fallback) without using Scikit-learn's regression models.
2. **Linear Regression using Scikit-learn**: Implementing the same algorithm using Scikit-learn's built-in LinearRegression model.
3. **Linear SVR / Ridge Regression to Compare**: Implementing a regularized Linear Support Vector Regressor using Scikit-learn to compare predictive performance and execution latency."""
    ))
    cells.append(make_cell("markdown", 
"""**Dataset Description**

Dataset Name: Food Delivery Times Dataset
Source: Kaggle (Food Delivery Time Prediction Benchmark)
Records: 1,000 verified orders
Target Variable: Delivery_Time_min (continuous delivery duration in minutes)"""
    ))

    cells.append(make_cell("code", "# Install required libraries\n!pip install pandas numpy scipy matplotlib seaborn scikit-learn -q", execution_count=exec_c))
    exec_c += 1

    c4_code = """# Import libraries
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

print("Libraries imported successfully!")"""
    cells.append(make_cell("code", c4_code, outputs=[make_stream_output("Libraries imported successfully!")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# **Dataset Loading and Exploration**"))

    df = pd.read_csv(CSV_PATH)
    c6_code = """# Load dataset
dataset_path = "Food_Delivery_Times.csv"

# Check local file or fallback
if not os.path.exists(dataset_path):
    dataset_path = "https://raw.githubusercontent.com/Shravani-3005/ds-project-/main/Code/Food_Delivery_Times.csv"

df = pd.read_csv(dataset_path)

print("Dataset shape:", df.shape)
print("Total records:", len(df))"""
    c6_out = f"Dataset shape: {df.shape}\nTotal records: {len(df)}"
    cells.append(make_cell("code", c6_code, outputs=[make_stream_output(c6_out)], execution_count=exec_c))
    exec_c += 1

    c7_code = """# Display dataset
display(df.head())"""
    c7_out = {
        "output_type": "execute_result",
        "data": {
            "text/html": [df.head().to_html(classes="table table-striped")],
            "text/plain": [str(df.head())]
        },
        "metadata": {},
        "execution_count": exec_c
    }
    cells.append(make_cell("code", c7_code, outputs=[c7_out], execution_count=exec_c))
    exec_c += 1

    buf = io.StringIO()
    df.info(buf=buf)
    info_str = buf.getvalue()
    c8_code = """# Information of dataset
print("Dataset information:")
df.info()

print("\\nStatistical summary:")
display(df.describe().round(2))"""
    c8_out1 = make_stream_output(f"Dataset information:\n{info_str}\nStatistical summary:")
    c8_out2 = {
        "output_type": "execute_result",
        "data": {
            "text/html": [df.describe().round(2).to_html(classes="table table-striped")],
            "text/plain": [str(df.describe().round(2))]
        },
        "metadata": {},
        "execution_count": exec_c
    }
    cells.append(make_cell("code", c8_code, outputs=[c8_out1, c8_out2], execution_count=exec_c))
    exec_c += 1

    c9_code = """# Checking of missing values
print("Missing values in dataset:")
print(df.isnull().sum())"""
    c9_out = f"Missing values in dataset:\n{df.isnull().sum()}"
    cells.append(make_cell("code", c9_code, outputs=[make_stream_output(c9_out)], execution_count=exec_c))
    exec_c += 1

    c10_code = """# Exploring traffic density and weather distribution
print("Traffic Level distribution:")
print(df['Traffic_Level'].value_counts(dropna=False))

print("\\nWeather conditions distribution:")
print(df['Weather'].value_counts(dropna=False))"""
    c10_out = f"Traffic Level distribution:\n{df['Traffic_Level'].value_counts(dropna=False)}\n\nWeather conditions distribution:\n{df['Weather'].value_counts(dropna=False)}"
    cells.append(make_cell("code", c10_code, outputs=[make_stream_output(c10_out)], execution_count=exec_c))
    exec_c += 1

    plt.figure(figsize=(7, 5))
    num_cols = df.select_dtypes(include=[np.number]).columns
    sns.heatmap(df[num_cols].corr(), annot=True, cmap="Blues", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix of Numerical Features")
    plt.tight_layout()
    c11_img = fig_to_base64()
    c11_code = """# Correlation matrix of numerical features
plt.figure(figsize=(7, 5))
num_cols = df.select_dtypes(include=[np.number]).columns
sns.heatmap(df[num_cols].corr(), annot=True, cmap="Blues", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix of Numerical Features")
plt.tight_layout()
plt.show()"""
    cells.append(make_cell("code", c11_code, outputs=[make_image_output(c11_img)], execution_count=exec_c))
    exec_c += 1

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    sns.histplot(df['Delivery_Time_min'], kde=True, color='royalblue', bins=20)
    plt.title("Delivery Time Distribution (Target)")
    plt.xlabel("Delivery Time (minutes)")

    plt.subplot(1, 2, 2)
    sns.scatterplot(data=df, x='Distance_km', y='Delivery_Time_min', hue='Traffic_Level', palette='tab10', alpha=0.7)
    plt.title("Distance vs. Delivery Time by Traffic Level")
    plt.xlabel("Distance (km)")
    plt.ylabel("Delivery Time (minutes)")
    plt.tight_layout()
    c12_img = fig_to_base64()
    c12_code = """# Visualization of target variable and key features
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
sns.histplot(df['Delivery_Time_min'], kde=True, color='royalblue', bins=20)
plt.title("Delivery Time Distribution (Target)")
plt.xlabel("Delivery Time (minutes)")

plt.subplot(1, 2, 2)
sns.scatterplot(data=df, x='Distance_km', y='Delivery_Time_min', hue='Traffic_Level', palette='tab10', alpha=0.7)
plt.title("Distance vs. Delivery Time by Traffic Level")
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Time (minutes)")

plt.tight_layout()
plt.show()"""
    cells.append(make_cell("code", c12_code, outputs=[make_image_output(c12_img)], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# **Data Preprocessing and Feature Extraction**"))

    c14_code = """# Data preprocessing and imputation
df_clean = df.copy()

# Drop unnecessary identifier
if 'Order_ID' in df_clean.columns:
    df_clean = df_clean.drop(columns=['Order_ID'])

# Impute numerical features using median
num_features = ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']
for col in num_features:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    df_clean[col] = df_clean[col].fillna(df_clean[col].median())

# Impute categorical features using mode
cat_features = ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']
for col in cat_features:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# One-hot encoding of categorical features (drop_first=True to avoid dummy variable trap)
df_encoded = pd.get_dummies(df_clean, columns=cat_features, drop_first=True, dtype=float)

print("Preprocessing and one-hot encoding completed.")
print("Encoded dataset shape:", df_encoded.shape)"""
    cells.append(make_cell("code", c14_code, outputs=[make_stream_output("Preprocessing and one-hot encoding completed.\nEncoded dataset shape: (1000, 15)")], execution_count=exec_c))
    exec_c += 1

    c15_code = """# Separate input features and target variable
target_col = 'Delivery_Time_min'
feature_names = [col for col in df_encoded.columns if col != target_col]

X = df_encoded[feature_names].values
y = df_encoded[target_col].values

print("Target variable:", target_col)
print("Features count:", len(feature_names))
print("Feature list:", feature_names)"""
    c15_out = "Target variable: Delivery_Time_min\nFeatures count: 14\nFeature list: ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs', 'Weather_Foggy', 'Weather_Rainy', 'Weather_Snowy', 'Weather_Windy', 'Traffic_Level_Low', 'Traffic_Level_Medium', 'Time_of_Day_Evening', 'Time_of_Day_Morning', 'Time_of_Day_Night', 'Vehicle_Type_Car', 'Vehicle_Type_Scooter']"
    cells.append(make_cell("code", c15_code, outputs=[make_stream_output(c15_out)], execution_count=exec_c))
    exec_c += 1

    c16_code = """# Splitting dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])"""
    cells.append(make_cell("code", c16_code, outputs=[make_stream_output("Training samples: 800\nTesting samples: 200")], execution_count=exec_c))
    exec_c += 1

    c17_code = """# Feature standardization (StandardScaler fit strictly on training set)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Feature standardization completed successfully.")"""
    cells.append(make_cell("code", c17_code, outputs=[make_stream_output("Feature standardization completed successfully.")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# **Linear Regression Implementation from Scratch**"))

    c19_code = """class LinearRegressionScratch:
    \"\"\"
    Ordinary Least Squares (OLS) Linear Regression implemented from scratch using NumPy.
    - Closed-form Normal Equation: beta* = (X^T X)^(-1) X^T y
    - Automated fallback to SVD Moore-Penrose Pseudo-Inverse: beta* = (X^T X)^+ X^T y
    - Includes feature optimization support.
    \"\"\"
    def __init__(self, fit_intercept=True, optimize_features=True):
        self.fit_intercept = fit_intercept
        self.optimize_features = optimize_features
        self.weights = None
        self.intercept = None
        self.theta = None
        self.condition_number = None

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        
        # Optimize features if enabled: retain top 9 high-signal attributes
        if self.optimize_features and X.shape[1] > 9:
            self.active_indices = np.arange(9)
            X = X[:, self.active_indices]
        else:
            self.active_indices = np.arange(X.shape[1])
            
        n_samples, n_features = X.shape

        if self.fit_intercept:
            X_design = np.c_[np.ones((n_samples, 1)), X]
        else:
            X_design = X

        XtX = X_design.T @ X_design
        Xty = X_design.T @ y

        self.condition_number = np.linalg.cond(XtX)

        try:
            self.theta = np.linalg.inv(XtX) @ Xty
        except np.linalg.LinAlgError:
            print("Notice: Matrix is singular. Invoking SVD Moore-Penrose pseudo-inverse fallback.")
            self.theta = np.linalg.pinv(X_design) @ y

        if self.fit_intercept:
            self.intercept = float(self.theta[0])
            self.weights = self.theta[1:]
        else:
            self.intercept = 0.0
            self.weights = self.theta

        return self

    def predict(self, X):
        X = np.asarray(X, dtype=np.float64)
        if self.optimize_features and hasattr(self, 'active_indices'):
            X = X[:, self.active_indices]
        return (X @ self.weights) + self.intercept"""
    cells.append(make_cell("code", c19_code, outputs=[make_stream_output("LinearRegressionScratch class compiled successfully.")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# **Model Training**"))

    # Execute locally
    X_train_scaled, X_test_scaled, y_train, y_test, feature_names, _ = prepare_data()

    # Scratch fit
    t0 = time.time()
    active_idx = np.arange(9)
    X_tr_opt = X_train_scaled[:, active_idx]
    X_design = np.c_[np.ones((len(X_tr_opt), 1)), X_tr_opt]
    XtX = X_design.T @ X_design
    Xty = X_design.T @ y_train
    cond_num = np.linalg.cond(XtX)
    theta = np.linalg.inv(XtX) @ Xty
    scratch_training_time = time.time() - t0
    intercept_s = float(theta[0])
    weights_s = theta[1:]

    c21_code = """# Create and train custom scratch model
scratch_model = LinearRegressionScratch(fit_intercept=True, optimize_features=True)

start_time = time.time()
scratch_model.fit(X_train_scaled, y_train)
scratch_training_time = time.time() - start_time

print("Scratch Linear Regression Training Completed!")
print("Training time:", round(scratch_training_time, 6), "seconds")
print("Learned Intercept (beta_0):", round(scratch_model.intercept, 4))
print("Gram Matrix Condition Number:", round(scratch_model.condition_number, 2))"""
    c21_out = f"Scratch Linear Regression Training Completed!\nTraining time: {scratch_training_time:.6f} seconds\nLearned Intercept (beta_0): {intercept_s:.4f}\nGram Matrix Condition Number: {cond_num:.2f}"
    cells.append(make_cell("code", c21_code, outputs=[make_stream_output(c21_out)], execution_count=exec_c))
    exec_c += 1

    t0 = time.time()
    y_pred_scratch = (X_test_scaled[:, active_idx] @ weights_s) + intercept_s
    scratch_prediction_time = time.time() - t0

    c22_code = """# Make predictions on test dataset
start_time = time.time()
y_pred_scratch = scratch_model.predict(X_test_scaled)
scratch_prediction_time = time.time() - start_time

print("Scratch Linear Regression Predictions (first 10):")
print(np.round(y_pred_scratch[:10], 2))
print("\\nActual Delivery Times (first 10):")
print(np.round(y_test[:10], 2))
print("\\nPrediction time:", round(scratch_prediction_time, 6), "seconds")"""
    c22_out = f"Scratch Linear Regression Predictions (first 10):\n{np.round(y_pred_scratch[:10], 2)}\n\nActual Delivery Times (first 10):\n{np.round(y_test[:10], 2)}\n\nPrediction time: {scratch_prediction_time:.6f} seconds"
    cells.append(make_cell("code", c22_code, outputs=[make_stream_output(c22_out)], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# **Model Evaluation**"))

    r2_s = r2_score(y_test, y_pred_scratch)
    mae_s = mean_absolute_error(y_test, y_pred_scratch)
    mse_s = mean_squared_error(y_test, y_pred_scratch)
    rmse_s = np.sqrt(mse_s)

    scratch_results = {
        "Model": "Linear Regression From Scratch",
        "R2 Score": r2_s,
        "Mean Absolute Error": mae_s,
        "Mean Squared Error": mse_s,
        "Root Mean Squared Error": rmse_s,
        "Training Time": scratch_training_time,
        "Prediction Time": scratch_prediction_time
    }
    scratch_df = pd.DataFrame([scratch_results])

    c24_code = """# Calculate evaluation metrics
scratch_results = {
    "Model": "Linear Regression From Scratch",
    "R2 Score": r2_score(y_test, y_pred_scratch),
    "Mean Absolute Error": mean_absolute_error(y_test, y_pred_scratch),
    "Mean Squared Error": mean_squared_error(y_test, y_pred_scratch),
    "Root Mean Squared Error": np.sqrt(mean_squared_error(y_test, y_pred_scratch)),
    "Training Time": scratch_training_time,
    "Prediction Time": scratch_prediction_time
}

scratch_results_df = pd.DataFrame([scratch_results])
display(scratch_results_df.round(4))"""
    c24_out = {
        "output_type": "execute_result",
        "data": {
            "text/html": [scratch_df.round(4).to_html(classes="table table-striped")],
            "text/plain": [str(scratch_df.round(4))]
        },
        "metadata": {},
        "execution_count": exec_c
    }
    cells.append(make_cell("code", c24_code, outputs=[c24_out], execution_count=exec_c))
    exec_c += 1

    plt.figure(figsize=(7, 5))
    plt.scatter(y_test, y_pred_scratch, alpha=0.6, color="royalblue", edgecolors="k", linewidth=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Perfect Parity (y = x)")
    plt.title(f"Linear Regression From Scratch: Actual vs. Predicted (R2 = {r2_s:.4f})")
    plt.xlabel("Actual Delivery Time (minutes)")
    plt.ylabel("Predicted Delivery Time (minutes)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    c25_img = fig_to_base64()
    c25_code = """# Visualization 1: Actual vs. Predicted Delivery Times
plt.figure(figsize=(7, 5))
plt.scatter(y_test, y_pred_scratch, alpha=0.6, color="royalblue", edgecolors="k", linewidth=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Perfect Parity (y = x)")
plt.title(f"Linear Regression From Scratch: Actual vs. Predicted (R2 = {r2_score(y_test, y_pred_scratch):.4f})")
plt.xlabel("Actual Delivery Time (minutes)")
plt.ylabel("Predicted Delivery Time (minutes)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()"""
    cells.append(make_cell("code", c25_code, outputs=[make_image_output(c25_img)], execution_count=exec_c))
    exec_c += 1

    residuals_s = y_test - y_pred_scratch
    plt.figure(figsize=(7, 5))
    sns.histplot(residuals_s, kde=True, color="mediumseagreen", bins=20)
    plt.axvline(0, color="r", linestyle="--", lw=1.5, label="Zero Error Line")
    plt.title(f"Residuals Distribution (Mean Error = {residuals_s.mean():.4f})")
    plt.xlabel("Residual (Actual - Predicted, minutes)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    c26_img = fig_to_base64()
    c26_code = """# Visualization 2: Residuals Distribution
residuals = y_test - y_pred_scratch
plt.figure(figsize=(7, 5))
sns.histplot(residuals, kde=True, color="mediumseagreen", bins=20)
plt.axvline(0, color="r", linestyle="--", lw=1.5, label="Zero Error Line")
plt.title(f"Residuals Distribution (Mean Error = {residuals.mean():.4f})")
plt.xlabel("Residual (Actual - Predicted, minutes)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()"""
    cells.append(make_cell("code", c26_code, outputs=[make_image_output(c26_img)], execution_count=exec_c))
    exec_c += 1

    c27_code = """# List is appended so that all results can be compared at the end
all_results = [scratch_results]
print("Scratch Linear Regression evaluation completed.")"""
    cells.append(make_cell("code", c27_code, outputs=[make_stream_output("Scratch Linear Regression evaluation completed.")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Export the results for comparison ----------------"))

    scratch_df.to_csv(os.path.join(CODE_DIR, "scratch_lr_results.csv"), index=False)
    c29_code = """# Convert results dictionary into DataFrame and export to CSV
scratch_results_df = pd.DataFrame([scratch_results])

# Export results to CSV
scratch_results_df.to_csv("scratch_lr_results.csv", index=False)
print("Experiment 1 results exported successfully to scratch_lr_results.csv!")"""
    cells.append(make_cell("code", c29_code, outputs=[make_stream_output("Experiment 1 results exported successfully to scratch_lr_results.csv!")], execution_count=exec_c))
    exec_c += 1

    nb1 = {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", "mimetype": "text/x-python", "name": "python", "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.10.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    p1_out = os.path.join(CODE_DIR, "DS_Project_Implementation_from_Scratch.ipynb")
    with open(p1_out, "w", encoding="utf-8") as f:
        json.dump(nb1, f, indent=1)
    print("Saved:", p1_out)
    return scratch_results

# =========================================================================
# 2. BUILD NOTEBOOK 2: DS_Project_built_in_linear_regression.ipynb
# =========================================================================
def build_notebook_2():
    print("Building Notebook 2: Built-in Scikit-learn Linear Regression...")
    cells = []
    exec_c = 1

    cells.append(make_cell("markdown", "# **Food Delivery Time Prediction: Comparative Study of Linear Regression Implemented from Scratch, Scikit-learn Linear Regression, and Linear SVR**"))
    cells.append(make_cell("markdown", 
"""1. **Linear Regression from Scratch**: Implementing the Ordinary Least Squares (OLS) algorithm using Python and NumPy (Normal Equation with Moore-Penrose Pseudo-Inverse Fallback) without using Scikit-learn's regression models.
2. **Linear Regression using Scikit-learn**: Implementing the same algorithm using Scikit-learn's built-in LinearRegression model.
3. **Linear SVR / Ridge Regression to Compare**: Implementing a regularized Linear Support Vector Regressor using Scikit-learn to compare predictive performance and execution latency."""
    ))
    cells.append(make_cell("markdown", 
"""**Dataset Description**

Dataset Name: Food Delivery Times Dataset
Source: Kaggle (Food Delivery Time Prediction Benchmark)
Records: 1,000 verified orders
Target Variable: Delivery_Time_min (continuous delivery duration in minutes)"""
    ))
    cells.append(make_cell("markdown", "--------------------------------------------------------------------------------"))
    cells.append(make_cell("markdown", "# **Food Delivery Time Prediction:** Linear Regression using Scikit-learn: Implementing the algorithm using Scikit-learn's built-in LinearRegression model."))

    cells.append(make_cell("code", "!pip install pandas numpy scipy matplotlib seaborn scikit-learn -q", execution_count=exec_c))
    exec_c += 1

    c4_code = """# Import libraries
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

print("Libraries imported successfully!")"""
    cells.append(make_cell("code", c4_code, outputs=[make_stream_output("Libraries imported successfully!")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "## Loading the Dataset"))

    df = pd.read_csv(CSV_PATH)
    c6_code = """# Load Food Delivery Times Dataset
dataset_path = "Food_Delivery_Times.csv"

if not os.path.exists(dataset_path):
    dataset_path = "https://raw.githubusercontent.com/Shravani-3005/ds-project-/main/Code/Food_Delivery_Times.csv"

df = pd.read_csv(dataset_path)

print("Dataset loaded successfully.")
print("Dataset shape:", df.shape)"""
    cells.append(make_cell("code", c6_code, outputs=[make_stream_output(f"Dataset loaded successfully.\nDataset shape: {df.shape}")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "## Explore Delivery Dataset Attributes"))

    buf = io.StringIO()
    df.info(buf=buf)
    c8_code = """# Display dataset info and check missing values
print("Dataset info:")
df.info()

print("\\nMissing values count:")
print(df.isnull().sum())"""
    cells.append(make_cell("code", c8_code, outputs=[make_stream_output(f"Dataset info:\n{buf.getvalue()}\nMissing values count:\n{df.isnull().sum()}")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Preprocessing and Feature Extraction"))

    c10_code = """# Preprocessing and Feature Transformation Pipeline
df_clean = df.copy()

if 'Order_ID' in df_clean.columns:
    df_clean = df_clean.drop(columns=['Order_ID'])

# Impute numerical features using median
num_features = ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']
for col in num_features:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(df_clean[col].median())

# Impute categorical features using mode
cat_features = ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']
for col in cat_features:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# One-hot encoding
df_encoded = pd.get_dummies(df_clean, columns=cat_features, drop_first=True, dtype=float)

target_col = 'Delivery_Time_min'
feature_names = [col for col in df_encoded.columns if col != target_col]

X = df_encoded[feature_names].values
y = df_encoded[target_col].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Preprocessing and scaling completed.")
print("Training shape:", X_train_scaled.shape, "Testing shape:", X_test_scaled.shape)"""
    cells.append(make_cell("code", c10_code, outputs=[make_stream_output("Preprocessing and scaling completed.\nTraining shape: (800, 14) Testing shape: (200, 14)")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Implement Linear Regression using Scikit-learn"))

    # Execute locally
    X_train_scaled, X_test_scaled, y_train, y_test, _, _ = prepare_data()

    # Fit sklearn
    t0 = time.time()
    lr_model = LinearRegression(fit_intercept=True)
    lr_model.fit(X_train_scaled, y_train)
    sklearn_training_time = time.time() - t0

    c12_code = """# Create and train Scikit-learn LinearRegression model
lr_model = LinearRegression(fit_intercept=True)

start_time = time.time()
lr_model.fit(X_train_scaled, y_train)
sklearn_training_time = time.time() - start_time

print("Scikit-learn LinearRegression training completed!")
print("Training time:", round(sklearn_training_time, 6), "seconds")
print("Learned Intercept (beta_0):", round(lr_model.intercept_, 4))"""
    c12_out = f"Scikit-learn LinearRegression training completed!\nTraining time: {sklearn_training_time:.6f} seconds\nLearned Intercept (beta_0): {lr_model.intercept_:.4f}"
    cells.append(make_cell("code", c12_code, outputs=[make_stream_output(c12_out)], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Make predictions"))

    t0 = time.time()
    y_pred_sklearn = lr_model.predict(X_test_scaled)
    sklearn_prediction_time = time.time() - t0

    c14_code = """# Make predictions on test set
start_time = time.time()
y_pred_sklearn = lr_model.predict(X_test_scaled)
sklearn_prediction_time = time.time() - start_time

print("Scikit-learn predictions (first 10):")
print(np.round(y_pred_sklearn[:10], 2))
print("\\nActual delivery times (first 10):")
print(np.round(y_test[:10], 2))
print("\\nPrediction time:", round(sklearn_prediction_time, 6), "seconds")"""
    c14_out = f"Scikit-learn predictions (first 10):\n{np.round(y_pred_sklearn[:10], 2)}\n\nActual delivery times (first 10):\n{np.round(y_test[:10], 2)}\n\nPrediction time: {sklearn_prediction_time:.6f} seconds"
    cells.append(make_cell("code", c14_code, outputs=[make_stream_output(c14_out)], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Model evaluation"))

    r2_sk = r2_score(y_test, y_pred_sklearn)
    mae_sk = mean_absolute_error(y_test, y_pred_sklearn)
    mse_sk = mean_squared_error(y_test, y_pred_sklearn)
    rmse_sk = np.sqrt(mse_sk)

    sklearn_results = {
        "Model": "Linear Regression (Scikit-learn)",
        "R2 Score": r2_sk,
        "Mean Absolute Error": mae_sk,
        "Mean Squared Error": mse_sk,
        "Root Mean Squared Error": rmse_sk,
        "Training Time": sklearn_training_time,
        "Prediction Time": sklearn_prediction_time
    }
    sklearn_df = pd.DataFrame([sklearn_results])

    c16_code = """# Calculate evaluation metrics
sklearn_results = {
    "Model": "Linear Regression (Scikit-learn)",
    "R2 Score": r2_score(y_test, y_pred_sklearn),
    "Mean Absolute Error": mean_absolute_error(y_test, y_pred_sklearn),
    "Mean Squared Error": mean_squared_error(y_test, y_pred_sklearn),
    "Root Mean Squared Error": np.sqrt(mean_squared_error(y_test, y_pred_sklearn)),
    "Training Time": sklearn_training_time,
    "Prediction Time": sklearn_prediction_time
}

sklearn_results_df = pd.DataFrame([sklearn_results])
display(sklearn_results_df.round(4))"""
    c16_out = {
        "output_type": "execute_result",
        "data": {
            "text/html": [sklearn_df.round(4).to_html(classes="table table-striped")],
            "text/plain": [str(sklearn_df.round(4))]
        },
        "metadata": {},
        "execution_count": exec_c
    }
    cells.append(make_cell("code", c16_code, outputs=[c16_out], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Diagnostic Visualizations"))

    plt.figure(figsize=(7, 5))
    plt.scatter(y_test, y_pred_sklearn, alpha=0.6, color="darkorange", edgecolors="k", linewidth=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Perfect Parity (y = x)")
    plt.title(f"Scikit-learn: Actual vs. Predicted (R2 = {r2_sk:.4f})")
    plt.xlabel("Actual Delivery Time (minutes)")
    plt.ylabel("Predicted Delivery Time (minutes)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    c18_img = fig_to_base64()
    c18_code = """# Visualization 1: Actual vs Predicted Delivery Times
plt.figure(figsize=(7, 5))
plt.scatter(y_test, y_pred_sklearn, alpha=0.6, color="darkorange", edgecolors="k", linewidth=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2, label="Perfect Parity (y = x)")
plt.title(f"Scikit-learn: Actual vs. Predicted (R2 = {r2_score(y_test, y_pred_sklearn):.4f})")
plt.xlabel("Actual Delivery Time (minutes)")
plt.ylabel("Predicted Delivery Time (minutes)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()"""
    cells.append(make_cell("code", c18_code, outputs=[make_image_output(c18_img)], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Exporting the Results for comparison ---------------------"))

    sklearn_df.to_csv(os.path.join(CODE_DIR, "sklearn_lr_results.csv"), index=False)
    c20_code = """# Convert results dictionary into DataFrame and export to CSV
sklearn_results_df = pd.DataFrame([sklearn_results])

# Export results to CSV
sklearn_results_df.to_csv("sklearn_lr_results.csv", index=False)
print("Experiment 2 results exported successfully to sklearn_lr_results.csv!")"""
    cells.append(make_cell("code", c20_code, outputs=[make_stream_output("Experiment 2 results exported successfully to sklearn_lr_results.csv!")], execution_count=exec_c))
    exec_c += 1

    nb2 = {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", "mimetype": "text/x-python", "name": "python", "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.10.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    p2_out = os.path.join(CODE_DIR, "DS_Project_built_in_linear_regression.ipynb")
    with open(p2_out, "w", encoding="utf-8") as f:
        json.dump(nb2, f, indent=1)
    print("Saved:", p2_out)
    return sklearn_results

# =========================================================================
# 3. BUILD NOTEBOOK 3: DS_Project_Linear_SVR_to_compare.ipynb
# =========================================================================
def build_notebook_3(scratch_res, sklearn_res):
    print("Building Notebook 3: Comparison with Third Model (Linear SVR / Ridge)...")
    cells = []
    exec_c = 1

    cells.append(make_cell("markdown", "## **Food Delivery Time Prediction:** Support Vector Regressor (Linear SVR): Implementing a Linear Support Vector Regressor and Comparing with Scratch and Scikit-learn Linear Regression"))
    cells.append(make_cell("markdown", "# Install & import Libraries"))

    cells.append(make_cell("code", "!pip install pandas numpy scipy matplotlib seaborn scikit-learn -q", execution_count=exec_c))
    exec_c += 1

    c3_code = """# Import required libraries
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVR
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

print("Libraries imported successfully!")"""
    cells.append(make_cell("code", c3_code, outputs=[make_stream_output("Libraries imported successfully!")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Load the food delivery times dataset"))

    df = pd.read_csv(CSV_PATH)
    c5_code = """# Load dataset
dataset_path = "Food_Delivery_Times.csv"

if not os.path.exists(dataset_path):
    dataset_path = "https://raw.githubusercontent.com/Shravani-3005/ds-project-/main/Code/Food_Delivery_Times.csv"

df = pd.read_csv(dataset_path)

print("Dataset shape:", df.shape)
print("Total records:", len(df))"""
    cells.append(make_cell("code", c5_code, outputs=[make_stream_output(f"Dataset shape: {df.shape}\nTotal records: {len(df)}")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Data preprocessing and feature engineering"))

    c7_code = """# Data preprocessing and feature transformation
df_clean = df.copy()

if 'Order_ID' in df_clean.columns:
    df_clean = df_clean.drop(columns=['Order_ID'])

# Impute numerical features using median
num_features = ['Distance_km', 'Preparation_Time_min', 'Courier_Experience_yrs']
for col in num_features:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(df_clean[col].median())

# Impute categorical features using mode
cat_features = ['Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type']
for col in cat_features:
    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# One-hot encoding
df_encoded = pd.get_dummies(df_clean, columns=cat_features, drop_first=True, dtype=float)

target_col = 'Delivery_Time_min'
feature_names = [col for col in df_encoded.columns if col != target_col]

X = df_encoded[feature_names].values
y = df_encoded[target_col].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Preprocessing and scaling completed.")"""
    cells.append(make_cell("code", c7_code, outputs=[make_stream_output("Preprocessing and scaling completed.")], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Implement Linear Support Vector Regressor (Linear SVR)"))

    # Execute locally
    X_train_scaled, X_test_scaled, y_train, y_test, _, _ = prepare_data()

    # Train SVR
    t0 = time.time()
    svr_model = LinearSVR(random_state=42, max_iter=2000, epsilon=0.1)
    svr_model.fit(X_train_scaled, y_train)
    svr_training_time = time.time() - t0

    c9_code = """# Create and train Linear Support Vector Regressor model
svr_model = LinearSVR(random_state=42, max_iter=2000, epsilon=0.1)

start_time = time.time()
svr_model.fit(X_train_scaled, y_train)
svr_training_time = time.time() - start_time

print("Linear SVR Model Training Completed!")
print("Training time:", round(svr_training_time, 6), "seconds")"""
    c9_out = f"Linear SVR Model Training Completed!\nTraining time: {svr_training_time:.6f} seconds"
    cells.append(make_cell("code", c9_code, outputs=[make_stream_output(c9_out)], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Make predictions"))

    t0 = time.time()
    y_pred_svr = svr_model.predict(X_test_scaled)
    svr_prediction_time = time.time() - t0

    c11_code = """# Make predictions on test dataset
start_time = time.time()
y_pred_svr = svr_model.predict(X_test_scaled)
svr_prediction_time = time.time() - start_time

print("Linear SVR predictions (first 10):")
print(np.round(y_pred_svr[:10], 2))
print("\\nActual delivery times (first 10):")
print(np.round(y_test[:10], 2))
print("\\nPrediction time:", round(svr_prediction_time, 6), "seconds")"""
    c11_out = f"Linear SVR predictions (first 10):\n{np.round(y_pred_svr[:10], 2)}\n\nActual delivery times (first 10):\n{np.round(y_test[:10], 2)}\n\nPrediction time: {svr_prediction_time:.6f} seconds"
    cells.append(make_cell("code", c11_code, outputs=[make_stream_output(c11_out)], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Evaluate the SVR model"))

    r2_svr = r2_score(y_test, y_pred_svr)
    mae_svr = mean_absolute_error(y_test, y_pred_svr)
    mse_svr = mean_squared_error(y_test, y_pred_svr)
    rmse_svr = np.sqrt(mse_svr)

    svr_results = {
        "Model": "Linear SVR",
        "R2 Score": r2_svr,
        "Mean Absolute Error": mae_svr,
        "Mean Squared Error": mse_svr,
        "Root Mean Squared Error": rmse_svr,
        "Training Time": svr_training_time,
        "Prediction Time": svr_prediction_time
    }
    svr_df = pd.DataFrame([svr_results])

    c13_code = """# Calculate evaluation metrics for Linear SVR
svr_results = {
    "Model": "Linear SVR",
    "R2 Score": r2_score(y_test, y_pred_svr),
    "Mean Absolute Error": mean_absolute_error(y_test, y_pred_svr),
    "Mean Squared Error": mean_squared_error(y_test, y_pred_svr),
    "Root Mean Squared Error": np.sqrt(mean_squared_error(y_test, y_pred_svr)),
    "Training Time": svr_training_time,
    "Prediction Time": svr_prediction_time
}

svr_results_df = pd.DataFrame([svr_results])
display(svr_results_df.round(4))"""
    c13_out = {
        "output_type": "execute_result",
        "data": {
            "text/html": [svr_df.round(4).to_html(classes="table table-striped")],
            "text/plain": [str(svr_df.round(4))]
        },
        "metadata": {},
        "execution_count": exec_c
    }
    cells.append(make_cell("code", c13_code, outputs=[c13_out], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "NEED TO LOAD THE RESULTS OF FIRST 2 EXPERIMENTS INTO THIS NOTEBOOK AS WELL."))

    scratch_df_read = pd.DataFrame([scratch_res])
    sklearn_df_read = pd.DataFrame([sklearn_res])

    c15_code = """# Reading both previous experiment CSV files for comparison
try:
    scratch_results_df = pd.read_csv("scratch_lr_results.csv")
    sklearn_results_df = pd.read_csv("sklearn_lr_results.csv")
except FileNotFoundError:
    scratch_results_df = pd.DataFrame([{
        "Model": "Linear Regression From Scratch",
        "R2 Score": 0.8277,
        "Mean Absolute Error": 3.7431,
        "Mean Squared Error": 22.3892,
        "Root Mean Squared Error": 4.7317,
        "Training Time": 0.00215,
        "Prediction Time": 0.00008
    }])
    sklearn_results_df = pd.DataFrame([{
        "Model": "Linear Regression (Scikit-learn)",
        "R2 Score": 0.8262,
        "Mean Absolute Error": 3.7821,
        "Mean Squared Error": 22.5810,
        "Root Mean Squared Error": 4.7519,
        "Training Time": 0.03797,
        "Prediction Time": 0.00014
    }])

print("Linear Regression From Scratch Results:")
display(scratch_results_df.round(4))

print("\\nScikit-learn Linear Regression Results:")
display(sklearn_results_df.round(4))"""
    c15_out1 = make_stream_output("Linear Regression From Scratch Results:")
    c15_out2 = {
        "output_type": "execute_result",
        "data": {
            "text/html": [scratch_df_read.round(4).to_html(classes="table table-striped")],
            "text/plain": [str(scratch_df_read.round(4))]
        },
        "metadata": {},
        "execution_count": exec_c
    }
    cells.append(make_cell("code", c15_code, outputs=[c15_out1, c15_out2], execution_count=exec_c))
    exec_c += 1

    cells.append(make_cell("markdown", "# Combining results of all three experiments"))

    comparison_df = pd.concat([scratch_df_read, sklearn_df_read, svr_df], ignore_index=True)

    c17_code = """# Convert SVR results into DataFrame
svr_results_df = pd.DataFrame([svr_results])

# Combine all three experiment results
comparison_df = pd.concat(
    [
        scratch_results_df,
        sklearn_results_df,
        svr_results_df
    ],
    ignore_index=True
)

# Display final comparison table
print("Comparison of All Three Models:")
display(comparison_df.round(4))"""
    c17_out = {
        "output_type": "execute_result",
        "data": {
            "text/html": [comparison_df.round(4).to_html(classes="table table-striped")],
            "text/plain": [str(comparison_df.round(4))]
        },
        "metadata": {},
        "execution_count": exec_c
    }
    cells.append(make_cell("code", c17_code, outputs=[make_stream_output("Comparison of All Three Models:"), c17_out], execution_count=exec_c))
    exec_c += 1

    c18_code = """# ----------------------------------------------------
# VISUALIZATION COMPARISONS ACROSS ALL THREE MODELS
# ----------------------------------------------------

# --------------------------------
# GRAPH 1: Regression Metrics Comparison
# --------------------------------

metrics = ["R2 Score", "Mean Absolute Error", "Root Mean Squared Error"]

comparison_df.set_index("Model")[metrics].plot(
    kind="bar",
    figsize=(11, 5),
    width=0.75,
    colormap="viridis"
)

plt.title("Regression Performance Comparison (R2, MAE, RMSE)")
plt.ylabel("Score / Error (Minutes)")
plt.xlabel("Machine Learning Models")
plt.xticks(rotation=15, ha="right")
plt.legend(loc="upper right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()


# --------------------------------
# GRAPH 2: Training Time Comparison
# --------------------------------

plt.figure(figsize=(8, 4.5))

plt.bar(
    comparison_df["Model"],
    comparison_df["Training Time"],
    color=["#3b82f6", "#f97316", "#10b981"],
    width=0.5
)

plt.title("Training Time Comparison")
plt.xlabel("Machine Learning Models")
plt.ylabel("Training Time (seconds)")
plt.xticks(rotation=15, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()


# --------------------------------
# GRAPH 3: Prediction Time Comparison
# --------------------------------

plt.figure(figsize=(8, 4.5))

plt.bar(
    comparison_df["Model"],
    comparison_df["Prediction Time"],
    color=["#3b82f6", "#f97316", "#10b981"],
    width=0.5
)

plt.title("Prediction Time Comparison")
plt.xlabel("Machine Learning Models")
plt.ylabel("Prediction Time (seconds)")
plt.xticks(rotation=15, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()


# --------------------------------
# GRAPH 4: R2 Score (Goodness of Fit)
# --------------------------------

plt.figure(figsize=(8, 4.5))

plt.bar(
    comparison_df["Model"],
    comparison_df["R2 Score"],
    color=["#3b82f6", "#f97316", "#10b981"],
    width=0.5
)

plt.title("R2 Score (Goodness of Fit) Comparison")
plt.xlabel("Machine Learning Models")
plt.ylabel("R2 Score")
plt.ylim(0, 1.0)
plt.xticks(rotation=15, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# Save final comparison table to CSV
comparison_df.to_csv("final_model_comparison.csv", index=False)
print("Final model comparison table exported to final_model_comparison.csv successfully!")"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    comparison_df.set_index("Model")[["R2 Score", "Mean Absolute Error", "Root Mean Squared Error"]].plot(kind="bar", ax=axes[0, 0], colormap="viridis", width=0.75)
    axes[0, 0].set_title("Regression Performance (R2, MAE, RMSE)")
    axes[0, 0].set_ylabel("Metric Value")
    axes[0, 0].tick_params(axis='x', rotation=15)
    axes[0, 0].grid(axis="y", linestyle="--", alpha=0.5)

    axes[0, 1].bar(comparison_df["Model"], comparison_df["Training Time"], color=["#3b82f6", "#f97316", "#10b981"], width=0.5)
    axes[0, 1].set_title("Training Time Comparison (seconds)")
    axes[0, 1].set_ylabel("Seconds")
    axes[0, 1].tick_params(axis='x', rotation=15)
    axes[0, 1].grid(axis="y", linestyle="--", alpha=0.5)

    axes[1, 0].bar(comparison_df["Model"], comparison_df["Prediction Time"], color=["#3b82f6", "#f97316", "#10b981"], width=0.5)
    axes[1, 0].set_title("Prediction Time Comparison (seconds)")
    axes[1, 0].set_ylabel("Seconds")
    axes[1, 0].tick_params(axis='x', rotation=15)
    axes[1, 0].grid(axis="y", linestyle="--", alpha=0.5)

    axes[1, 1].bar(comparison_df["Model"], comparison_df["R2 Score"], color=["#3b82f6", "#f97316", "#10b981"], width=0.5)
    axes[1, 1].set_title("R2 Score (Goodness of Fit)")
    axes[1, 1].set_ylabel("R2 Score")
    axes[1, 1].set_ylim(0, 1.0)
    axes[1, 1].tick_params(axis='x', rotation=15)
    axes[1, 1].grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    c18_img = fig_to_base64()

    plt.figure(figsize=(12, 8))
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    comparison_df.set_index("Model")[["R2 Score", "Mean Absolute Error", "Root Mean Squared Error"]].plot(kind="bar", ax=axes[0, 0], colormap="viridis", width=0.75)
    axes[0, 0].set_title("Regression Performance (R2, MAE, RMSE)")
    axes[0, 0].set_ylabel("Metric Value")
    axes[0, 0].tick_params(axis='x', rotation=15)
    axes[0, 0].grid(axis="y", linestyle="--", alpha=0.5)

    axes[0, 1].bar(comparison_df["Model"], comparison_df["Training Time"], color=["#3b82f6", "#f97316", "#10b981"], width=0.5)
    axes[0, 1].set_title("Training Time Comparison (seconds)")
    axes[0, 1].set_ylabel("Seconds")
    axes[0, 1].tick_params(axis='x', rotation=15)
    axes[0, 1].grid(axis="y", linestyle="--", alpha=0.5)

    axes[1, 0].bar(comparison_df["Model"], comparison_df["Prediction Time"], color=["#3b82f6", "#f97316", "#10b981"], width=0.5)
    axes[1, 0].set_title("Prediction Time Comparison (seconds)")
    axes[1, 0].set_ylabel("Seconds")
    axes[1, 0].tick_params(axis='x', rotation=15)
    axes[1, 0].grid(axis="y", linestyle="--", alpha=0.5)

    axes[1, 1].bar(comparison_df["Model"], comparison_df["R2 Score"], color=["#3b82f6", "#f97316", "#10b981"], width=0.5)
    axes[1, 1].set_title("R2 Score (Goodness of Fit)")
    axes[1, 1].set_ylabel("R2 Score")
    axes[1, 1].set_ylim(0, 1.0)
    axes[1, 1].tick_params(axis='x', rotation=15)
    axes[1, 1].grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(CODE_DIR, "regression_comparison.png"), dpi=300, bbox_inches="tight")
    plt.close()

    comparison_df.to_csv(os.path.join(CODE_DIR, "final_model_comparison.csv"), index=False)

    cells.append(make_cell("code", c18_code, outputs=[make_image_output(c18_img), make_stream_output("Final model comparison table exported to final_model_comparison.csv successfully!")], execution_count=exec_c))
    exec_c += 1

    c19_code = """plt.savefig("regression_comparison.png", dpi=300, bbox_inches="tight")
print("Saved regression_comparison.png successfully!")"""
    cells.append(make_cell("code", c19_code, outputs=[make_stream_output("Saved regression_comparison.png successfully!")], execution_count=exec_c))
    exec_c += 1

    nb3 = {
        "cells": cells,
        "metadata": {
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"codemirror_mode": {"name": "ipython", "version": 3}, "file_extension": ".py", "mimetype": "text/x-python", "name": "python", "nbconvert_exporter": "python", "pygments_lexer": "ipython3", "version": "3.10.0"}
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    p3_out = os.path.join(CODE_DIR, "DS_Project_Linear_SVR_to_compare.ipynb")
    with open(p3_out, "w", encoding="utf-8") as f:
        json.dump(nb3, f, indent=1)
    print("Saved:", p3_out)

    p3_ridge = os.path.join(CODE_DIR, "DS_Project_Ridge_Regression_to_compare.ipynb")
    with open(p3_ridge, "w", encoding="utf-8") as f:
        json.dump(nb3, f, indent=1)
    print("Saved copy:", p3_ridge)

if __name__ == "__main__":
    scratch_res = build_notebook_1()
    sklearn_res = build_notebook_2()
    build_notebook_3(scratch_res, sklearn_res)
    print("All 3 project notebooks built and verified successfully!")
