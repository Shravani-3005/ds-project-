# Food Delivery Time Prediction System

A complete Data Science machine learning system and interactive Liquid Glass 2.0 web application implementing Linear Regression from scratch and benchmarking against Scikit-Learn on the Kaggle Food Delivery Times dataset.

---

## 1. Project Overview

Predicting doorstep delivery duration is critical for quick-commerce and food delivery platforms. Accurate estimates drive delivery partner dispatch, kitchen order pacing, customer expectations, and route efficiency.

This project implements and benchmarks two distinct linear regression engines:

1. **New Model (Custom Pure NumPy Implementation)**: An end-to-end analytical Ordinary Least Squares regression engine built from scratch using pure NumPy matrix operations (Closed-Form Normal Equation with Moore-Penrose pseudo-inverse fallback), automated convergence detection, custom standard scalers, and domain-aware feature selection.
2. **Pre-existing Model (Scikit-Learn Production Baseline)**: Standard production Ordinary Least Squares linear regression (`sklearn.linear_model.LinearRegression`) utilizing LAPACK SVD matrix decomposition.

---

## 2. Dataset Information

* **Source**: Kaggle Food Delivery Time Prediction Dataset (by `denkuznetz`).
* **File**: `Food_Delivery_Times.csv` (included in root and `Code/`).
* **Records**: 1,000 real-world delivery transactions.
* **Train/Test Split**: 80% Training (800 records), 20% Unseen Holdout Testing (200 records), `random_state=42`.

### Dataset Features:

| Feature Name | Data Type | Role | Description | Value Range |
| :--- | :--- | :--- | :--- | :--- |
| `Distance_km` | Float | Feature | Direct transit distance | 0.59 to 19.99 km |
| `Preparation_Time_min` | Float | Feature | Kitchen cooking & packing duration | 5.0 to 29.0 min |
| `Courier_Experience_yrs` | Float | Feature | Delivery partner tenure | 0.0 to 9.0 years |
| `Weather` | String | Feature | Meteorological condition | Clear, Cloudy, Rainy, Snowy, Foggy, Windy |
| `Traffic_Level` | String | Feature | Road congestion | Low, Medium, High, Traffic Jam |
| `Time_of_Day` | String | Feature | Delivery time slot | Morning, Afternoon, Evening, Night |
| `Vehicle_Type` | String | Feature | Delivery vehicle mode | Bike, Scooter, Car |
| **`Delivery_Time_min`** | **Float** | **Target (y)** | **Total doorstep delivery duration** | **8.0 to 153.0 min** |
| `Order_ID` | Integer | Excluded | Arbitrary database tracking ID | Dropped |

### Preprocessing & Normalization Pipeline:
1. **Identifier Exclusion**: `Order_ID` is removed from the feature matrix as tracking numbers contain zero predictive signals.
2. **Missing Value Imputation**: Median imputation for numerical features; mode imputation for categorical attributes.
3. **Categorical Encoding**: One-Hot Encoding with `drop='first'` to prevent multicollinearity (dummy variable trap).
4. **Standardization**: Custom `StandardScalerScratch` computes $z = \frac{x - \mu}{\sigma}$ so that gradient updates and coefficient interpretations remain scale-invariant.

---

## 3. Mathematical Foundations

### Closed-Form Normal Equation
The optimal weight vector $w^*$ minimizing the sum of squared errors is computed analytically in a single step without requiring learning rate tuning:

$$w^* = (X^T X)^{-1} X^T y$$

When $X^T X$ approaches singularity, the engine uses the Moore-Penrose pseudo-inverse:

$$w^* = X^+ y$$

### Cost Function (Mean Squared Error)
$$J(w, b) = \frac{1}{2m} \sum_{i=1}^{m} \left( \hat{y}^{(i)} - y^{(i)} \right)^2$$

### Evaluation Metrics
* **Root Mean Squared Error (RMSE)**: $\sqrt{\frac{1}{m} \sum (\hat{y} - y)^2}$
* **Mean Absolute Error (MAE)**: $\frac{1}{m} \sum |\hat{y} - y|$
* **Coefficient of Determination ($R^2$)**: $1 - \frac{\sum (\hat{y} - y)^2}{\sum (y - \bar{y})^2}$
* **Adjusted $R^2$**: $1 - \left[ \frac{(1 - R^2)(n - 1)}{n - p - 1} \right]$ where $n$ is sample count and $p$ is feature count.

---

## 4. Holdout Performance Benchmark

Evaluation conducted on the 200 unseen holdout delivery orders:

| Performance Metric | New Model (Custom NumPy) | Pre-existing Model (Scikit-Learn) | Advantage / Delta |
| :--- | :--- | :--- | :--- |
| **R2 Score** | **0.82770** | 0.82619 | **+0.00151 higher accuracy** |
| **Adjusted R2 Score** | **0.81954** | 0.81304 | **+0.00650 higher explanatory power** |
| **Root Mean Squared Error** | **8.7881 min** | 8.8265 min | **-0.0384 min lower error** |
| **Mean Absolute Error** | 5.9244 min | **5.8992 min** | Within 1.5 seconds parity |
| **Mean Squared Error** | **77.2306** | 77.9066 | **-0.6760 lower variance** |
| **Training Speed** | **2.15 ms** | 37.97 ms | **17.7x faster execution** |

---

## 5. Liquid Glass 2.0 Web Application

The frontend is styled using Glassmorphism 2.0 principles:
* **Background Environment**: Pastel ambient gradient mesh (lavender, cyan, icy blue, and soft pink).
* **Floating Glass Master Frame**: 32px rounded translucent card with 30px backdrop blur and specular highlights.
* **Pill Navigation Tabs**:
  1. `Delivery Time Prediction`: Interactive sliders and dropdowns enclosed in 3 frosted glass cards (`Order Dynamics`, `Route Conditions`, `Dispatch & Logistics`).
  2. `Model Comparison & Statistics`: 4 KPI summary cards, holdout metrics benchmark table, parameter parity comparison, and Matplotlib feature weights chart.
* **Prediction Cards**:
  - **New Model Prediction**: Cyan/blue glass card showing custom engine ETA.
  - **Pre-existing Model Prediction**: Lavender/purple glass card showing Scikit-Learn baseline ETA.
  - **Difference (New - Pre-existing)**: Emerald mint glass card displaying model delta and Adjusted $R^2$ advantage.
* **Order Summary Panel**: Translucent scrim plate displaying live input pill chips and total doorstep arrival time.

---

## 6. How to Run This Project on Any System

Follow these step-by-step instructions to run the application on **Windows**, **macOS**, or **Linux**.

### Prerequisites
* **Python**: Version 3.9, 3.10, 3.11, or 3.12 installed.
* Verify Python installation:
  ```bash
  python --version
  ```
  *(On macOS or Linux, use `python3 --version`)*

---

### Step 1: Extract the Project Archive
Unzip `MiniProject_FoodDelivery.zip` into a directory of your choice, for example:
* Windows: `C:\Projects\FoodDelivery\`
* macOS/Linux: `~/Projects/FoodDelivery/`

---

### Step 2: Open Terminal or Command Prompt
* **Windows**: Open **PowerShell** or **Command Prompt** (CMD).
* **macOS**: Open **Terminal**.
* **Linux**: Open your shell terminal.

Navigate into the extracted project directory:
```bash
cd path/to/extracted/project
```

---

### Step 3: Create a Python Virtual Environment
A virtual environment ensures package dependencies do not clash with your system libraries.

* **On Windows**:
  ```powershell
  python -m venv venv
  ```
* **On macOS / Linux**:
  ```bash
  python3 -m venv venv
  ```

---

### Step 4: Activate the Virtual Environment

* **On Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *Note: If PowerShell displays an execution policy restriction, run:*
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\venv\Scripts\Activate.ps1
  ```
* **On Windows (Command Prompt - CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
* **On macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

Once activated, your terminal prompt will display `(venv)`.

---

### Step 5: Install Project Dependencies
Upgrade pip and install all required libraries using `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*Required packages include: `streamlit`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `python-docx`, `python-pptx`.*

---

### Step 6: Launch the Web Dashboard
Start the Streamlit application:

```bash
streamlit run app.py
```
*(Or alternatively: `streamlit run Code/dashboard.py`)*

The terminal will display:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Open your browser and navigate to:
**`http://localhost:8501`**

---

### Step 7: Running the Project via Jupyter Notebooks (.ipynb)

For coursework and academic submissions requiring execution via Jupyter Notebooks or Google Colab, the project provides a modular 3-stage notebook suite inside the `Code/` directory:

1. **`DS_Project_Implementation_from_Scratch.ipynb`**:
   - Implements data ingestion, exploratory data analysis (EDA), missing value handling, one-hot encoding, and feature scaling.
   - Builds the custom Pure NumPy Ordinary Least Squares (OLS) Linear Regression model from first principles (Normal Equation with Moore-Penrose pseudo-inverse fallback).
   - Trains the model, computes evaluation metrics ($R^2$, MAE, MSE, RMSE, latency), plots Actual vs. Predicted values and Residual distributions, and exports metrics to `scratch_lr_results.csv`.

2. **`DS_Project_built_in_linear_regression.ipynb`**:
   - Ingests the same standardized preprocessed dataset.
   - Fits Scikit-learn's production `LinearRegression` model.
   - Evaluates test-set performance, plots regression diagnostics, and exports metrics to `sklearn_lr_results.csv`.

3. **`DS_Project_Linear_SVR_to_compare.ipynb`** (or `DS_Project_Ridge_Regression_to_compare.ipynb`):
   - Trains a regularized comparison model (Support Vector Regression with Linear Kernel / Ridge Regression).
   - Automatically loads `scratch_lr_results.csv` and `sklearn_lr_results.csv` generated by the preceding notebooks.
   - Merges and benchmarks all three models into a unified comparison DataFrame.
   - Generates four side-by-side comparative visualizations:
     - Model Performance Metrics (MAE, MSE, RMSE)
     - Training Time Comparison
     - Prediction Time Comparison
     - $R^2$ Variance Explained Comparison
   - Exports `final_model_comparison.csv` and `regression_comparison.png`.

#### How to Run Locally with Jupyter:
```bash
cd Code
jupyter notebook
```
Then open and execute the notebooks in order: (1) Scratch $\rightarrow$ (2) Built-in $\rightarrow$ (3) Compare.

#### How to Run in Google Colab:
- Open [Google Colab](https://colab.research.google.com).
- Upload the notebook file or open directly from GitHub: `https://github.com/Shravani-3005/ds-project-`.
- The notebooks contain automated fallback dataset loaders that seamlessly fetch `Food_Delivery_Times.csv` from the GitHub raw repository or prompt for upload if running in an isolated Colab container.

---

### Step 8: Optional Command-Line Tools

You can also run the CLI analysis and benchmark scripts directly from your terminal:

* **Run Model Benchmark & Parity Check**:
  ```bash
  python Code/compare_models.py
  ```
* **Run Model Training CLI**:
  ```bash
  python Code/main.py
  ```
* **Re-generate Plots**:
  ```bash
  python Code/generate_plots.py
  ```
* **Re-generate Submission Deliverables (DOCX, PDF, PPTX)**:
  ```bash
  python Code/update_reports.py
  ```

---

## 7. Troubleshooting Common System Issues

### Issue 1: Port 8501 is already in use
If another application is using port 8501, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

### Issue 2: ModuleNotFoundError
Ensure your virtual environment is activated (`(venv)` shown in prompt) and run:
```bash
pip install -r requirements.txt
```

### Issue 3: Browser does not open automatically
Manually open any web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari) and go to:
`http://localhost:8501`

---

## 8. Package Contents & Deliverables

```
.
|-- app.py                              # Root entrypoint for Streamlit
|-- requirements.txt                    # Python library requirements
|-- README.md                           # Complete documentation & run instructions
|-- Food_Delivery_Times.csv             # Kaggle benchmark dataset (1,000 rows)
|-- .streamlit/
|   `-- config.toml                     # Streamlit light-theme configuration
|-- Code/
|   |-- DS_Project_Implementation_from_Scratch.ipynb  # Notebook 1: Custom NumPy OLS model
|   |-- DS_Project_built_in_linear_regression.ipynb   # Notebook 2: Scikit-learn Linear Regression
|   |-- DS_Project_Linear_SVR_to_compare.ipynb        # Notebook 3: Comparison with Linear SVR
|   |-- DS_Project_Ridge_Regression_to_compare.ipynb  # Alternative comparison with Ridge Regression
|   |-- dashboard.py                                  # Streamlit Liquid Glass 2.0 Web Application
|   |-- linear_regression_scratch.py                  # Custom Pure NumPy New Model implementation
|   |-- data_loader.py                                # Dataset preprocessor, scaler & encoder
|   |-- data_generator.py                             # Dataset synthetic augmentation utility
|   |-- compare_models.py                             # Benchmark engine: New vs Pre-existing Model
|   |-- main.py                                       # Standalone training & evaluation pipeline
|   |-- generate_plots.py                             # Matplotlib diagnostic plots generator
|   |-- generate_diagrams.py                          # Architecture & flowchart generator
|   |-- update_reports.py                             # Deliverable document compiler
|   |-- Food_Delivery_Times.csv                       # Benchmark dataset
|   |-- benchmark_summary.json                        # Benchmark metric output
|   |-- scratch_lr_results.csv                        # Notebook 1 exported metrics
|   |-- sklearn_lr_results.csv                        # Notebook 2 exported metrics
|   |-- final_model_comparison.csv                    # Notebook 3 consolidated 3-model benchmark
|   |-- regression_comparison.png                     # Notebook 3 comparative diagnostic plots
|   |-- model_metrics_comparison.csv                  # Metric comparison table
|   |-- model_parameters_comparison.csv               # Parameter parity table
|   `-- plots/                                        # PNG plots & visual diagnostics
`-- Report/
    |-- MiniProject_Report.pdf          # Official PDF Project Report
    |-- MiniProject_Report.docx         # Editable Word Document Report
    |-- MiniProject_Presentation.pptx   # PowerPoint Presentation Deck
    `-- MiniProject_Report.md           # Markdown Technical Report
```
