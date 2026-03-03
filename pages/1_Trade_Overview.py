# -------------------------------------------------- 
# IMPORTS AND UTILITIES
# --------------------------------------------------
import numpy as np
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
# HELPER FUNCTION FOR CHARTS FORMATTING
# --------------------------------------------------

def apply_globexim_chart_theme(fig, title_text):
    fig.update_layout(

        # ----------- BACKGROUND -----------
        plot_bgcolor="#E6E6E6",
        paper_bgcolor="#E6E6E6",

        # ----------- TITLE -----------
        title=dict(
            text=title_text,
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

        # ----------- GLOBAL FONT -----------
        font=dict(
            family="Georgia, serif",
            size=14,
            color="#1f1f1f"
        ),

        # ----------- HOVER LABEL -----------
        hoverlabel=dict(
            font=dict(
                family="Inter",
                size=14,
                color="black"
            ),
            bgcolor="white",
            bordercolor="#2F4B7C"
        ),

        # ----------- X AXIS -----------
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="#2F4B7C",
            tickfont=dict(
                family="Georgia, serif",
                size=13,
                color="#1f1f1f"
            ),
            title=dict(
                font=dict(
                    family="Georgia, serif",
                    size=15,
                    color="#1f1f1f"
                )
            )
        ),

        # ----------- Y AXIS -----------
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="#2F4B7C",
            tickfont=dict(
                family="Georgia, serif",
                size=13,
                color="#1f1f1f"
            ),
            title=dict(
                font=dict(
                    family="Georgia, serif",
                    size=15,
                    color="#1f1f1f"
                )
            )
        ),

        # ----------- LEGEND -----------
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.9,
            xanchor="center",
            x=1.02,
            font=dict(
                family="Georgia, serif",
                size=14,
                color="#1f1f1f"
            )
        ),

        margin=dict(t=90, l=60, r=60, b=50)
    )


# --------------------------------------------------
# INDIAN CURRENCY FORMATTER
# --------------------------------------------------
def format_inr(value, decimals=2):
    """
    Format a number in Indian numbering system with ₹ symbol.
    Example: 12345678 -> ₹ 1,23,45,678.00
    """
    if value is None or pd.isna(value):
        return "₹ 0"

    value = round(value, decimals)
    integer_part, _, decimal_part = f"{value:.{decimals}f}".partition(".")

    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        rest = integer_part[:-3]
        rest = ",".join(
            [rest[max(i - 2, 0):i] for i in range(len(rest), 0, -2)][::-1]
        )
        formatted = rest + "," + last_three
    else:
        formatted = integer_part

    return f"₹ {formatted}.{decimal_part}"


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(layout="wide", page_title="DIGITAL GLOBEXIM")
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
        background-color: #374151
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
c1, c2, c3 = st.columns([1.2, 4, 1])

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
            <h1 style="margin-bottom: 6px;color:#1E3A8A;">India's Medical Device Trade Profile</h1>
            
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
    df["Month_Num"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.month_name()

    return df


df = load_data()

# ==================================================
# TOP FILTER BAR (ALL IN ONE LINE)
# ==================================================

# ==================================================
# TOP FILTER BAR (ALL IN ONE LINE)
# ==================================================

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# Always initialize variables (prevents NameError)
df_product = df
entered_hsn = None
selected_product = "All"

f1, f2, f3, f4 = st.columns([0.6, 0.8, 0.8, 2])

# --------------------------------------------------
# YEAR
# --------------------------------------------------
with f1:
    year = st.selectbox(
        "Year",
        ["All"] + sorted(df["Year"].dropna().unique().tolist()),
        key="year_filter"
    )

df_year = df if year == "All" else df[df["Year"] == year]

# --------------------------------------------------
# SEGMENT
# --------------------------------------------------
with f2:
    segments = sorted(df_year["Segment"].dropna().unique())
    selected_segment = st.selectbox(
        "Segment",
        ["All"] + segments,
        key="segment_filter"
    )

df_segment = (
    df_year if selected_segment == "All"
    else df_year[df_year["Segment"] == selected_segment]
)

# --------------------------------------------------
# SEARCH BY
# --------------------------------------------------
with f3:
    search_by = st.selectbox(
        "Search By",
        ["Product Type", "HSN Code"],
        key="search_type"
    )

# --------------------------------------------------
# PRODUCT TYPE OR HSN FILTER
# --------------------------------------------------
with f4:

    # ================================
    # SEARCH BY PRODUCT TYPE
    # ================================
    if search_by == "Product Type":

        exclude_keywords = ["other", "parts"]

        product_hsn_df = (
            df_segment[
                ~df_segment["Product"]
                .str.lower()
                .str.contains("|".join(exclude_keywords), na=False)
            ][["Product", "HSN Code"]]
            .dropna()
            .drop_duplicates()
        )

        if not product_hsn_df.empty:

            product_hsn_df["Display"] = (
                product_hsn_df["Product"]
                + " ("
                + product_hsn_df["HSN Code"].astype(str)
                + ")"
            )

            product_options = sorted(product_hsn_df["Display"].unique())

            selected_display = st.selectbox(
                "Product",
                ["All"] + product_options,
                key="product_filter"
            )

            if selected_display == "All":
                df_product = df_segment
            else:
                selected_product = selected_display.split(" (")[0]
                df_product = df_segment[
                    df_segment["Product"] == selected_product
                ]
        else:
            df_product = df_segment

    # ================================
    # SEARCH BY HSN CODE
    # ================================
    else:

        entered_hsn = st.text_input(
            "HSN Code",
            placeholder="Enter 8 digit HSN Code",
            key="hsn_input"
        )

        if entered_hsn:

            entered_hsn = entered_hsn.strip()

            # 🔎 VALIDATION: must be exactly 8 digits
            if not (entered_hsn.isdigit() and len(entered_hsn) == 8):
                st.warning("Enter a valid 8 digit HSN Code")
                df_product = df_segment.iloc[0:0]

            else:
                df_filtered = df_segment[
                    df_segment["HSN Code"].astype(str) == entered_hsn
                ]

                if df_filtered.empty:
                    st.warning("Enter a valid HSN Code")
                    df_product = df_segment.iloc[0:0]
                else:
                    df_product = df_filtered

        else:
            df_product = df_segment
# --------------------------------------------------
# METRICS
# --------------------------------------------------
import_value = df_product[df_product["Imp / Exp"] == "Import"]["Trade Value in Crores"].sum()
export_value = df_product[df_product["Imp / Exp"] == "Export"]["Trade Value in Crores"].sum()
total_trade = import_value + export_value
trade_balance = export_value - import_value


# --------------------------------------------------
# YoY CALCULATIONS
# --------------------------------------------------
total_yoy = import_yoy = export_yoy = None

if year != "All":
    prev_df = df[
        (df["Year"] == year - 1)
        & ((df["Segment"] == selected_segment) if selected_segment != "All" else True)
        & ((df["Product"] == selected_product) if selected_product != "All" else True)
    ]

    prev_import = prev_df[prev_df["Imp / Exp"] == "Import"]["Trade Value in Crores"].sum()
    prev_export = prev_df[prev_df["Imp / Exp"] == "Export"]["Trade Value in Crores"].sum()
    prev_total = prev_import + prev_export

    if prev_total > 0:
        total_yoy = ((total_trade - prev_total) / prev_total) * 100
    if prev_import > 0:
        import_yoy = ((import_value - prev_import) / prev_import) * 100
    if prev_export > 0:
        export_yoy = ((export_value - prev_export) / prev_export) * 100


def pct(val):
    return "--" if val is None else f"{val:.2f}%"


# --------------------------------------------------
# KPI STYLES
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* ===== KPI TILE CONTAINER ===== */
    .kpi-card {
        background: #CFA6A0;
        border: 0px solid;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12);

        /* 🔒 FORCE SAME HEIGHT */
        height: 150px;
        width: 100%;

        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

        overflow: hidden;
    }

    /* ===== TITLES & VALUES ===== */
    .kpi-title {
        font-size: 26px;
        font-weight: 600;
        font-family: Georgia, serif;
        color: #4a4a4a;
        margin-bottom: 8px;
        text-align: center;
        line-height: 1.2;
    }

    .kpi-value {
        font-size: 30px;
        font-weight: 900;
        font-family: Georgia, serif;
        color: #2f2f2f;
        text-align: center;
        line-height: 1.2;
    }

    /* ===== YoY GRID ===== */
    .yoy-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        width: 100%;
        margin-top: 10px;
    }

    .yoy-item {
        background: rgba(255,255,255,0.65);
        padding: 8px;
        border-radius: 10px;
        text-align: center;
    }

    .yoy-label {
        font-size: 20px;
        font-weight: 600;
        font-family: Georgia, serif;
        color: #555;
        line-height: 1.2;
    }

    .yoy-value {
        font-size: 22px;
        font-weight: 900;
        font-family: Georgia, serif;
        color: #1f4fd8;
        line-height: 1.2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# KPI ROW
# --------------------------------------------------
k1, k2, k3 = st.columns([1, 2, 1])

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Total Trade</div>
            <div class="kpi-value">{format_inr(total_trade)} Cr</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card" style="justify-content: space-evenly;">
            <div class="kpi-title">📈 YoY Growth</div>
            <div class="yoy-grid">
                <div class="yoy-item">
                    <div class="yoy-label">Total Trade</div>
                    <div class="yoy-value">{pct(total_yoy)}</div>
                </div>
                <div class="yoy-item">
                    <div class="yoy-label">Imports</div>
                    <div class="yoy-value">{pct(import_yoy)}</div>
                </div>
                <div class="yoy-item">
                    <div class="yoy-label">Exports</div>
                    <div class="yoy-value">{pct(export_yoy)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    balance_text = (
        f"{format_inr(abs(trade_balance))} Cr (Deficit)"
        if trade_balance < 0
        else f"{format_inr(trade_balance)} Cr (Surplus)"
    )
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">⚖️ Trade Balance</div>
            <div class="kpi-value">{balance_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)


# ==================================================
# EXIM Analysis 
# ==================================================


col1, col2 = st.columns(2)

# -------------------------------
# LEFT: BAR CHART (VALUE)
# -------------------------------
with col1:

    bar_df = pd.DataFrame({
        "Trade Type": ["Import", "Export"],
        "Trade Value": [import_value, export_value]
    })

    bar_df["Formatted Value"] = bar_df["Trade Value"].apply(
        lambda x: format_inr(x) + " Cr"
    )

    bar_colors = ["#2F4B7C", "#7DA0C4"]

    fig_bar = px.bar(
        bar_df,
        x="Trade Type",
        y="Trade Value"
    )

    fig_bar.update_traces(
        textfont=dict(
        color="white",
        size=16,
        family="Georgia, serif"
    ),
        marker_color=bar_colors,
        text=bar_df["Formatted Value"],
        textposition="inside",
        customdata=bar_df["Formatted Value"],
        hovertemplate="Trade Value: %{customdata}<extra></extra>"
    )

    apply_globexim_chart_theme(fig_bar, "Import vs Export Value (₹ Crores)")

    fig_bar.update_layout(
        showlegend=False,
        uniformtext_minsize=11,
        uniformtext_mode="hide"
    )

    st.plotly_chart(fig_bar, use_container_width=True)



# -------------------------------
# RIGHT: PIE CHART (% SHARE)
# -------------------------------
with col2:
    fig_pie = px.pie(
        names=["Import", "Export"],
        values=[import_value, export_value],
        hole=0.5,
        color=["Import", "Export"],
        color_discrete_map={
            "Import": "#2F4B7C",
            "Export": "#7DA0C4"
        }
    )

    fig_pie.update_traces(
        textfont=dict(
        color="white",
        size=16,
        family="Georgia, serif"
    ),
        textinfo="percent",
        customdata=[
            format_inr(import_value) + " Cr",
            format_inr(export_value) + " Cr"
        ],
        hovertemplate="Trade Value: %{customdata}<extra></extra>"
    )

    apply_globexim_chart_theme(fig_pie, "Import vs Export Share (%)")

    st.plotly_chart(fig_pie, use_container_width=True)


# ==================================================
# IMPORT RISK METRICS
# ==================================================

df_imports = df_product[df_product['Imp / Exp'] == 'Import']

if df_imports.empty:
    total_import_volume = 0
    hhi = 0
    dominant_country = "N/A"
    dominant_share = 0
    volume_level = "No imports"
    concentration_level = "N/A"

else:
    # Import volume
    country_imports = (
        df_imports
        .groupby('Country')['Trade Value in Crores']
        .sum()
        .sort_values(ascending=False)
    )

    total_import_volume = country_imports.sum()

    # Market shares
    country_shares = country_imports / total_import_volume

    # HHI
    hhi = ((country_shares * 100) ** 2).sum()

    # Dominant country
    dominant_country = country_imports.idxmax()
    dominant_share = country_shares.loc[dominant_country] * 100

    # Volume classification
    if total_import_volume > 100:
        volume_level = "HIGH"
    elif total_import_volume >= 10:
        volume_level = "MODERATE"
    else:
        volume_level = "LOW"

    # Concentration classification
    if hhi > 2500:
        concentration_level = "HIGH"
    elif hhi >= 1500:
        concentration_level = "MODERATE"
    else:
        concentration_level = "LOW"


# --------------------------------------------------
# IMPORT RISK TILE STYLES
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* ===== RISK TILE (EQUAL HEIGHT + RESPONSIVE) ===== */
    .risk-tile {
        background: #CFA6A0;
        border: 0px solid;
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.25);

        height: 127px;
        width: 100%;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        text-align: center;
        box-sizing: border-box;
        overflow: hidden;
    }

    .risk-title {
        font-size: clamp(22px, 2vw, 22px);
        font-weight: 600;
        font-family: Georgia, serif;
        color: #4a4a4a;
        line-height: 1.2;
        margin-bottom: 6px;

        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .risk-value {
        font-size: clamp(20px, 2.8vw, 30px);
        font-weight: 900;
        font-family: Georgia, serif;
        color: #2f2f2f;
        line-height: 1.15;
        text-align: center;
    }

    .risk-subtext {
        font-size: clamp(13px, 1.6vw, 18px);
        font-family: Georgia, serif;
        color: #4b3434;
        margin-top: 6px;
        line-height: 1.15;

        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# IMPORT RISK METRICS — TILES
# ==================================================

t1, t2, t3 = st.columns(3)

# -------------------------------
# TILE 1: IMPORT VOLUME
# -------------------------------
with t1:
    st.markdown(
        f"""
        <div class="risk-tile">
            <div class="risk-title">📦 Import Volume</div>
            <div class="risk-value">{volume_level}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# TILE 2: IMPORT CONCENTRATION
# -------------------------------
with t2:
    st.markdown(
        f"""
        <div class="risk-tile">
            <div class="risk-title">📊 Import Concentration</div>
            <div class="risk-value">{concentration_level}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# TILE 3: DOMINANT COUNTRY
# -------------------------------
with t3:
    st.markdown(
        f"""
        <div class="risk-tile">
            <div class="risk-title">🌍 Dominant Import Source</div>
            <div class="risk-value">{dominant_country}</div>
            <div class="risk-subtext">
                {dominant_share:.2f}% of total imports
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# ==================================================
# MONTHLY TRADE TRENDS
# ==================================================

# Aggregate monthly trade
monthly = (
    df_product
    .groupby(['Year', 'Month_Num', 'Month_Name', 'Imp / Exp'])['Trade Value in Crores']
    .sum()
    .reset_index()
)

# Pivot Import / Export
monthly_pivot = (
    monthly
    .pivot_table(
        index=['Year', 'Month_Num', 'Month_Name'],
        columns='Imp / Exp',
        values='Trade Value in Crores',
        fill_value=0
    )
    .reset_index()
    .sort_values(['Year', 'Month_Num'])
)

# Total Trade
monthly_pivot['Total Trade'] = (
    monthly_pivot.get('Import', 0) + monthly_pivot.get('Export', 0)
)

# --------------------------------------------------
# Aggregate across years if Year = "All"
# --------------------------------------------------
if year == "All":
    plot_df = (
        monthly_pivot
        .groupby('Month_Num')[['Import', 'Export', 'Total Trade']]
        .sum()
        .reset_index()
        .sort_values('Month_Num')
    )

    plot_df['Month_Name'] = plot_df['Month_Num'].apply(
        lambda x: pd.to_datetime(str(x), format='%m').strftime('%B')
    )
else:
    plot_df = monthly_pivot.copy()

# --------------------------------------------------
# LINE CHART: MONTHLY TRADE TRENDS
# --------------------------------------------------
fig_line = go.Figure()

# TOTAL TRADE (GREEN)
fig_line.add_trace(
    go.Scatter(
        x=plot_df['Month_Name'],
        y=plot_df['Total Trade'],
        mode='lines+markers',
        name='Total Trade',
        line=dict(color='#2e7d32', width=3),
        marker=dict(size=7),
        customdata=[format_inr(v) + " Cr" for v in plot_df['Total Trade']],
        hovertemplate="%{customdata}<extra></extra>"
    )
)

# IMPORT (DARK BLUE)
fig_line.add_trace(
    go.Scatter(
        x=plot_df['Month_Name'],
        y=plot_df['Import'],
        mode='lines+markers',
        name='Import',
        line=dict(color="#2F4B7C", width=2),
        marker=dict(size=6),
        customdata=[format_inr(v) + " Cr" for v in plot_df['Import']],
        hovertemplate="%{customdata}<extra></extra>"
    )
)

# EXPORT (LIGHT BLUE)
fig_line.add_trace(
    go.Scatter(
        x=plot_df['Month_Name'],
        y=plot_df['Export'],
        mode='lines+markers',
        name='Export',
        line=dict(color="#7DA0C4", width=2),
        marker=dict(size=6),
        customdata=[format_inr(v) + " Cr" for v in plot_df['Export']],
        hovertemplate="%{customdata}<extra></extra>"
    )
)

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------
apply_globexim_chart_theme(fig_line, "Monthly Trade Trends")

fig_line.update_layout(
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_line, use_container_width=True)

st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

# ==================================================
# TOP 10 COUNTRIES (MIRRORED IMPORT / EXPORT)
# ==================================================
def format_k(val):
    if val >= 1000:
        return f"{int(val/1000)}k"
    return str(int(val))


def top_10(data, trade_type):
    return (
        data[data['Imp / Exp'] == trade_type]
        .groupby('Country')['Trade Value in Crores']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

top_imports = top_10(df_product, 'Import')
top_exports = top_10(df_product, 'Export')

# Mirror imports (negative only for plotting)
top_imports_plot = top_imports.copy()
top_imports_plot["Plot Value"] = -top_imports_plot["Trade Value in Crores"]

# Exports stay positive
top_exports_plot = top_exports.copy()
top_exports_plot["Plot Value"] = top_exports_plot["Trade Value in Crores"]

# Shared max for symmetric axis
max_val = max(
    top_imports["Trade Value in Crores"].max(),
    top_exports["Trade Value in Crores"].max()
)

tick_vals = np.linspace(0, max_val, 5)

col1, col2 = st.columns(2)



# -------------------------------
# IMPORTS (LEFT)
# -------------------------------
with col1:

    fig_imports = px.bar(
        top_imports_plot,
        x="Plot Value",
        y="Country",
        orientation="h",
        color_discrete_sequence=["#2F4B7C"]
    )

    fig_imports.update_layout(
        yaxis=dict(
        autorange="reversed",
        title=None,
        side="right",
        anchor="x"
        ),
        xaxis=dict(
            range=[-max_val, 0],
            tickvals=[-v for v in tick_vals],
            ticktext=[format_k(v) for v in tick_vals],
            title=None
        ),
        showlegend=False
    )

    fig_imports.update_traces(
        customdata=[
            f"{format_inr(v)} Cr"
            for v in top_imports_plot["Trade Value in Crores"]
        ],
        hovertemplate="%{y}<br>%{customdata}<extra></extra>"
    )

    apply_globexim_chart_theme(fig_imports, "Top 10 Import Countries")

    st.plotly_chart(fig_imports, use_container_width=True)


# -------------------------------
# EXPORTS (RIGHT)
# -------------------------------
with col2:

    fig_exports = px.bar(
        top_exports_plot,
        x="Plot Value",
        y="Country",
        orientation="h",
        color_discrete_sequence=["#7DA0C4"]
    )

    fig_exports.update_layout(
        yaxis=dict(
            autorange="reversed",
            title=None
        ),
        xaxis=dict(
            range=[0, max_val],
            tickvals=tick_vals.tolist(),
            ticktext=[format_k(v) for v in tick_vals],
            title=None
        ),
        showlegend=False
    )

    fig_exports.update_traces(
        customdata=[
            f"{format_inr(v)} Cr"
            for v in top_exports_plot["Trade Value in Crores"]
        ],
        hovertemplate="%{y}<br>%{customdata}<extra></extra>"
    )

    apply_globexim_chart_theme(fig_exports, "Top 10 Export Countries")

    st.plotly_chart(fig_exports, use_container_width=True)

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


