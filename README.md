# Digital GLOBEXIM - India's Medical Device Trade Intelligence Dashboard

A comprehensive Streamlit-based analytics platform for analyzing India's medical device import-export trade data.

## 🚀 Features

### Authentication System
- **User Registration**: Secure account creation with email and password
- **User Login**: Protected access with MongoDB-backed authentication
- **Session Management**: Persistent login state during browser session
- **Password Security**: Bcrypt-hashed passwords for maximum security

### Analytics Pages (5 Dashboards)

1. **Trade Overview**
   - Import vs Export analysis
   - Monthly trade trends
   - YoY growth metrics
   - Top 10 trading countries
   - Import risk indicators (HHI Index)

2. **Top Traded Devices**
   - Top 10 imported medical devices
   - Top 10 exported medical devices
   - Butterfly charts showing trade composition
   - Year and segment filters

3. **Import Risk Mapping**
   - Device-level import dependency analysis
   - HHI concentration index calculation
   - Import volume categorization (High/Moderate/Low)
   - Dominant source country identification

4. **Import Reliance**
   - Country-wise import dependency
   - Sensitivity analysis slider
   - Top 10 devices by import source
   - Scenario modeling capabilities

5. **Export Performance**
   - Country-wise export analysis
   - Top exported devices
   - Growth trend analysis
   - Sensitivity testing

## 📁 Project Structure

```
/app/streamlit_app/
├── Home.py                          # Main entry point with login/registration
├── auth.py                          # Authentication module
├── auth_utils.py                    # Authentication helper functions
├── requirements.txt                 # Python dependencies
├── Datasheet_DG.xlsx               # Medical device trade dataset
├── logos/
│   ├── globexim_logo.png
│   └── kiht_logo.png
└── pages/
    ├── 1_Trade_Overview.py
    ├── 2_Top_Traded_Devices.py
    ├── 3_Import_Risk_Mapping.py
    ├── 4_Import_Reliance.py
    └── 5_Export_Performance.py
```

## 🛠️ Technology Stack

- **Frontend Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly (interactive charts)
- **Database**: MongoDB (user authentication)
- **Security**: Bcrypt (password hashing)
- **File Handling**: openpyxl (Excel data)

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- MongoDB running on localhost:27017
- Supervisor for process management

### Install Dependencies
```bash
cd /app/streamlit_app
pip install -r requirements.txt
```

### Start the Application

**Using Supervisor (Recommended):**
```bash
sudo supervisorctl start streamlit
sudo supervisorctl status
```

**Manual Start:**
```bash
cd /app/streamlit_app
streamlit run Home.py --server.port 8501 --server.address 0.0.0.0
```

## 🌐 Access URLs

- **Streamlit Dashboard**: `https://health-trade-portal.preview.emergentagent.com:8501`
- **Frontend Info Page**: `https://health-trade-portal.preview.emergentagent.com`

## 🔐 Demo Credentials

For testing purposes:
- **Email**: test@example.com
- **Password**: password123

Or register your own account on the Home page!

## 📊 Data Source

The platform analyzes official import-export trade data using 155 Harmonized System of Nomenclature (HSN) codes mapped to medical devices.

**Data Source**: Department of Commerce, Ministry of Commerce and Industry, Government of India

## 💾 Database Schema

### Users Collection (MongoDB)
```javascript
{
  "_id": ObjectId,
  "email": String (unique),
  "password": Binary (bcrypt hash),
  "full_name": String,
  "created_at": DateTime,
  "last_login": DateTime
}
```

## 🔒 Security Features

1. **Password Hashing**: All passwords encrypted using bcrypt
2. **Session State**: Secure session management with Streamlit
3. **Authentication Gates**: All analytical pages protected
4. **Input Validation**: Email and password validation
5. **Database Security**: MongoDB with proper access controls

## 📈 Key Metrics & Analysis

- **Total Trade Value**: Import + Export in ₹ Crores
- **Trade Balance**: Export - Import (Surplus/Deficit)
- **YoY Growth**: Year-over-year percentage change
- **HHI Index**: Herfindahl-Hirschman Index for concentration
- **Import Volume Risk**: HIGH/MODERATE/LOW categorization
- **Import Concentration**: Supply chain dependency analysis

## 🎨 UI Features

- **Responsive Design**: Works on desktop and mobile
- **Custom Styling**: Professional color scheme (Blue/Amber/Silver)
- **Interactive Charts**: Plotly-based visualizations
- **Smart Filters**: Year, Segment, Product, HSN Code
- **Export Options**: Download charts and data

## 🐛 Troubleshooting

### Check Streamlit Status
```bash
sudo supervisorctl status streamlit
```

### View Logs
```bash
# Application logs
tail -f /var/log/supervisor/streamlit.out.log

# Error logs
tail -f /var/log/supervisor/streamlit.err.log
```

### Restart Service
```bash
sudo supervisorctl restart streamlit
```

### MongoDB Connection Issues
```bash
# Check MongoDB status
sudo supervisorctl status mongodb

# View MongoDB logs
tail -f /var/log/mongodb.out.log
```

## 📞 Contact & Support

**Andhra Pradesh MedTech Zone (AMTZ)**
- **Email**: info@amtz.in
- **Website**: www.kiht.in
- **Phone**: +91 8670694458

## 📄 License & Disclaimer

This platform is intended for analytical and informational purposes only. Findings should be interpreted alongside clinical, regulatory, and market context.

## 🎯 Future Enhancements

Potential additions:
- Email verification for registration
- Forgot password functionality
- User dashboard with saved filters
- Export reports as PDF
- Email notifications
- Advanced analytics (ML predictions)
- Real-time data updates
- Multi-language support

## 👥 User Roles (Future)

- **Viewer**: Read-only access
- **Analyst**: Full analytics access
- **Admin**: User management + analytics

---

**Built with ❤️ for India's Healthcare Industry**
