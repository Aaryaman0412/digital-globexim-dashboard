import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from auth_utils import check_authentication, show_logout_button

# Check authentication
check_authentication()

import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

globexim_logo = img_to_base64("logos/globexim_logo.png")
kiht_logo = img_to_base64("logos/kiht_logo.png")


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(layout="wide", page_title="Country-wise Import Dependency")

# --------------------------------------------------
# THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
/* App background */
.stApp {
    background-color: #FAFAFC;
    color: #1F2937;
}

/* SIDEBAR BACKGROUND */
[data-testid="stSidebar"] {
    background-color: #374151;
}

/* SIDEBAR TILES */
[data-testid="stSidebar"] a {
    background-color: #F3E8A3;
    color: #3A2E00 !important;
    border-radius: 12px;
    padding: 10px 16px;
    display: block;
    margin-bottom: 10px;
    font-weight: 600;
    text-decoration: none;
}

/* TILE HOVER */
[data-testid="stSidebar"] a:hover {
    background-color: #EEDC82;
    color: #3A2E00 !important;
}

/* ACTIVE TILE (GREEN + WHITE TEXT) */
[data-testid="stSidebar"] a[aria-current="page"],
[data-testid="stSidebar"] a[aria-current="page"] span {
    background-color: #556B2F;
    color: #FFFFFF !important;
    font-weight: 700;
}

/* SIDEBAR LABELS */
[data-testid="stSidebar"] label {
    color: #1E40AF;
    font-weight: 600;
}

/* ================================
   TOP FILTER CLARITY IMPROVEMENTS
   ================================ */

div[data-baseweb="select"] {
    background-color: #FFFFFF;
    border-radius: 10px;
    border: 1.5px solid #CBD5E1;
}

div[data-baseweb="select"] span {
    color: #111827;
    font-weight: 600;
    font-size: 15px;
}

div[data-baseweb="select"] svg {
    color: #1E3A8A;
}

label {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #1E3A8A !important;
}

div[data-baseweb="select"]:hover {
    border-color: #1E3A8A;
}

</style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------
c1, c2, c3 = st.columns([1.2, 4, 1.2])

with c1:
    st.markdown(
        f"""
        <img src="data:image/png;base64,{globexim_logo}" width="180">
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div style="
            text-align: center;
            margin-top: 30px;
        ">
            <h1 style="margin-bottom: 6px;color:#1E3A8A;">Country-wise Import Dependency of Medical Devices in India</h1>
            
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: flex-end;
            align-items: centre;
        ">
            <img src="data:image/png;base64,{kiht_logo}" width="180">
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    "<hr style='margin-top: 10px; margin-bottom: 12px;'>",
    unsafe_allow_html=True
)
# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("Datasheet_DG.xlsx")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    return df

df = load_data()

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
f1, f2 = st.columns(2)

with f1:
    year = st.selectbox("Select Year", ["All"] + sorted(df["Year"].dropna().unique()))

if year != "All":
    df = df[df["Year"] == year]

# --------------------------------------------------
# IMPORT DATA
# --------------------------------------------------
# FULL imports → KPIs
df_imports_full = df[df["Imp / Exp"] == "Import"]

# CLEAN imports → device bars
exclude_keywords = ["other", "parts"]
df_imports_clean = df_imports_full[
    ~df_imports_full["Product"].str.lower().str.contains("|".join(exclude_keywords), na=False)
]

# --------------------------------------------------
# COUNTRY-LEVEL IMPORTS (FULL DATA)
# --------------------------------------------------
country_imports = (
    df_imports_full
    .groupby("Country")["Trade Value in Crores"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# --------------------------------------------------
# COUNTRY SELECTOR (WITH ALL OPTION)
# --------------------------------------------------
all_countries = country_imports["Country"].tolist()

with f2:
    selected_countries = st.multiselect(
        "Select Country / Countries",
        ["All"] + all_countries,
        default=["All"]
    )

# --- Enforce ALL as mutually exclusive ---
if "All" in selected_countries and len(selected_countries) > 1:
    st.warning("Please deselect 'All' to choose specific countries.")
    countries = all_countries
elif "All" in selected_countries or len(selected_countries) == 0:
    countries = all_countries
else:
    countries = selected_countries

total_imports_india = country_imports["Trade Value in Crores"].sum()

country_value = country_imports[
    country_imports["Country"].isin(countries)
]["Trade Value in Crores"].sum()

# --------------------------------------------------
# SENSITIVITY ANALYSIS
# --------------------------------------------------
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

sensitivity = st.slider(
    "Sensitivity Analysis: Change in Import Value (%)",
    min_value=-50,
    max_value=50,
    value=0,
    step=1,
    help=(
        "This slider simulates a hypothetical increase or decrease in India's "
        "imports from the selected country. A positive value represents higher "
        "import dependence, while a negative value represents a reduction in "
        "imports. All import values, country share, and device-level figures "
        "update dynamically based on this scenario."
    )
)

import_adjustment_factor = 1 + sensitivity / 100

# --------------------------------------------------
# SCENARIO-AWARE KPIs (FULL DATA)
# --------------------------------------------------
adjusted_country_value = country_value * import_adjustment_factor

adjusted_total_imports = (
    total_imports_india + (adjusted_country_value - country_value)
)

adjusted_country_share = round(
    (adjusted_country_value / adjusted_total_imports) * 100, 2
)

# --------------------------------------------------
# KPI STYLES
# --------------------------------------------------
st.markdown(
    """
    <style>
    .kpi-tile {
        background: #CFA6A0;
        border-radius: 14px;
        padding: 22px;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-family: Georgia, serif;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12);
    }
    .kpi-title { font-size: 25px; font-weight: 600; color: #4a4a4a; }
    .kpi-value { font-size: 30px; font-weight: 900; color: #1f1f1f; }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# KPI TILES
# --------------------------------------------------
k1, k2 = st.columns(2)

with k1:
    st.markdown(
        f"""
        <div class="kpi-tile">
            <div class="kpi-title">Import Value (Scenario)</div>
            <div class="kpi-value">₹ {adjusted_country_value:,.2f} Cr</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-tile">
            <div class="kpi-title">Share of India’s Imports</div>
            <div class="kpi-value">{adjusted_country_share} %</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# TOP 10 DEVICES (CLEAN DATA ONLY)
# --------------------------------------------------
device_df = (
    df_imports_clean[df_imports_clean["Country"].isin(countries)]
    .groupby("Product", as_index=False)["Trade Value in Crores"]
    .sum()
    .sort_values(by="Trade Value in Crores", ascending=False)
    .head(10)
)

# Apply sensitivity to devices
device_df["Adjusted Trade Value"] = device_df["Trade Value in Crores"] * import_adjustment_factor

device_df["Device Share (%)"] = round(
    device_df["Adjusted Trade Value"] / adjusted_country_value * 100, 2
)

# --------------------------------------------------
# BAR CHART
# --------------------------------------------------
fig = px.bar(
    device_df,
    x="Adjusted Trade Value",
    y="Product",
    orientation="h",
    text=device_df["Adjusted Trade Value"].apply(lambda x: f"₹ {x:,.1f}"),
    color_discrete_sequence=["#2F4B7C"],
    category_orders={
        "Product": device_df.sort_values("Adjusted Trade Value", ascending=False)["Product"].tolist()
    }
)

fig.update_layout(
    hoverlabel=dict(
        font=dict(color="black", size=14, family="Inter"),
        bgcolor="white",
        bordercolor="#2F4B7C"
    ),
    xaxis=dict(
        title="Import Value (₹ Crores)",
        tickfont=dict(color="#1f1f1f", size=14, family="Georgia, serif")
    ),
    yaxis=dict(
        title_text="",
        tickfont=dict(color="#1f1f1f", size=14, family="Georgia, serif")
    )
)

fig.update_traces(
    textposition="inside",
    insidetextanchor="end",
    textfont=dict(color="white", size=13, family="Georgia, serif"),
    customdata=device_df["Device Share (%)"],
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Scenario Import Value: ₹ %{x:,.2f} Cr<br>"
        "Device share under scenario: %{customdata}%"
        "<extra></extra>"
    )
)

st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <hr style='border:1px solid #444;'>
    <p style='text-align:left;color:#1F2937;font-size:20px;'>
    DIGITAL GLOBEXIM · Medical Device Trade Intelligence ·
    Data source: Department of Commerce, Ministry of Commerce and Industry, Government of India
    </p>
    """,
    unsafe_allow_html=True
)

# Show logout button
show_logout_button()

st.sidebar.markdown(
    """
    <div style="
        position: fixed;
        bottom: 15px;
        left: 20px;
        font-size: 13px;
        line-height: 1.6;
        color: #E6E6E6;
    ">
        <b>Contact</b><br>
        ✉️ info@amtz.in<br>
        🌍 www.kiht.in<br>
        📞 +91 8670694458
    </div>
    """,
    unsafe_allow_html=True
)
