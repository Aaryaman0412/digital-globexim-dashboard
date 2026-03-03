import streamlit as st
import pandas as pd
import plotly.express as px


# Check authentication

import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

globexim_logo = img_to_base64("logos/globexim_logo.png")
kiht_logo = img_to_base64("logos/kiht_logo.png")


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(layout="wide", page_title="India's Country-wise Export Performance")

# --------------------------------------------------
# THEME (IDENTICAL TO IMPORT PAGE)
# --------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAFAFC;
        color: #1F2937;
    }

    [data-testid="stSidebar"] {
        background-color: #374151;
    }

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

    [data-testid="stSidebar"] a:hover {
        background-color: #EEDC82;
    }

    [data-testid="stSidebar"] a[aria-current="page"],
    [data-testid="stSidebar"] a[aria-current="page"] span {
        background-color: #556B2F;
        color: #FFFFFF !important;
        font-weight: 700;
    }

    label {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #1E3A8A !important;
    }

    div[data-baseweb="select"] {
        background-color: #FFFFFF;
        border-radius: 10px;
        border: 1.5px solid #CBD5E1;
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
            <h1 style="margin-bottom: 6px;color:#1E3A8A;">Country-wise Export Performance of Indian Medical Devices </h1>
            
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
    year = st.selectbox(
        "Select Year",
        ["All"] + sorted(df["Year"].dropna().unique().tolist())
    )

if year != "All":
    df = df[df["Year"] == year]

# --------------------------------------------------
# EXPORT DATA
# --------------------------------------------------
df_exports_full = df[df["Imp / Exp"] == "Export"]

exclude_keywords = ["other", "parts"]
df_exports_clean = df_exports_full[
    ~df_exports_full["Product"].str.lower().str.contains("|".join(exclude_keywords), na=False)
]

# --------------------------------------------------
# COUNTRY-LEVEL EXPORTS
# --------------------------------------------------
country_exports = (
    df_exports_full
    .groupby("Country")["Trade Value in Crores"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

all_countries = country_exports["Country"].tolist()

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

total_exports_india = country_exports["Trade Value in Crores"].sum()

country_value = country_exports[
    country_exports["Country"].isin(countries)
]["Trade Value in Crores"].sum()

# --------------------------------------------------
# SENSITIVITY ANALYSIS
# --------------------------------------------------
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

sensitivity = st.slider(
    "Sensitivity Analysis: Change in Export Value (%)",
    min_value=-50,
    max_value=50,
    value=0,
    step=1,
    help=(
        "Simulates a hypothetical increase or decrease in India’s exports "
        "to the selected country/countries. All values update dynamically."
    )
)

export_adjustment_factor = 1 + sensitivity / 100

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
adjusted_country_value = country_value * export_adjustment_factor

adjusted_total_exports = (
    total_exports_india + (adjusted_country_value - country_value)
)

adjusted_country_share = round(
    (adjusted_country_value / adjusted_total_exports) * 100, 2
)

# --------------------------------------------------
# KPI STYLES (IDENTICAL)
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

    .kpi-title {
        font-size: 25px;
        font-weight: 600;
        color: #4a4a4a;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 900;
        color: #1f1f1f;
    }
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
            <div class="kpi-title">Export Value (Scenario)</div>
            <div class="kpi-value">₹ {adjusted_country_value:,.2f} Cr</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-tile">
            <div class="kpi-title">Share of India’s Exports</div>
            <div class="kpi-value">{adjusted_country_share} %</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# TOP 10 EXPORTED DEVICES
# --------------------------------------------------
device_df = (
    df_exports_clean[df_exports_clean["Country"].isin(countries)]
    .groupby("Product", as_index=False)["Trade Value in Crores"]
    .sum()
    .sort_values(by="Trade Value in Crores", ascending=False)
    .head(10)
)

device_df["Adjusted Trade Value"] = (
    device_df["Trade Value in Crores"] * export_adjustment_factor
)

device_df["Device Share (%)"] = round(
    device_df["Adjusted Trade Value"] / adjusted_country_value * 100, 2
)

# --------------------------------------------------
# BAR CHART (IDENTICAL STYLE)
# --------------------------------------------------
fig = px.bar(
    device_df,
    x="Adjusted Trade Value",
    y="Product",
    orientation="h",
    text=device_df["Adjusted Trade Value"].apply(lambda x: f"₹ {x:,.1f}"),
    color_discrete_sequence=["#7DA0C4"],
    category_orders={
        "Product": device_df["Product"].tolist()
    }
)

fig.update_layout(
    hoverlabel=dict(
        font=dict(color="black", size=14, family="Inter"),
        bgcolor="white",
        bordercolor="#7DA0C4"
    ),
    xaxis=dict(
        title=dict(
            text="Export Value (₹ Crores)",
            font=dict(color="#000000", size=15, family="Georgia, serif")
        ),
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
        "Scenario Export Value: ₹ %{x:,.2f} Cr<br>"
        "Device share in India’s exports: %{customdata}%"
        "<extra></extra>"
    )
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# FOOTER (IDENTICAL)
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