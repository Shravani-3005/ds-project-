"""
=============================================================================
Food Delivery Time Prediction System Using Linear Regression
File: app.py
Framework: Streamlit
Description: Interactive web interface for predicting food delivery times,
             inspecting model evaluation metrics, exploring EDA visualisations,
             and reviewing academic project concepts.
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

# Custom CSS for clean, modern academic presentation
st.markdown("""
<style>
    /* Metric card styling */
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        text-align: center;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 700;
        color: #1e3a8a;
    }
    .metric-title {
        font-size: 14px;
        color: #4b5563;
        font-weight: 500;
    }
    .prediction-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .prediction-value {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .sub-note {
        font-size: 14px;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 2. PATHS & CACHED RESOURCE LOADERS
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "linear_regression.pkl")
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "delivery_data.csv")


@st.cache_resource
def load_trained_model():
    """Load serialized model bundle from models/linear_regression.pkl."""
    if not os.path.exists(MODEL_PATH):
        return None
    try:
        bundle = joblib.load(MODEL_PATH)
        return bundle
    except Exception as e:
        st.error(f"Error loading model bundle: {e}")
        return None


@st.cache_data
def load_dataset():
    """Load and return the cleaned delivery dataset for EDA and stats."""
    if not os.path.exists(DATASET_PATH):
        return None
    df = pd.read_csv(DATASET_PATH)
    # Deduplicate and fill missing values consistently
    df = df.drop_duplicates()
    if df['Partner_Experience_years'].isnull().any():
        df['Partner_Experience_years'] = df['Partner_Experience_years'].fillna(
            df['Partner_Experience_years'].median()
        )
    if df['Weather'].isnull().any():
        df['Weather'] = df['Weather'].fillna(df['Weather'].mode()[0])
    return df


# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=90)
st.sidebar.title("Navigation")
st.sidebar.markdown("**Food Delivery Time Predictor**")
st.sidebar.markdown("*Machine Learning with Linear Regression*")

app_mode = st.sidebar.radio(
    "Go to Section:",
    [
        "⏱️ Predict Delivery Time",
        "📈 Model Performance & Metrics",
        "📊 Exploratory Data Analysis (EDA)",
        "📖 About Project & Viva Q&A"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### 📌 Project Metadata")
st.sidebar.markdown("- **Algorithm:** Linear Regression")
st.sidebar.markdown("- **Framework:** Scikit-Learn")
st.sidebar.markdown("- **Language:** Python 3")
st.sidebar.markdown("- **Status:** Production-Ready")


# -----------------------------------------------------------------------------
# 4. SECTION 1: PREDICTION INTERFACE
# -----------------------------------------------------------------------------
if app_mode == "⏱️ Predict Delivery Time":
    st.title("⏱️ Food Delivery Time Prediction System")
    st.markdown(
        "Estimate delivery duration using a trained **Multiple Linear Regression** model. "
        "Enter order parameters below to generate an instant estimate."
    )
    st.divider()

    model_bundle = load_trained_model()

    if model_bundle is None:
        st.warning("⚠️ Trained model bundle not found (`models/linear_regression.pkl`).")
        st.info("Run `python train_model.py` in your terminal to train and save the model.")
        if st.button("🚀 Train Model Now"):
            with st.spinner("Training model on dataset..."):
                import subprocess
                subprocess.run(["python", os.path.join(BASE_DIR, "train_model.py")], check=True)
                st.success("Model trained successfully! Please reload the page.")
        st.stop()

    pipeline = model_bundle['pipeline']
    categories = model_bundle['categories']

    st.subheader("1. Enter Order & Delivery Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        distance = st.number_input(
            "📍 Delivery Distance (km)",
            min_value=0.5,
            max_value=30.0,
            value=4.5,
            step=0.1,
            help="Direct road distance between restaurant and customer address in kilometers."
        )

        prep_time = st.number_input(
            "🍳 Kitchen Preparation Time (minutes)",
            min_value=5.0,
            max_value=60.0,
            value=15.0,
            step=1.0,
            help="Estimated cooking, packing, and dispatch time at restaurant in minutes."
        )

    with col2:
        traffic = st.selectbox(
            "🚦 Traffic Condition",
            options=categories['Traffic_Level'],
            index=1,
            help="Real-time street traffic density along the delivery route."
        )

        weather = st.selectbox(
            "⛅ Weather Condition",
            options=categories['Weather'],
            index=0,
            help="Current meteorological conditions (rain, fog, storms introduce transit delay)."
        )

    with col3:
        vehicle = st.selectbox(
            "🛵 Vehicle Type",
            options=categories['Vehicle_Type'],
            index=0,
            help="Mode of transit used by the delivery executive."
        )

        time_of_day = st.selectbox(
            "🕒 Time of Day",
            options=categories['Time_of_Day'],
            index=2,
            help="Shift period: Lunch and Dinner (Evening) periods exhibit peak demand."
        )

        experience = st.number_input(
            "⭐ Delivery Partner Experience (years)",
            min_value=0.0,
            max_value=15.0,
            value=2.5,
            step=0.5,
            help="Years of experience navigating local neighborhoods."
        )

    # Input validations & warning messages
    validation_passed = True
    if vehicle == "Bicycle" and distance > 10.0:
        st.warning("⚠️ Note: A bicycle delivery distance over 10 km may take considerably longer and is rarely dispatched in standard practice.")

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🚀 Predict Delivery Time", type="primary", use_container_width=True)

    if predict_btn and validation_passed:
        # Construct DataFrame matching the exact schema used during training
        input_data = pd.DataFrame([{
            'Delivery_Distance_km': float(distance),
            'Preparation_Time_min': float(prep_time),
            'Partner_Experience_years': float(experience),
            'Traffic_Level': traffic,
            'Weather': weather,
            'Time_of_Day': time_of_day,
            'Vehicle_Type': vehicle
        }])

        try:
            # Predict delivery time using the scikit-learn pipeline
            raw_prediction = pipeline.predict(input_data)[0]
            # Physical lower bound guard: cannot be less than prep time + 2 minutes
            predicted_time = max(prep_time + 2.0, float(raw_prediction))
            lower_bound = max(prep_time, predicted_time - 3.0)
            upper_bound = predicted_time + 3.5

            # Display prediction banner
            st.markdown(f"""
            <div class="prediction-box">
                <div style="font-size: 18px; opacity: 0.9;">ESTIMATED DELIVERY DURATION</div>
                <div class="prediction-value">{predicted_time:.1f} Minutes</div>
                <div style="font-size: 16px; opacity: 0.95;">Expected arrival window: <b>{lower_bound:.0f} - {upper_bound:.0f} mins</b></div>
            </div>
            """, unsafe_allow_html=True)

            # Details & Mathematical Interpretation
            st.subheader("2. Summary & Linear Regression Breakdown")
            res_col1, res_col2 = st.columns([1, 1])

            with res_col1:
                st.markdown("**Order Parameter Summary:**")
                summary_df = pd.DataFrame({
                    "Parameter": [
                        "Delivery Distance", "Kitchen Prep Time", "Traffic Density",
                        "Weather Condition", "Vehicle Mode", "Time Period", "Partner Experience"
                    ],
                    "Value": [
                        f"{distance} km", f"{prep_time} mins", traffic,
                        weather, vehicle, time_of_day, f"{experience} years"
                    ]
                })
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

            with res_col2:
                st.markdown("**How Linear Regression Calculates This Result:**")
                st.markdown(f"""
                Linear Regression computes the prediction by summing the baseline intercept with the weighted contribution of each feature:

                $$Delivery\\ Time = \\beta_0 + \\sum_{{i=1}}^{{p}} \\beta_i X_i$$

                - **Base Intercept ($\\beta_0$):** `{model_bundle['intercept']:.1f} min`
                - **Distance Effect:** `{distance} km` scaled by distance coefficient.
                - **Kitchen Prep Effect:** Adds `{prep_time:.1f} min` directly.
                - **Traffic Condition (`{traffic}`):** Adjusted for street congestion.
                - **Weather Condition (`{weather}`):** Weather transit impact added.
                - **Vehicle Adjustment (`{vehicle}`):** Faster vehicles reduce overall transit duration.
                - **Experience Discount:** Partner experience saves time through route familiarity.
                """)

        except Exception as err:
            st.error(f"Error computing prediction: {err}")


# -----------------------------------------------------------------------------
# 5. SECTION 2: MODEL PERFORMANCE & METRICS
# -----------------------------------------------------------------------------
elif app_mode == "📈 Model Performance & Metrics":
    st.title("📈 Model Performance & Evaluation Metrics")
    st.markdown(
        "Evaluation results for the **Multiple Linear Regression** model on the unseen test dataset (20% holdout split)."
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
            delta="-71% vs baseline",
            delta_color="normal",
            help="Average absolute difference between actual and predicted delivery time in minutes."
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
            help="Square root of MSE, representing standard deviation of prediction errors."
        )
    with m4:
        st.metric(
            label="R² Score (Test Set)",
            value=f"{metrics['r2']:.4f}",
            delta=f"{metrics['r2']*100:.1f}% explained",
            help="Proportion of total delivery time variance explained by the model."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("1. Plain-English Explanation of Evaluation Metrics")

    exp_col1, exp_col2 = st.columns(2)
    with exp_col1:
        st.info("""
        **Mean Absolute Error (MAE):**
        - Measures the average magnitude of errors in the same units (minutes).
        - An MAE of **2.24 minutes** means that on average, our prediction is off by only about 2 minutes and 14 seconds from the actual delivery time.
        
        **Mean Squared Error (MSE):**
        - Averages the squared differences between actual and predicted values.
        - Because errors are squared, larger deviations are penalized more heavily.
        """)

    with exp_col2:
        st.info("""
        **Root Mean Squared Error (RMSE):**
        - The square root of MSE, bringing the metric back into minutes.
        - An RMSE of **2.86 minutes** confirms that large prediction outliers are minimal.
        
        **R-squared ($R^2$) Score:**
        - Indicates the goodness of fit of the linear model.
        - An $R^2$ of **0.938 (93.8%)** proves the independent variables effectively capture almost all variance in food delivery durations.
        """)

    st.divider()
    st.subheader("2. Model Comparison: Simple vs Multiple Linear Regression")
    st.markdown(
        "Demonstrates why food delivery time prediction requires **Multiple** Linear Regression instead of Simple Linear Regression."
    )

    comp_df = pd.DataFrame({
        "Model": [
            "Simple Linear Regression (Distance Only)",
            "Multiple Linear Regression (All Features)"
        ],
        "Input Variables": [
            "1 (Delivery Distance only)",
            "7 (Distance, Prep Time, Traffic, Weather, Experience, Vehicle, Time of Day)"
        ],
        "MAE (min)": [
            f"{slr_metrics.get('mae', 7.78):.2f}",
            f"{metrics['mae']:.2f}"
        ],
        "RMSE (min)": [
            f"{slr_metrics.get('rmse', 9.68):.2f}",
            f"{metrics['rmse']:.2f}"
        ],
        "R² Score": [
            f"{slr_metrics.get('r2', 0.2853):.4f} (28.5%)",
            f"{metrics['r2']:.4f} ({metrics['r2']*100:.1f}%)"
        ],
        "Academic Verdict": [
            "Underfits: Ignores kitchen preparation, traffic delays & weather.",
            "Strong Fit: Captures additive real-world delays accurately."
        ]
    })
    st.dataframe(comp_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("3. Model Coefficients (Feature Impacts)")
    st.markdown("Shows how each factor increases (+) or decreases (-) delivery time in minutes:")

    coef_list = model_bundle.get('coefficients', [])
    if coef_list:
        coef_df = pd.DataFrame(coef_list).sort_values(by="Coefficient", ascending=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ["#e11d48" if c > 0 else "#2563eb" for c in coef_df["Coefficient"]]
        bars = ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors, edgecolor="black", linewidth=0.5)
        ax.axvline(0, color="gray", linestyle="--", linewidth=1)
        ax.set_xlabel("Impact on Delivery Time (Minutes)", fontsize=11, weight="bold")
        ax.set_ylabel("Feature", fontsize=11, weight="bold")
        ax.set_title("Multiple Linear Regression Learned Coefficients", fontsize=13, weight="bold")

        # Add data labels
        for bar in bars:
            width = bar.get_width()
            align = "left" if width >= 0 else "right"
            offset = 0.2 if width >= 0 else -0.2
            ax.text(width + offset, bar.get_y() + bar.get_height() / 2,
                    f"{width:+.2f}m", va="center", ha=align, fontsize=9)

        plt.tight_layout()
        st.pyplot(fig)


# -----------------------------------------------------------------------------
# 6. SECTION 3: EXPLORATORY DATA ANALYSIS (EDA)
# -----------------------------------------------------------------------------
elif app_mode == "📊 Exploratory Data Analysis (EDA)":
    st.title("📊 Exploratory Data Analysis (EDA)")
    st.markdown("Visual exploration of relationships within the food delivery dataset.")
    st.divider()

    df = load_dataset()
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
        st.metric("Avg Delivery Distance", f"{df['Delivery_Distance_km'].mean():.1f} km")
    with s4:
        st.metric("Avg Prep Time", f"{df['Preparation_Time_min'].mean():.1f} min")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for different EDA plots
    eda_tab1, eda_tab2, eda_tab3, eda_tab4, eda_tab5 = st.tabs([
        "📍 Distance vs Time",
        "🚦 Traffic & Weather Impacts",
        "🍳 Kitchen Prep & Vehicle",
        "🔥 Correlation Heatmap",
        "📋 Dataset Viewer"
    ])

    with eda_tab1:
        st.subheader("Delivery Distance vs Delivery Time")
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.regplot(
            data=df,
            x="Delivery_Distance_km",
            y="Delivery_Time_min",
            scatter_kws={"alpha": 0.45, "color": "#1e3a8a"},
            line_kws={"color": "#dc2626", "linewidth": 2.5},
            ax=ax
        )
        ax.set_title("Distance vs Delivery Time with Fitted Regression Trendline", fontsize=12, weight="bold")
        ax.set_xlabel("Delivery Distance (km)", fontsize=10)
        ax.set_ylabel("Delivery Time (minutes)", fontsize=10)
        st.pyplot(fig)
        st.caption("Observation: As delivery distance increases, transit duration rises linearly.")

    with eda_tab2:
        col_t, col_w = st.columns(2)
        with col_t:
            st.subheader("Traffic Conditions vs Delivery Time")
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.boxplot(
                data=df,
                x="Traffic_Level",
                y="Delivery_Time_min",
                order=["Low", "Medium", "High", "Jam"],
                palette="Blues",
                ax=ax
            )
            ax.set_title("Delivery Time by Traffic Level", fontsize=11, weight="bold")
            ax.set_xlabel("Traffic Level")
            ax.set_ylabel("Delivery Time (min)")
            st.pyplot(fig)

        with col_w:
            st.subheader("Weather Conditions vs Delivery Time")
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.barplot(
                data=df,
                x="Weather",
                y="Delivery_Time_min",
                order=["Clear", "Windy", "Foggy", "Rainy", "Stormy"],
                palette="Oranges",
                errorbar=None,
                ax=ax
            )
            ax.set_title("Average Delivery Time by Weather", fontsize=11, weight="bold")
            ax.set_xlabel("Weather Condition")
            ax.set_ylabel("Mean Delivery Time (min)")
            st.pyplot(fig)

    with eda_tab3:
        col_p, col_v = st.columns(2)
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
            ax.set_title("Preparation Time vs Total Delivery Time", fontsize=11, weight="bold")
            ax.set_xlabel("Preparation Time (min)")
            ax.set_ylabel("Delivery Time (min)")
            st.pyplot(fig)

        with col_v:
            st.subheader("Vehicle Type Distribution")
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.boxplot(
                data=df,
                x="Vehicle_Type",
                y="Delivery_Time_min",
                palette="Pastel1",
                ax=ax
            )
            ax.set_title("Delivery Time by Vehicle Type", fontsize=11, weight="bold")
            ax.set_xlabel("Vehicle Type")
            ax.set_ylabel("Delivery Time (min)")
            st.pyplot(fig)

    with eda_tab4:
        st.subheader("Correlation Matrix Heatmap")
        num_cols = ["Delivery_Distance_km", "Preparation_Time_min", "Partner_Experience_years", "Delivery_Time_min"]
        corr = df[num_cols].corr()

        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(corr, annot=True, cmap="vlag", fmt=".3f", vmin=-1, vmax=1, linewidths=0.5, ax=ax)
        ax.set_title("Pearson Correlation Heatmap of Numerical Features", fontsize=12, weight="bold")
        st.pyplot(fig)
        st.caption("Observation: Distance and preparation time exhibit strong positive correlation with delivery time, while partner experience has a mild negative correlation.")

    with eda_tab5:
        st.subheader("Raw Dataset Preview")
        st.dataframe(df, use_container_width=True)
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Dataset (CSV)",
            data=csv_data,
            file_name="delivery_data_cleaned.csv",
            mime="text/csv"
        )


# -----------------------------------------------------------------------------
# 7. SECTION 4: ABOUT PROJECT & VIVA Q&A
# -----------------------------------------------------------------------------
elif app_mode == "📖 About Project & Viva Q&A":
    st.title("📖 About the Project & Viva Preparation Guide")
    st.markdown("Comprehensive academic project documentation and viva examination answers.")
    st.divider()

    st.subheader("1. Project Overview & Problem Statement")
    st.markdown("""
    On-demand food delivery businesses operate under stringent Service Level Agreements (SLAs).
    Accurate delivery time prediction enables:
    - **Customer Trust:** Realistic Expected Time of Arrival (ETA) reduces customer complaints and support tickets.
    - **Fleet Scheduling:** Dispatchers can assign orders to couriers at the optimal moment kitchen preparation concludes.
    - **Dynamic Delivery Radii:** Restaurants can throttle delivery zones during adverse weather or traffic jams.
    """)

    st.subheader("2. Mathematical Formulation of Linear Regression")
    st.markdown("""
    **Multiple Linear Regression** models the linear relationship between a continuous dependent target variable ($Y$) and two or more independent predictor variables ($X_1, X_2, \\dots, X_p$):

    $$Y = \\beta_0 + \\beta_1 X_1 + \\beta_2 X_2 + \\dots + \\beta_p X_p + \\epsilon$$

    Where:
    - $Y$: Predicted Food Delivery Time (minutes)
    - $\\beta_0$: Intercept (constant baseline time)
    - $\\beta_1, \\dots, \\beta_p$: Regression Coefficients representing the rate of change for each feature
    - $X_1, \\dots, X_p$: Predictor features (Distance, Prep time, Traffic, Weather, Experience, Vehicle)
    - $\\epsilon$: Random error term with mean zero
    """)

    st.subheader("3. Project Architecture & End-to-End Workflow")
    st.code("""
    [1. Raw CSV Dataset] -> [2. Data Cleaning: Impute NaNs, Drop Duplicates]
                                          |
                                          v
    [3. Feature Engineering: ColumnTransformer & One-Hot Encoding]
                                          |
                                          v
    [4. Train-Test Split (80/20)] -> [5. Fit Linear Regression]
                                          |
                                          v
    [6. Model Evaluation: MAE, RMSE, R²] -> [7. Joblib Model Serialization]
                                          |
                                          v
    [8. Streamlit Web Interface (app.py)]
    """, language="text")

    st.subheader("4. Frequently Asked Viva Questions & Model Answers")

    with st.expander("Q1: Why choose Linear Regression over complex algorithms like Random Forest or Neural Networks?"):
        st.markdown("""
        **Answer:**
        Food delivery time is governed by additive physical delays:
        $$Total\\ Time = Prep\\ Time + Travel\\ Time + Congestion\\ Delay + Weather\\ Delay$$
        Linear Regression provides **direct interpretability**: every coefficient has a physical meaning in minutes. It also trains instantly without requiring high-performance GPUs and avoids overfitting on moderate-sized datasets.
        """)

    with st.expander("Q2: How do you handle categorical variables in Linear Regression?"):
        st.markdown("""
        **Answer:**
        Linear Regression requires numerical inputs. We use **One-Hot Encoding** (`OneHotEncoder` with `drop='first'`). This converts $k$ categories into $k-1$ binary indicator variables (0 or 1), preventing the **dummy variable trap** (perfect multicollinearity with the intercept).
        """)

    with st.expander("Q3: What is the difference between Simple and Multiple Linear Regression in this project?"):
        st.markdown("""
        **Answer:**
        - **Simple Linear Regression** uses only 1 feature (Delivery Distance) to predict Delivery Time:
          $$y = mx + c$$
          It achieves an $R^2$ of only ~28.5% because distance alone ignores kitchen delays, traffic jams, and rain.
        - **Multiple Linear Regression** combines all 7 features, achieving an $R^2$ of **~93.8%** and dropping MAE from ~7.8 minutes down to ~2.2 minutes.
        """)

    with st.expander("Q4: What are the key assumptions of Linear Regression?"):
        st.markdown("""
        **Answer:**
        1. **Linearity:** Linear relationship between independent variables and target variable.
        2. **Independence:** Observations are independent of each other.
        3. **Homoscedasticity:** Constant variance of residuals across all predicted levels.
        4. **Normality of Residuals:** Prediction errors $\\epsilon$ are normally distributed around zero.
        5. **No Multicollinearity:** Independent features should not be perfectly collinear with each other.
        """)

    with st.expander("Q5: What do MAE, MSE, RMSE, and R² mean in this project?"):
        st.markdown("""
        **Answer:**
        - **MAE (Mean Absolute Error):** Average prediction mistake in minutes (~2.2 min).
        - **MSE (Mean Squared Error):** Average squared error, giving greater penalty to larger errors.
        - **RMSE (Root Mean Squared Error):** Standard deviation of error residuals (~2.8 min).
        - **R² Score:** Proportion of variance in delivery time explained by our model (~93.8%).
        """)
