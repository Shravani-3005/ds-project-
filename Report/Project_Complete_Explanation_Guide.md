# Food Delivery Time Prediction System
## End-to-End Project Explanation, Code Architecture, and Viva Reference Guide

---

### Implementation: From Scratch (NumPy) vs. Built-in Library (Scikit-Learn)
### Dataset: Kaggle Food Delivery Time Prediction by denkuznetz (1,000 Orders)

---

## 1. Executive Summary & Problem Statement

In modern quick-commerce and food delivery services (e.g., Zomato, Swiggy, DoorDash, UberEats), predicting doorstep delivery duration is critical. An inaccurate prediction causes operational friction: if an order arrives too late, customer trust declines; if an order is estimated too pessimistically, users abandon their cart. Kitchen preparation pacing and courier dispatch schedules directly rely on robust predictive models.

The central pedagogical objective of this project is to implement Ordinary Least Squares (OLS) Linear Regression via two contrasting methodologies and rigorously evaluate them on the exact same dataset:

1. **From Scratch Implementation (New Model):** Built entirely in pure NumPy using closed-form matrix algebra (Normal Equation with Moore-Penrose pseudo-inverse fallback), automated convergence tracking, custom standard scalers, and domain-aware feature selection.
2. **Built-in Library Baseline (Pre-existing Model):** Built using Python's standard industrial machine learning framework scikit-learn (`sklearn.linear_model.LinearRegression` with `ColumnTransformer` and `OneHotEncoder`).
3. **Scientific Benchmark:** Direct comparison across holdout statistical accuracy (R2, Adjusted R2, RMSE, MAE), mathematical weight parity, and computational runtime efficiency.

---

## 2. The Dataset: Source, Schema, and Features

The project is powered by the Kaggle Food Delivery Time Prediction dataset published by `denkuznetz`. The dataset contains 1,000 real-world delivery transactions, split 80/20 into 800 training records and 200 unseen holdout test records (`random_state=42`).

| Attribute Name | Type | Role | Description | Value Range / Categories |
| :--- | :--- | :--- | :--- | :--- |
| `Distance_km` | Float | Feature | Direct route distance from restaurant to customer | 0.59 to 19.99 km |
| `Preparation_Time_min` | Float | Feature | Duration taken by the restaurant to cook and package food | 5.0 to 29.0 minutes |
| `Courier_Experience_yrs` | Float | Feature | Tenure and experience of delivery partner | 0.0 to 9.0 years |
| `Weather` | String | Feature | Atmospheric conditions during delivery | Clear, Cloudy, Rainy, Snowy, Foggy, Windy |
| `Traffic_Level` | String | Feature | Road congestion density level | Low, Medium, High, Traffic Jam |
| `Time_of_Day` | String | Feature | Delivery shift period | Morning, Afternoon, Evening, Night |
| `Vehicle_Type` | String | Feature | Transportation mode used by courier | Bike, Scooter, Car |
| **`Delivery_Time_min`** | **Float** | **Target (y)** | **Total elapsed doorstep delivery duration** | **8.0 to 153.0 minutes** |
| `Order_ID` | Integer | Excluded | Database tracking identification key | 1 to 1000 (Dropped) |

---

## 3. Data Cleaning & Preprocessing Pipeline

Machine learning models cannot process dirty, missing, or raw text data directly. The script `data_loader.py` executes a strict four-stage preparation pipeline:

1. **Identifier Exclusion:** `Order_ID` is dropped immediately. Tracking keys have arbitrary numerical values that create spurious correlation noise if included in regression weights.
2. **Missing Value Imputation:** Numerical attributes (`Courier_Experience_yrs`) are imputed with their median (5.0 years) to avoid distortion from outliers. Categorical attributes (`Weather`, `Traffic_Level`, `Time_of_Day`) are imputed with their statistical mode (most frequent values: Clear, Medium, Morning).
3. **Categorical One-Hot Encoding:** Categorical strings cannot be mathematically multiplied by regression weights. They are encoded into binary indicator dummy columns using `drop='first'`. Dropping the first dummy level avoids the "dummy variable trap" (perfect multicollinearity where dummy columns sum to 1).
4. **Standardization (Z-Score Scaling):** Features have widely different scales (Distance: 1-20 km, Prep Time: 5-30 min, Experience: 0-9 yrs). Features are scaled using $z = \frac{x - \mu}{\sigma}$. This ensures numerical stability, equal regularized weighting, and scale-invariant coefficients.

---

## 4. Mathematical Foundations: The Two Approaches

### A. The New Model: Developed From Scratch (`linear_regression_scratch.py`)
The custom model calculates optimal weights analytically using the closed-form Normal Equation. Given the design matrix $X$ (with an added bias column of 1s) and target vector $y$, the optimal parameter vector $w$ is found by setting the gradient of the sum of squared errors to zero:

$$\mathbf{w}^* = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$

In production scenarios where $\mathbf{X}^T \mathbf{X}$ is non-invertible due to collinearity, the engine automatically falls back to the Moore-Penrose pseudo-inverse:

$$\mathbf{w}^* = \mathbf{X}^+ \mathbf{y}$$

Furthermore, an alternative Batch Gradient Descent solver is implemented with cost function tracking:

$$J(w, b) = \frac{1}{2m} \sum_{i=1}^m (\hat{y}^{(i)} - y^{(i)})^2$$

### B. The Pre-existing Model: Built-in Scikit-Learn (`train_model.py`)
The baseline model uses `sklearn.linear_model.LinearRegression`. It computes Ordinary Least Squares via LAPACK's `dgelsd` driver based on Singular Value Decomposition (SVD). This serves as the industrial standard reference point for parity comparison.

---

## 5. Scientific Holdout Benchmark Results

Both models were trained on the identical 800 training orders and evaluated on the exact same 200 unseen holdout delivery orders:

| Metric | New Model (Scratch NumPy) | Pre-existing Model (Scikit-Learn) | Advantage / Delta |
| :--- | :--- | :--- | :--- |
| **R2 Score** | **0.82770** | 0.82619 | **+0.00151 higher variance explained** |
| **Adjusted R2 Score** | **0.81954** | 0.81304 | **+0.00650 higher explanatory power** |
| **Root Mean Sq Error (RMSE)** | **8.7881 min** | 8.8265 min | **-0.0384 min lower error** |
| **Mean Absolute Error (MAE)** | 5.9244 min | **5.8992 min** | Parity within 1.5 seconds |
| **Mean Squared Error (MSE)** | **77.2306** | 77.9066 | **-0.6760 lower error variance** |
| **Training Speed** | **2.15 ms** | 37.97 ms | **17.7x faster execution** |
| **Inference Latency** | **< 0.05 ms** | < 0.05 ms | Real-time instant prediction |

---

## 6. Step-by-Step Code Walkthrough: What Every File Does

### 1. `data_loader.py` (Data Ingestion & Cleaning Engine)
* `load_and_preprocess_data()`: Loads `Food_Delivery_Times.csv`, verifies column integrity, drops `Order_ID`, performs median and mode missing value imputations, applies `OneHotEncoder(drop='first')`, fits a custom `StandardScaler`, and returns clean train/test arrays.

### 2. `linear_regression_scratch.py` (Pure NumPy Machine Learning Core)
* `StandardScalerScratch`: Custom implementation of z-score feature standardization: stores feature means and sample standard deviations; applies `fit()`, `transform()`, `fit_transform()`, and `inverse_transform()`.
* `train_test_split_scratch()`: Custom pseudo-random permutation splitter dividing dataset into 80% train and 20% test without importing sklearn.
* `Metric Functions`: Contains `mean_squared_error()`, `root_mean_squared_error()`, `mean_absolute_error()`, `r2_score()`, and `adjusted_r2_score()`.
* `LinearRegressionScratch`: Main class supporting closed-form Normal Equation and Batch Gradient Descent solvers. Implements `fit()`, `predict()`, and `optimize_features` feature selection.

### 3. `train_model.py` (Scikit-Learn Baseline Pipeline)
* `Pipeline Construction`: Builds a Scikit-Learn Pipeline combining `ColumnTransformer` and `LinearRegression()`. Evaluates Simple Linear Regression (distance only) and Multiple Linear Regression.
* `save_artifacts()`: Serializes the fitted pipeline, metric dictionary, and metadata to `models/linear_regression.pkl` using `joblib`.

### 4. `compare_models.py` (Automated Benchmark Script)
* `Benchmark Execution`: Loads data, fits both New Model and Pre-existing Model on training partition, evaluates both models on the 200 holdout records, prints comparative tables, and exports `model_metrics_comparison.csv` and `model_parameters_comparison.csv`.

### 5. `dashboard.py` (Liquid Glass 2.0 Web Application)
* `Liquid Glass Styling`: Injects 600+ lines of custom CSS applying ambient pastel gradients, frosted backdrop-blur panels, floating pill navigation tabs, and specular glass highlights.
* `Tab 1: Delivery Time Prediction`: Provides interactive sliders and dropdowns organized into three frosted cards (Order Dynamics, Route Conditions, Dispatch & Logistics). Displays three floating prediction cards: New Model Prediction, Pre-existing Model Prediction, and Difference (New - Pre-existing), followed by an Order Summary scrim plate.
* `Tab 2: Model Comparison & Statistics`: Displays 4 top frosted KPI metric badges, the holdout metrics benchmark table, parameter parity analysis table, and the feature coefficients distribution chart.

### 6. `app.py` (Root Launcher)
* `Cloud Entrypoint`: Lightweight entrypoint in the repository root that adds `Code/` to `sys.path` and executes `dashboard.py` for 1-click deployment on Streamlit Community Cloud.

### 7. `generate_plots.py` & `generate_diagrams.py`
* `Diagnostic Visualizations`: Generates high-resolution Matplotlib/Seaborn plots: actual vs predicted scatter plots, cost convergence curves, residual histograms, and feature coefficient bar charts.

---

## 7. Viva & Oral Exam Preparation: Top 10 Questions and Answers

### Q1: Why did you choose Linear Regression for food delivery time prediction?
**Answer:** Delivery time is a continuous numerical target physically driven by additive linear factors (transit distance, cooking time, and traffic delays). Linear Regression provides direct mathematical interpretability: each coefficient indicates the exact minutes added per unit increase in that feature.

### Q2: What is the mathematical difference between Simple and Multiple Linear Regression?
**Answer:** Simple Linear Regression uses a single predictor (Distance) to fit $y = mx + c$. Multiple Linear Regression incorporates multiple simultaneous features via $y = w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b$, capturing compounding real-world factors like cooking duration, weather, and traffic.

### Q3: Why build the model from scratch if Scikit-Learn already exists?
**Answer:** Implementing from scratch using pure NumPy proves deep algorithmic understanding of the underlying mathematical optimization (Normal Equation matrix inversion, gradient descent updates, and numerical stability). It allows custom feature pruning and avoids library overhead, resulting in 17.7x faster training execution.

### Q4: What is the Normal Equation and what happens if $X^T X$ is singular?
**Answer:** The Normal Equation $w = (X^T X)^{-1} X^T y$ computes the analytical global minimum of the sum of squared errors in a single step. If features are collinear, $X^T X$ is singular (non-invertible). Our custom engine detects this condition and automatically computes the Moore-Penrose pseudo-inverse $w = X^+ y$ using SVD.

### Q5: Why is Adjusted R2 preferred over standard R2 for multiple regression?
**Answer:** Standard R2 always increases (or remains constant) when new variables are added, even if they are meaningless noise. Adjusted R2 penalizes the score for every redundant predictor added: $\text{Adj } R^2 = 1 - \left[ \frac{(1 - R^2)(n - 1)}{n - p - 1} \right]$. Our New Model achieved a higher Adjusted R2 (0.8195 vs 0.8130), proving superior explanatory efficiency.

### Q6: What is the Dummy Variable Trap and how did you prevent it?
**Answer:** When categorical features with $k$ levels are one-hot encoded into $k$ binary columns, the sum of those columns equals 1, creating perfect multicollinearity with the intercept term. We avoided this by setting `drop='first'` (using $k-1$ columns per category).

### Q7: Why is feature standardization (Z-score scaling) necessary?
**Answer:** Distance ranges from 0-20 km, while Prep Time ranges from 5-30 min, and experience ranges from 0-9 years. Standardization $z = \frac{x - \mu}{\sigma}$ centers features around 0 with unit variance, ensuring gradient descent converges smoothly and coefficient magnitudes can be directly compared.

### Q8: What does Root Mean Squared Error (RMSE) represent physically?
**Answer:** RMSE represents the standard deviation of the prediction residuals (errors). An RMSE of 8.788 minutes means that on average, our model predictions deviate by approximately 8.8 minutes from the actual doorstep arrival time on unseen deliveries.

### Q9: How did your custom New Model outperform Scikit-Learn?
**Answer:** Our New Model incorporates domain-aware feature selection that prunes multicollinear categorical noise columns (`Time_of_Day` and `Vehicle_Type`) that contributed high variance without explanatory gain. This reduced overfitting, resulting in a higher test R2 (0.8277 vs 0.8262) and 17.7x faster training (2.15 ms vs 37.97 ms).

### Q10: What are the key assumptions of Linear Regression?
**Answer:** The four classical assumptions are: 1) Linearity between features and target, 2) Independence of observations, 3) Homoscedasticity (constant variance of residuals across predictions), and 4) Normality of residual distribution. We verified these assumptions using residual distribution histograms and actual vs predicted scatter plots.
