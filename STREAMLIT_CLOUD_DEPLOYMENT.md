# 🚀 Streamlit Cloud Deployment Guide

Complete step-by-step guide to deploy Digital GLOBEXIM on Streamlit Cloud with MongoDB Atlas.

---

## 📋 Prerequisites

- GitHub account
- MongoDB Atlas account (free tier available)
- Your Streamlit app files ready

---

## Step 1: Set Up MongoDB Atlas (Free Tier)

### 1.1 Create MongoDB Atlas Account
1. Go to https://cloud.mongodb.com
2. Click "Try Free"
3. Sign up with email or Google
4. Verify your email

### 1.2 Create a Cluster
1. After login, click "Build a Database"
2. Choose **FREE** tier (M0)
3. Select cloud provider: **AWS** (recommended)
4. Choose region: **Closest to your users** (e.g., Mumbai for India)
5. Cluster Name: `Cluster0` (or your choice)
6. Click "Create"

⏱️ Wait 3-5 minutes for cluster creation

### 1.3 Configure Database Access
1. Click "Database Access" in left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. **Username**: `globexim_admin` (or your choice)
5. **Password**: Click "Autogenerate Secure Password" and **SAVE IT**
6. Database User Privileges: Select "Read and write to any database"
7. Click "Add User"

### 1.4 Configure Network Access
1. Click "Network Access" in left sidebar
2. Click "Add IP Address"
3. Select "Allow Access from Anywhere" (0.0.0.0/0)
   - ⚠️ This is required for Streamlit Cloud
   - Comment: "Streamlit Cloud Access"
4. Click "Confirm"

### 1.5 Get Connection String
1. Click "Database" in left sidebar
2. Click "Connect" button on your cluster
3. Select "Connect your application"
4. Driver: **Python**, Version: **3.11 or later**
5. Copy the connection string:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. **Replace** `<username>` with your database username
7. **Replace** `<password>` with your database password
8. **SAVE THIS** - you'll need it later!

### 1.6 Create Database
1. In MongoDB Atlas, click "Browse Collections"
2. Click "Add My Own Data"
3. Database name: `globexim_db`
4. Collection name: `users`
5. Click "Create"

✅ MongoDB Atlas setup complete!

---

## Step 2: Prepare Your GitHub Repository

### Option A: Using Emergent's "Save to GitHub"

1. In Emergent interface, look for "Save to GitHub" button/feature
2. Click it and follow prompts
3. Create new repository: `digital-globexim-dashboard`
4. Make it **Public**
5. Push all files from `/app/streamlit_app/`

### Option B: Manual GitHub Setup

1. Go to https://github.com
2. Click "New Repository"
3. Repository name: `digital-globexim-dashboard`
4. Description: "India's Medical Device Trade Intelligence Dashboard"
5. Choose **Public**
6. ✅ Check "Add a README file"
7. Click "Create repository"

Then upload these files from `/app/streamlit_app/`:
- `Home.py`
- `auth.py`
- `auth_utils.py`
- `Datasheet_DG.xlsx`
- `requirements.txt`
- `.gitignore`
- `.streamlit/config.toml`
- `logos/` folder (both PNG files)
- `pages/` folder (all 5 Python files)
- `README.md`
- `USER_GUIDE.md`

**DO NOT upload**: `.streamlit/secrets.toml` (if it exists)

---

## Step 3: Deploy to Streamlit Cloud

### 3.1 Sign Up for Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "Sign up" or "Continue with GitHub"
3. Authorize Streamlit to access your GitHub
4. Accept permissions

### 3.2 Create New App
1. Click "New app" button
2. Fill in details:
   - **Repository**: Select your GitHub repo (`digital-globexim-dashboard`)
   - **Branch**: `main` (or `master`)
   - **Main file path**: `Home.py`
3. Click "Advanced settings" (expand)

### 3.3 Configure Secrets
1. In Advanced settings, find "Secrets" section
2. Paste the following (replace with your actual MongoDB details):

```toml
[mongo]
connection_string = "mongodb+srv://globexim_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
database_name = "globexim_db"
```

**Replace**:
- `YOUR_PASSWORD` with your MongoDB password
- `cluster0.xxxxx.mongodb.net` with your actual cluster address

### 3.4 Deploy
1. Click "Deploy!"
2. ⏱️ Wait 2-3 minutes for deployment
3. Watch the logs in the terminal window

✅ Your app will be live at: `https://your-app-name.streamlit.app`

---

## Step 4: Test Your Deployment

### 4.1 Access the App
1. Open your Streamlit Cloud URL
2. You should see the login/registration page

### 4.2 Register Test User
1. Click "Register" tab
2. Fill in:
   - Full Name: Test User
   - Email: test@example.com
   - Password: password123
   - Confirm Password: password123
3. Click "Register"

### 4.3 Login
1. Switch to "Login" tab
2. Enter credentials
3. Click "Login"
4. You should see the dashboard home page!

### 4.4 Test All Pages
Navigate through all 5 pages:
- ✅ Trade Overview
- ✅ Top Traded Devices
- ✅ Import Risk Mapping
- ✅ Import Reliance
- ✅ Export Performance

---

## 🎉 You're Live!

Your dashboard is now publicly accessible at your Streamlit Cloud URL!

**Share it**:
- `https://your-app-name.streamlit.app`

---

## 🔧 Troubleshooting

### Issue: MongoDB Connection Error

**Error**: "pymongo.errors.ServerSelectionTimeoutError"

**Solution**:
1. Check MongoDB Atlas Network Access
2. Ensure "0.0.0.0/0" is allowed
3. Verify connection string is correct
4. Check username/password (no special characters that need encoding)

**Fix Special Characters in Password**:
If your password has special characters, URL-encode them:
- `@` → `%40`
- `#` → `%23`
- `$` → `%24`
- etc.

### Issue: Module Not Found

**Error**: "ModuleNotFoundError: No module named 'xxx'"

**Solution**:
1. Check `requirements.txt` includes all dependencies
2. Redeploy the app (Streamlit Cloud will reinstall)

### Issue: File Not Found

**Error**: "FileNotFoundError: Datasheet_DG.xlsx"

**Solution**:
1. Ensure `Datasheet_DG.xlsx` is in the root of your GitHub repo
2. Check file name exactly matches (case-sensitive)
3. Ensure file was actually uploaded to GitHub

### Issue: Secrets Not Working

**Error**: "KeyError: 'mongo'"

**Solution**:
1. Go to Streamlit Cloud → Your App → Settings
2. Click "Secrets"
3. Verify format matches exactly:
```toml
[mongo]
connection_string = "mongodb+srv://..."
database_name = "globexim_db"
```
4. Click "Save"
5. Reboot app

### Issue: App is Slow

**Solution**:
- Streamlit Cloud free tier has resource limits
- Consider upgrading to Streamlit Cloud Teams
- Optimize data loading with `@st.cache_data`

---

## 📊 MongoDB Atlas Tips

### View Your Users
1. Go to MongoDB Atlas
2. Click "Browse Collections"
3. Select `globexim_db` → `users`
4. See all registered users

### Backup Database
1. Go to "Backups" in MongoDB Atlas
2. Free tier doesn't include automated backups
3. Manually export data: Collections → Export Collection

### Monitor Usage
1. Go to "Metrics" in MongoDB Atlas
2. See connection count, operations, storage
3. Free tier limits:
   - 512 MB storage
   - Shared CPU
   - No backups

---

## 🔒 Security Best Practices

### ✅ Do's
- ✅ Use strong passwords for MongoDB
- ✅ Keep secrets in Streamlit Cloud (not in code)
- ✅ Regularly review registered users
- ✅ Monitor MongoDB access logs

### ❌ Don'ts
- ❌ Never commit secrets.toml to GitHub
- ❌ Don't share your MongoDB connection string
- ❌ Don't use simple passwords for database
- ❌ Don't disable network access restrictions without reason

---

## 🔄 Updating Your App

### Update Code
1. Make changes to your local files
2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push
   ```
3. Streamlit Cloud will auto-redeploy!

### Update Dataset
1. Replace `Datasheet_DG.xlsx` in GitHub repo
2. Commit and push
3. App will reload with new data

### Update Secrets
1. Go to Streamlit Cloud → App → Settings
2. Edit Secrets
3. Save
4. Reboot app

---

## 💰 Pricing

### MongoDB Atlas (Free Tier)
- ✅ 512 MB storage
- ✅ Shared RAM
- ✅ No credit card required
- Upgrade: $0.08/hr for dedicated clusters

### Streamlit Cloud (Free Tier)
- ✅ 1 GB RAM per app
- ✅ Unlimited public apps
- ✅ No credit card required
- ✅ GitHub integration
- Upgrade: $20/month for Teams (more resources)

---

## 📈 Monitoring Your App

### Streamlit Cloud Dashboard
1. Go to https://share.streamlit.io
2. Click on your app
3. View:
   - Deployment logs
   - Active users (limited in free tier)
   - Resource usage

### MongoDB Atlas Dashboard
1. Go to MongoDB Atlas
2. View:
   - Database size
   - Number of users
   - Connection count
   - Query performance

---

## 🎓 Next Steps

After successful deployment:

1. **Custom Domain** (Streamlit Teams):
   - Point your domain to Streamlit app
   - `dashboard.yourdomain.com`

2. **Analytics**:
   - Add Google Analytics
   - Track user behavior
   - Monitor popular features

3. **Email Notifications**:
   - Integrate SendGrid or similar
   - Send welcome emails
   - Password reset emails

4. **Advanced Features**:
   - Add admin panel
   - User role management
   - Export to PDF/Excel
   - Real-time data updates

---

## 📞 Support

### Streamlit Cloud Issues
- Docs: https://docs.streamlit.io/streamlit-community-cloud
- Forum: https://discuss.streamlit.io
- Email: support@streamlit.io

### MongoDB Atlas Issues
- Docs: https://docs.atlas.mongodb.com
- Support: https://support.mongodb.com
- Forum: https://community.mongodb.com

### App Issues
📧 info@amtz.in  
🌐 www.kiht.in  
📱 +91 8670694458

---

## ✅ Deployment Checklist

Before going live:

- [ ] MongoDB Atlas cluster created
- [ ] Database user created with password saved
- [ ] Network access configured (0.0.0.0/0)
- [ ] Connection string tested
- [ ] GitHub repository created (public)
- [ ] All files uploaded to GitHub
- [ ] `.gitignore` includes `secrets.toml`
- [ ] Streamlit Cloud account created
- [ ] App deployed with correct repo/file
- [ ] Secrets configured in Streamlit Cloud
- [ ] Test registration works
- [ ] Test login works
- [ ] All 5 pages accessible
- [ ] Charts loading correctly
- [ ] Filters working
- [ ] Logout working
- [ ] Shared URL with others

---

## 🎉 Congratulations!

Your Digital GLOBEXIM dashboard is now live on Streamlit Cloud with MongoDB Atlas!

**Share your app**: `https://your-app-name.streamlit.app`

---

*Last Updated: February 2025*  
*Version: 1.0 - Streamlit Cloud Edition*
