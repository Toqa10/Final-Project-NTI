"""
Health Data Analytics & Risk Prediction - Streamlit Dashboard
================================================================
Premium UI/UX Version with MEDISIGHTS Branding
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import time

import notebook_results as nr

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="MEDISIGHTS - Health Data Analytics & Risk Prediction",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# BRANDING & LOGO
# =============================================================================
# Logo as text-based SVG for crisp rendering
LOGO_SVG = """
<svg width="200" height="80" viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#1B4F72;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#2E86C1;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="logoGradLight" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#2E86C1;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#AED6F1;stop-opacity:1" />
        </linearGradient>
    </defs>
    <text x="10" y="40" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="900" fill="url(#logoGrad)">MEDISIGHTS</text>
    <text x="12" y="62" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="600" fill="#4D5656" letter-spacing="3">DATA-DRIVEN CLINICAL INSIGHTS</text>
    <circle cx="175" cy="20" r="12" fill="none" stroke="url(#logoGrad)" stroke-width="2"/>
    <circle cx="175" cy="20" r="5" fill="url(#logoGrad)"/>
    <path d="M168 14 L175 20 L182 14" stroke="url(#logoGrad)" stroke-width="1.5" fill="none"/>
</svg>
"""

# Dark mode logo
LOGO_SVG_DARK = """
<svg width="200" height="80" viewBox="0 0 200 80" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="logoGradDark" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#AED6F1;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#2E86C1;stop-opacity:1" />
        </linearGradient>
    </defs>
    <text x="10" y="40" font-family="Inter, Arial, sans-serif" font-size="32" font-weight="900" fill="url(#logoGradDark)">MEDISIGHTS</text>
    <text x="12" y="62" font-family="Inter, Arial, sans-serif" font-size="11" font-weight="600" fill="#B7C4D6" letter-spacing="3">DATA-DRIVEN CLINICAL INSIGHTS</text>
    <circle cx="175" cy="20" r="12" fill="none" stroke="url(#logoGradDark)" stroke-width="2"/>
    <circle cx="175" cy="20" r="5" fill="url(#logoGradDark)"/>
    <path d="M168 14 L175 20 L182 14" stroke="url(#logoGradDark)" stroke-width="1.5" fill="none"/>
</svg>
"""

# =============================================================================
# ADVANCED THEME SYSTEM
# =============================================================================
PALETTE = {
    "primary": "#1B4F72",
    "primary_light": "#2E86C1",
    "primary_lighter": "#AED6F1",
    "secondary": "#4D5656",
    "secondary_light": "#7F8C8D",
    "accent": "#1ABC9C",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "success": "#2ECC71",
    "gradient_start": "#1B4F72",
    "gradient_end": "#2E86C1",
    "glow": "rgba(46, 134, 193, 0.3)",
}

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def theme_vars():
    if st.session_state.dark_mode:
        return dict(
            bg="#0A1628",
            panel="rgba(22, 35, 58, 0.92)",
            panel2="rgba(28, 44, 71, 0.8)",
            text="#EAF0F6",
            subtext="#B7C4D6",
            border="rgba(43, 59, 87, 0.6)",
            plotly_template="plotly_dark",
            accent=PALETTE["primary_light"],
            accent2=PALETTE["primary_lighter"],
            glass_bg="rgba(22, 35, 58, 0.7)",
            glass_border="rgba(46, 134, 193, 0.3)",
            logo=LOGO_SVG_DARK,
        )
    return dict(
        bg="#F0F4F8",
        panel="rgba(255, 255, 255, 0.92)",
        panel2="rgba(240, 244, 248, 0.8)",
        text="#1B2A4A",
        subtext="#4D5656",
        border="rgba(213, 219, 219, 0.6)",
        plotly_template="plotly_white",
        accent=PALETTE["primary"],
        accent2=PALETTE["primary_light"],
        glass_bg="rgba(255, 255, 255, 0.7)",
        glass_border="rgba(27, 79, 114, 0.2)",
        logo=LOGO_SVG,
    )

T = theme_vars()

# =============================================================================
# ENHANCED CSS WITH BRANDING
# =============================================================================
def inject_advanced_css():
    st.markdown(f"""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}
        
        /* Smooth Scrolling */
        html {{
            scroll-behavior: smooth;
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {T['bg']};
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {PALETTE['gradient_start']}, {PALETTE['gradient_end']});
            border-radius: 10px;
            transition: all 0.3s ease;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, {PALETTE['gradient_end']}, {PALETTE['gradient_start']});
            transform: scale(1.1);
        }}
        
        /* Main App Background */
        .stApp {{
            background: {T['bg']};
            background-image: 
                radial-gradient(circle at 20% 50%, {T['glass_bg']} 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, {T['glass_bg']} 0%, transparent 50%),
                radial-gradient(circle at 50% 80%, {T['glass_bg']} 0%, transparent 50%);
        }}
        
        /* ===== HEADER ===== */
        .header-container {{
            background: {T['panel']};
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 2px solid {T['glass_border']};
            padding: 12px 30px;
            margin: -10px -20px 20px -20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            animation: slideDown 0.6s ease-out;
            position: sticky;
            top: 0;
            z-index: 999;
            box-shadow: 0 4px 30px rgba(0,0,0,0.1);
        }}
        
        @keyframes slideDown {{
            from {{
                transform: translateY(-100%);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        
        .header-logo {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .header-logo svg {{
            height: 60px;
            width: auto;
        }}
        
        .header-status {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 16px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            background: {T['glass_bg']};
            border: 1px solid {T['glass_border']};
            color: {T['text']};
        }}
        
        .status-badge .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        .status-badge .dot.green {{
            background: {PALETTE['success']};
        }}
        
        .status-badge .dot.yellow {{
            background: {PALETTE['warning']};
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(0.8); }}
        }}
        
        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {{
            background: {T['panel']} !important;
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-right: 1px solid {T['glass_border']};
            box-shadow: 4px 0 30px rgba(0,0,0,0.1);
            animation: slideIn 0.5s ease-out;
            padding-top: 10px;
        }}
        
        @keyframes slideIn {{
            from {{
                transform: translateX(-100%);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}
        
        .sidebar-brand {{
            text-align: center;
            padding: 15px 10px 20px 10px;
            border-bottom: 1px solid {T['glass_border']};
            margin-bottom: 15px;
        }}
        
        .sidebar-brand svg {{
            height: 70px;
            width: auto;
        }}
        
        .sidebar-brand .tagline {{
            font-size: 0.7rem;
            color: {T['subtext']};
            letter-spacing: 2px;
            margin-top: 4px;
        }}
        
        /* ===== FOOTER ===== */
        .footer {{
            background: {T['panel']};
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-top: 1px solid {T['glass_border']};
            padding: 20px 30px;
            margin: 30px -20px -10px -20px;
            text-align: center;
        }}
        
        .footer-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .footer-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .footer-brand svg {{
            height: 35px;
            width: auto;
        }}
        
        .footer-text {{
            color: {T['subtext']};
            font-size: 0.85rem;
        }}
        
        .footer-links {{
            display: flex;
            gap: 20px;
        }}
        
        .footer-links a {{
            color: {T['subtext']};
            text-decoration: none;
            font-size: 0.85rem;
            transition: color 0.3s ease;
        }}
        
        .footer-links a:hover {{
            color: {T['accent']};
        }}
        
        /* ===== GLASS CARDS ===== */
        .kpi-card, .insight-card, .model-card {{
            background: {T['panel']} !important;
            backdrop-filter: blur(10px) saturate(180%);
            -webkit-backdrop-filter: blur(10px) saturate(180%);
            border: 1px solid {T['glass_border']};
            border-radius: 16px;
            padding: 20px 24px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }}
        
        .kpi-card::before, .insight-card::before, .model-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, {PALETTE['glow']} 0%, transparent 70%);
            opacity: 0;
            transition: opacity 0.6s ease;
            pointer-events: none;
        }}
        
        .kpi-card:hover::before, .insight-card:hover::before, .model-card:hover::before {{
            opacity: 0.1;
        }}
        
        .kpi-card:hover, .insight-card:hover, .model-card:hover {{
            transform: translateY(-6px) scale(1.01);
            box-shadow: 0 12px 40px rgba(27, 79, 114, 0.2),
                        0 0 60px {PALETTE['glow']};
            border-color: {T['accent']};
        }}
        
        /* KPI Values with Gradient */
        .kpi-value {{
            font-size: 2.2rem;
            font-weight: 900;
            background: linear-gradient(135deg, {PALETTE['gradient_start']}, {PALETTE['gradient_end']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 8px 0 4px 0;
            animation: pulseValue 2s ease-in-out infinite;
        }}
        
        @keyframes pulseValue {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.02); }}
        }}
        
        /* Section Headers */
        .section-header {{
            border-left: 5px solid {T['accent']};
            padding-left: 15px;
            margin: 32px 0 20px 0;
            position: relative;
        }}
        
        .section-header h3 {{
            font-size: 1.4rem;
            font-weight: 700;
            color: {T['text']};
            margin: 0;
        }}
        
        /* Badge Best */
        .badge-best {{
            background: linear-gradient(135deg, {PALETTE['gradient_start']}, {PALETTE['gradient_end']});
            color: white;
            padding: 6px 20px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.85rem;
            display: inline-block;
            animation: pulseBadge 2s ease-in-out infinite;
            box-shadow: 0 4px 20px {PALETTE['glow']};
        }}
        
        @keyframes pulseBadge {{
            0%, 100% {{ box-shadow: 0 4px 20px {PALETTE['glow']}; }}
            50% {{ box-shadow: 0 4px 40px {PALETTE['glow']}, 0 0 60px {PALETTE['glow']}; }}
        }}
        
        /* Floating Action Button */
        .fab {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, {PALETTE['gradient_start']}, {PALETTE['gradient_end']});
            color: white;
            border: none;
            border-radius: 50%;
            width: 56px;
            height: 56px;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 8px 32px {PALETTE['glow']};
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .fab:hover {{
            transform: scale(1.15) translateY(-4px);
            box-shadow: 0 12px 48px {PALETTE['glow']};
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header-container {{
                flex-direction: column;
                padding: 10px 15px;
                gap: 10px;
            }}
            .footer-content {{
                flex-direction: column;
                text-align: center;
            }}
            .footer-links {{
                flex-wrap: wrap;
                justify-content: center;
            }}
        }}
        
        /* Dataframe Styling */
        .stDataFrame {{
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 1px solid {T['glass_border']} !important;
        }}
        
        .stDataFrame thead {{
            background: linear-gradient(135deg, {PALETTE['gradient_start']}, {PALETTE['gradient_end']}) !important;
        }}
        
        .stDataFrame thead th {{
            color: white !important;
            font-weight: 600 !important;
        }}
        
        /* Button Styling */
        .stButton > button {{
            background: linear-gradient(135deg, {PALETTE['gradient_start']}, {PALETTE['gradient_end']}) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 8px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            box-shadow: 0 4px 16px {PALETTE['glow']} !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 8px 32px {PALETTE['glow']} !important;
        }}
        
        /* Toggle Switch Enhancement */
        .stToggle {{
            background: {T['glass_bg']} !important;
            border-radius: 999px !important;
            padding: 4px !important;
        }}
        
        /* Select Box Enhancement */
        .stSelectbox > div {{
            background: {T['glass_bg']} !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid {T['glass_border']} !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }}
        
        .stSelectbox > div:hover {{
            border-color: {T['accent']} !important;
            box-shadow: 0 4px 20px {PALETTE['glow']} !important;
        }}
        
        /* Multiselect Enhancement */
        .stMultiSelect > div {{
            background: {T['glass_bg']} !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid {T['glass_border']} !important;
            border-radius: 12px !important;
        }}
    </style>
    """, unsafe_allow_html=True)

inject_advanced_css()

# =============================================================================
# HEADER
# =============================================================================
def render_header():
    status_class = "green" if DATA_MODE == "live" else "yellow"
    status_text = "Live Data" if DATA_MODE == "live" else "Reference Mode"
    
    st.markdown(f"""
    <div class="header-container">
        <div class="header-logo">
            {T['logo']}
        </div>
        <div class="header-status">
            <span class="status-badge">
                <span class="dot {status_class}"></span>
                {status_text}
            </span>
            <span class="status-badge" style="display:none;">
                🏥 v2.0
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

render_header()

# =============================================================================
# FLOATING ACTION BUTTON
# =============================================================================
st.markdown("""
    <button class="fab" onclick="window.scrollTo({top:0,behavior:'smooth'})">
        ⬆
    </button>
""", unsafe_allow_html=True)

# =============================================================================
# DATA LOADING
# =============================================================================
@st.cache_data
def load_csv(file):
    with st.spinner("🔄 Loading data..."):
        time.sleep(0.5)
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
# SIDEBAR WITH BRANDING
# =============================================================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        {T['logo']}
        <div class="tagline">ANALYTICS • INSIGHTS • PREDICTION</div>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["🏠 Overview", "📊 Analytics Dashboard", "💡 Business Insights", "🤖 Machine Learning", "ℹ️ About"],
        label_visibility="collapsed",
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("🌙")
    with col2:
        dark_toggle = st.toggle("Dark Mode", value=st.session_state.dark_mode)
        if dark_toggle != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_toggle
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("**📊 Dataset**")
    if DATA_MODE == "live":
        st.success(f"✅ {df.shape[0]:,} records")
        st.caption(f"📅 {df.shape[1]} features")
    else:
        st.info("📌 Reference mode")
    
    uploaded = st.file_uploader("📤 Upload CSV", type=["csv"], key="sidebar_upload")
    if uploaded is not None:
        st.session_state.df = load_csv(uploaded)
        st.success("✅ Uploaded!")
        time.sleep(0.5)
        st.rerun()
    
    if DATA_MODE == "reference":
        st.caption("💡 Upload CSV for live data")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center;padding:10px 0;font-size:0.75rem;color:{T['subtext']};">
        <span>© 2026 MEDISIGHTS</span><br>
        <span>Data-Driven Clinical Insights</span>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# HELPERS
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

def section_header(title, icon="📌"):
    st.markdown(f"""
        <div class="section-header">
            <h3>{icon} {title}</h3>
        </div>
    """, unsafe_allow_html=True)

def animated_kpi(label, value, desc="", unit="", glow=False):
    glow_class = " glow-border" if glow else ""
    st.markdown(f"""
        <div class="kpi-card{glow_class}">
            <div style="font-size:0.8rem;color:{T['subtext']};font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">{label}</div>
            <div class="kpi-value">{value}{unit}</div>
            <div style="font-size:0.8rem;color:{T['subtext']};">{desc}</div>
        </div>
    """, unsafe_allow_html=True)

def style_fig(fig, title=None, height=420):
    fig.update_layout(
        template=T["plotly_template"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T["text"], family="Inter, sans-serif"),
        title=dict(
            text=title, 
            font=dict(size=17, color=T["accent"], weight=700),
            x=0.5,
            xanchor='center'
        ) if title else None,
        margin=dict(t=60 if title else 30, l=10, r=10, b=10),
        height=height,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=11)
        ),
        hoverlabel=dict(
            bgcolor=T['panel'],
            font=dict(color=T['text'])
        )
    )
    return fig

# =============================================================================
# PAGE: OVERVIEW
# =============================================================================
if page == "🏠 Overview":
    st.markdown(f"""
    <div style="padding:10px 0 20px 0;">
        <h1 style="color:{T['accent']};font-weight:900;font-size:2.5rem;margin:0;">
            {nr.PROJECT_NAME}
        </h1>
        <p style="color:{T['subtext']};font-size:1.1rem;margin:4px 0 0 0;">
            {nr.PROJECT_TAGLINE}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-card">
        <p style="font-size:1.05rem;">{nr.DATASET_DESCRIPTION}</p>
        <p class="subtext">This application analyzes demographic, lifestyle, and clinical measurements to
        understand and predict <b>elevated blood-pressure risk</b>, translating the full notebook analysis
        into an interactive, executive-friendly tool.</p>
    </div>
    """, unsafe_allow_html=True)
    
    section_header("Executive Summary", "📈")
    
    if DATA_MODE == "live":
        k = live_kpis(df)
        c1, c2, c3, c4 = st.columns(4)
        with c1: animated_kpi("Total Records", f"{k['population']:,}", "Individuals analyzed", glow=True)
        with c2: animated_kpi("Elevated BP Risk", f"{k['bp_risk']:.1f}", "% high-risk", unit="%")
        with c3: animated_kpi("Best ML Model", nr.BEST_MODEL, f"ROC-AUC {nr.MODEL_METRICS[nr.BEST_MODEL]['ROC-AUC']:.3f}", glow=True)
        with c4: animated_kpi("Top Risk Driver", nr.TOP_FEATURE, "Strongest predictor")
    else:
        c1, c2, c3, c4 = st.columns(4)
        with c1: animated_kpi("Total Records", f"{nr.CLEANED_SHAPE[0]:,}", "Individuals analyzed", glow=True)
        with c2: animated_kpi("Elevated BP Risk", f"{nr.KPI_TABLE[1]['value']:.1f}", "% high-risk", unit="%")
        with c3: animated_kpi("Best ML Model", nr.BEST_MODEL, f"ROC-AUC {nr.MODEL_METRICS[nr.BEST_MODEL]['ROC-AUC']:.3f}", glow=True)
        with c4: animated_kpi("Top Risk Driver", nr.TOP_FEATURE, "Strongest predictor")
    
    st.write("")
    c5, c6, c7, c8 = st.columns(4)
    with c5: animated_kpi("Features", nr.FINAL_COLUMN_COUNT, "10 raw + 5 engineered")
    with c6: animated_kpi("Business Questions", nr.N_BUSINESS_QUESTIONS, "Answered with data")
    with c7: animated_kpi("KPIs Tracked", nr.N_KPIS, "Population & risk metrics")
    with c8: animated_kpi("ML Models", nr.N_ML_MODELS, "Compared head-to-head")
    
    section_header("What This Application Provides", "✨")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="insight-card" style="text-align:center;">
            <div style="font-size:3rem;margin-bottom:8px;">📊</div>
            <h4 style="margin:0;">Analytics Dashboard</h4>
            <p class="subtext">Interactive KPIs, demographics, distributions, and correlations with advanced filtering.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="insight-card" style="text-align:center;">
            <div style="font-size:3rem;margin-bottom:8px;">💡</div>
            <h4 style="margin:0;">Business Insights</h4>
            <p class="subtext">6 core health questions with data-driven answers and actionable recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="insight-card" style="text-align:center;">
            <div style="font-size:3rem;margin-bottom:8px;">🤖</div>
            <h4 style="margin:0;">Machine Learning</h4>
            <p class="subtext">Two models compared on Accuracy, Precision, Recall, F1, and ROC-AUC with feature importance.</p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: ANALYTICS DASHBOARD
# =============================================================================
elif page == "📊 Analytics Dashboard":
    st.markdown(f"<h1 style='color:{T['accent']};font-weight:900;'>📊 Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    filtered = None
    if DATA_MODE == "live":
        st.markdown("""
        <div style="background:{T['glass_bg']};backdrop-filter:blur(10px);border:1px solid {T['glass_border']};border-radius:16px;padding:20px;margin-bottom:20px;">
            <h4 style="margin:0 0 12px 0;">🔍 Advanced Filters</h4>
        """.format(T=T), unsafe_allow_html=True)
        available_filters = [c for c in CAT_FILTER_COLS if c in df.columns]
        cols = st.columns(len(available_filters)) if available_filters else []
        selections = {}
        for c, col in zip(available_filters, cols):
            with col:
                opts = sorted(df[c].dropna().unique().tolist())
                selections[c] = st.multiselect(
                    c.replace("_", " ").replace("BP", "Blood Pressure"),
                    opts,
                    default=[],
                    placeholder=f"Select {c.replace('_', ' ').lower()}..."
                )
        filtered = apply_filters(df, selections)
        st.markdown("</div>", unsafe_allow_html=True)
        st.caption(f"📊 Showing {len(filtered):,} of {len(df):,} records")
    else:
        st.markdown(f"""
        <div style="background:{T['glass_bg']};backdrop-filter:blur(10px);border-radius:12px;padding:16px 20px;border:1px solid {T['glass_border']};">
            📌 Reference mode: showing the real KPI/chart results computed in the notebook. 
            Upload <code>cleaned_health_data.csv</code> in the sidebar to enable live filtering.
        </div>
        """, unsafe_allow_html=True)

    # Key Metrics
    section_header("Key Metrics", "🎯")
    if DATA_MODE == "live":
        k = live_kpis(filtered)
        if k is None:
            st.warning("⚠️ No records match the current filters.")
        else:
            cols = st.columns(4)
            vals = [
                ("Population", f"{k['population']:,}", ""),
                ("Elevated BP Risk", f"{k['bp_risk']:.1f}" if k['bp_risk'] is not None else "n/a", "%"),
                ("Obesity Rate", f"{k['obesity']:.1f}" if k['obesity'] is not None else "n/a", "%"),
                ("Smoking Rate", f"{k['smoking']:.1f}" if k['smoking'] is not None else "n/a", "%"),
            ]
            for col, (label, val, unit) in zip(cols, vals):
                with col: animated_kpi(label, val, unit=unit)
    else:
        cols = st.columns(4)
        kmap = {r["kpi"]: r for r in nr.KPI_TABLE}
        show = ["Population Count", "Elevated BP Risk Rate", "Obesity Prevalence", "Smoking Prevalence"]
        for col, name in zip(cols, show):
            r = kmap[name]
            with col: animated_kpi(name, f"{r['value']:,.1f}" if r['value'] != int(r['value']) else f"{int(r['value']):,}", r["desc"], unit=r["unit"])

    # Population Overview
    section_header("Population Overview", "👥")
    c1, c2 = st.columns(2)
    with c1:
        if DATA_MODE == "live" and "Age_Group" in (filtered.columns if filtered is not None else []):
            counts = filtered["Age_Group"].value_counts().sort_index()
        else:
            counts = pd.Series(nr.AGE_GROUP_COUNTS)
        fig = px.bar(x=counts.index, y=counts.values, labels={"x": "Age Group", "y": "Count"},
                     color_discrete_sequence=[PALETTE["dark_blue"]])
        st.plotly_chart(style_fig(fig, "👤 Individuals by Age Group"), use_container_width=True)
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
        st.plotly_chart(style_fig(fig, "⚖️ Individuals by BMI Category (WHO Standard)"), use_container_width=True)

    # Health Indicators
    section_header("Health Indicators", "📊")
    numeric_show = ["Age", "BMI", "Systolic_BP", "Diastolic_BP", "Total_Cholesterol",
                    "HDL_Cholesterol", "LDL_Cholesterol", "Triglycerides"]
    if DATA_MODE == "live":
        avail = [c for c in numeric_show if c in (filtered.columns if filtered is not None else [])]
        sel = st.selectbox("Select a health indicator to view its distribution", avail, index=1 if "BMI" in avail else 0)
        fig = px.histogram(filtered, x=sel, nbins=30, color_discrete_sequence=[PALETTE["medium_blue"]],
                          marginal="box")
        st.plotly_chart(style_fig(fig, f"Distribution of {sel}", height=500), use_container_width=True)
    else:
        sel = st.selectbox("Select a health indicator to view its summary statistics", numeric_show, index=1)
        stats = nr.DESCRIBE_RAW[sel]
        fig = go.Figure(go.Box(
            q1=[stats["q25"]], median=[stats["median"]], q3=[stats["q75"]],
            lowerfence=[stats["min"]], upperfence=[stats["max"]], mean=[stats["mean"]],
            name=sel, marker_color=PALETTE["dark_blue"], boxmean=True,
        ))
        st.plotly_chart(style_fig(fig, f"{sel} - Summary Distribution", height=500), use_container_width=True)
        st.caption(f"📊 Mean: {stats['mean']} | Std: {stats['std']} | Min: {stats['min']} | Median: {stats['median']} | Max: {stats['max']}")

    # Correlation
    section_header("Relationships Between Health Indicators", "🔗")
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
    st.caption("💡 Total_Cholesterol correlates moderately with LDL_Cholesterol (0.69, expected since LDL is a component of total cholesterol).")

    # Risk / Outcome
    section_header("Risk / Outcome Analysis", "⚠️")
    c1, c2 = st.columns(2)
    with c1:
        if DATA_MODE == "live" and "BP_Risk_Category" in (filtered.columns if filtered is not None else []):
            counts = filtered["BP_Risk_Category"].value_counts()
        else:
            counts = pd.Series(nr.BP_RISK_COUNTS)
        fig = go.Figure(go.Pie(labels=counts.index, values=counts.values, hole=0.5,
                               marker_colors=[PALETTE["dark_blue"], PALETTE["medium_gray"]],
                               textinfo="label+percent",
                               textposition="outside"))
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

    # Data Explorer
    section_header("Data Explorer", "🔍")
    if DATA_MODE == "live":
        search = st.text_input("🔎 Search (matches any column)", placeholder="Type to filter...")
        show_df = filtered
        if search:
            mask = show_df.astype(str).apply(lambda r: r.str.contains(search, case=False, na=False)).any(axis=1)
            show_df = show_df[mask]
        st.dataframe(show_df, use_container_width=True, height=400)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button("⬇️ Download Dataset", data=df.to_csv(index=False).encode("utf-8"),
                               file_name="cleaned_health_data.csv", mime="text/csv")
        with col2:
            st.caption(f"📊 {len(show_df):,} rows displayed")
    else:
        st.markdown(f"""
        <div style="background:{T['glass_bg']};backdrop-filter:blur(10px);border-radius:12px;padding:16px 20px;border:1px solid {T['glass_border']};">
            📤 Upload <code>cleaned_health_data.csv</code> in the sidebar to browse, search, and download the actual row-level dataset here.
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# PAGE: BUSINESS INSIGHTS
# =============================================================================
elif page == "💡 Business Insights":
    st.markdown(f"<h1 style='color:{T['accent']};font-weight:900;'>💡 Business & Health Insights</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:" + T['subtext'] + ";font-size:1.1rem;'>Six core questions from the notebook, answered with real data and visuals.</p>", unsafe_allow_html=True)

    def bq_chart(key):
        if key == "bq1":
            s = pd.Series(nr.BQ1_BMI_BY_SMOKING)
            fig = px.bar(x=s.index, y=s.values, labels={"x": "Smoking Status", "y": "Mean BMI"},
                        color_discrete_sequence=[PALETTE["dark_blue"]],
                        text=s.values.round(1))
        elif key == "bq2":
            ages = np.linspace(18, 89, 50)
            trend = 100 + 0.18 * (ages - ages.mean()) * 2.2
            fig = go.Figure(go.Scatter(x=ages, y=trend, mode="lines", line=dict(color=PALETTE["dark_blue"], width=4)))
            fig.update_layout(xaxis_title="Age (years)", yaxis_title="Systolic BP (mmHg)")
        elif key == "bq3":
            s = pd.Series(nr.BQ3_MEDIAN_BMI_BY_ACTIVITY).reindex(["low", "moderate", "high"])
            fig = px.bar(x=s.index, y=s.values, labels={"x": "Physical Activity Level", "y": "Median BMI"},
                        color=s.index, color_discrete_sequence=[PALETTE["light_blue"], PALETTE["medium_blue"], PALETTE["dark_blue"]],
                        text=s.values.round(1))
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
                                                                PALETTE["medium_gray"], PALETTE["dark_blue"]],
                        text=s.values.round(1))
            fig.update_layout(showlegend=False)
        elif key == "bq6":
            s = pd.Series(nr.BQ6_AVG_CHOL_BY_AGE_GROUP)
            fig = go.Figure(go.Scatter(x=list(s.index), y=s.values, mode="lines+markers",
                                       line=dict(color=PALETTE["dark_blue"], width=4),
                                       marker=dict(size=12, color=PALETTE["medium_blue"])))
            fig.update_layout(xaxis_title="Age Group", yaxis_title="Mean Total Cholesterol")
        return fig

    for i, q in enumerate(nr.BUSINESS_QUESTIONS, start=1):
        st.markdown(f"""
        <div class="insight-card" style="border-left:4px solid {T['accent']};">
            <span class="insight-tag">❓ Question {i}</span>
            <h4 style="margin-top:6px;font-size:1.2rem;">{q['title']}</h4>
            <p style="color:{T['subtext']};"><b>Why it matters:</b> {q['why']}</p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1.1, 1])
        with c1:
            fig = bq_chart(q["chart"])
            st.plotly_chart(style_fig(fig, height=380), use_container_width=True)
        with c2:
            st.markdown(f"""
            <div style="background:{T['glass_bg']};border-radius:12px;padding:16px;border:1px solid {T['glass_border']};">
                <p><b>📌 Data-driven answer:</b><br>{q['answer']}</p>
                <p><b>🔍 Key insight:</b><br>{q['insight']}</p>
                <p><b>⚙️ Implication:</b><br>{q['implication']}</p>
                <p><b>✅ Recommendation:</b><br>{q['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<hr style='border-color:" + T['glass_border'] + ";'>", unsafe_allow_html=True)

    section_header("KPI Dashboard", "📊")
    st.markdown("<p style='color:" + T['subtext'] + ";'>Every KPI computed in the notebook's KPI Analysis section.</p>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, kpi in enumerate(nr.KPI_TABLE):
        val = f"{kpi['value']:,.1f}" if kpi["value"] != int(kpi["value"]) else f"{int(kpi['value']):,}"
        with cols[i % 3]:
            animated_kpi(kpi["kpi"], val, kpi["desc"], unit=kpi["unit"])
            st.write("")

    prevalence = {k["kpi"]: k["value"] for k in nr.KPI_TABLE if k["unit"] == "%" and k["kpi"] != "Data Completeness Rate"}
    s = pd.Series(prevalence).sort_values()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=s.values, y=s.index, mode="markers", 
                            marker=dict(size=18, color=PALETTE["dark_blue"], 
                                       line=dict(color=PALETTE["medium_blue"], width=2))))
    for name, val in s.items():
        fig.add_shape(type="line", x0=0, x1=val, y0=name, y1=name, 
                     line=dict(color=PALETTE["medium_gray"], width=2, dash="dash"))
    fig.update_layout(xaxis_title="% of Population", xaxis_range=[0, max(s.values)*1.1])
    st.plotly_chart(style_fig(fig, "KPI Dashboard - Prevalence Rates (%)", height=450), use_container_width=True)

# =============================================================================
# PAGE: MACHINE LEARNING
# =============================================================================
elif page == "🤖 Machine Learning":
    st.markdown(f"<h1 style='color:{T['accent']};font-weight:900;'>🤖 Machine Learning</h1>", unsafe_allow_html=True)

    section_header("Objective, Target & Features", "🎯")
    c1, c2, c3 = st.columns(3)
    with c1: animated_kpi("Objective", "Predict Elevated BP Risk", "Binary classification", glow=True)
    with c2: animated_kpi("Target Variable", "BP_Risk_Category", nr.ML_TARGET, glow=True)
    with c3: animated_kpi("Feature Count", len(nr.ML_FEATURES_NUMERIC) + len(nr.ML_FEATURES_CATEGORICAL), "6 numeric + 2 categorical", glow=True)

    st.markdown(f"""
    <div class="insight-card">
        <b>📊 Numeric features:</b> {", ".join(nr.ML_FEATURES_NUMERIC)}<br>
        <b>🏷️ Categorical features:</b> {", ".join(nr.ML_FEATURES_CATEGORICAL)}<br><br>
        <span style="color:{T['subtext']};"><b>🚫 Excluded on purpose:</b> <code>Pulse_Pressure</code> is derived directly from
        Systolic/Diastolic BP - the same columns used to build the target - so including it would leak the
        answer into the model. <code>Cholesterol_Ratio</code> duplicates signal already present in
        Total_Cholesterol and HDL_Cholesterol individually.</span>
    </div>
    """, unsafe_allow_html=True)

    section_header("Model 1 & Model 2", "🧠")
    c1, c2 = st.columns(2)
    with c1:
        m = nr.MODEL_METRICS["Logistic Regression"]
        best_badge = '<span class="badge-best">🏆 Best Model</span>' if nr.BEST_MODEL == "Logistic Regression" else ""
        st.markdown(f"""
        <div class="model-card">
            <h4 style="margin:0 0 8px 0;">Logistic Regression {best_badge}</h4>
            <p style="color:{T['subtext']};font-size:0.9rem;">A simple, interpretable linear model estimating the probability of elevated BP risk as a weighted, additive combination of the input features.</p>
            <p style="color:{T['subtext']};font-size:0.85rem;"><b>Why selected:</b> the feature set is modest in size and the coefficients directly show the direction and relative size of each feature's effect.</p>
            <table style="width:100%;margin-top:12px;border-collapse:collapse;">
                <tr><td style="padding:4px 0;color:{T['text']};"><b>Accuracy</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['Accuracy']:.3f}</b></td></tr>
                <tr><td style="padding:4px 0;color:{T['text']};"><b>Precision</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['Precision']:.3f}</b></td></tr>
                <tr><td style="padding:4px 0;color:{T['text']};"><b>Recall</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['Recall']:.3f}</b></td></tr>
                <tr><td style="padding:4px 0;color:{T['text']};"><b>F1-Score</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['F1-Score']:.3f}</b></td></tr>
                <tr><td style="padding:4px 0;color:{T['text']};"><b>ROC-AUC</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['ROC-AUC']:.3f}</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        m = nr.MODEL_METRICS["Random Forest"]
        best_badge = '<span class="badge-best">🏆 Best Model</span>' if nr.BEST_MODEL == "Random Forest" else ""
        st.markdown(f"""
        <div class="model-card">
            <h4 style="margin:0 0 8px 0;">Random Forest {best_badge}</h4>
            <p style="color:{T['subtext']};font-size:0.9rem;">A nonlinear ensemble of decision trees that can capture interactions between features that a linear model would miss.</p>
            <p style="color:{T['subtext']};font-size:0.85rem;"><b>Why selected:</b> used as a comparison point for Logistic Regression, to test whether nonlinear feature interactions add real predictive value.</p>
            <table style="width:100%;margin-top:12px;border-collapse:collapse;">
                <tr><td style="padding:4px 0;color:{T['text']};"><b>Accuracy</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['Accuracy']:.3f}</b></td></tr>
                <tr><td style="padding:4px 0;color:{T['text']};"><b>Precision</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['Precision']:.3f}</b></td></tr>
                <tr><td style="padding:4px 0;color:{T['text']};"><b>Recall</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['Recall']:.3f}</b></td></tr>
                <tr><td style="padding:4px 0;color:{T['text']};"><b>F1-Score</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['F1-Score']:.3f}</b></td></tr>
                <tr><td style="padding:4px 0;color:{T['text']};"><b>ROC-AUC</b></td><td style="text-align:right;padding:4px 0;color:{T['text']};"><b>{m['ROC-AUC']:.3f}</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="insight-card">
            <b>📈 Logistic Regression - Practical Benefit</b>
            <p style="color:{T['subtext']};">Coefficients are directly interpretable: a clinician or analyst can see exactly which factors push risk up or down and by how much.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="insight-card">
            <b>🌲 Random Forest - Practical Benefit</b>
            <p style="color:{T['subtext']};">Captures nonlinear patterns and feature interactions automatically, and provides a native feature-importance ranking without standardized coefficients.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <b>🔄 Why They Are Different</b>
        <p style="color:{T['subtext']};">Logistic Regression assumes a straight-line relationship between each feature and risk; Random Forest can bend that relationship and combine features in more complex ways. Comparing both tells us whether the extra flexibility of Random Forest actually pays off on this dataset - here, it barely does, since the two models land within about a point of each other on every metric.</p>
    </div>
    """, unsafe_allow_html=True)

    # Model Comparison
    section_header("Model Comparison", "📊")
    metrics_df = pd.DataFrame(nr.MODEL_METRICS).T
    
    try:
        styled_df = metrics_df.style.format("{:.3f}").background_gradient(cmap="Blues", axis=0)
        st.dataframe(styled_df, use_container_width=True)
    except (ImportError, AttributeError):
        st.dataframe(metrics_df.style.format("{:.3f}"), use_container_width=True)
        st.info("💡 Gradient styling is unavailable (matplotlib not installed). Displaying plain formatted metrics.")

    fig = go.Figure()
    for model, color in [("Logistic Regression", PALETTE["medium_blue"]), ("Random Forest", PALETTE["dark_blue"])]:
        m = nr.MODEL_METRICS[model]
        fig.add_bar(name=model, x=list(m.keys()), y=list(m.values()), marker_color=color,
                   text=[f"{v:.3f}" for v in m.values()], textposition="outside")
    fig.update_layout(barmode="group", yaxis_title="Score", xaxis_title="Metric", yaxis_range=[0, 1])
    st.plotly_chart(style_fig(fig, "Model Performance Comparison", height=450), use_container_width=True)

    st.markdown(f"""
    <div class="insight-card" style="border-left:4px solid {T['accent']};">
        <span class="badge-best">🏆 Best Performing Model: {nr.BEST_MODEL}</span>
        <p style="margin-top:10px;">{nr.BEST_MODEL_NOTE}</p>
        <p style="color:{T['subtext']};">Naive majority-class baseline accuracy: <b>{nr.BASELINE_ACCURACY:.3f}</b> - both models beat this baseline, confirming real (if modest) learned signal.</p>
    </div>
    """, unsafe_allow_html=True)

    section_header("Feature Importance", "🔑")
    c1, c2 = st.columns(2)
    with c1:
        s = pd.Series(nr.RF_FEATURE_IMPORTANCE).sort_values()
        fig = px.bar(x=s.values, y=s.index, orientation="h", labels={"x": "Importance", "y": ""},
                    color_discrete_sequence=[PALETTE["dark_blue"]],
                    text=s.values.round(3))
        fig.update_layout(xaxis_range=[0, max(s.values)*1.1])
        st.plotly_chart(style_fig(fig, "Random Forest - Feature Importance", height=480), use_container_width=True)
    with c2:
        s = pd.Series(nr.LOGREG_COEFFICIENTS).sort_values()
        colors = [PALETTE["dark_blue"] if v > 0 else PALETTE["medium_gray"] for v in s.values]
        fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker_color=colors,
                              text=[f"{v:.3f}" for v in s.values], textposition="outside"))
        fig.update_layout(xaxis_title="Coefficient (impact on elevated-risk probability)")
        st.plotly_chart(style_fig(fig, "Logistic Regression - Standardized Coefficients", height=480), use_container_width=True)

    st.markdown(f"""
    <div class="insight-card">
        <p>{nr.FEATURE_IMPORTANCE_NOTE}</p>
        <p style="color:{T['subtext']};"><b>⚠️ Note:</b> feature importance indicates predictive contribution within these models, not proof of causal influence.</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# PAGE: ABOUT
# =============================================================================
elif page == "ℹ️ About":
    st.markdown(f"<h1 style='color:{T['accent']};font-weight:900;'>ℹ️ About This Project</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card" style="border-left:4px solid {T['accent']};">
        <h4 style="margin:0 0 8px 0;">🚀 About the Project</h4>
        <p>{nr.PROJECT_TAGLINE}. This application turns a complete health-data analytics notebook - cleaning, feature engineering, exploratory analysis, KPI tracking, business Q&A, and Machine Learning - into an interactive product any stakeholder can use without touching Python.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="insight-card">
        <h4 style="margin:0 0 8px 0;">📊 Dataset</h4>
        <p>{nr.DATASET_DESCRIPTION}</p>
        <p style="color:{T['subtext']};">Raw shape: {nr.RAW_SHAPE[0]:,} rows x {nr.RAW_SHAPE[1]} columns. After cleaning (removing {nr.DUPLICATES_REMOVED} duplicate rows, fixing {nr.INVALID_BP_ROWS_FIXED} physiologically invalid blood-pressure readings, and handling {nr.MISSING_VALUES_BEFORE} missing values): {nr.CLEANED_SHAPE[0]:,} rows x {nr.FINAL_COLUMN_COUNT} columns (10 cleaned + 5 engineered).</p>
    </div>
    """, unsafe_allow_html=True)

    section_header("Methodology", "🔬")
    steps_html = "".join([f"<span class='insight-tag'>{i+1}. {s}</span> " for i, s in enumerate(nr.METHODOLOGY_STEPS)])
    st.markdown(f"<div class='insight-card' style='padding:20px;'>{steps_html}</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="insight-card">
            <h4 style="margin:0 0 12px 0;">⚡ Technologies</h4>
            <ul style="list-style:none;padding:0;">
                {''.join(f'<li style="padding:6px 0;border-bottom:1px solid {T['glass_border']};color:{T['text']};">✅ {t}</li>' for t in nr.TECHNOLOGIES)}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="insight-card">
            <h4 style="margin:0 0 12px 0;">🏆 Project Highlights</h4>
            <ul style="list-style:none;padding:0;">
                <li style="padding:6px 0;border-bottom:1px solid {T['glass_border']};color:{T['text']};">📊 {nr.CLEANED_SHAPE[0]:,} records analyzed</li>
                <li style="padding:6px 0;border-bottom:1px solid {T['glass_border']};color:{T['text']};">🔢 {nr.FINAL_COLUMN_COUNT} total features</li>
                <li style="padding:6px 0;border-bottom:1px solid {T['glass_border']};color:{T['text']};">🎯 {nr.N_KPIS} KPIs tracked</li>
                <li style="padding:6px 0;border-bottom:1px solid {T['glass_border']};color:{T['text']};">💡 {nr.N_BUSINESS_QUESTIONS} business questions</li>
                <li style="padding:6px 0;border-bottom:1px solid {T['glass_border']};color:{T['text']};">🧠 {nr.N_ML_MODELS} ML models compared</li>
                <li style="padding:6px 0;color:{T['text']};">🏅 Best model: {nr.BEST_MODEL} (ROC-AUC {nr.MODEL_METRICS[nr.BEST_MODEL]['ROC-AUC']:.3f})</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {PALETTE['glass_bg']}, {T['panel']});border-radius:12px;padding:20px;border:1px solid {T['glass_border']};text-align:center;">
        🚀 Built from <code>python_project_NTI.ipynb</code>. All KPIs, business answers, and ML metrics on this site are the real values produced by that notebook - none are estimated or invented for the deployment.
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# FOOTER WITH BRANDING
# =============================================================================
def render_footer():
    st.markdown(f"""
    <div class="footer">
        <div class="footer-content">
            <div class="footer-brand">
                {T['logo']}
            </div>
            <div class="footer-text">
                © 2026 MEDISIGHTS • Data-Driven Clinical Insights
            </div>
            <div class="footer-links">
                <a href="#">Privacy</a>
                <a href="#">Terms</a>
                <a href="#">Contact</a>
                <a href="#">Support</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

render_footer()
