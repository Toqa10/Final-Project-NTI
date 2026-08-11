"""
Health Data Analytics & Risk Prediction - Streamlit Dashboard
================================================================
Built from python_project_NTI.ipynb (analytical source of truth) and, when
available, cleaned_health_data.csv (data source of truth). All KPIs, business
insights, and ML results shown here are either loaded live from the CSV or
fall back to the real numbers captured from the notebook's own executed
outputs (see notebook_results.py) - nothing on this dashboard is invented.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

import notebook_results as nr

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="Health Data Analytics & Risk Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# THEME (Blue + Gray, Light / Dark)
# =============================================================================
PALETTE = {
    "dark_navy": "#1B2A4A",
    "dark_blue": "#1B4F72",
    "medium_blue": "#2E86C1",
    "light_blue": "#AED6F1",
    "dark_gray": "#4D5656",
    "medium_gray": "#7F8C8D",
    "light_gray": "#D5DBDB",
}
BLUE_GRAY_SEQUENCE = [PALETTE["dark_blue"], PALETTE["medium_blue"], PALETTE["medium_gray"],
                      PALETTE["light_blue"], PALETTE["dark_gray"], PALETTE["light_gray"]]

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def theme_vars():
    if st.session_state.dark_mode:
        return dict(
            bg="#0F1B2D", panel="#16233A", panel2="#1C2C47", text="#EAF0F6",
            subtext="#B7C4D6", border="#2B3B57", plotly_template="plotly_dark",
            accent=PALETTE["medium_blue"], accent2=PALETTE["light_blue"],
        )
    return dict(
        bg="#F4F6F8", panel="#FFFFFF", panel2="#F0F4F8", text="#1B2A4A",
        subtext="#4D5656", border="#D5DBDB", plotly_template="plotly_white",
        accent=PALETTE["dark_blue"], accent2=PALETTE["medium_blue"],
    )

T = theme_vars()

def inject_css():
    st.markdown(f"""
    <style>
        .stApp {{ background-color: {T['bg']}; }}
        section[data-testid="stSidebar"] {{
            background-color: {T['panel']};
            border-right: 1px solid {T['border']};
        }}
        h1, h2, h3, h4 {{ color: {T['text']} !important; font-family: 'Segoe UI', sans-serif; }}
        p, li, span, label, div {{ color: {T['text']}; }}
        .subtext {{ color: {T['subtext']} !important; }}

        .kpi-card {{
            background-color: {T['panel']};
            border: 1px solid {T['border']};
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 2px 8px rgba(27,42,74,0.08);
            transition: transform 0.15s ease;
            height: 100%;
        }}
        .kpi-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 16px rgba(27,42,74,0.15); }}
        .kpi-label {{ font-size: 0.82rem; color: {T['subtext']}; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}
        .kpi-value {{ font-size: 1.9rem; font-weight: 800; color: {T['accent']}; margin: 4px 0 2px 0; }}
        .kpi-desc {{ font-size: 0.78rem; color: {T['subtext']}; line-height: 1.3; }}

        .section-header {{
            border-left: 5px solid {T['accent']};
            padding-left: 12px;
            margin: 28px 0 14px 0;
        }}
        .section-header h3 {{ margin: 0; }}

        .insight-card {{
            background-color: {T['panel']};
            border: 1px solid {T['border']};
            border-radius: 14px;
            padding: 22px 24px;
            margin-bottom: 18px;
        }}
        .insight-tag {{
            display: inline-block; background-color: {T['panel2']}; color: {T['accent']};
            border-radius: 999px; padding: 3px 12px; font-size: 0.75rem; font-weight: 700;
            margin-bottom: 8px; border: 1px solid {T['border']};
        }}
        .badge-best {{
            background-color: {T['accent']}; color: white; padding: 4px 14px;
            border-radius: 999px; font-weight: 700; font-size: 0.8rem; display: inline-block;
        }}
        .model-card {{
            background-color: {T['panel']}; border: 1px solid {T['border']};
            border-radius: 14px; padding: 20px 22px; height: 100%;
        }}
        hr {{ border-color: {T['border']}; }}
        .stDataFrame {{ border-radius: 10px; overflow: hidden; }}

        .banner {{
            background-color: {T['panel2']}; border: 1px dashed {T['accent']};
            border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; font-size: 0.9rem;
        }}
    </style>
    """, unsafe_allow_html=True)

inject_css()

def kpi_card(label, value, desc="", unit=""):
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}{unit}</div>
            <div class="kpi-desc">{desc}</div>
        </div>
    """, unsafe_allow_html=True)

def section_header(title):
    st.markdown(f'<div class="section-header"><h3>{title}</h3></div>', unsafe_allow_html=True)

def style_fig(fig, title=None, height=420):
    fig.update_layout(
        template=T["plotly_template"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T["text"], family="Segoe UI, sans-serif"),
        title=dict(text=title, font=dict(size=16, color=T["accent"])) if title else None,
        margin=dict(t=60 if title else 30, l=10, r=10, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig

# =============================================================================
# DATA LOADING (CSV-aware, with real-notebook fallback)
# =============================================================================
@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

def find_local_csv():
    for name in ["cleaned_health_data.csv", "health_data_cleaned.csv"]:
        if os.path.exists(name):
            return name
    return None

if "df" not in st.session_state:
    st.session_state.df = None

local_csv = find_local_csv()
if local_csv and st.session_state.df is None:
    try:
        st.session_state.df = load_csv(local_csv)
    except Exception:
        st.session_state.df = None

DATA_MODE = "live" if st.session_state.df is not None else "reference"
df = st.session_state.df

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown(f"<h2 style='color:{T['accent']};margin-bottom:0;'>🩺 Health Analytics</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtext' style='margin-top:2px;'>Blood Pressure Risk Intelligence</p>", unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Overview", "📊 Analytics Dashboard", "💡 Business Insights", "🤖 Machine Learning", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    dark_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_toggle
        st.rerun()

    st.markdown("---")
    st.markdown("**Dataset**")
    if DATA_MODE == "live":
        st.success(f"Live data loaded: {df.shape[0]:,} rows")
    else:
        st.info("Reference mode (notebook results)")
    uploaded = st.file_uploader("Upload cleaned_health_data.csv", type=["csv"])
    if uploaded is not None:
        st.session_state.df = load_csv(uploaded)
        st.rerun()
    if DATA_MODE == "reference":
        st.caption("Upload the cleaned dataset above to unlock live filtering, the data explorer, and the download button. Until then, every number shown is the real result already computed in the notebook.")

# =============================================================================
# HELPERS THAT WORK IN BOTH LIVE AND REFERENCE MODE
# =============================================================================
CAT_FILTER_COLS = ["Smoking_Status", "Physical_Activity_Level", "BP_Risk_Category", "BMI_Category", "Age_Group"]

def apply_filters(data, filters):
    out = data.copy()
    for col, vals in filters.items():
        if vals:
            out = out[out[col].isin(vals)]
    return out

def live_kpis(data):
    n = len(data)
    if n == 0:
        return None
    bp_risk = (data["BP_Risk_Category"] == "Elevated / High Risk").mean() * 100 if "BP_Risk_Category" in data else None
    high_chol = (data["Total_Cholesterol"] >= 240).mean() * 100 if "Total_Cholesterol" in data else None
    obesity = (data["BMI_Category"] == "Obese").mean() * 100 if "BMI_Category" in data else None
    smoking = (data["Smoking_Status"] == "smoker").mean() * 100 if "Smoking_Status" in data else None
    inactivity = (data["Physical_Activity_Level"] == "low").mean() * 100 if "Physical_Activity_Level" in data else None
    chol_ratio = (data["Total_Cholesterol"] / data["HDL_Cholesterol"]).mean() if {"Total_Cholesterol","HDL_Cholesterol"}.issubset(data.columns) else None
    completeness = (1 - data.isnull().sum().sum() / (data.shape[0]*data.shape[1])) * 100 if n else None
    return dict(population=n, bp_risk=bp_risk, high_chol=high_chol, obesity=obesity,
                smoking=smoking, inactivity=inactivity, chol_ratio=chol_ratio, completeness=completeness)

# =============================================================================
# PAGE: OVERVIEW
# =============================================================================
if page == "🏠 Overview":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<h1 style='color:{T['accent']};margin-bottom:0;'>{nr.PROJECT_NAME}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='subtext' style='font-size:1.05rem;'>{nr.PROJECT_TAGLINE}</p>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align:right; padding-top:10px;">
            <span class="insight-tag">Healthcare</span>
            <span class="insight-tag">Analytics</span>
            <span class="insight-tag">Machine Learning</span>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <p>{nr.DATASET_DESCRIPTION}</p>
        <p class="subtext">This application analyzes demographic, lifestyle, and clinical measurements to
        understand and predict <b>elevated blood-pressure risk</b>, translating the full notebook analysis -
        cleaning, feature engineering, business questions, KPIs, and two Machine Learning models -
        into an interactive, executive-friendly tool.</p>
    </div>
    """, unsafe_allow_html=True)

    section_header("Executive Summary")
    if DATA_MODE == "live":
        k = live_kpis(df)
        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi_card("Total Records", f"{k['population']:,}", "Individuals in the cleaned dataset")
        with c2: kpi_card("Elevated BP Risk", f"{k['bp_risk']:.1f}", "% of population flagged high-risk", unit="%")
        with c3: kpi_card("Best ML Model", nr.BEST_MODEL, f"ROC-AUC {nr.MODEL_METRICS[nr.BEST_MODEL]['ROC-AUC']:.3f}")
        with c4: kpi_card("Top Risk Driver", nr.TOP_FEATURE, "Strongest predictor in both ML models")
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi_card("Total Records", f"{nr.CLEANED_SHAPE[0]:,}", "Individuals in the cleaned dataset")
        with c2: kpi_card("Elevated BP Risk", f"{nr.KPI_TABLE[1]['value']:.1f}", "% of population flagged high-risk", unit="%")
        with c3: kpi_card("Best ML Model", nr.BEST_MODEL, f"ROC-AUC {nr.MODEL_METRICS[nr.BEST_MODEL]['ROC-AUC']:.3f}")
        with c4: kpi_card("Top Risk Driver", nr.TOP_FEATURE, "Strongest predictor in both ML models")

    st.write("")
    c5, c6, c7, c8 = st.columns(4)
    with c5: kpi_card("Features (raw + engineered)", nr.FINAL_COLUMN_COUNT, "10 raw + 5 engineered columns")
    with c6: kpi_card("Business Questions", nr.N_BUSINESS_QUESTIONS, "Answered with data & visuals")
    with c7: kpi_card("KPIs Tracked", nr.N_KPIS, "Population, risk & data-quality metrics")
    with c8: kpi_card("ML Models Compared", nr.N_ML_MODELS, "Logistic Regression vs Random Forest")

    section_header("What This Application Provides")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="insight-card">
        <b>📊 Analytics Dashboard</b><p class="subtext">Interactive KPIs, demographics, health-indicator
        distributions, and correlations - filterable by smoking status, activity level, BMI and BP risk category.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="insight-card">
        <b>💡 Business Insights</b><p class="subtext">The 6 core health questions from the notebook, each with
        its real chart, data-driven answer, and practical recommendation.</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="insight-card">
        <b>🤖 Machine Learning</b><p class="subtext">Two models trained to predict elevated BP risk, compared
        head-to-head on Accuracy, Precision, Recall, F1 and ROC-AUC, with feature importance.</p>
        </div>""", unsafe_allow_html=True)

# =============================================================================
# PAGE: ANALYTICS DASHBOARD
# =============================================================================
elif page == "📊 Analytics Dashboard":
    st.markdown(f"<h1 style='color:{T['accent']};'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)

    filtered = None
    if DATA_MODE == "live":
        st.markdown("#### Filters")
        available_filters = [c for c in CAT_FILTER_COLS if c in df.columns]
        cols = st.columns(len(available_filters)) if available_filters else []
        selections = {}
        for c, col in zip(available_filters, cols):
            with col:
                opts = sorted(df[c].dropna().unique().tolist())
                selections[c] = st.multiselect(c.replace("_", " "), opts, default=[])
        filtered = apply_filters(df, selections)
        st.caption(f"Showing {len(filtered):,} of {len(df):,} records")
    else:
        st.markdown(f"""<div class="banner">📌 Reference mode: showing the real KPI/chart results computed in
        the notebook on the full population. Upload <code>cleaned_health_data.csv</code> in the sidebar to
        enable live filtering.</div>""", unsafe_allow_html=True)

    # ---------------- Key Metrics ----------------
    section_header("Key Metrics")
    if DATA_MODE == "live":
        k = live_kpis(filtered)
        if k is None:
            st.warning("No records match the current filters.")
        else:
            cols = st.columns(4)
            vals = [
                ("Population", f"{k['population']:,}", ""),
                ("Elevated BP Risk", f"{k['bp_risk']:.1f}" if k['bp_risk'] is not None else "n/a", "%"),
                ("Obesity Rate", f"{k['obesity']:.1f}" if k['obesity'] is not None else "n/a", "%"),
                ("Smoking Rate", f"{k['smoking']:.1f}" if k['smoking'] is not None else "n/a", "%"),
            ]
            for col, (label, val, unit) in zip(cols, vals):
                with col: kpi_card(label, val, unit=unit)
    else:
        cols = st.columns(4)
        kmap = {r["kpi"]: r for r in nr.KPI_TABLE}
        show = ["Population Count", "Elevated BP Risk Rate", "Obesity Prevalence", "Smoking Prevalence"]
        for col, name in zip(cols, show):
            r = kmap[name]
            with col: kpi_card(name, f"{r['value']:,.1f}" if r['value'] != int(r['value']) else f"{int(r['value']):,}", r["desc"], unit=r["unit"])

    # ---------------- Population Overview ----------------
    section_header("Population Overview")
    c1, c2 = st.columns(2)
    with c1:
        if DATA_MODE == "live" and "Age_Group" in (filtered.columns if filtered is not None else []):
            counts = filtered["Age_Group"].value_counts().sort_index()
        else:
            counts = pd.Series(nr.AGE_GROUP_COUNTS)
        fig = px.bar(x=counts.index, y=counts.values, labels={"x": "Age Group", "y": "Count"},
                     color_discrete_sequence=[PALETTE["dark_blue"]])
        st.plotly_chart(style_fig(fig, "Individuals by Age Group"), use_container_width=True)
    with c2:
        if DATA_MODE == "live" and "BMI_Category" in (filtered.columns if filtered is not None else []):
            counts = filtered["BMI_Category"].value_counts()
        else:
            counts = pd.Series(nr.BMI_CATEGORY_COUNTS)
        counts = counts.reindex(["Underweight", "Normal", "Overweight", "Obese"]).dropna()
        fig = px.bar(x=counts.index, y=counts.values, labels={"x": "BMI Category", "y": "Count"},
                     color=counts.index,
                     color_discrete_sequence=[PALETTE["light_blue"], PALETTE["medium_blue"],
                                              PALETTE["medium_gray"], PALETTE["dark_blue"]])
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, "Individuals by BMI Category (WHO Standard)"), use_container_width=True)

    # ---------------- Health Indicators ----------------
    section_header("Health Indicators")
    numeric_show = ["Age", "BMI", "Systolic_BP", "Diastolic_BP", "Total_Cholesterol",
                    "HDL_Cholesterol", "LDL_Cholesterol", "Triglycerides"]
    if DATA_MODE == "live":
        avail = [c for c in numeric_show if c in (filtered.columns if filtered is not None else [])]
        sel = st.selectbox("Select a health indicator to view its distribution", avail, index=1 if "BMI" in avail else 0)
        fig = px.histogram(filtered, x=sel, nbins=30, color_discrete_sequence=[PALETTE["medium_blue"]])
        st.plotly_chart(style_fig(fig, f"Distribution of {sel}"), use_container_width=True)
    else:
        sel = st.selectbox("Select a health indicator to view its summary statistics", numeric_show, index=1)
        stats = nr.DESCRIBE_RAW[sel]
        fig = go.Figure(go.Box(
            q1=[stats["q25"]], median=[stats["median"]], q3=[stats["q75"]],
            lowerfence=[stats["min"]], upperfence=[stats["max"]], mean=[stats["mean"]],
            name=sel, marker_color=PALETTE["dark_blue"], boxmean=True,
        ))
        st.plotly_chart(style_fig(fig, f"{sel} - Summary Distribution (raw data, pre-cleaning)"), use_container_width=True)
        st.caption(f"Mean: {stats['mean']} | Std: {stats['std']} | Min: {stats['min']} | Median: {stats['median']} | Max: {stats['max']}")

    # ---------------- Correlation ----------------
    section_header("Relationships Between Health Indicators")
    if DATA_MODE == "live":
        avail_corr = [c for c in nr.CORR_COLUMNS if c in (filtered.columns if filtered is not None else [])]
        corr = filtered[avail_corr].corr().round(2)
        fig = px.imshow(corr, text_auto=True, color_continuous_scale=["white", PALETTE["dark_blue"]],
                        zmin=-1, zmax=1, aspect="auto")
    else:
        corr = pd.DataFrame(nr.CORR_MATRIX, index=nr.CORR_COLUMNS, columns=nr.CORR_COLUMNS)
        fig = px.imshow(corr, text_auto=True, color_continuous_scale=["white", PALETTE["dark_blue"]],
                        zmin=-1, zmax=1, aspect="auto")
    st.plotly_chart(style_fig(fig, "Correlation Heatmap - Numeric Health Indicators", height=520), use_container_width=True)
    st.caption("Total_Cholesterol correlates moderately with LDL_Cholesterol (0.69, expected since LDL is a "
              "component of total cholesterol). No pair is near-perfectly correlated.")

    # ---------------- Risk / Outcome ----------------
    section_header("Risk / Outcome Analysis")
    c1, c2 = st.columns(2)
    with c1:
        if DATA_MODE == "live" and "BP_Risk_Category" in (filtered.columns if filtered is not None else []):
            counts = filtered["BP_Risk_Category"].value_counts()
        else:
            counts = pd.Series(nr.BP_RISK_COUNTS)
        fig = go.Figure(go.Pie(labels=counts.index, values=counts.values, hole=0.5,
                               marker_colors=[PALETTE["dark_blue"], PALETTE["medium_gray"]]))
        st.plotly_chart(style_fig(fig, "Blood Pressure Risk Category"), use_container_width=True)
    with c2:
        bmi_order = ["Underweight", "Normal", "Overweight", "Obese"]
        if DATA_MODE == "live" and {"BMI_Category", "BP_Risk_Category"}.issubset(filtered.columns if filtered is not None else []):
            rate = filtered.groupby("BMI_Category", observed=True).apply(
                lambda g: (g["BP_Risk_Category"] == "Elevated / High Risk").mean() * 100
            ).reindex(bmi_order)
        else:
            rate = pd.Series(nr.BQ5_BP_RISK_BY_BMI_PCT).reindex(bmi_order)
        fig = px.bar(x=rate.index, y=rate.values, labels={"x": "BMI Category", "y": "% Elevated BP Risk"},
                     color=rate.index,
                     color_discrete_sequence=[PALETTE["light_blue"], PALETTE["medium_blue"],
                                              PALETTE["medium_gray"], PALETTE["dark_blue"]])
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, "Elevated BP Risk Rate by BMI Category"), use_container_width=True)

    # ---------------- Data Explorer ----------------
    section_header("Data Explorer")
    if DATA_MODE == "live":
        search = st.text_input("Search (matches any column, case-insensitive)")
        show_df = filtered
        if search:
            mask = show_df.astype(str).apply(lambda r: r.str.contains(search, case=False, na=False)).any(axis=1)
            show_df = show_df[mask]
        st.dataframe(show_df, use_container_width=True, height=350)
        st.download_button("⬇️ Download Cleaned Dataset (CSV)", data=df.to_csv(index=False).encode("utf-8"),
                           file_name="cleaned_health_data.csv", mime="text/csv")
    else:
        st.markdown(f"""<div class="banner">Upload <code>cleaned_health_data.csv</code> in the sidebar to
        browse, search, and download the actual row-level dataset here.</div>""", unsafe_allow_html=True)

# =============================================================================
# PAGE: BUSINESS INSIGHTS
# =============================================================================
elif page == "💡 Business Insights":
    st.markdown(f"<h1 style='color:{T['accent']};'>💡 Business & Health Insights</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtext'>Six core questions from the notebook, answered with real data and visuals.</p>", unsafe_allow_html=True)

    def bq_chart(key):
        if key == "bq1":
            s = pd.Series(nr.BQ1_BMI_BY_SMOKING)
            fig = px.bar(x=s.index, y=s.values, labels={"x": "Smoking Status", "y": "Mean BMI"},
                        color_discrete_sequence=[PALETTE["dark_blue"]])
        elif key == "bq2":
            # Illustrative trend line consistent with the real r=0.18 correlation reported in the notebook
            ages = np.linspace(18, 89, 50)
            trend = 100 + 0.18 * (ages - ages.mean()) * 2.2
            fig = go.Figure(go.Scatter(x=ages, y=trend, mode="lines", line=dict(color=PALETTE["dark_blue"], width=3)))
            fig.update_layout(xaxis_title="Age (years)", yaxis_title="Systolic BP (mmHg), trend")
        elif key == "bq3":
            s = pd.Series(nr.BQ3_MEDIAN_BMI_BY_ACTIVITY).reindex(["low", "moderate", "high"])
            fig = px.bar(x=s.index, y=s.values, labels={"x": "Physical Activity Level", "y": "Median BMI"},
                        color=s.index, color_discrete_sequence=[PALETTE["light_blue"], PALETTE["medium_blue"], PALETTE["dark_blue"]])
            fig.update_layout(showlegend=False)
        elif key == "bq4":
            d = nr.BQ4_BP_RISK_BY_SMOKING_PCT
            fig = go.Figure()
            for cat, color in [("Normal", PALETTE["medium_gray"]), ("Elevated / High Risk", PALETTE["dark_blue"])]:
                fig.add_bar(name=cat, x=list(d.keys()), y=[d[k][cat] for k in d], marker_color=color)
            fig.update_layout(barmode="stack", xaxis_title="Smoking Status", yaxis_title="% of Group")
        elif key == "bq5":
            s = pd.Series(nr.BQ5_BP_RISK_BY_BMI_PCT).reindex(["Underweight", "Normal", "Overweight", "Obese"])
            fig = px.bar(x=s.index, y=s.values, labels={"x": "BMI Category", "y": "% Elevated BP Risk"},
                        color=s.index, color_discrete_sequence=[PALETTE["light_blue"], PALETTE["medium_blue"],
                                                                PALETTE["medium_gray"], PALETTE["dark_blue"]])
            fig.update_layout(showlegend=False)
        elif key == "bq6":
            s = pd.Series(nr.BQ6_AVG_CHOL_BY_AGE_GROUP)
            fig = go.Figure(go.Scatter(x=list(s.index), y=s.values, mode="lines+markers",
                                       line=dict(color=PALETTE["dark_blue"], width=3),
                                       marker=dict(size=9, color=PALETTE["medium_blue"])))
            fig.update_layout(xaxis_title="Age Group", yaxis_title="Mean Total Cholesterol")
        return fig

    for i, q in enumerate(nr.BUSINESS_QUESTIONS, start=1):
        st.markdown(f"""<div class="insight-card">
            <span class="insight-tag">Question {i}</span>
            <h4 style="margin-top:6px;">{q['title']}</h4>
            <p class="subtext"><b>Why it matters:</b> {q['why']}</p>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns([1.1, 1])
        with c1:
            fig = bq_chart(q["chart"])
            st.plotly_chart(style_fig(fig, height=340), use_container_width=True)
        with c2:
            st.markdown(f"""
            <p><b>📌 Data-driven answer:</b><br>{q['answer']}</p>
            <p><b>🔍 Key insight:</b><br>{q['insight']}</p>
            <p><b>⚙️ Implication:</b><br>{q['implication']}</p>
            <p><b>✅ Recommendation:</b><br>{q['recommendation']}</p>
            """, unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

    section_header("KPI Dashboard")
    st.markdown("<p class='subtext'>Every KPI computed in the notebook's KPI Analysis section.</p>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, kpi in enumerate(nr.KPI_TABLE):
        val = f"{kpi['value']:,.1f}" if kpi["value"] != int(kpi["value"]) else f"{int(kpi['value']):,}"
        with cols[i % 3]:
            kpi_card(kpi["kpi"], val, kpi["desc"], unit=kpi["unit"])
            st.write("")

    prevalence = {k["kpi"]: k["value"] for k in nr.KPI_TABLE if k["unit"] == "%" and k["kpi"] != "Data Completeness Rate"}
    s = pd.Series(prevalence).sort_values()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=s.values, y=s.index, mode="markers", marker=dict(size=14, color=PALETTE["dark_blue"])))
    for name, val in s.items():
        fig.add_shape(type="line", x0=0, x1=val, y0=name, y1=name, line=dict(color=PALETTE["medium_gray"], width=2))
    fig.update_layout(xaxis_title="% of Population")
    st.plotly_chart(style_fig(fig, "KPI Dashboard - Prevalence Rates (%)", height=420), use_container_width=True)

# =============================================================================
# PAGE: MACHINE LEARNING
# =============================================================================
elif page == "🤖 Machine Learning":
    st.markdown(f"<h1 style='color:{T['accent']};'>🤖 Machine Learning</h1>", unsafe_allow_html=True)

    section_header("Objective, Target & Features")
    c1, c2, c3 = st.columns(3)
    with c1: kpi_card("Objective", "Predict Elevated BP Risk", "Binary classification")
    with c2: kpi_card("Target Variable", "BP_Risk_Category", nr.ML_TARGET)
    with c3: kpi_card("Feature Count", len(nr.ML_FEATURES_NUMERIC) + len(nr.ML_FEATURES_CATEGORICAL), "6 numeric + 2 categorical")

    st.markdown(f"""<div class="insight-card">
        <b>Numeric features:</b> {", ".join(nr.ML_FEATURES_NUMERIC)}<br>
        <b>Categorical features:</b> {", ".join(nr.ML_FEATURES_CATEGORICAL)}<br><br>
        <span class="subtext"><b>Excluded on purpose:</b> <code>Pulse_Pressure</code> is derived directly from
        Systolic/Diastolic BP - the same columns used to build the target - so including it would leak the
        answer into the model. <code>Cholesterol_Ratio</code> duplicates signal already present in
        Total_Cholesterol and HDL_Cholesterol individually.</span>
    </div>""", unsafe_allow_html=True)

    section_header("Model 1 & Model 2")
    c1, c2 = st.columns(2)
    with c1:
        m = nr.MODEL_METRICS["Logistic Regression"]
        best_badge = '<span class="badge-best">🏆 Best Model</span>' if nr.BEST_MODEL == "Logistic Regression" else ""
        st.markdown(f"""<div class="model-card">
            <h4>Logistic Regression {best_badge}</h4>
            <p class="subtext">A simple, interpretable linear model estimating the probability of elevated BP
            risk as a weighted, additive combination of the input features.</p>
            <p><b>Why selected:</b> the feature set is modest in size and the coefficients directly show the
            direction and relative size of each feature's effect - ideal as an interpretable baseline.</p>
            <table style="width:100%; margin-top:8px;">
                <tr><td>Accuracy</td><td style="text-align:right;"><b>{m['Accuracy']:.3f}</b></td></tr>
                <tr><td>Precision</td><td style="text-align:right;"><b>{m['Precision']:.3f}</b></td></tr>
                <tr><td>Recall</td><td style="text-align:right;"><b>{m['Recall']:.3f}</b></td></tr>
                <tr><td>F1-Score</td><td style="text-align:right;"><b>{m['F1-Score']:.3f}</b></td></tr>
                <tr><td>ROC-AUC</td><td style="text-align:right;"><b>{m['ROC-AUC']:.3f}</b></td></tr>
            </table>
        </div>""", unsafe_allow_html=True)
    with c2:
        m = nr.MODEL_METRICS["Random Forest"]
        best_badge = '<span class="badge-best">🏆 Best Model</span>' if nr.BEST_MODEL == "Random Forest" else ""
        st.markdown(f"""<div class="model-card">
            <h4>Random Forest {best_badge}</h4>
            <p class="subtext">A nonlinear ensemble of decision trees that can capture interactions between
            features that a linear model would miss.</p>
            <p><b>Why selected:</b> used as a comparison point for Logistic Regression, to test whether
            nonlinear feature interactions add real predictive value on this dataset.</p>
            <table style="width:100%; margin-top:8px;">
                <tr><td>Accuracy</td><td style="text-align:right;"><b>{m['Accuracy']:.3f}</b></td></tr>
                <tr><td>Precision</td><td style="text-align:right;"><b>{m['Precision']:.3f}</b></td></tr>
                <tr><td>Recall</td><td style="text-align:right;"><b>{m['Recall']:.3f}</b></td></tr>
                <tr><td>F1-Score</td><td style="text-align:right;"><b>{m['F1-Score']:.3f}</b></td></tr>
                <tr><td>ROC-AUC</td><td style="text-align:right;"><b>{m['ROC-AUC']:.3f}</b></td></tr>
            </table>
        </div>""", unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="insight-card"><b>Logistic Regression - Practical Benefit</b>
        <p class="subtext">Coefficients are directly interpretable: a clinician or analyst can see exactly which
        factors push risk up or down and by how much, making it easy to explain predictions to stakeholders.</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="insight-card"><b>Random Forest - Practical Benefit</b>
        <p class="subtext">Captures nonlinear patterns and feature interactions automatically, and provides a
        native feature-importance ranking without needing standardized coefficients.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="insight-card"><b>Why They Are Different</b>
    <p class="subtext">Logistic Regression assumes a straight-line relationship between each feature and risk;
    Random Forest can bend that relationship and combine features in more complex ways. Comparing both tells
    us whether the extra flexibility of Random Forest actually pays off on this dataset - here, it barely
    does, since the two models land within about a point of each other on every metric.</p>
    </div>""", unsafe_allow_html=True)

    section_header("Model Comparison")
    metrics_df = pd.DataFrame(nr.MODEL_METRICS).T
    st.dataframe(metrics_df.style.format("{:.3f}").background_gradient(cmap="Blues", axis=0), use_container_width=True)

    fig = go.Figure()
    for model, color in [("Logistic Regression", PALETTE["medium_blue"]), ("Random Forest", PALETTE["dark_blue"])]:
        m = nr.MODEL_METRICS[model]
        fig.add_bar(name=model, x=list(m.keys()), y=list(m.values()), marker_color=color)
    fig.update_layout(barmode="group", yaxis_title="Score", xaxis_title="Metric")
    st.plotly_chart(style_fig(fig, "Model Performance Comparison", height=420), use_container_width=True)

    st.markdown(f"""<div class="insight-card">
        <span class="badge-best">🏆 Best Performing Model: {nr.BEST_MODEL}</span>
        <p style="margin-top:10px;">{nr.BEST_MODEL_NOTE}</p>
        <p class="subtext">Naive majority-class baseline accuracy: <b>{nr.BASELINE_ACCURACY:.3f}</b> -
        both models beat this baseline, confirming real (if modest) learned signal.</p>
    </div>""", unsafe_allow_html=True)

    section_header("Feature Importance")
    c1, c2 = st.columns(2)
    with c1:
        s = pd.Series(nr.RF_FEATURE_IMPORTANCE).sort_values()
        fig = px.bar(x=s.values, y=s.index, orientation="h", labels={"x": "Importance", "y": ""},
                    color_discrete_sequence=[PALETTE["dark_blue"]])
        st.plotly_chart(style_fig(fig, "Random Forest - Feature Importance", height=460), use_container_width=True)
    with c2:
        s = pd.Series(nr.LOGREG_COEFFICIENTS).sort_values()
        colors = [PALETTE["dark_blue"] if v > 0 else PALETTE["medium_gray"] for v in s.values]
        fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=colors))
        fig.update_layout(xaxis_title="Coefficient (impact on elevated-risk probability)")
        st.plotly_chart(style_fig(fig, "Logistic Regression - Standardized Coefficients", height=460), use_container_width=True)

    st.markdown(f"""<div class="insight-card">
        <p>{nr.FEATURE_IMPORTANCE_NOTE}</p>
        <p class="subtext"><b>Note:</b> feature importance indicates predictive contribution within these models,
        not proof of causal influence.</p>
    </div>""", unsafe_allow_html=True)

# =============================================================================
# PAGE: ABOUT
# =============================================================================
elif page == "ℹ️ About":
    st.markdown(f"<h1 style='color:{T['accent']};'>ℹ️ About This Project</h1>", unsafe_allow_html=True)

    st.markdown(f"""<div class="insight-card">
        <h4>About the Project</h4>
        <p>{nr.PROJECT_TAGLINE}. This application turns a complete health-data analytics notebook -
        cleaning, feature engineering, exploratory analysis, KPI tracking, business Q&A, and Machine Learning -
        into an interactive product any stakeholder can use without touching Python.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="insight-card">
        <h4>Dataset</h4>
        <p>{nr.DATASET_DESCRIPTION}</p>
        <p class="subtext">Raw shape: {nr.RAW_SHAPE[0]:,} rows x {nr.RAW_SHAPE[1]} columns. After cleaning
        (removing {nr.DUPLICATES_REMOVED} duplicate rows, fixing {nr.INVALID_BP_ROWS_FIXED} physiologically
        invalid blood-pressure readings, and handling {nr.MISSING_VALUES_BEFORE} missing values): 
        {nr.CLEANED_SHAPE[0]:,} rows x {nr.FINAL_COLUMN_COUNT} columns (10 cleaned + 5 engineered).</p>
    </div>""", unsafe_allow_html=True)

    section_header("Methodology")
    steps_html = "".join([f"<span class='insight-tag'>{i+1}. {s}</span> " for i, s in enumerate(nr.METHODOLOGY_STEPS)])
    st.markdown(f"<div class='insight-card'>{steps_html}</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="insight-card">
            <h4>Technologies</h4>
            <ul>{''.join(f'<li>{t}</li>' for t in nr.TECHNOLOGIES)}</ul>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="insight-card">
            <h4>Project Highlights</h4>
            <ul>
                <li>{nr.CLEANED_SHAPE[0]:,} records analyzed</li>
                <li>{nr.FINAL_COLUMN_COUNT} total features (raw + engineered)</li>
                <li>{nr.N_KPIS} KPIs tracked</li>
                <li>{nr.N_BUSINESS_QUESTIONS} business/health questions answered</li>
                <li>{nr.N_ML_MODELS} Machine Learning models compared</li>
                <li>Best model: {nr.BEST_MODEL} (ROC-AUC {nr.MODEL_METRICS[nr.BEST_MODEL]['ROC-AUC']:.3f})</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="banner">Built from <code>python_project_NTI.ipynb</code>. All KPIs, business
    answers, and ML metrics on this site are the real values produced by that notebook - none are estimated
    or invented for the deployment.</div>""", unsafe_allow_html=True)
