# Food Delivery Time Prediction System

A production-grade machine learning system and interactive Liquid Glass 2.0 web application built on the Kaggle Food Delivery Time Prediction benchmark dataset (by denkuznetz, 1,000 orders).

---

## 1. Project Overview

Accurately predicting doorstep food delivery duration is critical for logistics scheduling, courier routing, and customer satisfaction. This project implements and benchmarks two distinct linear regression engines:

1. **New Model (Custom Pure NumPy Implementation)**: An end-to-end analytical Ordinary Least Squares regression engine built from scratch using NumPy matrix algebra (Normal Equation with Moore-Penrose pseudo-inverse fallback), automated convergence detection, custom standard scalers, and domain-aware feature selection.
2. **Pre-existing Model (Scikit-Learn Production Baseline)**: Standard production Ordinary Least Squares linear regression (`sklearn.linear_model.LinearRegression`) utilizing LAPACK SVD matrix decomposition.

---

## 2. Dataset Information (Kaggle: denkuznetz)

The benchmark dataset consists of 1,000 verified delivery orders.

### Features:
- `Distance_km`: Delivery transit distance (km).
- `Preparation_Time_min`: Kitchen cooking and packing time (min).
- `Courier_Experience_yrs`: Courier experience (years).
- `Weather`: Meteorological conditions (`Clear`, `Cloudy`, `Rainy`, `Snowy`, `Foggy`, `Windy`).
- `Traffic_Level`: Real-time street congestion (`Low`, `Medium`, `High`, `Traffic Jam`).
- `Time_of_Day`: Delivery slot (`Morning`, `Afternoon`, `Evening`, `Night`).
- `Vehicle_Type`: Transportation mode (`Bike`, `Scooter`, `Car`).
- **Target (`Delivery_Time_min`)**: Total end-to-end doorstep duration (min).

---

## 3. Comparative Benchmark Results

Direct evaluation on 200 unseen holdout delivery orders from the Kaggle dataset:

| Model | Root Mean Squared Error (RMSE) | Mean Absolute Error (MAE) | Mean Squared Error (MSE) | R2 Score | Adjusted R2 Score | Training Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **New Model (Custom NumPy)** | **8.7881 min** | **5.9244 min** | **77.2306** | **0.82770** | **0.81954** | **2.15 ms** |
| **Pre-existing Model (Scikit-Learn)** | 8.8265 min | 5.8992 min | 77.9066 | 0.82619 | 0.81304 | 37.97 ms |
| **Advantage / Delta** | **-0.0384 min lower** | +0.0252 min | **-0.6760 lower** | **+0.00151 higher** | **+0.00650 higher** | **17.7x faster** |

---

## 4. Architecture & Key Innovations

1. **Closed-Form Normal Equation**:
   $$w = (X^T X)^{-1} X^T y$$
   Computes exact global optimal parameter weights analytically in a single pass without iterative gradient tuning hyperparameters.
2. **Domain-Aware Feature Optimization**:
   Eliminates multicollinear noise while focusing weight on physical factors (Transit Distance, Kitchen Prep Time, Courier Experience, Weather, and Traffic).
3. **Liquid Glass 2.0 UI**:
   Rebuilt modern frontend featuring pastel ambient gradients, frosted translucent glass panels with background blur, floating prediction cards, and responsive glass inputs.

---

## 5. Repository Structure

```
.
|-- app.py                        # Root entrypoint for Streamlit Community Cloud
|-- requirements.txt              # Production Python package dependencies
|-- .gitignore                    # Git exclusions
|-- README.md                     # Comprehensive project documentation
|-- Code/                         # Core source code and assets
|   |-- dashboard.py              # Streamlit Liquid Glass 2.0 web application
|   |-- linear_regression_scratch.py  # Pure NumPy New Model implementation
|   |-- data_loader.py            # Dataset preprocessor and scaler
|   |-- data_generator.py         # Synthetic dataset generator utility
|   |-- compare_models.py         # Automated model benchmark script
|   |-- generate_plots.py         # Diagnostic plots generator
|   |-- generate_diagrams.py      # Architectural diagrams generator
|   |-- update_reports.py         # Automated report synchronization script
|   |-- Food_Delivery_Times.csv   # Kaggle benchmark dataset (1,000 orders)
|   |-- benchmark_summary.json    # Machine-readable benchmark outputs
|   |-- model_metrics_comparison.csv
|   |-- model_parameters_comparison.csv
|   |-- .streamlit/config.toml    # Streamlit light-theme configuration
|   `-- plots/                    # Diagnostic PNG plots
`-- Report/                       # Academic submission deliverables
    |-- MiniProject_Report.md     # Markdown technical project report
    |-- MiniProject_Report.docx   # Word formatted report
    |-- MiniProject_Report.pdf    # PDF document
    |-- MiniProject_Presentation.pptx # Slide deck
    `-- diagrams/                 # Architecture & workflow diagrams
```

---

## 6. Local Installation & Execution

### Prerequisites
- Python 3.9 to 3.12
- Git

### Steps:
```bash
# Clone the repository
git clone https://github.com/Shravani-3005/ds-project-.git
cd ds-project-

# Install dependencies
pip install -r requirements.txt

# Run the web dashboard
streamlit run app.py
```

---

## 7. Deployment to Streamlit Community Cloud

1. Fork or push this repository to your GitHub account.
2. Sign in to [share.streamlit.io](https://share.streamlit.io) with GitHub.
3. Click **New app**, select this repository (`Shravani-3005/ds-project-`), branch `main`.
4. Leave Main file path as `app.py`.
5. Click **Deploy**. Your application will be live at `https://<your-subdomain>.streamlit.app` with zero warning screens or passwords.
