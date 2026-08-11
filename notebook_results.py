"""
notebook_results.py
--------------------
Every value in this file was read directly from the executed outputs of
`python_project_NTI.ipynb` (the real run, on the real health_data.csv - 4,157
individuals). Nothing here is invented. This module exists so the Streamlit
app always has a correct fallback to show even before a fresh copy of
`cleaned_health_data.csv` is uploaded into the app (see app.py), and so every
number on every page can be traced back to a specific notebook cell.

If a matching `cleaned_health_data.csv` is uploaded/found at runtime, the app
recomputes everything live from the real rows instead of these constants -
these are the fallback/reference values, not made-up placeholders.
"""

# ---------------------------------------------------------------------------
# Dataset shape & quality (Sections 3, 5, 8 of the notebook)
# ---------------------------------------------------------------------------
RAW_SHAPE = (4157, 11)                 # df.shape right after loading (cell 8)
CLEANED_SHAPE = (4155, 10)             # after dropping Unnamed:0 + de-duplication (cell 55)
N_ENGINEERED_FEATURES = 5              # BP_Risk_Category, Age_Group, BMI_Category,
                                        # Cholesterol_Ratio, Pulse_Pressure (Section 9)
FINAL_COLUMN_COUNT = CLEANED_SHAPE[1] + N_ENGINEERED_FEATURES  # 15

MISSING_VALUES_BEFORE = 121            # sum of df.isnull().sum() before imputation (cell 22)
DUPLICATES_REMOVED = 2                 # cell 55
INVALID_BP_ROWS_FIXED = 47             # Systolic < Diastolic swapped back (cell 57)

OUTLIER_BOUNDS = {                     # IQR capping bounds (cell 45/46)
    "Age":               (-16.50, 123.50),
    "BMI":                (13.58,  40.44),
    "Systolic_BP":        (81.95, 135.89),
    "Diastolic_BP":       (59.95, 103.80),
    "Total_Cholesterol": (148.42, 237.83),
    "HDL_Cholesterol":    (23.90,  50.52),
    "LDL_Cholesterol":   (178.17, 253.39),
    "Triglycerides":     (191.49, 306.71),
}

# Raw (pre-cleaning) descriptive statistics - df.describe() (cell 19)
DESCRIBE_RAW = {
    "Age":               dict(mean=53.30, std=20.59, min=18.00, q25=36.00, median=53.00, q75=71.00, max=89.00),
    "BMI":                dict(mean=27.03, std=4.88,  min=10.68, q25=23.65, median=27.03, q75=30.37, max=46.51),
    "Systolic_BP":        dict(mean=108.96, std=10.31, min=73.90, q25=102.18, median=108.96, q75=115.66, max=147.02),
    "Diastolic_BP":       dict(mean=81.85, std=8.24,  min=48.53, q25=76.32, median=81.84, q75=87.41, max=112.23),
    "Total_Cholesterol":  dict(mean=193.19, std=16.40, min=131.54, q25=181.93, median=193.19, q75=204.31, max=256.24),
    "HDL_Cholesterol":    dict(mean=37.22, std=4.99,  min=19.41, q25=33.88, median=37.22, q75=40.54, max=55.68),
    "LDL_Cholesterol":    dict(mean=215.73, std=13.99, min=162.39, q25=206.35, median=215.73, q75=225.26, max=263.84),
    "Triglycerides":      dict(mean=248.96, std=21.55, min=175.58, q25=234.67, median=248.95, q75=263.52, max=331.22),
}

# ---------------------------------------------------------------------------
# Feature-engineered category breakdowns (Section 9, real value_counts())
# ---------------------------------------------------------------------------
BP_RISK_COUNTS = {"Elevated / High Risk": 2484, "Normal": 1671}   # cell 62

AGE_GROUP_COUNTS = {                                              # cell 63
    "18-29": 673, "30-39": 602, "40-49": 564,
    "50-59": 626, "60-69": 558, "70+": 1132,
}

BMI_CATEGORY_COUNTS = {                                           # cell 64
    "Underweight": 165, "Normal": 1257, "Overweight": 1575, "Obese": 1158,
}

CHOLESTEROL_RATIO_STATS = dict(mean=5.29, std=0.88, min=2.94, q25=4.68, median=5.19, q75=5.77, max=9.61)  # cell 65
PULSE_PRESSURE_STATS = dict(mean=27.20, std=11.61, min=0.05, q25=19.08, median=27.12, q75=35.23, max=66.59)  # cell 66

SMOKING_RATE_PCT = 29.72          # KPI 5 - % of population who are smokers
INACTIVITY_RATE_PCT = 20.39       # KPI 6 - % of population with 'low' activity

# ---------------------------------------------------------------------------
# Correlation matrix - numeric health indicators (Section 10, cell 71 heatmap)
# ---------------------------------------------------------------------------
CORR_COLUMNS = ["Age", "BMI", "Systolic_BP", "Diastolic_BP",
                "Total_Cholesterol", "HDL_Cholesterol", "LDL_Cholesterol", "Triglycerides"]

CORR_MATRIX = [
    [1.00, -0.02,  0.18,  0.03,  0.25,  0.01,  0.18,  0.07],
    [-0.02, 1.00,  0.21,  0.27,  0.35, -0.10,  0.23,  0.27],
    [0.18,  0.21,  1.00,  0.21,  0.12, -0.05,  0.07,  0.06],
    [0.03,  0.27,  0.21,  1.00,  0.11, -0.01,  0.06,  0.07],
    [0.25,  0.35,  0.12,  0.11,  1.00, -0.03,  0.69,  0.34],
    [0.01, -0.10, -0.05, -0.01, -0.03,  1.00, -0.02, -0.04],
    [0.18,  0.23,  0.07,  0.06,  0.69, -0.02,  1.00,  0.24],
    [0.07,  0.27,  0.06,  0.07,  0.34, -0.04,  0.24,  1.00],
]

# ---------------------------------------------------------------------------
# Business & Health Questions - real printed results (Section 11)
# ---------------------------------------------------------------------------
BQ1_BMI_BY_SMOKING = {"non-smoker": 27.06, "smoker": 26.94}                       # cell 78
BQ2_AGE_SYSTOLIC_CORR = 0.18                                                      # cell 81
BQ3_MEDIAN_BMI_BY_ACTIVITY = {"low": 27.00, "moderate": 27.03, "high": 27.03}     # cell 84
BQ4_BP_RISK_BY_SMOKING_PCT = {                                                    # cell 87
    "non-smoker": {"Normal": 39.6, "Elevated / High Risk": 60.4},
    "smoker":     {"Normal": 41.6, "Elevated / High Risk": 58.4},
}
BQ5_BP_RISK_BY_BMI_PCT = {                                                        # cell 90
    "Underweight": 33.9, "Normal": 50.4, "Overweight": 60.7, "Obese": 72.5,
}
BQ6_AVG_CHOL_BY_AGE_GROUP = {                                                     # cell 93
    "18-29": 187.66, "30-39": 188.43, "40-49": 192.30,
    "50-59": 193.22, "60-69": 194.74, "70+": 198.66,
}

BUSINESS_QUESTIONS = [
    {
        "title": "Does smoking associate with a higher BMI?",
        "why": "BMI is a core obesity indicator; if smokers carry a materially different average "
               "BMI, it affects how lifestyle-risk screening should be weighted.",
        "answer": "Average BMI is nearly identical between smokers (26.94) and non-smokers (27.06) - "
                  "under a 1-point difference.",
        "insight": "Smoking status alone does not distinguish body-weight risk in this population.",
        "implication": "BMI-based screening should be applied uniformly regardless of smoking status.",
        "recommendation": "Treat smoking and obesity as separate, independent risk factors to screen for.",
        "chart": "bq1",
    },
    {
        "title": "How does systolic blood pressure change with age?",
        "why": "If blood pressure rises predictably with age, screening frequency can be tailored by age band.",
        "answer": f"There is a positive but modest correlation (r = {BQ2_AGE_SYSTOLIC_CORR}) between "
                  "Age and Systolic BP.",
        "insight": "Age alone explains only part of BP variation, so it is a contributing, not sole, risk factor.",
        "implication": "Blood-pressure screening should not rely on age alone.",
        "recommendation": "Combine age with BMI and lipid markers when prioritizing BP screening.",
        "chart": "bq2",
    },
    {
        "title": "Does physical activity level associate with lower BMI?",
        "why": "If more active individuals carry lower BMI, activity-promotion programs have a clear, "
               "data-backed rationale.",
        "answer": "Median BMI is nearly flat across activity levels: low 27.00, moderate 27.03, high 27.03.",
        "insight": "Self-reported activity level is not a strong standalone differentiator of BMI in this dataset.",
        "implication": "Activity level should be treated as a complementary lifestyle indicator, not a proxy for weight status.",
        "recommendation": "Pair activity-level tracking with direct BMI/weight measurement rather than substituting one for the other.",
        "chart": "bq3",
    },
    {
        "title": "What share of individuals fall into elevated BP risk, and does it differ by smoking status?",
        "why": "This quantifies the size of a high-priority population and tests whether smoking-status-based "
               "outreach would catch a disproportionate share of at-risk individuals.",
        "answer": "Elevated BP risk is 60.4% among non-smokers and 58.4% among smokers - a very similar rate.",
        "insight": "Elevated BP risk is widespread across the population rather than concentrated in smokers specifically.",
        "implication": "Smoking status is not an efficient single filter for BP-risk outreach.",
        "recommendation": "Screen for blood pressure broadly across the whole population, not just among smokers.",
        "chart": "bq4",
    },
    {
        "title": "Which BMI category carries the highest elevated-BP-risk rate?",
        "why": "Tests whether obesity status identifies high-BP-risk individuals better than smoking status did.",
        "answer": "Elevated BP risk rises steadily: Underweight 33.9% -> Normal 50.4% -> Overweight 60.7% -> Obese 72.5%.",
        "insight": "BMI category is a much sharper, more usable gradient than smoking status for BP risk.",
        "implication": "Obesity status is a strong, actionable segmentation variable for BP screening priority.",
        "recommendation": "Prioritize BMI-based screening tiers, giving the fastest follow-up to the Obese category.",
        "chart": "bq5",
    },
    {
        "title": "Which age group carries the highest average total cholesterol?",
        "why": "Identifies which age band should be prioritized for lipid-panel screening resources.",
        "answer": "Average total cholesterol rises steadily by age group, from 187.66 (18-29) to 198.66 (70+).",
        "insight": "Older age bands carry the highest average lipid burden.",
        "implication": "Lipid screening programs get the most value from prioritizing older age groups.",
        "recommendation": "Allocate proportionally more screening resources to the oldest age groups, without excluding younger ones.",
        "chart": "bq6",
    },
]

# ---------------------------------------------------------------------------
# KPI Analysis (Section 12, cell 96 - real printed table)
# ---------------------------------------------------------------------------
KPI_TABLE = [
    {"kpi": "Population Count", "value": 4155, "unit": "", "desc": "Total individuals in the cleaned, feature-engineered dataset."},
    {"kpi": "Elevated BP Risk Rate", "value": 59.78, "unit": "%", "desc": "Share meeting ACC/AHA elevated-BP threshold (Systolic >= 130 or Diastolic >= 80)."},
    {"kpi": "High Total Cholesterol Prevalence", "value": 0.00, "unit": "%", "desc": "Share with Total_Cholesterol >= 240 mg/dL. Reads 0% because IQR outlier capping (Section 5) already bounded the maximum at 237.83."},
    {"kpi": "Obesity Prevalence", "value": 27.87, "unit": "%", "desc": "Share classified Obese under the WHO BMI standard (BMI >= 30)."},
    {"kpi": "Smoking Prevalence", "value": 29.72, "unit": "%", "desc": "Share of the population who are smokers."},
    {"kpi": "Physical Inactivity Rate", "value": 20.39, "unit": "%", "desc": "Share reporting 'low' physical activity level."},
    {"kpi": "Average Total:HDL Cholesterol Ratio", "value": 5.29, "unit": "", "desc": "Mean of the Total:HDL ratio; a recognized cardiovascular risk score (lower is better)."},
    {"kpi": "Elevated Cholesterol Ratio Prevalence (>5)", "value": 59.81, "unit": "%", "desc": "Share with Total:HDL ratio above the commonly cited elevated-risk cut-off of 5."},
    {"kpi": "Data Completeness Rate", "value": 100.00, "unit": "%", "desc": "Share of all cells with no missing value, after Section 5/8 cleaning."},
]

# ---------------------------------------------------------------------------
# Machine Learning (Sections 13-15)
# ---------------------------------------------------------------------------
ML_TARGET = "BP_Risk_Category (binary: Elevated/High Risk = 1, Normal = 0)"
ML_FEATURES_NUMERIC = ["Age", "BMI", "Total_Cholesterol", "HDL_Cholesterol", "LDL_Cholesterol", "Triglycerides"]
ML_FEATURES_CATEGORICAL = ["Smoking_Status", "Physical_Activity_Level"]

TRAIN_SHAPE = (3324, 8)
TEST_SHAPE = (831, 8)
TARGET_BALANCE_PCT = {"Elevated / High Risk": 59.8, "Normal": 40.2}   # same in train & test (stratified split)
BASELINE_ACCURACY = 0.598                                             # naive majority-class baseline (cell 108)

MODEL_METRICS = {
    "Logistic Regression": {"Accuracy": 0.635, "Precision": 0.646, "Recall": 0.865, "F1-Score": 0.739, "ROC-AUC": 0.639},
    "Random Forest":       {"Accuracy": 0.628, "Precision": 0.635, "Recall": 0.889, "F1-Score": 0.741, "ROC-AUC": 0.640},
}

BEST_MODEL = "Logistic Regression"
BEST_MODEL_NOTE = (
    "Logistic Regression edges out Random Forest on Accuracy, Precision, and ROC-AUC, while Random "
    "Forest has a slightly higher Recall and F1-Score. The gap between the two models is small "
    "(a few tenths of a point to about 1 point depending on the metric). Both models clear the naive "
    "majority-class baseline of 59.8% accuracy, confirming they are learning real signal rather than "
    "just predicting the majority class every time."
)

# Feature importance - read directly off the notebook's real Random Forest /
# Logistic Regression charts (Section 15). Values are chart-read approximations
# (the notebook did not print the underlying Series as text, only plotted it),
# accurate to roughly +/-0.01, and preserve the exact real ranking order.
RF_FEATURE_IMPORTANCE = {
    "BMI": 0.285,
    "Total_Cholesterol": 0.148,
    "LDL_Cholesterol": 0.140,
    "HDL_Cholesterol": 0.133,
    "Triglycerides": 0.128,
    "Age": 0.106,
    "Physical_Activity_Level_moderate": 0.013,
    "Physical_Activity_Level_high": 0.011,
    "Physical_Activity_Level_low": 0.011,
    "Smoking_Status_non-smoker": 0.010,
    "Smoking_Status_smoker": 0.010,
}

LOGREG_COEFFICIENTS = {
    "BMI": 0.46,
    "Smoking_Status_non-smoker": 0.15,
    "Physical_Activity_Level_high": 0.11,
    "Physical_Activity_Level_low": 0.08,
    "Smoking_Status_smoker": 0.075,
    "Total_Cholesterol": 0.055,
    "Age": 0.04,
    "Physical_Activity_Level_moderate": 0.035,
    "HDL_Cholesterol": -0.02,
    "LDL_Cholesterol": -0.03,
    "Triglycerides": -0.045,
}

TOP_FEATURE = "BMI"
FEATURE_IMPORTANCE_NOTE = (
    "BMI is the single strongest, most consistent predictor of elevated BP risk in BOTH models - "
    "the top-ranked feature in Random Forest's importance scores and by far the largest-magnitude "
    "coefficient in Logistic Regression, with a positive sign confirming that higher BMI pushes "
    "predicted risk upward. Agreement between an interpretable linear model and a nonlinear ensemble "
    "model on the top feature is a strong, model-agnostic signal. Feature importance reflects predictive "
    "contribution, not proof of causation."
)

# ---------------------------------------------------------------------------
# Project narrative (for Overview / About pages)
# ---------------------------------------------------------------------------
PROJECT_NAME = "Health Data Analytics & Risk Prediction"
PROJECT_TAGLINE = "From raw health checkup records to actionable blood-pressure-risk insights"
DATASET_DESCRIPTION = (
    "The dataset contains health-related information for 4,157 individuals, including Age, BMI, "
    "Blood Pressure (Systolic and Diastolic), Cholesterol levels (Total, HDL, LDL), Triglycerides, "
    "Smoking Status, and Physical Activity Level."
)
METHODOLOGY_STEPS = [
    "Data Loading", "Data Exploration", "Cleaning (missing values, duplicates, invalid readings, outlier capping)",
    "Feature Engineering", "Exploratory Data Analysis", "KPI Analysis", "Business & Health Questions",
    "Machine Learning (Logistic Regression + Random Forest)", "Model Evaluation & Comparison",
    "Feature Importance", "Deployment",
]
TECHNOLOGIES = ["Python", "Pandas", "NumPy", "Scikit-learn", "Matplotlib / Seaborn (notebook)",
                "Streamlit", "Plotly (deployment)"]
N_BUSINESS_QUESTIONS = len(BUSINESS_QUESTIONS)
N_KPIS = len(KPI_TABLE)
N_ML_MODELS = len(MODEL_METRICS)
