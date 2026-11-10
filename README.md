# Food Delivery Time Prediction System Using Linear Regression

A complete, beginner-friendly academic Data Science project built using the **Kaggle Food Delivery Time Prediction dataset by denkuznetz**.

---

## 1. Project Overview
In modern food delivery applications, accurately estimating delivery duration is essential for dispatch optimization and customer satisfaction. This project implements a machine learning system using **Linear Regression** (Simple and Multiple) to predict delivery time based on distance, traffic conditions, weather, order preparation time, courier experience, vehicle type, and time of day.

---

## 2. Dataset Information (Kaggle: `denkuznetz`)

The main dataset is stored at:
`dataset/Food_Delivery_Times.csv`

### Dataset Attributes (1,000 Records):

| Column Name | Data Type | Role | Description | Observed Values / Range |
| :--- | :--- | :--- | :--- | :--- |
| `Order_ID` | Integer | Excluded | Unique order identifier | `1` to `1000` |
| `Distance_km` | Float | Feature | Direct delivery distance | `0.59` to `19.99 km` |
| `Weather` | String | Feature | Meteorological condition | `Clear`, `Windy`, `Foggy`, `Rainy`, `Snowy` |
| `Traffic_Level` | String | Feature | Street traffic density | `Low`, `Medium`, `High` |
| `Time_of_Day` | String | Feature | Shift time period | `Morning`, `Afternoon`, `Evening`, `Night` |
| `Vehicle_Type` | String | Feature | Courier vehicle mode | `Bike`, `Scooter`, `Car` |
| `Preparation_Time_min` | Integer | Feature | Cooking and packing time | `5` to `29 minutes` |
| `Courier_Experience_yrs` | Float | Feature | Courier experience in years | `0.0` to `9.0 years` |
| **`Delivery_Time_min`** | **Integer** | **Target** | **Total food delivery time** | **`8` to `153 minutes`** |

### Data Cleaning & Preprocessing Steps:
1. **Identifier Exclusion:** Dropped `Order_ID` from the feature matrix as tracking IDs have no predictive power.
2. **Missing Value Imputation:**
   - `Courier_Experience_yrs` (30 missing): Imputed using the **median** (`5.0 years`).
   - `Weather` (30 missing): Imputed using the **mode** (`Clear`).
   - `Traffic_Level` (30 missing): Imputed using the **mode** (`Medium`).
   - `Time_of_Day` (30 missing): Imputed using the **mode** (`Morning`).
3. **Categorical Encoding:** One-Hot Encoded using Scikit-Learn `ColumnTransformer` with `drop='first'` to prevent multicollinearity (the dummy variable trap).

---

## 3. Technology Stack

- **Python 3**
- **Pandas:** Data loading, missing value imputation, and tabular operations
- **NumPy:** Numerical arrays and mathematical operations
- **Matplotlib & Seaborn:** Visualizations, regression plots, box plots, and correlation heatmaps
- **Scikit-learn:** Simple Linear Regression, Multiple Linear Regression pipeline, and metrics
- **Joblib:** Serializing the complete preprocessor and regression pipeline
- **Streamlit:** Interactive web interface with real-time predictions and charts

---

## 4. Model Training & Evaluation (80/20 Train-Test Split)

Models were evaluated on a holdout test set (200 unseen samples):

| Metric | Simple Linear Regression (`Distance_km` Only) | Multiple Linear Regression (All Available Features) | Plain-English Explanation |
| :--- | :---: | :---: | :--- |
| **Mean Absolute Error (MAE)** | `9.58 minutes` | **`5.90 minutes`** | On average, prediction deviates by less than **5.9 minutes**. |
| **Mean Squared Error (MSE)** | `158.16` | **`77.91`** | Average squared error. |
| **Root Mean Squared Error (RMSE)** | `12.58 minutes` | **`8.83 minutes`** | Standard deviation of prediction errors. |
| **R² Score** | `0.6471 (64.7%)` | **`0.8262 (82.6%)`** | Model accounts for **82.6%** of variance in delivery time. |

### Learned Coefficients Breakdown:
- **Base Intercept ($\beta_0$):** `+17.37 minutes`
- **Distance (`Distance_km`):** `+3.00 min/km` (each km adds ~3 minutes)
- **Preparation Time (`Preparation_Time_min`):** `+0.97 min/min` (direct 1:1 kitchen delay)
- **Courier Experience (`Courier_Experience_yrs`):** `-0.68 min/yr` (experience reduces delivery time)
- **Weather Adjustments:**
  - `Snowy`: `+9.25 min`
  - `Foggy`: `+5.82 min`
  - `Rainy`: `+4.64 min`
  - `Windy`: `+1.45 min`
- **Traffic Adjustments:**
  - `Low`: `-11.13 min` (compared to High traffic)
  - `Medium`: `-5.45 min` (compared to High traffic)

---

## 5. Project Directory Structure

```text
Food-Delivery-Time-Prediction/
│
├── dataset/
│   └── Food_Delivery_Times.csv    # Kaggle dataset (1000 records, 9 columns)
│
├── notebooks/
│   └── analysis.ipynb             # Jupyter Notebook with full EDA & models
│
├── models/
│   └── linear_regression.pkl      # Serialized Scikit-learn pipeline & metrics
│
├── app.py                         # Interactive Streamlit Web Application
├── train_model.py                 # End-to-end data processing & model training script
├── requirements.txt               # Dependencies list
└── README.md                      # Project documentation
```

---

## 6. How to Run the Project Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Models
```bash
python train_model.py
```

### 3. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 7. Sample Prediction Walkthrough

### Inputs:
- **Distance:** `10.5 km`
- **Preparation Time:** `15 minutes`
- **Courier Experience:** `3.0 years`
- **Weather:** `Clear`
- **Traffic Level:** `Medium`
- **Time of Day:** `Evening`
- **Vehicle Type:** `Scooter`

### Output:
```text
Estimated Delivery Time : 56.0 Minutes
Expected Window         : 52 - 61 Minutes
```

---

## 8. Viva & Academic Q&A Preparation

1. **Why exclude Order_ID?**  
   `Order_ID` is an arbitrary sequence number. Including it creates spurious correlations that harm generalization.

2. **Why use Linear Regression?**  
   Food delivery duration is naturally additive: $\text{Total Time} = \text{Prep} + \text{Transit} + \text{Weather Delay} + \text{Traffic Delay}$. Linear Regression provides full coefficient transparency where each factor has a measurable unit impact in minutes.

3. **How does Multiple Linear Regression compare to Simple Linear Regression?**  
   Simple Linear Regression on distance alone achieves $R^2 = 64.7\%$ with an MAE of $9.58\text{ min}$. Multiple Linear Regression increases $R^2$ to **$82.6\%$** and reduces MAE to **$5.90\text{ min}$** by including kitchen preparation, courier experience, traffic, and weather.
