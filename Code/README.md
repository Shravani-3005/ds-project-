# Food Delivery Time Prediction using Linear Regression from Scratch

A comprehensive Data Science project implementing **Ordinary Least Squares (OLS) Linear Regression from scratch** using pure NumPy, applied to a realistic **Food Delivery Time Prediction** task, with extensive benchmarking and parameter-by-parameter comparison against **Scikit-Learn LinearRegression** and **SGDRegressor**.

---

## Project Overview and Problem Statement

Accurately predicting food delivery time is critical for customer satisfaction, restaurant scheduling, and courier dispatching in platforms like UberEats, DoorDash, Zomato, and Swiggy. 

In this project:
- We formulate delivery time as a continuous regression target dependent on key operational, geographical, and environmental variables.
- We implement **Linear Regression entirely from scratch** without relying on high-level ML libraries for model internals.
- We implement both **Batch Gradient Descent** with loss tracking and convergence checks, and the closed-form **Normal Equation**.
- We compare **all learned parameters** (intercept b and feature weights w_i), training times, convergence behaviors, and predictive performance metrics against Scikit-Learn's production implementation.

---

## Mathematical Formulation

### 1. Hypothesis Function
For a sample with n features x = [x_1, x_2, ..., x_n]^T:
y_hat = h_{w, b}(x) = w^T x + b = w_1 x_1 + w_2 x_2 + ... + w_n x_n + b

In vectorized form over m training samples:
y_hat = X w + b 1

### 2. Cost Function (Mean Squared Error)
J(w, b) = (1 / 2m) * sum_{i=1}^m (y_hat^{(i)} - y^{(i)})^2

### 3. Gradient Descent Optimization
Parameter updates using learning rate alpha:
grad_w = (1 / m) * X^T (y_hat - y)
grad_b = (1 / m) * sum_{i=1}^m (y_hat^{(i)} - y^{(i)})

Update rules at iteration t+1:
w^{(t+1)} = w^{(t)} - alpha * grad_w
b^{(t+1)} = b^{(t)} - alpha * grad_b

### 4. Normal Equation (Closed-form Analytical Solution)
By setting grad J(theta) = 0 with augmented feature matrix X_aug = [1, X]:
theta = (X_aug^T X_aug)^(-1) X_aug^T y
where theta_0 = b and theta_{1:n} = w.

---

## Dataset Description

The dataset `food_delivery_data.csv` contains 1,500 delivery orders with the following features:

| Feature Name | Type | Range / Domain | Description |
| :--- | :--- | :--- | :--- |
| `distance_km` | Float | 1.0 - 18.0 km | Distance from restaurant to customer destination |
| `prep_time_min` | Float | 8.0 - 45.0 min | Time taken by restaurant kitchen to prepare order |
| `traffic_level` | Categorical / Ordinal | 1 (Low) to 4 (Jam) | Real-time traffic congestion score |
| `weather_condition`| Categorical / Ordinal | 0 (Clear) to 3 (Storm) | Weather impact severity factor |
| `delivery_partner_rating` | Float | 3.5 - 5.0 | Courier rating (measure of efficiency and familiarity) |
| `delivery_partner_age` | Integer | 20 - 52 yrs | Courier age |
| `num_items` | Integer | 1 - 7 items | Number of items in order (packaging and handling overhead) |
| **`delivery_time_min`** | **Target** | **12.0 - 95.0 min** | **Total elapsed time from order to doorstep delivery** |

---

## Project Architecture

```
food-delivery-time-prediction/
|
|-- data_generator.py           # Synthetic ground-truth realistic data generator
|-- data_loader.py              # Data pipeline, scaling, and train-test splitting
|-- linear_regression_scratch.py# Pure NumPy Linear Regression, Scaler, and Metrics
|-- compare_models.py           # Benchmark pipeline and parameter comparison
|-- generate_plots.py           # High-resolution diagnostic plots
|-- main.py                     # Project entry point and live prediction demo
|-- food_delivery_data.csv      # Generated food delivery dataset
|-- model_metrics_comparison.csv# Exported performance metrics table
|-- model_parameters_comparison.csv# Exported weights and bias comparison table
|-- benchmark_summary.json      # Structured JSON benchmark results
`-- plots/                      # Diagnostic plots directory
    |-- cost_convergence.png
    |-- actual_vs_predicted.png
    |-- residuals_distribution.png
    |-- coefficients_comparison.png
    `-- learning_rate_comparison.png
```

---

## How to Run

1. Open terminal in the project directory:
   ```bash
   cd food-delivery-time-prediction
   ```

2. Run the end-to-end comparison and demonstration pipeline:
   ```bash
   python main.py
   ```

3. To launch the web dashboard:
   ```bash
   streamlit run dashboard.py
   ```
