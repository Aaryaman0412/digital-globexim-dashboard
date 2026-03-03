# ✅ Streamlit Cloud Deployment - Quick Checklist

Follow these steps in order. Check off each one as you complete it.

---

## 🗄️ Part 1: MongoDB Atlas Setup (15 minutes)

- [ ] **1.** Go to https://cloud.mongodb.com and sign up
- [ ] **2.** Create FREE cluster (M0 tier)
- [ ] **3.** Wait 3-5 minutes for cluster to deploy
- [ ] **4.** Create database user:
  - Username: `globexim_admin`
  - Generate secure password
  - **SAVE PASSWORD SOMEWHERE SAFE!**
- [ ] **5.** Set network access to `0.0.0.0/0` (Allow from anywhere)
- [ ] **6.** Get connection string from "Connect" button
- [ ] **7.** Replace `<username>` and `<password>` in connection string
- [ ] **8.** Create database named `globexim_db` with collection `users`

**Your connection string should look like:**
```
mongodb+srv://globexim_admin:YOUR_PASSWORD@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
```

---

## 📂 Part 2: GitHub Repository (10 minutes)

- [ ] **9.** Go to https://github.com and login
- [ ] **10.** Create new repository:
  - Name: `digital-globexim-dashboard`
  - Visibility: **Public**
  - Add README: ✅
- [ ] **11.** Upload these files from `/app/streamlit_app/`:
  - [ ] `Home.py`
  - [ ] `auth.py`
  - [ ] `auth_utils.py`
  - [ ] `Datasheet_DG.xlsx`
  - [ ] `requirements.txt`
  - [ ] `.gitignore`
  - [ ] `.streamlit/config.toml`
  - [ ] `logos/globexim_logo.png`
  - [ ] `logos/kiht_logo.png`
  - [ ] `pages/1_Trade_Overview.py`
  - [ ] `pages/2_Top_Traded_Devices.py`
  - [ ] `pages/3_Import_Risk_Mapping.py`
  - [ ] `pages/4_Import_Reliance.py`
  - [ ] `pages/5_Export_Performance.py`
  - [ ] `README.md`

**DO NOT upload:** `.streamlit/secrets.toml` (if it exists)

---

## ☁️ Part 3: Streamlit Cloud (5 minutes)

- [ ] **12.** Go to https://share.streamlit.io
- [ ] **13.** Sign up with GitHub account
- [ ] **14.** Click "New app"
- [ ] **15.** Configure:
  - Repository: `your-username/digital-globexim-dashboard`
  - Branch: `main`
  - Main file: `Home.py`
- [ ] **16.** Click "Advanced settings"
- [ ] **17.** In Secrets section, paste this (with YOUR details):

```toml
[mongo]
connection_string = "mongodb+srv://globexim_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
database_name = "globexim_db"
```

- [ ] **18.** Click "Deploy!"
- [ ] **19.** Wait 2-3 minutes for deployment

---

## ✅ Part 4: Testing (5 minutes)

- [ ] **20.** Open your app URL (looks like: `https://xxx.streamlit.app`)
- [ ] **21.** See login/registration page? ✅
- [ ] **22.** Click "Register" tab
- [ ] **23.** Create test account:
  - Name: Test User
  - Email: test@example.com
  - Password: password123
- [ ] **24.** Click "Register" - see success message? ✅
- [ ] **25.** Switch to "Login" tab
- [ ] **26.** Login with test account ✅
- [ ] **27.** Navigate to all 5 pages:
  - [ ] Trade Overview
  - [ ] Top Traded Devices
  - [ ] Import Risk Mapping
  - [ ] Import Reliance
  - [ ] Export Performance
- [ ] **28.** Test filters on any page ✅
- [ ] **29.** Click Logout ✅

---

## 🎉 Done!

- [ ] **30.** Copy your Streamlit app URL
- [ ] **31.** Share with others!

**Your app URL**: `https://_____________.streamlit.app`

---

## ⚠️ Troubleshooting

### ❌ MongoDB Connection Error
1. Check Network Access in MongoDB Atlas is `0.0.0.0/0`
2. Verify connection string has correct password
3. Check for special characters in password (URL encode them)

### ❌ File Not Found Error
1. Check all files are uploaded to GitHub
2. Verify file names match exactly (case-sensitive)
3. Ensure `Datasheet_DG.xlsx` is in root folder

### ❌ Module Import Error
1. Check `requirements.txt` is uploaded
2. Click "Reboot app" in Streamlit Cloud settings

### ❌ Secrets Not Working
1. Go to Streamlit Cloud → App → Settings → Secrets
2. Verify format matches exactly (no extra spaces/quotes)
3. Click Save and Reboot app

---

## 📞 Need Help?

**Complete guide**: See `STREAMLIT_CLOUD_DEPLOYMENT.md`

**Support**:
- Streamlit: https://discuss.streamlit.io
- MongoDB: https://community.mongodb.com
- AMTZ: info@amtz.in

---

## ⏱️ Total Time: ~35 minutes

You're ready to deploy! Start with Part 1. 🚀
