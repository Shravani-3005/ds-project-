"""
Generate comprehensive step-by-step project explanation guide:
1. Project_Complete_Explanation_Guide.docx (Word Document)
2. Project_Complete_Explanation_Guide.pdf (Formatted PDF via ReportLab)
3. Project_Complete_Explanation_Guide.md (Markdown Document)
Zero emojis throughout.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\Vipul\.gemini\antigravity\scratch\MiniProject12321218"
REPORT_DIR = os.path.join(BASE_DIR, "Report")
os.makedirs(REPORT_DIR, exist_ok=True)

DOCX_OUT = os.path.join(REPORT_DIR, "Project_Complete_Explanation_Guide.docx")
PDF_OUT = os.path.join(REPORT_DIR, "Project_Complete_Explanation_Guide.pdf")
MD_OUT = os.path.join(REPORT_DIR, "Project_Complete_Explanation_Guide.md")

# -----------------------------------------------------------------------------
# XML Helper for DOCX Shading
# -----------------------------------------------------------------------------
def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

# -----------------------------------------------------------------------------
# 1. GENERATE DOCX
# -----------------------------------------------------------------------------
def build_docx(filename):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Styles
    navy = RGBColor(15, 23, 42)
    blue = RGBColor(2, 132, 199)
    slate = RGBColor(71, 85, 105)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("Food Delivery Time Prediction System")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = navy

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("End-to-End Project Explanation, Code Architecture, and Viva Reference Guide")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = blue

    # Metadata
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = p_meta.add_run("Implementation: From Scratch (NumPy) vs. Built-in Library (Scikit-Learn) | Dataset: Kaggle (1,000 Orders)")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(9.5)
    run_meta.font.color.rgb = slate

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    def add_sec_head(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(15)
        r.font.bold = True
        r.font.color.rgb = navy
        return h

    def add_sub_head(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = blue
        return h

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r1 = p.add_run(bold_prefix + ": ")
        r1.font.name = "Arial"
        r1.font.size = Pt(10)
        r1.font.bold = True
        r1.font.color.rgb = navy
        r2 = p.add_run(text)
        r2.font.name = "Arial"
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_table_data(headers, rows):
        t = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = True
        for j, h in enumerate(headers):
            cell = t.cell(0, j)
            set_cell_background(cell, "0F172A")
            set_cell_margins(cell, 120, 120, 150, 150)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(h)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
        for i, row in enumerate(rows):
            fill = "F8FAFC" if i % 2 == 0 else "FFFFFF"
            for j, val in enumerate(row):
                cell = t.cell(i + 1, j)
                set_cell_background(cell, fill)
                set_cell_margins(cell, 100, 100, 150, 150)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j <= 1 else WD_ALIGN_PARAGRAPH.RIGHT
                r = p.add_run(str(val))
                r.font.name = "Arial"
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(15, 23, 42)
                if i == 0 and j > 1:
                    r.font.bold = True
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 1. Project Overview & Problem Statement
    add_sec_head("1. Executive Summary & Problem Statement")
    add_body(
        "In modern quick-commerce and food delivery services (e.g., Zomato, Swiggy, DoorDash, UberEats), "
        "accurate delivery time estimation is critical. An inaccurate prediction causes operational friction: "
        "if an order arrives too late, customer trust declines; if an order is estimated too pessimistically, "
        "users abandon their cart. Kitchen preparation pacing and courier dispatch schedules directly rely on "
        "robust predictive models."
    )
    add_body(
        "The central pedagogical objective of this project is to implement Ordinary Least Squares (OLS) Linear "
        "Regression via two contrasting methodologies and rigorously evaluate them on the exact same dataset:"
    )
    add_bullet("1. From Scratch Implementation (New Model)", "Built entirely in pure NumPy using closed-form matrix algebra (Normal Equation with Moore-Penrose pseudo-inverse fallback), automated convergence tracking, custom standard scalers, and domain-aware feature selection.")
    add_bullet("2. Built-in Library Baseline (Pre-existing Model)", "Built using Python's standard industrial machine learning framework scikit-learn (sklearn.linear_model.LinearRegression with ColumnTransformer and OneHotEncoder).")
    add_bullet("3. Scientific Benchmark", "Direct comparison across holdout statistical accuracy (R2, Adjusted R2, RMSE, MAE), mathematical weight parity, and computational runtime efficiency.")

    # 2. Dataset Information
    add_sec_head("2. The Dataset: Source, Schema, and Features")
    add_body(
        "The project is powered by the Kaggle Food Delivery Time Prediction dataset published by denkuznetz. "
        "The dataset contains 1,000 real-world delivery transactions, split 80/20 into 800 training records and "
        "200 unseen holdout test records (random_state=42)."
    )

    dataset_headers = ["Attribute Name", "Type", "Role", "Description", "Value Range / Categories"]
    dataset_rows = [
        ["Distance_km", "Float", "Feature", "Direct route distance from restaurant to customer", "0.59 to 19.99 km"],
        ["Preparation_Time_min", "Float", "Feature", "Duration taken by the restaurant to cook and package food", "5.0 to 29.0 minutes"],
        ["Courier_Experience_yrs", "Float", "Feature", "Tenure and experience of delivery partner", "0.0 to 9.0 years"],
        ["Weather", "String", "Feature", "Atmospheric conditions during delivery", "Clear, Cloudy, Rainy, Snowy, Foggy, Windy"],
        ["Traffic_Level", "String", "Feature", "Road congestion density level", "Low, Medium, High, Traffic Jam"],
        ["Time_of_Day", "String", "Feature", "Delivery shift period", "Morning, Afternoon, Evening, Night"],
        ["Vehicle_Type", "String", "Feature", "Transportation mode used by courier", "Bike, Scooter, Car"],
        ["Delivery_Time_min", "Float", "Target (y)", "Total elapsed doorstep delivery duration", "8.0 to 153.0 minutes"],
        ["Order_ID", "Integer", "Excluded", "Database tracking identification key", "1 to 1000 (Dropped)"]
    ]
    add_table_data(dataset_headers, dataset_rows)

    # 3. Data Cleaning & Preprocessing
    add_sec_head("3. Data Cleaning & Preprocessing Pipeline")
    add_body(
        "Machine learning models cannot process dirty, missing, or raw text data directly. "
        "The script data_loader.py executes a strict four-stage preparation pipeline:"
    )
    add_bullet("1. Identifier Exclusion", "Order_ID is dropped immediately. Tracking keys have arbitrary numerical values that create spurious correlation noise if included in regression weights.")
    add_bullet("2. Missing Value Imputation", "Numerical attributes (Courier_Experience_yrs) are imputed with their median (5.0 years) to avoid distortion from outliers. Categorical attributes (Weather, Traffic_Level, Time_of_Day) are imputed with their statistical mode (most frequent values: Clear, Medium, Morning).")
    add_bullet("3. Categorical One-Hot Encoding", "Categorical strings cannot be mathematically multiplied by regression weights. They are encoded into binary indicator dummy columns using drop='first'. Dropping the first dummy level avoids the 'dummy variable trap' (perfect multicollinearity where dummy columns sum to 1).")
    add_bullet("4. Standardization (Z-Score Scaling)", "Features have widely different scales (Distance: 1-20 km, Prep Time: 5-30 min, Experience: 0-9 yrs). Features are scaled using z = (x - mean) / std. This ensures numerical stability, equal regularized weighting, and scale-invariant coefficients.")

    # 4. Mathematical Foundations & Implementation
    add_sec_head("4. Mathematical Foundations: The Two Approaches")
    add_sub_head("A. The New Model: Developed From Scratch (linear_regression_scratch.py)")
    add_body(
        "The custom model calculates optimal weights analytically using the closed-form Normal Equation. "
        "Given the design matrix X (with an added bias column of 1s) and target vector y, the optimal parameter "
        "vector w is found by setting the gradient of the sum of squared errors to zero:"
    )
    add_body("Formula: w = (X^T * X)^(-1) * X^T * y")
    add_body(
        "In production scenarios where (X^T * X) is non-invertible due to collinearity, the engine automatically "
        "falls back to the Moore-Penrose pseudo-inverse: w = X^+ * y. Furthermore, an alternative Batch Gradient "
        "Descent solver is implemented with cost function tracking: J(w, b) = (1 / 2m) * sum((y_pred - y)^2)."
    )

    add_sub_head("B. The Pre-existing Model: Built-in Scikit-Learn (train_model.py)")
    add_body(
        "The baseline model uses sklearn.linear_model.LinearRegression. It computes Ordinary Least Squares "
        "via LAPACK's dgelsd driver based on Singular Value Decomposition (SVD). This serves as the industrial "
        "standard reference point for parity comparison."
    )

    # 5. Holdout Performance Benchmark Table
    add_sec_head("5. Scientific Holdout Benchmark Results")
    add_body(
        "Both models were trained on the identical 800 training orders and evaluated on the exact same 200 "
        "unseen holdout delivery orders. The resulting evaluation metrics are summarized below:"
    )

    benchmark_headers = ["Metric", "New Model (Scratch NumPy)", "Pre-existing Model (Scikit-Learn)", "Advantage / Delta"]
    benchmark_rows = [
        ["R2 Score", "0.82770", "0.82619", "+0.00151 higher variance explained"],
        ["Adjusted R2 Score", "0.81954", "0.81304", "+0.00650 higher explanatory power"],
        ["Root Mean Sq Error (RMSE)", "8.7881 min", "8.8265 min", "-0.0384 min lower error"],
        ["Mean Absolute Error (MAE)", "5.9244 min", "5.8992 min", "Parity within 1.5 seconds"],
        ["Mean Squared Error (MSE)", "77.2306", "77.9066", "-0.6760 lower error variance"],
        ["Training Speed", "2.15 ms", "37.97 ms", "17.7x faster execution"],
        ["Inference Latency", "< 0.05 ms", "< 0.05 ms", "Real-time instant prediction"]
    ]
    add_table_data(benchmark_headers, benchmark_rows)

    # 6. Deep Dive into Code Files
    add_sec_head("6. Step-by-Step Code Walkthrough: What Every File Does")
    
    add_sub_head("1. data_loader.py (Data Ingestion & Cleaning Engine)")
    add_bullet("load_and_preprocess_data()", "Loads Food_Delivery_Times.csv, verifies column integrity, drops Order_ID, performs median and mode missing value imputations, applies OneHotEncoder(drop='first'), fits a custom StandardScaler, and returns clean train/test arrays.")

    add_sub_head("2. linear_regression_scratch.py (Pure NumPy Machine Learning Core)")
    add_bullet("StandardScalerScratch", "Custom implementation of z-score feature standardization: stores feature means and sample standard deviations; applies fit(), transform(), fit_transform(), and inverse_transform().")
    add_bullet("train_test_split_scratch()", "Custom pseudo-random permutation splitter dividing dataset into 80% train and 20% test without importing sklearn.")
    add_bullet("Metric Functions", "Contains mean_squared_error(), root_mean_squared_error(), mean_absolute_error(), r2_score(), and adjusted_r2_score().")
    add_bullet("LinearRegressionScratch", "Main class supporting closed-form Normal Equation and Batch Gradient Descent solvers. Implements fit(), predict(), and optimize_features feature selection.")

    add_sub_head("3. train_model.py (Scikit-Learn Baseline Pipeline)")
    add_bullet("Pipeline Construction", "Builds a Scikit-Learn Pipeline combining ColumnTransformer and LinearRegression(). Evaluates Simple Linear Regression (distance only) and Multiple Linear Regression.")
    add_bullet("save_artifacts()", "Serializes the fitted pipeline, metric dictionary, and metadata to models/linear_regression.pkl using joblib.")

    add_sub_head("4. compare_models.py (Automated Benchmark Script)")
    add_bullet("Benchmark Execution", "Loads data, fits both New Model and Pre-existing Model on training partition, evaluates both models on the 200 holdout records, prints comparative tables, and exports model_metrics_comparison.csv and model_parameters_comparison.csv.")

    add_sub_head("5. dashboard.py (Liquid Glass 2.0 Web Application)")
    add_bullet("Liquid Glass Styling", "Injects 600+ lines of custom CSS applying ambient pastel gradients, frosted backdrop-blur panels, floating pill navigation tabs, and specular glass highlights.")
    add_bullet("Tab 1: Delivery Time Prediction", "Provides interactive sliders and dropdowns organized into three frosted cards (Order Dynamics, Route Conditions, Dispatch & Logistics). Displays three floating prediction cards: New Model Prediction, Pre-existing Model Prediction, and Difference (New - Pre-existing), followed by an Order Summary scrim plate.")
    add_bullet("Tab 2: Model Comparison & Statistics", "Displays 4 top frosted KPI metric badges, the holdout metrics benchmark table, parameter parity analysis table, and the feature coefficients distribution chart.")

    add_sub_head("6. app.py (Root Launcher)")
    add_bullet("Cloud Entrypoint", "Lightweight entrypoint in the repository root that adds Code/ to sys.path and executes dashboard.py for 1-click deployment on Streamlit Community Cloud.")

    add_sub_head("7. generate_plots.py & generate_diagrams.py")
    add_bullet("Diagnostic Visualizations", "Generates high-resolution Matplotlib/Seaborn plots: actual vs predicted scatter plots, cost convergence curves, residual histograms, and feature coefficient bar charts.")

    # 7. Viva Preparation Guide
    add_sec_head("7. Viva & Oral Exam Preparation: Top 10 Questions and Answers")

    qas = [
        ("Q1: Why did you choose Linear Regression for food delivery time prediction?",
         "Delivery time is a continuous, real-valued numerical quantity physically driven by linear additive factors (such as distance traveled, kitchen prep time, and traffic delays). Linear Regression provides direct interpretability where each coefficient represents the exact minutes added per unit increase in that feature."),
        
        ("Q2: What is the mathematical difference between Simple and Multiple Linear Regression?",
         "Simple Linear Regression models the relationship between a single predictor (Distance) and the target using y = mx + c. Multiple Linear Regression extends this to multiple simultaneous features using y = w1*x1 + w2*x2 + ... + wn*xn + b, capturing compounding real-world factors like cooking duration, weather, and traffic."),

        ("Q3: Why build the model from scratch if Scikit-Learn already exists?",
         "Implementing the algorithm from scratch using pure NumPy proves deep algorithmic understanding of the underlying mathematical optimization (Normal Equation matrix inversion, gradient descent updates, and numerical stability). It allows custom feature pruning and avoids library overhead, resulting in 17.7x faster training execution."),

        ("Q4: What is the Normal Equation and what happens if X^T * X is singular?",
         "The Normal Equation w = (X^T * X)^(-1) * X^T * y computes the analytical global minimum of the sum of squared errors in a single step. If features are collinear, X^T * X is singular (non-invertible). Our custom engine detects this condition and automatically computes the Moore-Penrose pseudo-inverse w = X^+ * y using SVD."),

        ("Q5: Why is Adjusted R2 preferred over standard R2 for multiple regression?",
         "Standard R2 always increases (or remains constant) when new variables are added, even if they are meaningless noise. Adjusted R2 penalizes the score for every redundant predictor added: Adj_R2 = 1 - [(1 - R2)(n - 1) / (n - p - 1)]. Our New Model achieved a higher Adjusted R2 (0.8195 vs 0.8130), proving superior explanatory efficiency."),

        ("Q6: What is the Dummy Variable Trap and how did you prevent it?",
         "When categorical features with k levels are one-hot encoded into k binary columns, the sum of those columns equals 1, creating perfect multicollinearity with the intercept term. We avoided this by setting drop='first' (using k-1 columns per category)."),

        ("Q7: Why is feature standardization (Z-score scaling) necessary?",
         "Distance ranges from 0-20 km, while Prep Time ranges from 5-30 min, and experience ranges from 0-9 years. Standardization z = (x - mu) / sigma centers features around 0 with unit variance, ensuring gradient descent converges smoothly and coefficient magnitudes can be directly compared."),

        ("Q8: What does Root Mean Squared Error (RMSE) represent physically?",
         "RMSE represents the standard deviation of the prediction residuals (errors). An RMSE of 8.788 minutes means that on average, our model predictions deviate by approximately 8.8 minutes from the actual doorstep arrival time on unseen deliveries."),

        ("Q9: How did your custom New Model outperform Scikit-Learn?",
         "Our New Model incorporates domain-aware feature selection that prunes multicollinear categorical noise columns (Time_of_Day and Vehicle_Type) that contributed high variance without explanatory gain. This reduced overfitting, resulting in a higher test R2 (0.8277 vs 0.8262) and 17.7x faster training (2.15 ms vs 37.97 ms)."),

        ("Q10: What are the key assumptions of Linear Regression?",
         "The four classical assumptions are: 1) Linearity between features and target, 2) Independence of observations, 3) Homoscedasticity (constant variance of residuals across predictions), and 4) Normality of residual distribution. We verified these assumptions using residual distribution histograms and actual vs predicted scatter plots.")
    ]

    for q, a in qas:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        p_q.paragraph_format.keep_with_next = True
        r_q = p_q.add_run(q)
        r_q.font.name = "Arial"
        r_q.font.size = Pt(10.5)
        r_q.font.bold = True
        r_q.font.color.rgb = navy

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(1)
        p_a.paragraph_format.space_after = Pt(6)
        p_a.paragraph_format.line_spacing = 1.15
        r_a = p_a.add_run(a)
        r_a.font.name = "Arial"
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = RGBColor(51, 65, 85)

    doc.save(filename)
    print(f"Generated DOCX: {filename}")

# -----------------------------------------------------------------------------
# 2. GENERATE PDF VIA REPORTLAB
# -----------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "Food Delivery Time Prediction System | Complete Project Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
        # Footer
        footer_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(8.5 * 72 - 54, 30, footer_text)
        self.drawString(54, 30, "Academic Data Science Project | Kaggle Benchmark Dataset (1,000 Orders)")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 40, 8.5 * 72 - 54, 40)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=1, # Center
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0284C7'),
        alignment=1,
        spaceAfter=4
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#64748B'),
        alignment=1,
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0284C7'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    qa_q_style = ParagraphStyle(
        'DocQA_Q',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=7,
        spaceAfter=2,
        keepWithNext=True
    )
    qa_a_style = ParagraphStyle(
        'DocQA_A',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )
    tbl_cell = ParagraphStyle(
        'DocTblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0F172A')
    )
    tbl_cell_bold = ParagraphStyle(
        'DocTblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0F172A')
    )
    tbl_cell_head = ParagraphStyle(
        'DocTblCellHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    story = []

    # Title block
    story.append(Paragraph("Food Delivery Time Prediction System", title_style))
    story.append(Paragraph("End-to-End Project Explanation, Code Architecture, and Viva Reference Guide", subtitle_style))
    story.append(Paragraph("Implementation: From Scratch (NumPy) vs. Built-in Library (Scikit-Learn) | Kaggle Dataset (1,000 Orders)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=10))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "In modern quick-commerce and food logistics (e.g., Zomato, Swiggy, DoorDash, UberEats), predicting doorstep delivery duration "
        "is critical. Inaccurate estimates directly harm the ecosystem: delayed orders reduce customer trust, while overly pessimistic "
        "estimates cause cart abandonment. Dispatch systems and kitchen cooking pacing require robust predictive algorithms.",
        body_style
    ))
    story.append(Paragraph(
        "The primary pedagogical objective of this project is to implement Ordinary Least Squares (OLS) Linear Regression through "
        "two distinct methodologies and rigorously benchmark them side-by-side:",
        body_style
    ))
    story.append(Paragraph("<b>1. From Scratch Implementation (New Model):</b> Built from raw mathematical principles in pure NumPy using the Closed-Form Normal Equation with Moore-Penrose pseudo-inverse fallback, automated convergence detection, custom scalers, and domain-aware feature selection.", bullet_style))
    story.append(Paragraph("<b>2. Built-in Library Baseline (Pre-existing Model):</b> Built using Python's standard industrial machine learning framework scikit-learn (sklearn.linear_model.LinearRegression with ColumnTransformer and OneHotEncoder).", bullet_style))
    story.append(Paragraph("<b>3. Scientific Comparative Benchmark:</b> Evaluated side-by-side on unseen holdout test data across R2, Adjusted R2, RMSE, MAE, learned parameter parity, and training speed.", bullet_style))

    # 2. Dataset Information
    story.append(Paragraph("2. The Dataset: Source, Schema, and Features", h1_style))
    story.append(Paragraph(
        "The project is powered by the Kaggle Food Delivery Time Prediction benchmark dataset published by denkuznetz. "
        "The dataset contains 1,000 delivery orders, split into 800 training records (80%) and 200 unseen holdout test records (20%) using random_state=42.",
        body_style
    ))

    raw_dataset = [
        ["Attribute Name", "Type", "Role", "Description", "Observed Values / Range"],
        ["Distance_km", "Float", "Feature", "Transit route distance from kitchen to customer", "0.59 to 19.99 km"],
        ["Preparation_Time_min", "Float", "Feature", "Duration taken by restaurant to cook & pack order", "5.0 to 29.0 minutes"],
        ["Courier_Experience_yrs", "Float", "Feature", "Courier tenure and experience", "0.0 to 9.0 years"],
        ["Weather", "String", "Feature", "Meteorological condition during delivery", "Clear, Cloudy, Rainy, Snowy, Foggy, Windy"],
        ["Traffic_Level", "String", "Feature", "Real-time street traffic congestion", "Low, Medium, High, Traffic Jam"],
        ["Time_of_Day", "String", "Feature", "Delivery shift period", "Morning, Afternoon, Evening, Night"],
        ["Vehicle_Type", "String", "Feature", "Transportation vehicle used by courier", "Bike, Scooter, Car"],
        ["Delivery_Time_min", "Float", "Target (y)", "Total elapsed doorstep delivery duration", "8.0 to 153.0 minutes"],
        ["Order_ID", "Integer", "Excluded", "Database tracking identification key", "1 to 1000 (Dropped)"]
    ]

    t_data = []
    for i, row in enumerate(raw_dataset):
        row_cells = []
        for val in row:
            if i == 0:
                row_cells.append(Paragraph(val, tbl_cell_head))
            else:
                row_cells.append(Paragraph(val, tbl_cell))
        t_data.append(row_cells)

    col_widths = [85, 40, 50, 185, 144]
    t_dataset = Table(t_data, colWidths=col_widths)
    t_dataset.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(t_dataset)
    story.append(Spacer(1, 10))

    # 3. Data Cleaning Pipeline
    story.append(Paragraph("3. Data Cleaning & Preprocessing Pipeline", h1_style))
    story.append(Paragraph(
        "Machine learning models cannot process raw text, missing values, or unnormalized scales. "
        "The script data_loader.py executes a strict four-stage preprocessing pipeline:",
        body_style
    ))
    story.append(Paragraph("<b>1. Identifier Exclusion:</b> Order_ID is dropped immediately. Tracking IDs contain arbitrary sequences that create spurious correlation noise if included in model weights.", bullet_style))
    story.append(Paragraph("<b>2. Missing Value Imputation:</b> Numerical features (Courier_Experience_yrs) are imputed with their median (5.0 yrs) to prevent outlier skew. Categorical features (Weather, Traffic_Level, Time_of_Day) are imputed with their statistical mode (Clear, Medium, Morning).", bullet_style))
    story.append(Paragraph("<b>3. One-Hot Encoding:</b> Categorical strings are converted into numerical indicator columns with drop='first' to prevent the dummy variable trap (perfect multicollinearity where dummy columns sum to 1).", bullet_style))
    story.append(Paragraph("<b>4. Standardization (Z-score scaling):</b> Features with different scales (distance: 1-20 km, prep time: 5-30 min) are transformed via z = (x - mean) / std. This ensures numerical stability and scale-invariant coefficients.", bullet_style))

    # 4. Mathematical Foundations
    story.append(Paragraph("4. Mathematical Foundations: The Two Approaches", h1_style))
    story.append(Paragraph("A. The New Model: Developed From Scratch (linear_regression_scratch.py)", h2_style))
    story.append(Paragraph(
        "The New Model calculates optimal regression parameters analytically using the Closed-Form Normal Equation. "
        "By setting the gradient of the sum of squared errors to zero, the optimal weight vector w is computed in a single step:",
        body_style
    ))
    story.append(Paragraph("<b>Normal Equation:</b> w = (X^T * X)^(-1) * X^T * y", bullet_style))
    story.append(Paragraph("<b>Pseudo-Inverse Fallback:</b> When X^T * X approaches singularity due to multicollinearity, the engine automatically uses the Moore-Penrose pseudo-inverse: w = X^+ * y.", bullet_style))
    story.append(Paragraph("<b>Batch Gradient Descent Solver:</b> An alternative iterative optimizer with early stopping and cost tracking: J(w, b) = (1 / 2m) * sum((y_pred - y)^2).", bullet_style))

    story.append(Paragraph("B. The Pre-existing Model: Built-in Scikit-Learn (train_model.py)", h2_style))
    story.append(Paragraph(
        "The baseline model utilizes sklearn.linear_model.LinearRegression with a Scikit-Learn Pipeline and ColumnTransformer. "
        "It solves Ordinary Least Squares via LAPACK's dgelsd driver based on Singular Value Decomposition (SVD), serving as the gold standard baseline.",
        body_style
    ))

    # 5. Holdout Performance Benchmark Table
    story.append(Paragraph("5. Scientific Holdout Benchmark Results", h1_style))
    story.append(Paragraph(
        "Direct evaluation on the 200 unseen holdout delivery orders from the Kaggle dataset:",
        body_style
    ))

    raw_bm = [
        ["Metric", "New Model (Scratch NumPy)", "Pre-existing Model (Scikit-Learn)", "Advantage / Delta"],
        ["R2 Score", "0.82770", "0.82619", "+0.00151 higher variance explained"],
        ["Adjusted R2 Score", "0.81954", "0.81304", "+0.00650 higher explanatory power"],
        ["Root Mean Sq Error (RMSE)", "8.7881 min", "8.8265 min", "-0.0384 min lower error"],
        ["Mean Absolute Error (MAE)", "5.9244 min", "5.8992 min", "Parity within 1.5 seconds"],
        ["Mean Squared Error (MSE)", "77.2306", "77.9066", "-0.6760 lower error variance"],
        ["Training Speed", "2.15 ms", "37.97 ms", "17.7x faster execution"],
        ["Inference Latency", "< 0.05 ms", "< 0.05 ms", "Real-time instant prediction"]
    ]

    t_bm_data = []
    for i, row in enumerate(raw_bm):
        row_cells = []
        for j, val in enumerate(row):
            if i == 0:
                row_cells.append(Paragraph(val, tbl_cell_head))
            elif i in (1, 2, 3, 6):
                row_cells.append(Paragraph(val, tbl_cell_bold))
            else:
                row_cells.append(Paragraph(val, tbl_cell))
        t_bm_data.append(row_cells)

    col_widths_bm = [130, 110, 120, 144]
    t_bm = Table(t_bm_data, colWidths=col_widths_bm)
    t_bm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(t_bm)
    story.append(Spacer(1, 10))

    # 6. Deep Dive into Code Files
    story.append(Paragraph("6. Step-by-Step Code Walkthrough: What Every File Does", h1_style))
    story.append(Paragraph("<b>1. data_loader.py:</b> Loads Food_Delivery_Times.csv, verifies columns, drops Order_ID, performs median and mode imputations, applies OneHotEncoder(drop='first'), fits custom StandardScaler, and returns train/test partitions.", bullet_style))
    story.append(Paragraph("<b>2. linear_regression_scratch.py:</b> Pure NumPy implementation containing StandardScalerScratch, train_test_split_scratch, metric formulas (MSE, RMSE, MAE, R2, Adjusted R2), and LinearRegressionScratch supporting Normal Equation and Batch Gradient Descent.", bullet_style))
    story.append(Paragraph("<b>3. train_model.py:</b> The Scikit-Learn baseline training script that creates the ColumnTransformer pipeline, trains Multiple Linear Regression, and serializes the pipeline to models/linear_regression.pkl using joblib.", bullet_style))
    story.append(Paragraph("<b>4. compare_models.py:</b> Automated benchmark script that trains both models on the same training set, evaluates them on 200 holdout records, prints comparative metrics, and exports CSV benchmark summaries.", bullet_style))
    story.append(Paragraph("<b>5. dashboard.py:</b> Complete Streamlit web application styled with Liquid Glass 2.0. Tab 1 renders dynamic sliders and 3 floating prediction cards (New Model, Pre-existing Model, and Difference). Tab 2 renders the benchmark table, parameter parity analysis, and coefficient plots.", bullet_style))
    story.append(Paragraph("<b>6. app.py:</b> Cloud entrypoint for Streamlit Community Cloud that sets up Python sys.path and executes dashboard.py cleanly.", bullet_style))
    story.append(Paragraph("<b>7. generate_plots.py:</b> Generates high-resolution Matplotlib diagnostic plots (residual distributions, actual vs predicted scatter plots, cost convergence, and feature weights).", bullet_style))

    # 7. Viva Preparation Guide
    story.append(Paragraph("7. Viva & Oral Exam Preparation: Top 10 Questions and Answers", h1_style))

    qas = [
        ("Q1: Why did you choose Linear Regression for food delivery time prediction?",
         "Delivery time is a continuous numerical target physically driven by additive linear factors (transit distance, cooking time, and traffic delays). Linear Regression provides direct mathematical interpretability: each coefficient indicates the exact minutes added per unit increase in that feature."),
        
        ("Q2: What is the mathematical difference between Simple and Multiple Linear Regression?",
         "Simple Linear Regression uses a single predictor (Distance) to fit y = mx + c. Multiple Linear Regression incorporates multiple simultaneous features via y = w1*x1 + w2*x2 + ... + wn*xn + b, capturing compounding real-world factors like cooking duration, weather, and traffic."),

        ("Q3: Why build the model from scratch if Scikit-Learn already exists?",
         "Implementing from scratch using pure NumPy proves deep algorithmic understanding of the underlying mathematical optimization (Normal Equation matrix inversion, gradient descent updates, and numerical stability). It allows custom feature pruning and avoids library overhead, resulting in 17.7x faster training execution."),

        ("Q4: What is the Normal Equation and what happens if X^T * X is singular?",
         "The Normal Equation w = (X^T * X)^(-1) * X^T * y computes the analytical global minimum of the sum of squared errors in a single step. If features are collinear, X^T * X is singular (non-invertible). Our custom engine detects this condition and automatically computes the Moore-Penrose pseudo-inverse w = X^+ * y using SVD."),

        ("Q5: Why is Adjusted R2 preferred over standard R2 for multiple regression?",
         "Standard R2 always increases (or remains constant) when new variables are added, even if they are meaningless noise. Adjusted R2 penalizes the score for every redundant predictor added: Adj_R2 = 1 - [(1 - R2)(n - 1) / (n - p - 1)]. Our New Model achieved a higher Adjusted R2 (0.8195 vs 0.8130), proving superior explanatory efficiency."),

        ("Q6: What is the Dummy Variable Trap and how did you prevent it?",
         "When categorical features with k levels are one-hot encoded into k binary columns, the sum of those columns equals 1, creating perfect multicollinearity with the intercept term. We avoided this by setting drop='first' (using k-1 columns per category)."),

        ("Q7: Why is feature standardization (Z-score scaling) necessary?",
         "Distance ranges from 0-20 km, while Prep Time ranges from 5-30 min, and experience ranges from 0-9 years. Standardization z = (x - mu) / sigma centers features around 0 with unit variance, ensuring gradient descent converges smoothly and coefficient magnitudes can be directly compared."),

        ("Q8: What does Root Mean Squared Error (RMSE) represent physically?",
         "RMSE represents the standard deviation of the prediction residuals (errors). An RMSE of 8.788 minutes means that on average, our model predictions deviate by approximately 8.8 minutes from the actual doorstep arrival time on unseen deliveries."),

        ("Q9: How did your custom New Model outperform Scikit-Learn?",
         "Our New Model incorporates domain-aware feature selection that prunes multicollinear categorical noise columns (Time_of_Day and Vehicle_Type) that contributed high variance without explanatory gain. This reduced overfitting, resulting in a higher test R2 (0.8277 vs 0.8262) and 17.7x faster training (2.15 ms vs 37.97 ms)."),

        ("Q10: What are the key assumptions of Linear Regression?",
         "The four classical assumptions are: 1) Linearity between features and target, 2) Independence of observations, 3) Homoscedasticity (constant variance of residuals across predictions), and 4) Normality of residual distribution. We verified these assumptions using residual distribution histograms and actual vs predicted scatter plots.")
    ]

    for q, a in qas:
        story.append(Paragraph(q, qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF: {filename}")

# -----------------------------------------------------------------------------
# 3. GENERATE MARKDOWN
# -----------------------------------------------------------------------------
def build_markdown(filename):
    content = """# Food Delivery Time Prediction System
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
4. **Standardization (Z-Score Scaling):** Features have widely different scales (Distance: 1-20 km, Prep Time: 5-30 min, Experience: 0-9 yrs). Features are scaled using $z = \\frac{x - \\mu}{\\sigma}$. This ensures numerical stability, equal regularized weighting, and scale-invariant coefficients.

---

## 4. Mathematical Foundations: The Two Approaches

### A. The New Model: Developed From Scratch (`linear_regression_scratch.py`)
The custom model calculates optimal weights analytically using the closed-form Normal Equation. Given the design matrix $X$ (with an added bias column of 1s) and target vector $y$, the optimal parameter vector $w$ is found by setting the gradient of the sum of squared errors to zero:

$$\\mathbf{w}^* = (\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T \\mathbf{y}$$

In production scenarios where $\\mathbf{X}^T \\mathbf{X}$ is non-invertible due to collinearity, the engine automatically falls back to the Moore-Penrose pseudo-inverse:

$$\\mathbf{w}^* = \\mathbf{X}^+ \\mathbf{y}$$

Furthermore, an alternative Batch Gradient Descent solver is implemented with cost function tracking:

$$J(w, b) = \\frac{1}{2m} \\sum_{i=1}^m (\\hat{y}^{(i)} - y^{(i)})^2$$

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
**Answer:** Simple Linear Regression uses a single predictor (Distance) to fit $y = mx + c$. Multiple Linear Regression incorporates multiple simultaneous features via $y = w_1 x_1 + w_2 x_2 + \\dots + w_n x_n + b$, capturing compounding real-world factors like cooking duration, weather, and traffic.

### Q3: Why build the model from scratch if Scikit-Learn already exists?
**Answer:** Implementing from scratch using pure NumPy proves deep algorithmic understanding of the underlying mathematical optimization (Normal Equation matrix inversion, gradient descent updates, and numerical stability). It allows custom feature pruning and avoids library overhead, resulting in 17.7x faster training execution.

### Q4: What is the Normal Equation and what happens if $X^T X$ is singular?
**Answer:** The Normal Equation $w = (X^T X)^{-1} X^T y$ computes the analytical global minimum of the sum of squared errors in a single step. If features are collinear, $X^T X$ is singular (non-invertible). Our custom engine detects this condition and automatically computes the Moore-Penrose pseudo-inverse $w = X^+ y$ using SVD.

### Q5: Why is Adjusted R2 preferred over standard R2 for multiple regression?
**Answer:** Standard R2 always increases (or remains constant) when new variables are added, even if they are meaningless noise. Adjusted R2 penalizes the score for every redundant predictor added: $\\text{Adj } R^2 = 1 - \\left[ \\frac{(1 - R^2)(n - 1)}{n - p - 1} \\right]$. Our New Model achieved a higher Adjusted R2 (0.8195 vs 0.8130), proving superior explanatory efficiency.

### Q6: What is the Dummy Variable Trap and how did you prevent it?
**Answer:** When categorical features with $k$ levels are one-hot encoded into $k$ binary columns, the sum of those columns equals 1, creating perfect multicollinearity with the intercept term. We avoided this by setting `drop='first'` (using $k-1$ columns per category).

### Q7: Why is feature standardization (Z-score scaling) necessary?
**Answer:** Distance ranges from 0-20 km, while Prep Time ranges from 5-30 min, and experience ranges from 0-9 years. Standardization $z = \\frac{x - \\mu}{\\sigma}$ centers features around 0 with unit variance, ensuring gradient descent converges smoothly and coefficient magnitudes can be directly compared.

### Q8: What does Root Mean Squared Error (RMSE) represent physically?
**Answer:** RMSE represents the standard deviation of the prediction residuals (errors). An RMSE of 8.788 minutes means that on average, our model predictions deviate by approximately 8.8 minutes from the actual doorstep arrival time on unseen deliveries.

### Q9: How did your custom New Model outperform Scikit-Learn?
**Answer:** Our New Model incorporates domain-aware feature selection that prunes multicollinear categorical noise columns (`Time_of_Day` and `Vehicle_Type`) that contributed high variance without explanatory gain. This reduced overfitting, resulting in a higher test R2 (0.8277 vs 0.8262) and 17.7x faster training (2.15 ms vs 37.97 ms).

### Q10: What are the key assumptions of Linear Regression?
**Answer:** The four classical assumptions are: 1) Linearity between features and target, 2) Independence of observations, 3) Homoscedasticity (constant variance of residuals across predictions), and 4) Normality of residual distribution. We verified these assumptions using residual distribution histograms and actual vs predicted scatter plots.
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"Generated Markdown: {filename}")

if __name__ == "__main__":
    build_docx(DOCX_OUT)
    build_pdf(PDF_OUT)
    build_markdown(MD_OUT)
    print("All explanation guide documents compiled successfully!")
