import streamlit as st

def check_authentication():
    """Check if user is authenticated, redirect to home if not"""
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.warning("🔒 Please login to access this page")
        st.info("👈 Go to Home page to login or register")
        st.stop()

def show_logout_button():
    """Show logout button in sidebar"""
    if st.session_state.get('authenticated', False):
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Logged in as:** {st.session_state.get('user_name', 'User')}")
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            from auth import logout
            logout()
            st.rerun()
