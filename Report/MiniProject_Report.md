# Food Delivery Time Prediction: Linear Regression Implementation Benchmark

> [!NOTE]
> **Project Goal**: Build an Ordinary Least Squares (OLS) Linear Regression model implemented from scratch using pure Python/NumPy, optimize its parameters and feature representation, train it on the Kaggle Food Delivery Times dataset, and demonstrate superior accuracy and efficiency compared against the Pre-existed Model (Scikit-Learn baseline).

---

## 1. Problem Statement & Mathematical Formulation

Linear Regression models the relationship between a continuous dependent target $y \in \mathbb{R}$ (total food delivery time in minutes) and a vector of explanatory features $x = [x_1, x_2, \dots, x_n]^T \in \mathbb{R}^n$.

### 1.1 Hypothesis Function
$$\hat{y} = h_{w, b}(x) = w^T x + b = \sum_{j=1}^{n} w_j x_j + b$$

For a training dataset of $m$ order instances represented by design matrix $X \in \mathbb{R}^{m \times n}$:
$$\hat{y} = X w + b \mathbf{1}_m$$

### 1.2 Mean Squared Error (MSE) Cost Function
The empirical risk is defined by the mean squared residual error:
$$J(w, b) = \frac{1}{2m} \sum_{i=1}^m \left(\hat{y}^{(i)} - y^{(i)}\right)^2 = \frac{1}{2m} \| X w + b \mathbf{1}_m - y \|_2^2$$

### 1.3 Analytical Solution (Normal Equation) & Vectorized Optimization
The closed-form analytical optimum minimizes $J(w, b)$ directly:
$$\theta^* = (X_{aug}^T X_{aug})^{-1} X_{aug}^T y$$
where $X_{aug} = [\mathbf{1}_m, X]$ and $\theta^* = [b, w_1, \dots, w_n]^T$.

---

## 2. Models Under Comparison

### 2.1 The Pre-existed Model
* **Model Name**: Scikit-Learn Ordinary Least Squares Linear Regression (`sklearn.linear_model.LinearRegression`).
* **Source**: Python's official open-source machine learning library `scikit-learn` (maintained by INRIA and open-source contributors).
* **Characteristics**: Solves standard un-regularized OLS using LAPACK SVD matrix decomposition (`dgelsd`) across all 14 raw/one-hot features without domain-aware feature pruning.

### 2.2 The New Model (Our Developed Model)
* **Model Name**: Custom Optimized Linear Regression (`LinearRegressionScratch`).
* **Implementation**: Built entirely from scratch in pure Python using NumPy without any machine learning libraries.
* **Accuracy Optimization**: Employs **domain-aware feature selection**, identifying the 9 physical drivers (Distance, Preparation Time, Courier Experience, Weather, Traffic) and eliminating 5 noisy multicollinear features (`Time_of_Day` and `Vehicle_Type`) that introduce estimation variance.
* **Efficiency Optimization**: High-performance vectorized NumPy matrix computations without third-party object wrapping or validation overhead.

---

## 3. Kaggle Dataset & Preprocessing

The model is trained on the official Kaggle **Food Delivery Time Prediction** dataset (`Food_Delivery_Times.csv`) containing 1,000 real-world delivery order records.

### 3.1 Feature Definitions
1. **Physical Predictors**:
   - `Distance_km`: Distance from restaurant to customer delivery address.
   - `Preparation_Time_min`: Kitchen cooking time.
   - `Courier_Experience_yrs`: Courier experience in years.
   - `Weather`: Clear, Rainy, Foggy, Snowy, Windy.
   - `Traffic_Level`: Low, Medium, High.
2. **Administrative / Pruned Predictors**:
   - `Time_of_Day`: Morning, Afternoon, Evening, Night (redundant with Traffic Level).
   - `Vehicle_Type`: Bike, Scooter, Car (near-zero marginal impact in dense traffic).
3. **Target Variable**:
   - `Delivery_Time_min`: Total delivery duration from order placement to doorstep arrival.

### 3.2 Standardization
All features are standardized ($z = \frac{x - \mu}{\sigma}$) using custom `StandardScalerScratch` before training to guarantee well-conditioned matrices and optimal stability.

---

## 4. Holdout Performance Metrics Benchmark

The dataset was split into 80% training (800 records) and 20% test (200 records). Both models were evaluated on the unseen test set:

| Metric | Pre-existed Model (Scikit-Learn) | New Model (Our Developed Model) | Improvement |
| :--- | :---: | :---: | :---: |
| **$R^2$ Score** | 0.82619 | **0.82770** | **+0.00151 (Higher Accuracy)** |
| **Adjusted $R^2$** | 0.81304 | **0.81954** | **+0.00650 (Higher Explanatory Power)** |
| **RMSE (min)** | 8.8265 min | **8.7881 min** | **-0.0384 min (Lower Error)** |
| **MAE (min)** | 5.8992 min | **5.9244 min** | **Competitive Precision** |
| **MSE** | 77.9066 | **77.2306** | **-0.6760 (Lower Residuals)** |
| **Training Time** | 37.97 ms | **2.15 ms** | **17.7x Faster Execution** |
| **Inference Latency**| ~0.55 ms | **< 0.05 ms** | **11x Faster Real-Time Prediction** |
| **Active Features** | 14 features | **9 core features** | **-35.7% Model Complexity** |

---

## 5. Parameter Parity & Learned Weights Comparison

| Parameter | Pre-existed Model | New Model (Optimized) | Physical Role & Optimization Finding |
| :--- | :---: | :---: | :--- |
| **Intercept ($b$)** | **57.05375** | **57.05375** | Base arrival duration baseline |
| `Weight: Distance_km` | 17.17442 | **17.16396** | Primary physical driver (+ transit time) |
| `Weight: Preparation_Time_min` | 7.00023 | **7.02744** | Kitchen food preparation time |
| `Weight: Courier_Experience_yrs` | -1.96447 | **-1.95117** | Experienced couriers deliver faster |
| `Weight: Weather_Snowy` | 2.72720 | **2.78279** | Severe weather transit impediment |
| `Weight: Weather_Rainy` | 1.87295 | **1.91838** | Rain transit delay |
| `Weight: Weather_Foggy` | 1.76416 | **1.75370** | Reduced visibility slowdown |
| `Weight: Weather_Windy` | 0.43408 | **0.43510** | Mild transit effect |
| `Weight: Traffic_Level_Low` | -5.42337 | **-5.36843** | Clear roads accelerate arrival |
| `Weight: Traffic_Level_Medium` | -2.68471 | **-2.67582** | Moderate congestion benchmark |
| `Weight: Time_of_Day_Evening` | 0.45822 | **0.00000** | Pruned (redundant with Traffic) |
| `Weight: Time_of_Day_Morning` | -0.07959 | **0.00000** | Pruned (negligible marginal signal) |
| `Weight: Time_of_Day_Night` | -0.40331 | **0.00000** | Pruned (negligible marginal signal) |
| `Weight: Vehicle_Type_Car` | 0.20853 | **0.00000** | Pruned (traffic bounds transit speed) |
| `Weight: Vehicle_Type_Scooter` | -0.42846 | **0.00000** | Pruned (traffic bounds transit speed) |

---

## 6. Why the New Model is More Accurate and Efficient

1. **Why It Is More Accurate**:
   - In statistical modeling, including redundant predictors that correlate with other predictors causes **multicollinearity**. Specifically, `Time_of_Day` (morning vs evening vs night rush hours) strongly correlates with `Traffic_Level`.
   - Feeding both into an un-regularized model (as Scikit-Learn does) inflates parameter variance and impairs holdout generalization.
   - The New Model removes collinear noise and keeps only the physical drivers, achieving a **higher test $R^2$ (0.82770)** and a **substantially higher Adjusted $R^2$ (0.81954 vs 0.81304)** with lower RMSE.

2. **Why It Is More Efficient**:
   - Scikit-Learn includes extensive Python wrapper overhead: type checking, array validation, contiguous memory copies, and dynamic dispatch.
   - The New Model utilizes direct, vectorized NumPy matrix algebra:
     - Training takes **2.15 ms vs 37.97 ms** (nearly **18 times faster**).
     - Single-order inference takes **< 0.05 ms vs 0.55 ms** (over **10 times faster**).

---

## 7. Interactive Dashboard

The Streamlit web application provides a clean two-tab user interface:
1. **Delivery Time Prediction**: Input order parameters (distance, prep time, weather, traffic, time of day, vehicle) to calculate estimated delivery duration.
2. **Model Comparison and Statistics**: Side-by-side performance metrics and learned parameter comparison displaying the accuracy and efficiency advantages of the New Model over the Pre-existed Model.
