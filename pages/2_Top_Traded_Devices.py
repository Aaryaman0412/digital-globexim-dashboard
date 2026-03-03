import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

import base64
from auth_utils import check_authentication, show_logout_button

# Check authentication
check_authentication()


def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

globexim_logo = img_to_base64("logos/globexim_logo.png")
kiht_logo = img_to_base64("logos/kiht_logo.png")



# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(layout="wide", page_title="Top 10 Commodities")

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
            <h1 style="margin-bottom: 6px;color:#1E3A8A;">India's Top Imported and Exported Medical Devices by Year</h1>
            
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
# LOAD DATA (reuse logic from main app)
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

with f2:
    if year == "All":
        df_year = df.copy()
    else:
        df_year = df[df["Year"] == year]

    segments = sorted(df_year["Segment"].dropna().unique())
    segment = st.selectbox(
        "Select Segment",
        ["All"] + segments
    )

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
df_filtered = df_year if segment == "All" else df_year[df_year["Segment"] == segment]

exclude_keywords = ["other", "parts"]

df_clean_products = df_filtered[
    ~df_filtered["Product"]
    .str.lower()
    .str.contains("|".join(exclude_keywords), na=False)
]

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# ==================================================
# BUTTERFLY CHART: TOP 10 TRADED PRODUCTS
# ==================================================

# Aggregate trade by product and type
product_trade = (
    df_clean_products
    .groupby(["Product", "Imp / Exp"])["Trade Value in Crores"]
    .sum()
    .reset_index()
)

# Pivot to Import / Export columns
pivot = (
    product_trade
    .pivot(index="Product", columns="Imp / Exp", values="Trade Value in Crores")
    .fillna(0)
)

# Total trade
pivot["Total Trade"] = pivot.get("Import", 0) + pivot.get("Export", 0)

# Top 10 products by total trade
top_products = (
    pivot
    .sort_values("Total Trade", ascending=False)
    .head(10)
    .reset_index()
)

# Plot values (imports negative, exports positive)
top_products["Import Plot"] = -top_products["Import"]
top_products["Export Plot"] = top_products["Export"]

# Percent contributions
top_products["Import %"] = (
    top_products["Import"] / top_products["Total Trade"] * 100
).round(2)

top_products["Export %"] = (
    top_products["Export"] / top_products["Total Trade"] * 100
).round(2)

# Symmetric axis range
max_val = max(
    top_products["Export Plot"].max(),
    abs(top_products["Import Plot"].min())
)

# --------------------------------------------------
# CREATE BUTTERFLY CHART
# --------------------------------------------------
fig_butterfly = px.bar(
    top_products,
    y="Product",
    x=["Import Plot", "Export Plot"],
    orientation="h",
    color_discrete_map={
        "Import Plot": "#2F4B7C",
        "Export Plot": "#7DA0C4"
    }
)

# Rename legend entries
fig_butterfly.for_each_trace(
    lambda t: t.update(
        name="Imports" if "Import" in t.name else "Exports"
    )
)

# Layout & styling (SILVER THEME – LOCAL)
fig_butterfly.update_layout(

    hoverlabel=dict(
        font=dict(
            color="black",
            size=14,
            family="Inter"
        ),
        bgcolor="white",
        bordercolor="#2F4B7C"
    ),

    plot_bgcolor="#E6E6E6",
    paper_bgcolor="#E6E6E6",

    title=dict(
        text="Trade composition of the most traded medical devices",
        x=0.5,
        xanchor="center",
        y=0.95,
        yanchor="top",
        font=dict(
            family="Georgia, serif",
            size=22,
            color="#1f1f1f"
        )
    ),

    font=dict(
        family="Georgia, serif",
        size=14,
        color="#1f1f1f"
    ),

    legend=dict(
        title_text="",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(
            family="Georgia, serif",
            size=14,
            color="#1f1f1f"
        )
    ),

    xaxis=dict(
        range=[-max_val, max_val],
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor="#1f1f1f",
        showgrid=False,
        tickformat="~s",
        tickfont=dict(
            family="Georgia, serif",
            size=13,
            color="#1f1f1f"
        ),
        title=dict(
            text="Trade Value (₹ Crores)",
            font=dict(
                family="Georgia, serif",
                size=14,
                color="#1f1f1f"
            )
        ),
        linecolor="#2F4B7C"
    ),

    yaxis=dict(
        autorange="reversed",
        title=None,
        showgrid=False,
        tickfont=dict(
            family="Georgia, serif",
            size=13,
            color="#1f1f1f"
        ),
        linecolor="#2F4B7C"
    ),

    margin=dict(t=90, l=60, r=60, b=50),
    barmode="relative",
    showlegend=True
)

# Hover details
fig_butterfly.update_traces(
    customdata=top_products[
        ["Import", "Export", "Total Trade", "Import %", "Export %"]
    ].values,
    hovertemplate=(
        "<b>%{y}</b><br><br>"
        "Imports: ₹ %{customdata[0]:,.2f} Cr "
        "(%{customdata[3]:.2f}%)<br>"
        "Exports: ₹ %{customdata[1]:,.2f} Cr "
        "(%{customdata[4]:.2f}%)<br><br>"
        "<b>Total Trade:</b> ₹ %{customdata[2]:,.2f} Cr"
        "<extra></extra>"
    )
)

# Render
st.plotly_chart(fig_butterfly, use_container_width=True)

st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)


# --------------------------------------------------
# TOP 10 IMPORTED PRODUCTS
# --------------------------------------------------
top_imports = (
    df_clean_products[df_clean_products["Imp / Exp"] == "Import"]
    .groupby("Product")["Trade Value in Crores"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# --------------------------------------------------
# TOP 10 EXPORTED PRODUCTS
# --------------------------------------------------
top_exports = (
    df_clean_products[df_clean_products["Imp / Exp"] == "Export"]
    .groupby("Product")["Trade Value in Crores"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

# -------------------------------
# TOP IMPORTED PRODUCTS
# -------------------------------


fig_imp = px.bar(
    top_imports,
    x="Trade Value in Crores",
    y="Product",
    orientation="h",
    color_discrete_sequence=["#2F4B7C"]
)

fig_imp.update_layout(
    
    hoverlabel=dict(
        font=dict(
            color="black",
            size=14,
            family="Inter"
        ),
        bgcolor="white",
        bordercolor="#2F4B7C"
    ),

    # ----------- BACKGROUND -----------
    plot_bgcolor="#E6E6E6",
    paper_bgcolor="#E6E6E6",

    # ----------- TITLE INSIDE CHART -----------
    title=dict(
        text="Top imported medical devices",
        x=0.5,
        xanchor="center",
        y=0.95,
        yanchor="top",
        font=dict(
            family="Georgia, serif",
            size=20,
            color="#1f1f1f"
        )
    ),

    # ----------- GLOBAL FONT -----------
    font=dict(
        family="Georgia, serif",
        size=14,
        color="#1f1f1f"
    ),

    # ----------- AXES -----------
    xaxis=dict(
        title=dict(
            text="Trade Value (₹ Crores)",
            font=dict(
                family="Georgia, serif",
                size=14,
                color="#1f1f1f"
            )
        ),
        tickformat="~s",
        showgrid=False,
        linecolor="#2F4B7C",
        tickfont=dict(
            family="Georgia, serif",
            size=13,
            color="#1f1f1f"
        )
    ),

    yaxis=dict(
        autorange="reversed",
        title=None,
        showgrid=False,
        linecolor="#2F4B7C",
        tickfont=dict(
            family="Georgia, serif",
            size=13,
            color="#1f1f1f"
        )
    ),

    # ----------- MARGINS -----------
    margin=dict(t=80, l=60, r=40, b=50),

    # ----------- LEGEND OFF -----------
    showlegend=False
)

fig_imp.update_traces(
    customdata=[
        f"₹ {v:,.2f} Cr" for v in top_imports["Trade Value in Crores"]
    ],
    hovertemplate=(
        "<b>%{y}</b><br><br>"
        "Imports: %{customdata}"
        "<extra></extra>"
    )
)

st.plotly_chart(fig_imp, use_container_width=True)

# -------------------------------
# TOP 10 EXPORTED PRODUCTS
# -------------------------------
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

fig_exp = px.bar(
    top_exports,
    x="Trade Value in Crores",
    y="Product",
    orientation="h",
    color_discrete_sequence=["#7DA0C4"]
)

fig_exp.update_layout(
    hoverlabel=dict(
        font=dict(
            color="black",
            size=14,
            family="Inter"
        ),
        bgcolor="white",
        bordercolor="#2F4B7C"
    ),
    # ----------- BACKGROUND -----------
    plot_bgcolor="#E6E6E6",
    paper_bgcolor="#E6E6E6",

    # ----------- TITLE INSIDE CHART -----------
    title=dict(
        text="Top exported medical devices",
        x=0.5,
        xanchor="center",
        y=0.95,
        yanchor="top",
        font=dict(
            family="Georgia, serif",
            size=20,
            color="#1f1f1f"
        )
    ),

    # ----------- GLOBAL FONT -----------
    font=dict(
        family="Georgia, serif",
        size=14,
        color="#1f1f1f"
    ),

    # ----------- AXES -----------
    xaxis=dict(
        title=dict(
            text="Trade Value (₹ Crores)",
            font=dict(
                family="Georgia, serif",
                size=14,
                color="#1f1f1f"
            )
        ),
        tickformat="~s",
        showgrid=False,
        linecolor="#2F4B7C",
        tickfont=dict(
            family="Georgia, serif",
            size=13,
            color="#1f1f1f"
        )
    ),

    yaxis=dict(
        autorange="reversed",
        title=None,
        showgrid=False,
        linecolor="#2F4B7C",
        tickfont=dict(
            family="Georgia, serif",
            size=13,
            color="#1f1f1f"
        )
    ),

    # ----------- MARGINS -----------
    margin=dict(t=80, l=60, r=40, b=50),

    # ----------- LEGEND OFF -----------
    showlegend=False
)

fig_exp.update_traces(
    customdata=[
        f"₹ {v:,.2f} Cr" for v in top_exports["Trade Value in Crores"]
    ],
    hovertemplate=(
        "<b>%{y}</b><br><br>"
        "Exports: %{customdata}"
        "<extra></extra>"
    )
)

st.plotly_chart(fig_exp, use_container_width=True)

st.markdown(
    """
    <hr style='border:1px solid #444;'>
    <p style='text-align:left;color:#1F2937;font-size:20px;'>
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
