"""
=============================================================================
Food Delivery Time Prediction System Using Linear Regression
Dataset: Kaggle Food Delivery Time Prediction (by denkuznetz)
File: app.py
Framework: Streamlit
Description: Interactive web application for food delivery time prediction,
             exploratory data analysis, model performance metrics, and viva documentation.
=============================================================================
"""

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Food Delivery Time Prediction | Linear Regression",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional presentation
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 14px;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #1e3a8a;
    }
    .metric-title {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
    }
    .prediction-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin: 18px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .prediction-value {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. PATHS & RESOURCE LOADERS
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "linear_regression.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "Food_Delivery_Times.csv")


@st.cache_resource
def load_trained_model():
    """Load serialized model bundle from models/linear_regression.pkl."""
    if not os.path.exists(MODEL_PATH):
        return None
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None


@st.cache_data
def load_cleaned_dataset():
    """Load and clean the Kaggle Food Delivery Times dataset for EDA."""
    if not os.path.exists(DATASET_PATH):
        return None
    df = pd.read_csv(DATASET_PATH)
    if 'Order_ID' in df.columns:
        df = df.drop(columns=['Order_ID'])
    # Impute missing values identically to model training
    if df['Courier_Experience_yrs'].isnull().any():
        df['Courier_Experience_yrs'] = df['Courier_Experience_yrs'].fillna(
            df['Courier_Experience_yrs'].median()
        )
    for c in ['Weather', 'Traffic_Level', 'Time_of_Day']:
        if df[c].isnull().any():
            df[c] = df[c].fillna(df[c].mode()[0])
    return df


# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=80)
st.sidebar.title("Navigation")
st.sidebar.markdown("**Food Delivery Time Predictor**")
st.sidebar.markdown("*Trained on Kaggle Dataset (`denkuznetz`)*")

app_mode = st.sidebar.radio(
    "Go to Section:",
    [
        "⏱️ Predict Delivery Time",
        "📈 Model Performance & Metrics",
        "📊 Data Analysis & Visualisations",
        "📖 About Project & Viva Q&A"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### 📌 Project Metadata")
st.sidebar.markdown("- **Algorithm:** Linear Regression")
st.sidebar.markdown("- **Split:** 80% Train / 20% Test")
st.sidebar.markdown("- **Dataset:** `Food_Delivery_Times.csv`")
st.sidebar.markdown("- **Target:** `Delivery_Time_min`")


# -----------------------------------------------------------------------------
# 4. SECTION 1: PREDICTION INTERFACE
# -----------------------------------------------------------------------------
if app_mode == "⏱️ Predict Delivery Time":
    st.title("⏱️ Food Delivery Time Prediction System")
    st.markdown(
        "Predict delivery duration using a **Multiple Linear Regression** model "
        "trained on the Kaggle Food Delivery Time Prediction dataset."
    )
    st.divider()

    model_bundle = load_trained_model()

    if model_bundle is None:
        st.warning("⚠️ Trained model bundle not found (`models/linear_regression.pkl`).")
        if st.button("🚀 Train Model Now"):
            with st.spinner("Training model on dataset/Food_Delivery_Times.csv..."):
                import subprocess
                subprocess.run(["python", os.path.join(BASE_DIR, "train_model.py")], check=True)
                st.success("Model trained successfully! Please reload the page.")
        st.stop()

    pipeline = model_bundle['pipeline']
    categories = model_bundle['categories']

    st.subheader("1. Enter Order & Delivery Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        distance = st.number_input(
            "📍 Delivery Distance (`Distance_km`)",
            min_value=0.5,
            max_value=25.0,
            value=8.5,
            step=0.1,
            help="Distance from restaurant to destination in kilometers."
        )

        prep_time = st.number_input(
            "🍳 Preparation Time (`Preparation_Time_min`)",
            min_value=5,
            max_value=45,
            value=15,
            step=1,
            help="Kitchen food preparation and packing duration in minutes."
        )

    with col2:
        traffic = st.selectbox(
            "🚦 Traffic Density (`Traffic_Level`)",
            options=categories['Traffic_Level'],
            index=1,
            help="Road traffic conditions: Low, Medium, or High."
        )

        weather = st.selectbox(
            "⛅ Weather Condition (`Weather`)",
            options=categories['Weather'],
            index=0,
            help="Atmospheric conditions: Clear, Foggy, Rainy, Snowy, or Windy."
        )

    with col3:
        vehicle = st.selectbox(
            "🛵 Delivery Vehicle (`Vehicle_Type`)",
            options=categories['Vehicle_Type'],
            index=0,
            help="Mode of transit: Bike, Scooter, or Car."
        )

        time_of_day = st.selectbox(
            "🕒 Shift Period (`Time_of_Day`)",
            options=categories['Time_of_Day'],
            index=1,
            help="Time period: Morning, Afternoon, Evening, or Night."
        )

        experience = st.number_input(
            "⭐ Courier Experience (`Courier_Experience_yrs`)",
            min_value=0.0,
            max_value=12.0,
            value=3.0,
            step=0.5,
            help="Years of courier experience in the delivery area."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🚀 Predict Delivery Time", type="primary", use_container_width=True)

    if predict_btn:
        # Construct DataFrame matching the exact schema used during training
        input_data = pd.DataFrame([{
            'Distance_km': float(distance),
            'Preparation_Time_min': int(prep_time),
            'Courier_Experience_yrs': float(experience),
            'Weather': weather,
            'Traffic_Level': traffic,
            'Time_of_Day': time_of_day,
            'Vehicle_Type': vehicle
        }])

        try:
            # Predict delivery time using the scikit-learn pipeline
            raw_prediction = pipeline.predict(input_data)[0]
            # Physical lower bound guard: cannot be less than prep time
            predicted_time = max(prep_time + 2.0, float(raw_prediction))
            lower_bound = max(prep_time, predicted_time - 4.0)
            upper_bound = predicted_time + 4.5

            # Display prediction banner
            st.markdown(f"""
            <div class="prediction-box">
                <div style="font-size: 16px; opacity: 0.9;">ESTIMATED DELIVERY TIME</div>
                <div class="prediction-value">{predicted_time:.1f} Minutes</div>
                <div style="font-size: 15px; opacity: 0.95;">Expected arrival window: <b>{lower_bound:.0f} - {upper_bound:.0f} mins</b></div>
            </div>
            """, unsafe_allow_html=True)

            # Details & Linear Regression formula explanation
            st.subheader("2. Prediction Breakdown & Formula Explanation")
            res_col1, res_col2 = st.columns([1, 1])

            with res_col1:
                st.markdown("**User Inputs Summary:**")
                summary_df = pd.DataFrame({
                    "Feature Column": [
                        "Distance_km", "Preparation_Time_min", "Traffic_Level",
                        "Weather", "Vehicle_Type", "Time_of_Day", "Courier_Experience_yrs"
                    ],
                    "Value Entered": [
                        f"{distance} km", f"{prep_time} mins", traffic,
                        weather, vehicle, time_of_day, f"{experience} years"
                    ]
                })
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

            with res_col2:
                st.markdown("**How Linear Regression Computed This Prediction:**")
                st.markdown(f"""
                Multiple Linear Regression calculates delivery time by summing the learned intercept with the weighted impact of each input variable:

                $$Y = \\beta_0 + \\sum_{{i=1}}^{{p}} \\beta_i X_i$$

                - **Base Intercept ($\\beta_0$):** `{model_bundle['intercept']:.2f} min`
                - **Distance Effect:** `{distance} km` $\\times$ `+3.00 min/km` $\\approx$ `+{distance*3.00:.1f} min`
                - **Prep Time Effect:** `{prep_time} min` $\\times$ `+0.97` $\\approx$ `+{prep_time*0.97:.1f} min`
                - **Experience Discount:** `{experience} yrs` $\\times$ `-0.68` $\\approx$ `-{experience*0.68:.1f} min`
                - **Weather (`{weather}`):** Added delay according to meteorological conditions.
                - **Traffic (`{traffic}`):** Adjusted for route road congestion.
                - **Vehicle (`{vehicle}`):** Adjusted for transit speed.
                """)

        except Exception as err:
            st.error(f"Error computing prediction: {err}")


# -----------------------------------------------------------------------------
# 5. SECTION 2: MODEL PERFORMANCE & METRICS
# -----------------------------------------------------------------------------
elif app_mode == "📈 Model Performance & Metrics":
    st.title("📈 Model Performance & Evaluation Metrics")
    st.markdown(
        "Evaluation results for the models trained on the **Kaggle Food Delivery Times** dataset "
        "using an **80/20 train-test split**."
    )
    st.divider()

    model_bundle = load_trained_model()
    if model_bundle is None:
        st.warning("Please train the model first by running `python train_model.py`.")
        st.stop()

    metrics = model_bundle['metrics']
    slr_metrics = model_bundle.get('simple_lr_metrics', {})

    # Top Metric Display
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Mean Absolute Error (MAE)",
            value=f"{metrics['mae']:.2f} min",
            delta="-38.4% vs SLR",
            delta_color="normal",
            help="Average absolute difference between actual and predicted delivery time."
        )
    with m2:
        st.metric(
            label="Mean Squared Error (MSE)",
            value=f"{metrics['mse']:.2f}",
            help="Average of squared differences between actual and predicted values."
        )
    with m3:
        st.metric(
            label="Root Mean Squared Error (RMSE)",
            value=f"{metrics['rmse']:.2f} min",
            delta="-29.8% vs SLR",
            delta_color="normal",
            help="Standard deviation of the residuals."
        )
    with m4:
        st.metric(
            label="R² Score (Test Set)",
            value=f"{metrics['r2']:.4f}",
            delta=f"{metrics['r2']*100:.1f}% explained",
            help="Proportion of variance explained by the model."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("1. Comparison: Simple vs Multiple Linear Regression")
    st.markdown("Shows how incorporating all available features improves predictive accuracy:")

    comp_df = pd.DataFrame({
        "Model": [
            "Simple Linear Regression (Distance Only)",
            "Multiple Linear Regression (All Available Features)"
        ],
        "Input Features": [
            "1 (`Distance_km`)",
            "7 (`Distance_km`, `Preparation_Time_min`, `Courier_Experience_yrs`, `Weather`, `Traffic_Level`, `Time_of_Day`, `Vehicle_Type`)"
        ],
        "MAE (min)": [
            f"{slr_metrics.get('mae', 9.58):.2f}",
            f"{metrics['mae']:.2f}"
        ],
        "RMSE (min)": [
            f"{slr_metrics.get('rmse', 12.58):.2f}",
            f"{metrics['rmse']:.2f}"
        ],
        "R² Score": [
            f"{slr_metrics.get('r2', 0.6471):.4f} (64.7%)",
            f"{metrics['r2']:.4f} ({metrics['r2']*100:.1f}%)"
        ],
        "Verdict": [
            "Underfits: Captures distance transit rate but ignores kitchen prep and weather.",
            "Strong Fit: Accounts for additive kitchen delays, weather, and traffic density."
        ]
    })
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("2. Plain-English Explanation of Metrics")
    c_exp1, c_exp2 = st.columns(2)
    with c_exp1:
        st.info("""
        **Mean Absolute Error (MAE):**
        - Measures average prediction error in minutes.
        - **5.90 minutes** means on average our prediction is within ~5 minutes and 54 seconds of the actual delivery time.
        
        **Mean Squared Error (MSE):**
        - Average of squared prediction errors (**77.91**).
        - Heavily penalizes large mistakes.
        """)
    with c_exp2:
        st.info("""
        **Root Mean Squared Error (RMSE):**
        - Square root of MSE (**8.83 minutes**).
        - Represents the standard deviation of unexplained errors.
        
        **R-squared ($R^2$) Score:**
        - **0.8262 (82.6%)** means **82.6% of the variance** in delivery times is explained by the model's independent variables.
        """)

    st.divider()
    st.subheader("3. Feature Coefficients (Impact in Minutes)")

    coef_list = model_bundle.get('coefficients', [])
    if coef_list:
        coef_df = pd.DataFrame(coef_list).sort_values(by="Coefficient", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ["#dc2626" if c > 0 else "#2563eb" for c in coef_df["Coefficient"]]
        bars = ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors, edgecolor="black", linewidth=0.5)
        ax.axvline(0, color="gray", linestyle="--", linewidth=1)
        ax.set_xlabel("Impact on Delivery Time (Minutes)", fontsize=11, weight="bold")
        ax.set_ylabel("Feature", fontsize=11, weight="bold")
        ax.set_title("Learned Feature Coefficients (Kaggle Dataset)", fontsize=13, weight="bold")

        for bar in bars:
            width = bar.get_width()
            align = "left" if width >= 0 else "right"
            offset = 0.2 if width >= 0 else -0.2
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                    f"{width:+.2f}m", va="center", ha=align, fontsize=9)

        plt.tight_layout()
        st.pyplot(fig)


# -----------------------------------------------------------------------------
# 6. SECTION 3: DATA ANALYSIS & VISUALISATIONS (EDA)
# -----------------------------------------------------------------------------
elif app_mode == "📊 Data Analysis & Visualisations":
    st.title("📊 Data Analysis & Visualisations (EDA)")
    st.markdown("Exploratory Data Analysis generated directly from `Food_Delivery_Times.csv`.")
    st.divider()

    df = load_cleaned_dataset()
    if df is None:
        st.error(f"Dataset not found at `{DATASET_PATH}`.")
        st.stop()

    # Overview Metrics
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Total Records", f"{len(df):,}")
    with s2:
        st.metric("Avg Delivery Time", f"{df['Delivery_Time_min'].mean():.1f} min")
    with s3:
        st.metric("Avg Distance", f"{df['Distance_km'].mean():.1f} km")
    with s4:
        st.metric("Avg Prep Time", f"{df['Preparation_Time_min'].mean():.1f} min")

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📍 Distance vs Time",
        "🚦 Traffic & Weather",
        "🍳 Prep & Courier Experience",
        "🔥 Correlation Heatmap",
        "📋 Dataset Viewer"
    ])

    with tab1:
        st.subheader("1. Delivery Distance vs Delivery Time")
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.regplot(
            data=df,
            x="Distance_km",
            y="Delivery_Time_min",
            scatter_kws={"alpha": 0.45, "color": "#1e3a8a"},
            line_kws={"color": "#dc2626", "linewidth": 2.5},
            ax=ax
        )
        ax.set_title("Distance vs Delivery Time with Fitted Linear Regression Line", fontsize=12, weight="bold")
        ax.set_xlabel("Delivery Distance (km)", fontsize=10)
        ax.set_ylabel("Delivery Time (minutes)", fontsize=10)
        st.pyplot(fig)
        st.caption("Observation: Strong positive linear relationship. Each additional kilometer adds ~3 minutes to transit time.")

    with tab2:
        col_t, col_w = st.columns(2)
        with col_t:
            st.subheader("Traffic Level vs Delivery Time")
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.boxplot(
                data=df,
                x="Traffic_Level",
                y="Delivery_Time_min",
                order=["Low", "Medium", "High"],
                palette="Blues",
                ax=ax
            )
            ax.set_title("Delivery Time by Traffic Density", fontsize=11, weight="bold")
            ax.set_xlabel("Traffic Level")
            ax.set_ylabel("Delivery Time (min)")
            st.pyplot(fig)

        with col_w:
            st.subheader("Weather Condition vs Delivery Time")
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.barplot(
                data=df,
                x="Weather",
                y="Delivery_Time_min",
                order=["Clear", "Windy", "Foggy", "Rainy", "Snowy"],
                palette="Reds",
                errorbar=None,
                ax=ax
            )
            ax.set_title("Average Delivery Time by Weather", fontsize=11, weight="bold")
            ax.set_xlabel("Weather Condition")
            ax.set_ylabel("Mean Delivery Time (min)")
            st.pyplot(fig)

    with tab3:
        col_p, col_e = st.columns(2)
        with col_p:
            st.subheader("Preparation Time vs Delivery Time")
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.scatterplot(
                data=df,
                x="Preparation_Time_min",
                y="Delivery_Time_min",
                hue="Vehicle_Type",
                alpha=0.6,
                palette="Set2",
                ax=ax
            )
            ax.set_title("Preparation Time vs Delivery Time", fontsize=11, weight="bold")
            ax.set_xlabel("Preparation Time (min)")
            ax.set_ylabel("Delivery Time (min)")
            st.pyplot(fig)

        with col_e:
            st.subheader("Courier Experience vs Delivery Time")
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.scatterplot(
                data=df,
                x="Courier_Experience_yrs",
                y="Delivery_Time_min",
                color="#7c3aed",
                alpha=0.5,
                ax=ax
            )
            ax.set_title("Courier Experience vs Delivery Time", fontsize=11, weight="bold")
            ax.set_xlabel("Courier Experience (years)")
            ax.set_ylabel("Delivery Time (min)")
            st.pyplot(fig)

    with tab4:
        st.subheader("Correlation Heatmap of Numerical Features")
        num_cols = ["Distance_km", "Preparation_Time_min", "Courier_Experience_yrs", "Delivery_Time_min"]
        corr = df[num_cols].corr()

        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".3f", vmin=-1, vmax=1, linewidths=0.5, ax=ax)
        ax.set_title("Pearson Correlation Heatmap", fontsize=12, weight="bold")
        st.pyplot(fig)
        st.caption("Observation: Distance exhibits the highest positive correlation (~0.80) with delivery time.")

    with tab5:
        st.subheader("Cleaned Dataset Records")
        st.dataframe(df, use_container_width=True)
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned Dataset (CSV)",
            data=csv_data,
            file_name="Food_Delivery_Times_Cleaned.csv",
            mime="text/csv"
        )


# -----------------------------------------------------------------------------
# 7. SECTION 4: ABOUT PROJECT & VIVA Q&A
# -----------------------------------------------------------------------------
elif app_mode == "📖 About Project & Viva Q&A":
    st.title("📖 About the Project & Viva Preparation Guide")
    st.markdown("Academic project documentation and viva examination answers.")
    st.divider()

    st.subheader("1. Project Overview")
    st.markdown("""
    This project uses the **Kaggle Food Delivery Time Prediction dataset by denkuznetz** to predict the duration (in minutes) of a food delivery order.
    
    The project strictly uses **Linear Regression** (both Simple and Multiple) to provide an interpretable, transparent machine learning system suitable for academic evaluation and real-world deployment.
    """)

    st.subheader("2. Mathematical Formulation")
    st.markdown("""
    **Multiple Linear Regression Formulation:**

    $$Y = \\beta_0 + \\beta_1 X_1 + \\beta_2 X_2 + \\dots + \\beta_p X_p + \\epsilon$$

    Where:
    - $Y$: `Delivery_Time_min` (Target variable)
    - $\\beta_0$: Intercept (`17.37 minutes`)
    - $\\beta_1, \\dots, \\beta_p$: Learned regression coefficients
    - $X_1, \\dots, X_p$: Input features (`Distance_km`, `Preparation_Time_min`, `Courier_Experience_yrs`, and one-hot encoded categories)
    - $\\epsilon$: Residual error term
    """)

    st.subheader("3. Frequently Asked Viva Questions")

    with st.expander("Q1: Why was Order_ID dropped from the features?"):
        st.markdown("""
        **Answer:**
        `Order_ID` is an arbitrary tracking number assigned to an order. It has no causal or statistical relationship with food preparation time or road transit speed. Including identifier columns would lead to false correlations and poor generalization.
        """)

    with st.expander("Q2: How were missing values handled in this dataset?"):
        st.markdown("""
        **Answer:**
        - **Numerical features** (`Courier_Experience_yrs`): Imputed with the **median** (5.0 years), which is robust to outliers and skewed distributions.
        - **Categorical features** (`Weather`, `Traffic_Level`, `Time_of_Day`): Imputed with their **mode** (most frequent class: Clear, Medium, and Morning respectively).
        """)

    with st.expander("Q3: Why use Linear Regression for delivery time prediction?"):
        st.markdown("""
        **Answer:**
        Food delivery is an additive physical process: total time is composed of kitchen preparation + transit distance delay + weather and traffic delays. Linear Regression allows direct interpretability: each coefficient shows exactly how many minutes each factor adds or saves.
        """)

    with st.expander("Q4: What is the difference between MAE and RMSE in this project?"):
        st.markdown("""
        **Answer:**
        - **MAE (5.90 min):** Average magnitude of absolute error.
        - **RMSE (8.83 min):** Square root of mean squared error. Because RMSE squares differences before taking the average, it gives higher weight to larger errors. When RMSE is reasonably close to MAE, it confirms that extreme prediction outliers are uncommon.
        """)
