# Food Delivery Time Prediction System Using Linear Regression

A complete, beginner-friendly academic Data Science project demonstrating how **Linear Regression** can predict food delivery duration based on operational and environmental factors.

---

## 1. Project Overview & Introduction
On-demand food delivery platforms (such as Zomato, Swiggy, Uber Eats, and DoorDash) rely heavily on precise Expected Time of Arrival (ETA) predictions. Accurate delivery time estimation builds customer trust, streamlines kitchen order dispatching, and allows delivery executives to navigate routes efficiently.

This project implements a complete, end-to-end Machine Learning pipeline using **Linear Regression** to predict total food delivery time (in minutes) based on distance, traffic conditions, weather, kitchen preparation time, delivery courier experience, vehicle mode, and time of day.

---

## 2. Problem Statement
Given dynamic delivery variables including physical road distance, kitchen cooking delays, weather hindrances, and urban traffic congestion, predict the total delivery time (in minutes) that a customer will wait from order placement to delivery at their doorstep.

---

## 3. Project Objectives
1. **Analyze Key Delivery Drivers:** Quantify how distance, traffic density, and weather conditions prolong food delivery times.
2. **Apply Linear Regression:** Implement both **Simple Linear Regression** (Distance $\to$ Time) and **Multiple Linear Regression** (All factors $\to$ Time) to highlight the educational transition from single to multiple predictors.
3. **Evaluate with Standard Metrics:** Calculate and clearly explain MAE, MSE, RMSE, and $R^2$ Score.
4. **Interactive Prediction Interface:** Provide an intuitive, modern Streamlit web application for real-time delivery time forecasting with input validation and mathematical explanations.

---

## 4. Technology Stack

This project strictly adheres to core, lightweight Data Science libraries:

| Technology | Purpose |
| :--- | :--- |
| **Python 3** | Primary programming language |
| **Pandas** | Tabular data manipulation, cleaning, and preprocessing |
| **NumPy** | High-performance numerical and vector operations |
| **Matplotlib** | Foundational data visualization and plot rendering |
| **Seaborn** | Statistical graphics, distribution plots, and correlation heatmaps |
| **Scikit-learn** | Machine learning preprocessing, Linear Regression, and evaluation |
| **Streamlit** | Interactive, browser-based user interface |
| **Jupyter Notebook** | Step-by-step exploratory analysis, documentation, and experimentation |
| **Joblib** | Serialization and loading of the trained model pipeline |

*No complex frameworks, databases, or cloud APIs are required. Everything runs locally on your computer.*

---

## 5. Dataset Description

The dataset is stored locally at `dataset/delivery_data.csv` and contains 1,500+ records with the following features:

| Column Name | Data Type | Description | Values / Range |
| :--- | :--- | :--- | :--- |
| `Delivery_Distance_km` | Numerical (`float64`) | Direct road distance between restaurant and customer | $1.0\text{ to }18.0\text{ km}$ |
| `Preparation_Time_min` | Numerical (`float64`) | Time taken by kitchen staff to prepare and pack food | $8.0\text{ to }40.0\text{ minutes}$ |
| `Partner_Experience_years` | Numerical (`float64`) | Years of experience of the delivery partner | $0.2\text{ to }8.0\text{ years}$ |
| `Traffic_Level` | Categorical (`str`) | Real-time traffic density along the route | `Low`, `Medium`, `High`, `Jam` |
| `Weather` | Categorical (`str`) | Weather condition during transit | `Clear`, `Windy`, `Foggy`, `Rainy`, `Stormy` |
| `Time_of_Day` | Categorical (`str`) | Period of the order placement | `Morning`, `Afternoon`, `Evening`, `Night` |
| `Vehicle_Type` | Categorical (`str`) | Vehicle used by courier | `Motorcycle`, `Scooter`, `Electric Bike`, `Bicycle` |
| **`Delivery_Time_min`** | **Numerical (`float64`)** | **Target variable: Total delivery time** | **$12.0\text{ to }84.0\text{ minutes}$** |

### Data Preprocessing Performed:
- **Duplicate Removal:** Automatically detects and removes redundant records.
- **Missing Value Imputation:**
  - `Partner_Experience_years`: Imputed using the **median** (robust against outliers).
  - `Weather`: Imputed using the **mode** (most frequent categorical observation).
- **Categorical Encoding:** One-Hot Encoding (`OneHotEncoder(drop='first')`) avoids the dummy variable trap while preserving interpretability.

---

## 6. Understanding Linear Regression

### A. Simple Linear Regression
Simple Linear Regression models the relationship between a single independent variable ($X$, Distance) and the dependent variable ($Y$, Delivery Time):

$$Y = mX + c$$

- **$m$ (Slope):** Represents the additional minutes per kilometer of distance ($\approx +2.21\text{ min/km}$).
- **$c$ (Intercept):** Represents the baseline delivery time when distance is zero ($\approx 29.03\text{ min}$).
- **Limitation:** Achieves an $R^2$ of only **~28.5%** because distance alone cannot account for kitchen preparation delays or traffic jams.

### B. Multiple Linear Regression (Primary Model)
Multiple Linear Regression extends the formulation to $p$ independent variables:

$$Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_p X_p + \epsilon$$

Where:
- $Y$ = Total Delivery Time (minutes)
- $\beta_0$ = Base intercept
- $\beta_1, \beta_2, \dots, \beta_p$ = Coefficients for distance, prep time, experience, traffic dummies, weather dummies, etc.
- $\epsilon$ = Random error term

By including all factors, the model achieves an $R^2$ of **~93.8%** and cuts prediction errors down to **~2.2 minutes**.

---

## 7. Project Directory Structure

```text
Food-Delivery-Time-Prediction/
│
├── dataset/
│   └── delivery_data.csv          # Local dataset file
│
├── notebooks/
│   └── analysis.ipynb             # Jupyter Notebook with full EDA & models
│
├── models/
│   └── linear_regression.pkl      # Serialized Scikit-learn pipeline & metrics
│
├── app.py                         # Interactive Streamlit Web Application
├── train_model.py                 # Automated training and evaluation script
├── requirements.txt               # Dependencies list
└── README.md                      # Project documentation
```

---

## 8. Installation & Setup Instructions

### Prerequisites
Make sure you have **Python 3.9+** installed on your system.

### Step 1: Open Terminal / PowerShell
Navigate to the project root directory:
```bash
cd Food-Delivery-Time-Prediction
```

### Step 2: Install Required Libraries
Install all required packages with pip:
```bash
pip install -r requirements.txt
```

---

## 9. How to Train the Model

To run the complete data preprocessing, train both Simple and Multiple Linear Regression models, evaluate performance, and generate `models/linear_regression.pkl`, run:

```bash
python train_model.py
```

### Expected Training Terminal Output:
```text
======================================================================
STEP 1: LOADING AND INSPECTING DATASET
======================================================================
Dataset loaded successfully with 1510 rows and 8 columns.

======================================================================
STEP 2: DATA CLEANING & PREPROCESSING
======================================================================
-> Removed 10 duplicate records.
-> Imputed missing 'Partner_Experience_years' with median (1.4 years).
-> Imputed missing 'Weather' with mode ('Clear').
-> Cleaned dataset contains 1500 rows.

======================================================================
STEP 3: SIMPLE LINEAR REGRESSION (Baseline Model)
======================================================================
Simple Linear Regression Formula:
   Delivery_Time = (2.21 * Delivery_Distance_km) + 29.03

Performance Metrics (Distance only):
   - Mean Absolute Error (MAE) : 7.78 minutes
   - Root Mean Sq. Error (RMSE): 9.68 minutes
   - R-squared (R2) Score      : 0.2853 (28.5% variance explained)

======================================================================
STEP 4: MULTIPLE LINEAR REGRESSION (Primary Model)
======================================================================
Training set: 1200 samples | Testing set: 300 samples

Multiple Linear Regression Performance:
   - Mean Absolute Error (MAE) : 2.24 minutes
   - Mean Squared Error (MSE)  : 8.19
   - Root Mean Sq. Error (RMSE): 2.86 minutes
   - Test R2 Score             : 0.9375 (93.8%)
   - Train R2 Score            : 0.9439 (94.4%)

======================================================================
STEP 5: SAVING TRAINED MODEL ARTIFACTS
======================================================================
Model bundle successfully saved to: models/linear_regression.pkl
```

---

## 10. How to Run the Streamlit Application

Launch the interactive web application with:

```bash
streamlit run app.py
```

Streamlit will open the application in your default web browser at:
`http://localhost:8501`

### Application Sections:
1. **⏱️ Predict Delivery Time:** Input delivery parameters and receive instantaneous ETA predictions with an arrival interval and coefficient breakdown.
2. **📈 Model Performance & Metrics:** View live evaluation metrics (MAE, MSE, RMSE, $R^2$), a comparative study against Simple Linear Regression, and feature impact charts.
3. **📊 Exploratory Data Analysis (EDA):** Interactive tabs showcasing regression trendlines, box plots for traffic and vehicle types, weather impact bar charts, and a Pearson correlation heatmap.
4. **📖 About Project & Viva Q&A:** Academic documentation, formulas, workflow diagrams, and common viva questions with answers.

---

## 11. Model Evaluation Metrics

| Metric | Formula | Value (Test Set) | Simple Explanation |
| :--- | :--- | :--- | :--- |
| **MAE** (Mean Absolute Error) | $\frac{1}{n}\sum \|y_i - \hat{y}_i\|$ | **2.24 minutes** | On average, predictions deviate by just ~2 minutes and 14 seconds from actual delivery time. |
| **MSE** (Mean Squared Error) | $\frac{1}{n}\sum (y_i - \hat{y}_i)^2$ | **8.19** | Average squared difference; penalizes larger errors more heavily. |
| **RMSE** (Root Mean Squared Error) | $\sqrt{\text{MSE}}$ | **2.86 minutes** | Standard deviation of prediction residuals in minutes. Confirms minimal large outliers. |
| **$R^2$ Score** (Coefficient of Determination) | $1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ | **0.9375 (93.8%)** | Explains **93.8%** of the variance in delivery duration from the input features. |

---

## 12. Sample Prediction Walkthrough

### Sample Input:
- **Delivery Distance:** `5.5 km`
- **Kitchen Prep Time:** `15.0 minutes`
- **Delivery Partner Experience:** `3.0 years`
- **Traffic Condition:** `Medium`
- **Weather Condition:** `Clear`
- **Vehicle Type:** `Motorcycle`
- **Time of Day:** `Evening`

### Model Output:
```text
Estimated Delivery Time : 32.6 Minutes
Expected Window         : 29 - 36 Minutes
```

### Mathematical Breakdown:
- **Base Intercept:** `+19.66 min`
- **Distance Impact (5.5 km × +2.16):** `+11.88 min`
- **Kitchen Prep Time:** `+15.00 min`
- **Traffic Level (Medium):** `-5.75 min` (relative to high/jam reference level)
- **Vehicle (Motorcycle):** `-8.64 min` (faster than bicycle baseline)
- **Time of Day (Evening Rush):** `+2.75 min`
- **Partner Experience (3.0 yrs × -0.77):** `-2.31 min`
- **Net Predicted Time:** $\mathbf{\approx 32.6\text{ minutes}}$

---

## 13. Academic Viva & Interview Preparation

1. **Why Linear Regression instead of Random Forest or Deep Learning?**
   - *Answer:* Food delivery time is fundamentally an **additive physical process** ($Delivery = Prep + Transit + Traffic + Weather$). Linear Regression provides complete transparency and mathematical interpretability where each coefficient directly translates into added or saved minutes.
2. **What does the $R^2$ score indicate?**
   - *Answer:* $R^2$ measures how well independent variables explain the variance of the target variable. An $R^2$ of 0.938 indicates 93.8% of the variability in delivery times is accounted for by the model.
3. **Why is RMSE usually slightly larger than MAE?**
   - *Answer:* Because RMSE squares errors before averaging, it gives proportionally higher weight to larger errors. When RMSE is close to MAE (2.86 vs 2.24), it shows that large outlier errors are infrequent.
4. **How are categorical features handled?**
   - *Answer:* Through **One-Hot Encoding** with `drop='first'` inside a Scikit-learn `ColumnTransformer`. This converts $k$ categories into $k-1$ binary features to prevent multicollinearity (the dummy variable trap).

---

## 14. License & Academic Attribution
Developed as an educational Data Science demonstration project. Free to use for coursework, viva presentations, laboratory demonstrations, and learning.
