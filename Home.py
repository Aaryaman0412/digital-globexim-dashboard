import streamlit as st
import base64
from auth import init_session_state, register_user, login_user, logout

# Initialize session state
init_session_state()

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="India Medical Device Trade Intelligence",
    layout="wide"
)

# --------------------------------------------------
# STYLING
# --------------------------------------------------
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
        background-color: #374151;
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

    /* Sidebar labels */
    [data-testid="stSidebar"] label {
        color: #1E40AF;
        font-weight: 600;
    }
    
    /* Login Container */
    .login-container {
        max-width: 450px;
        margin: 50px auto;
        padding: 40px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .login-title {
        text-align: center;
        color: #1E3A8A;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# CHECK AUTHENTICATION STATUS
# --------------------------------------------------
if not st.session_state.authenticated:
    # Show login/registration page
    
    # Header with logos
    try:
        globexim_logo = img_to_base64("logos/globexim_logo.png")
        kiht_logo = img_to_base64("logos/kiht_logo.png")
        
        c1, c2, c3 = st.columns([1.2, 4, 1.5])
        
        with c1:
            st.markdown(
                f"""
                <img src="data:image/png;base64,{globexim_logo}" width="210">
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
                    <h1 style="margin-bottom: 6px;color:#1E3A8A;">Digital GLOBEXIM</h1>
                    <h3 style="margin-top: 0;">
                        India's Medical Device Trade Intelligence Dashboard
                    </h3>
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
                    align-items: center;
                ">
                    <img src="data:image/png;base64,{kiht_logo}" width="210">
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown(
            "<hr style='margin-top: 10px; margin-bottom: 12px;'>",
            unsafe_allow_html=True
        )
    except:
        st.title("Digital GLOBEXIM")
        st.subheader("India's Medical Device Trade Intelligence Dashboard")
    
    # Login/Registration tabs
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Login to Access Dashboard</div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if email and password:
                    success, result = login_user(email, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_name = result.get('full_name', 'User')
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.warning("⚠️ Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Create New Account</div>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            reg_email = st.text_input("Email", placeholder="your.email@example.com", key="reg_email")
            reg_password = st.text_input("Password", type="password", placeholder="Choose a strong password", key="reg_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            register_submit = st.form_submit_button("Register", use_container_width=True)
            
            if register_submit:
                if full_name and reg_email and reg_password and confirm_password:
                    if reg_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(reg_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        success, message = register_user(reg_email, reg_password, full_name)
                        if success:
                            st.success(f"✅ {message}! Please login to continue.")
                        else:
                            st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer info
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("ℹ️ **Note:** Register with your email to access comprehensive medical device trade analytics for India.")

else:
    # User is authenticated - show main content
    
    # Header with logos and logout
    try:
        globexim_logo = img_to_base64("logos/globexim_logo.png")
        kiht_logo = img_to_base64("logos/kiht_logo.png")
        
        c1, c2, c3 = st.columns([1.2, 4, 1.5])
        
        with c1:
            st.markdown(
                f"""
                <img src="data:image/png;base64,{globexim_logo}" width="210">
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
                    <h1 style="margin-bottom: 6px;color:#1E3A8A;">Digital GLOBEXIM</h1>
                    <h3 style="margin-top: 0;">
                        India's Medical Device Trade Intelligence Dashboard
                    </h3>
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
                    align-items: center;
                ">
                    <img src="data:image/png;base64,{kiht_logo}" width="210">
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown(
            "<hr style='margin-top: 10px; margin-bottom: 12px;'>",
            unsafe_allow_html=True
        )
    except:
        st.title("Digital GLOBEXIM")
    
    # Welcome message and logout button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"👋 Welcome, **{st.session_state.user_name}**!")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    
    # Main content
    st.markdown(
        """
        <style>
        /* Justify paragraph text */
        p {
            text-align: justify;
            text-justify: inter-word;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("India's Medical Device Landscape")

    st.markdown(
        """
    Medical Devices form an intrinsic part of any modern day healthcare system. In recent years, India's medical devices sector has gained considerable prominence, particularly in the wake of the COVID-19 pandemic, which underscored its strategic importance in supporting both domestic and international healthcare responses. The crisis served as a catalyst for accelerated production of critical devices such as ventilators, Rapid Antigen Test kits, RT-PCR kits, infrared thermometers, PPE kits, and N-95 masks. 

    During this period, the **Andhra Pradesh MedTech Zone (AMTZ)** emerged as a key contributor by rapidly scaling the production of essential medical equipment—including low-cost ventilators, up to 10 lakh RT-PCR kits and 1 lakh N-95 masks per day, oxygen concentrators, and PPE kits. AMTZ also deployed innovative solutions such as mobile RT-PCR laboratories (i-Labs), container-based ICU units to reach underserved regions. Through its incubators, it fast-tracked COVID-19–related innovations and trained biomedical professionals under the Indian Biomedical Skill Consortium (IBSC). These developments  strengthened India's crisis preparedness and response capabilities at a global level. These efforts not only filled critical gaps in the medical supply chain during a global emergency but also demonstrated AMTZ's pivotal role in advancing India's healthcare infrastructure and self-reliance in medical technology.

    Despite showing signs of positive future growth  and ranking among the top global markets, the industry is predominantly import-driven, with imports constituting around 70% of total trade value. Nonetheless, the future of this industry is immense, underscored by favourable socio-economic trends, technological advancements and supportive policy initiatives.
    """
    )

    st.header("Why This Platform?")

    st.markdown(
        """
    India's medical device trade is dynamic, complex, and increasingly critical to health system resilience, yet the underlying data often remains fragmented, static, and difficult to interpret for timely decision-making. This platform has been developed to translate granular import–export data into structured, interactive, and continuously explorable insights that supports analysis across policy, industry, and research domains. It serves as a digital, analytical extension of the annual flagship **GLOBEXIM** report, complementing its comprehensive narrative and macro-level findings with device-level drill-downs, trend exploration, and risk mapping capabilities. Together, the report and this platform enable stakeholders to move beyond static snapshots toward a deeper, more actionable understanding of India's medical device trade landscape.
    """
    )

    st.header("Methodology")

    st.markdown(
        """
    The analysis presented on this platform is based on structured extraction and processing of official import–export trade data using 155 Harmonized System of Nomenclature (HSN) codes mapped to different medical devices. During data preparation, HSN codes with labels like "Others" and "Parts" were excluded from device-level product lists to avoid dilution of interpretability, as these codes often aggregate heterogeneous products or intermediate components that cannot be reliably assigned to a specific finished medical device. However, to preserve the integrity of overall trade magnitude, the final import and export values reported at the aggregate level include these excluded codes, ensuring that total trade values accurately reflect the full scale of medical device trade.

    Building on the processed dataset, the platform computes a set of trade indicators including total import and export values, year-wise trends, and measures of supply concentration. Import concentration is assessed using the Herfindahl–Hirschman Index (HHI), calculated by squaring the percentage share of imports from each source country and summing them across all exporting countries; HHI = Σ (sᵢ × 100)², where sᵢ denotes the share of imports from country i. Expressing import shares in percentage terms places the index on a 0–10,000 scale, improving interpretability and aligning the analysis with standard trade and competition economics practices.

    For ease of interpretation and comparative analysis across medical devices, both import concentration and import volume are categorised into high, moderate, and low groups. Import concentration is classified based on HHI values, with HHI below 1,500 indicating low concentration, 1,500–2,500 indicating moderate concentration, and values above 2,500 indicating high concentration, reflecting increasing dependence on a limited number of source countries. Import volumes are categorised using absolute trade value thresholds, with imports below ₹10 crore classified as low volume, ₹10–₹100 crore as moderate volume, and imports exceeding ₹100 crore as high volume. This combined classification framework allows concentration risk to be interpreted in the context of trade magnitude, ensuring that devices with both high concentration and high import volumes are appropriately prioritised, while avoiding over-interpretation of concentrated but low-volume imports.
    """
    )

    st.header("How to Use This Platform")

    st.markdown(
        """
    Use the sidebar to navigate across dashboards and explore India's medical device trade at multiple levels. Begin with the high-level trade views to understand overall import and export trends, then drill down to specific devices to examine trade values, growth patterns, and import concentration. Interactive filters allow users to select years, device categories, and risk levels to tailor the analysis to specific questions. For deeper insights, combine import concentration indicators with import volumes to identify devices that may pose strategic supply risks. Together, these tools enable users to move seamlessly from overview to device-level evidence, supporting informed policy analysis, market assessment, and research applications.
    """
    )

    st.header("Who Can Benefit")

    st.markdown(
        """
    - **Policy makers** to support evidence-based planning, import substitution strategies, and supply-chain resilience

    - **Researchers** for trade-based risk assessment, evidence synthesis, and system-level analysis

    - **Manufacturers & startups** to identify import-dependent devices, market gaps, and domestic manufacturing opportunities

    - **Investors & industry analysts** to assess market structure, dependency risks, and growth potential across device segments

    - **Healthcare institutions & procurement bodies**  to understand supply vulnerabilities and continuity-of-care risks

    - **International agencies & development partners**  to evaluate trade exposure and local manufacturing capacity in a global health security context
    """
    )

    st.markdown(
        """
        <hr style='border:1px solid #444;'>
        <p style='text-align:left;color:#1F2937;font-size:18px;'>
       Disclaimer: This platform is intended for analytical and informational purposes only. Findings should be interpreted alongside clinical, regulatory, and market context.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
        <div style="
            position: fixed;
            bottom: 15px;
            left: 20px;
            font-size: 15px;
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
