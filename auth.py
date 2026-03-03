import bcrypt
import streamlit as st
from pymongo import MongoClient
from datetime import datetime

def get_db():
    """Get MongoDB database connection"""
    # Try to get connection from Streamlit secrets (Cloud deployment)
    try:
        mongo_url = st.secrets["mongo"]["connection_string"]
        db_name = st.secrets["mongo"]["database_name"]
    except (KeyError, FileNotFoundError):
        # Fallback to local development
        mongo_url = "mongodb://localhost:27017"
        db_name = "globexim_db"
    
    client = MongoClient(mongo_url)
    return client[db_name]

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify a password against a hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def register_user(email, password, full_name):
    """Register a new user"""
    db = get_db()
    users = db.users
    
    # Check if user already exists
    if users.find_one({"email": email}):
        return False, "Email already registered"
    
    # Create new user
    user_data = {
        "email": email,
        "password": hash_password(password),
        "full_name": full_name,
        "created_at": datetime.now(),
        "last_login": None
    }
    
    users.insert_one(user_data)
    return True, "Registration successful"

def login_user(email, password):
    """Authenticate user login"""
    db = get_db()
    users = db.users
    
    # Find user
    user = users.find_one({"email": email})
    
    if not user:
        return False, "Email not found"
    
    # Verify password
    if verify_password(password, user['password']):
        # Update last login
        users.update_one(
            {"email": email},
            {"$set": {"last_login": datetime.now()}}
        )
        return True, user
    else:
        return False, "Incorrect password"

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_name = None
