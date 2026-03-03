# 🎯 Digital GLOBEXIM - Quick Start Guide

## 📱 Accessing the Dashboard

### Method 1: Direct Access (Recommended)
**URL**: `https://health-trade-portal.preview.emergentagent.com:8501`

### Method 2: Via Frontend Info Page
1. Visit: `https://health-trade-portal.preview.emergentagent.com`
2. Click "Open Dashboard" button

---

## 🔐 First Time Setup

### Option A: Use Demo Account
```
Email: test@example.com
Password: password123
```

### Option B: Create New Account
1. Click on **"Register"** tab
2. Fill in:
   - Full Name
   - Email address
   - Password (minimum 6 characters)
   - Confirm Password
3. Click **"Register"** button
4. Switch to **"Login"** tab
5. Enter your credentials and login

---

## 📊 Dashboard Features

### 🏠 Home Page
- Platform overview and methodology
- Login/Registration interface
- User authentication status

### 📈 1. Trade Overview
**What it shows:**
- Total trade value (Imports + Exports)
- Trade balance (Surplus/Deficit)
- Year-over-year growth percentages
- Monthly trade trends
- Top 10 import/export countries
- Import risk indicators

**Filters:**
- Year (All or specific year)
- Segment
- Search by Product Type or HSN Code

**Key Metrics:**
- Import Volume Risk (HIGH/MODERATE/LOW)
- Import Concentration (HHI Index)
- Dominant Import Source Country

### 📦 2. Top Traded Devices
**What it shows:**
- Butterfly chart of top 10 most traded devices
- Top 10 imported medical devices
- Top 10 exported medical devices
- Trade value composition

**Filters:**
- Year selection
- Segment selection

### 🗺️ 3. Import Risk Mapping
**What it shows:**
- Device-level import dependency
- Import concentration risk assessment
- HHI (Herfindahl-Hirschman Index) values
- Dominant source countries
- Import volumes

**Filters:**
- Year
- Import Volume Risk (All/HIGH/MODERATE/LOW)
- Import Concentration Risk (All/HIGH/MODERATE/LOW)

**Understanding HHI:**
- HHI < 1,500 = Low concentration
- HHI 1,500-2,500 = Moderate concentration
- HHI > 2,500 = High concentration

### 🌍 4. Import Reliance
**What it shows:**
- Country-wise import dependency
- Top 10 devices imported from selected countries
- Sensitivity analysis capabilities

**Filters:**
- Year selection
- Country/Countries selection (multi-select)

**Interactive Feature:**
- Sensitivity slider (-50% to +50%)
- See impact of import changes in real-time

### 📤 5. Export Performance
**What it shows:**
- Country-wise export analysis
- Top 10 exported devices by destination
- Export growth trends

**Filters:**
- Year selection
- Country/Countries selection

**Interactive Feature:**
- Sensitivity analysis slider
- Export scenario modeling

---

## 🎨 Using Filters

### Year Filter
- **"All"**: Shows combined data across all years
- **Specific Year**: Shows data for selected year only

### Segment Filter
- Medical device categories
- Examples: Diagnostic, Therapeutic, etc.

### Product Type Search
- Select from dropdown of medical devices
- Excludes generic "Others" and "Parts" categories
- Shows HSN code in parentheses

### HSN Code Search
- Enter 8-digit HSN code
- Must be exact match
- Validates input automatically

### Country Selection
- **"All"**: Includes all countries
- **Multiple Countries**: Hold Ctrl/Cmd to select multiple
- Note: "All" and specific countries are mutually exclusive

---

## 📊 Understanding the Charts

### Bar Charts
- **Horizontal bars**: Better readability for country/product names
- **Hover**: Shows exact values
- **Colors**: 
  - Dark Blue (#2F4B7C) = Imports
  - Light Blue (#7DA0C4) = Exports

### Pie Charts
- Shows percentage distribution
- Hover for exact values
- Donut style for better aesthetics

### Line Charts
- Monthly trends over time
- Multiple series (Total, Import, Export)
- Interactive legend (click to hide/show)

### Butterfly Charts
- Left side = Imports (negative values for visualization)
- Right side = Exports
- Center = Product names
- Shows relative importance of each device

---

## 🔒 Security Features

✅ **Password Protection**: Bcrypt hashing
✅ **Session Management**: Auto-logout on browser close
✅ **Email Validation**: Prevents duplicate registrations
✅ **Input Sanitization**: Protected against injection attacks
✅ **Secure Database**: MongoDB with proper access controls

---

## 💡 Tips & Best Practices

### For Policy Makers
1. Start with **Trade Overview** for macro trends
2. Use **Import Risk Mapping** to identify critical dependencies
3. Check **Import Reliance** for country-specific strategies
4. Use sensitivity analysis for scenario planning

### For Researchers
1. Use filters to narrow down to specific devices
2. Export charts for presentations (right-click → Save)
3. Compare year-over-year trends
4. Analyze HHI values for concentration studies

### For Industry Analysts
1. Check **Top Traded Devices** for market opportunities
2. Use **Export Performance** to identify growing markets
3. Monitor import volumes for competitive analysis
4. Track monthly trends for seasonality

### For Manufacturers
1. Identify high-import devices for substitution opportunities
2. Check export destinations for expansion
3. Monitor import concentration for supply chain risks
4. Use trade balance data for market sizing

---

## ⚡ Performance Tips

1. **Initial Load**: First page load may take 10-15 seconds
2. **Filters**: Apply filters sequentially for faster response
3. **Large Datasets**: "All" year filter may be slower
4. **Charts**: Hover interactions are instant
5. **Session**: Stays active until browser closes

---

## 🐛 Troubleshooting

### Cannot Access Dashboard
- Check URL includes port `:8501`
- Try incognito/private browsing mode
- Clear browser cache

### Login Not Working
- Verify email is registered
- Check password (case-sensitive)
- Try resetting by re-registering with different email

### Page Not Loading
- Check internet connection
- Refresh the page (F5)
- Logout and login again

### Charts Not Displaying
- Wait 5-10 seconds for data processing
- Check if filters are too restrictive
- Try selecting "All" for broader view

### Slow Performance
- Select specific year instead of "All"
- Use single country instead of multiple
- Refresh the page if it becomes sluggish

---

## 📞 Support & Contact

**For Technical Issues:**
- Check logs in supervisor
- Contact system administrator

**For Data Questions:**
📧 Email: info@amtz.in
🌐 Website: www.kiht.in
📱 Phone: +91 8670694458

**For Feature Requests:**
- Submit feedback through contact information above

---

## 🔄 Session Management

### Active Session
- Shows: "Welcome, [Your Name]" at top
- Can access all 5 dashboard pages
- Logout button visible in sidebar

### Expired Session
- Automatically redirected to login
- Message: "Please login to access this page"
- Simply login again to continue

### Logout
- Click "🚪 Logout" button in sidebar
- Or close browser window
- All session data cleared

---

## 📥 Data Download Options

Currently available via browser:
1. **Charts**: Right-click → Save image
2. **Screenshots**: Use browser screenshot tools
3. **Data Export**: Copy from charts (hover + click)

Future enhancement: Direct Excel/PDF export

---

## 🎓 Glossary

**HHI**: Herfindahl-Hirschman Index - measures market concentration

**HSN Code**: Harmonized System of Nomenclature - international product classification

**Cr**: Crores (₹1 crore = ₹10 million)

**YoY**: Year-over-Year comparison

**Trade Balance**: Exports minus Imports

**Sensitivity Analysis**: Testing impact of hypothetical changes

**Import Concentration**: Degree of dependence on few source countries

**Device Segment**: Category of medical devices (e.g., diagnostic, therapeutic)

---

## ✅ Checklist for First-Time Users

- [ ] Access the dashboard URL
- [ ] Register new account OR use demo credentials
- [ ] Login successfully
- [ ] Navigate to Trade Overview
- [ ] Apply year filter
- [ ] Try product search
- [ ] Hover over charts to see details
- [ ] Visit all 5 pages
- [ ] Try sensitivity analysis slider
- [ ] Logout and login again to verify

---

**🎉 You're now ready to explore India's Medical Device Trade Intelligence!**

For advanced features and custom analysis, contact the support team.

---

*Last Updated: February 2025*
*Version: 1.0*
