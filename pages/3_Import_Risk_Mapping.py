import streamlit as st
import pandas as pd
import numpy as np

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
st.set_page_config(layout="wide", page_title="Device Import Risk Mapping")

st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #FAFAFC;
        color: #1F2937;
    }

    /* SIDEBAR BACKGROUND  */
    [data-testid="stSidebar"] {
        background-color: #374151 /* darker pastel blue */
    }

    /*  SIDEBAR TILES (YELLOW / AMBER) */
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

    /* Sidebar labels (radio/selectbox titles, if any) */
    [data-testid="stSidebar"] label {
        color: #1E40AF;
        font-weight: 600;
    }

 /* ================================
   TOP FILTER CLARITY IMPROVEMENTS
   ================================ */

/* Selectbox container */
div[data-baseweb="select"] {
    background-color: #FFFFFF;
    border-radius: 10px;
    border: 1.5px solid #CBD5E1;
}

/* Selectbox text */
div[data-baseweb="select"] span {
    color: #111827;
    font-weight: 600;
    font-size: 15px;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    color: #1E3A8A;
}

/* Label above selectbox */
label {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #1E3A8A !important;
}

/* Hover */
div[data-baseweb="select"]:hover {
    border-color: #1E3A8A;
}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# PAGE TITLE (CENTERED)
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
            <h1 style="margin-bottom: 6px;color:#1E3A8A;">Mapping Import Dependency in India for Medical Devices</h1>
            
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
# FILTERS (TOP)
# --------------------------------------------------
f1, f2, f3 = st.columns(3)

with f1:
    year_filter = st.selectbox(
        "Select Year",
        ["All"] + sorted(df["Year"].dropna().unique().tolist())
    )

with f2:
    volume_filter = st.selectbox(
        "Filter by Import Volume Risk",
        ["All", "HIGH", "MODERATE", "LOW"]
    )

with f3:
    concentration_filter = st.selectbox(
        "Filter by Import Concentration Risk",
        ["All", "HIGH", "MODERATE", "LOW"]
    )

# --------------------------------------------------
# IMPORT-ONLY DATA (YEAR FILTER)
# --------------------------------------------------
if year_filter == "All":
    df_imports = df[df["Imp / Exp"] == "Import"].copy()
else:
    df_imports = df[
        (df["Imp / Exp"] == "Import") &
        (df["Year"] == year_filter)
    ].copy()

# --------------------------------------------------
# EXCLUDE "OTHER" AND "PARTS"
# --------------------------------------------------
exclude_keywords = ["other", "parts"]

df_imports = df_imports[
    ~df_imports["Product"]
    .str.lower()
    .str.contains("|".join(exclude_keywords), na=False)
]

# --------------------------------------------------
# SAFETY CHECK
# --------------------------------------------------
if df_imports.empty:
    st.warning("No import data available for the selected filters.")
    st.stop()

# --------------------------------------------------
# AGGREGATE DEVICE-LEVEL METRICS
# --------------------------------------------------
device_country = (
    df_imports
    .groupby(["Product", "Country"], dropna=True)["Trade Value in Crores"]
    .sum()
    .reset_index()
)

device_total = (
    device_country
    .groupby("Product")["Trade Value in Crores"]
    .sum()
    .rename("Total Imports")
    .reset_index()
)

device_country = device_country.merge(
    device_total, on="Product", how="left"
)

# Remove zero-import devices
device_country = device_country[
    device_country["Total Imports"] > 0
]

device_country["Share"] = (
    device_country["Trade Value in Crores"] /
    device_country["Total Imports"]
)

# --------------------------------------------------
# RISK CALCULATION (SAFE LOOP)
# --------------------------------------------------
risk_rows = []

for product, g in device_country.groupby("Product"):
    if g.empty:
        continue

    total_imports = g["Total Imports"].iloc[0]

    hhi = ((g["Share"] * 100) ** 2).sum()

    dominant_row = g.loc[g["Share"].idxmax()]
    dominant_country = dominant_row["Country"]
    dominant_share = dominant_row["Share"] * 100

    # Volume Risk
    if total_imports > 100:
        vol_risk = "HIGH"
    elif total_imports >= 10:
        vol_risk = "MODERATE"
    else:
        vol_risk = "LOW"

    # Concentration Risk
    if hhi > 2500:
        conc_risk = "HIGH"
    elif hhi >= 1500:
        conc_risk = "MODERATE"
    else:
        conc_risk = "LOW"

    risk_rows.append([
        product,
        round(total_imports, 2),
        vol_risk,
        round(hhi, 2),
        conc_risk,
        dominant_country,
        round(dominant_share, 2)
    ])

risk_df = pd.DataFrame(
    risk_rows,
    columns=[
        "Device",
        "Import Value (₹ Cr)",
        "Import Volume Risk",
        "HHI",
        "Import Concentration Risk",
        "Dominant Country",
        "Dominant Share (%)"
    ]
)

# --------------------------------------------------
# APPLY RISK FILTERS
# --------------------------------------------------
if volume_filter != "All":
    risk_df = risk_df[
        risk_df["Import Volume Risk"] == volume_filter
    ]

if concentration_filter != "All":
    risk_df = risk_df[
        risk_df["Import Concentration Risk"] == concentration_filter
    ]


# --------------------------------------------------
# DISPLAY TABLE (STATIC, CENTERED TITLE, VISIBLE COLUMNS)
# --------------------------------------------------

display_df = risk_df[
    [
        "Device",
        "Import Value (₹ Cr)",
        "Dominant Country",
        "Dominant Share (%)"
    ]
].sort_values(
    "Import Value (₹ Cr)", ascending=False
).reset_index(drop=True)

# Add serial number
display_df.insert(0, "Sl. No.", range(1, len(display_df) + 1))

# Table styling
st.markdown(
    """
    <style>
    .globexim-table {
        font-family: Georgia, serif;
        font-size: 15px;
        color: #1f1f1f;
        background-color: #E6E6E6;
        border-collapse: collapse;
        width: 100%;
    }

    .globexim-table th {
        background-color: #F3E8D6
        color: #1f1f1f;
        font-weight: 700;
        padding: 10px;
        border-bottom: 2px solid #B8A97A;
        text-align: left;
        white-space: nowrap;
    }

    .globexim-table td {
        padding: 10px;
        border-bottom: 1px solid #CFC4A5;
        vertical-align: middle;
    }

    .globexim-table tr:hover {
        background-color: #EFE5CF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Render table
st.markdown(
    display_df.to_html(
        index=False,
        classes="globexim-table"
    ),
    unsafe_allow_html=True
)


st.markdown(
    """
    <hr style='border:1px solid #444;'>
    <p style='text-align:left;color#1F2937;font-size:20px;'>
    DIGITAL GLOBEXIM · Medical Device Trade Intelligence ·
    Data source: Department of Commerce, Minsitry of Commerce and Industry, Government of India
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

