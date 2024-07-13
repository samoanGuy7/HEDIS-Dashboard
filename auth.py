import streamlit as st
import requests

def login_page():
    if st.session_state.get("logged_in", False):
        return

    st.title("Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        if authenticate(email, password):
            st.session_state["logged_in"] = True
            st.success("Login successful! Redirecting...")
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")

def authenticate(email, password):
    url = "https://izife981fidwfw-8000.proxy.runpod.net/auth/jwt/create/"
    payload = {"email": email, "password": password}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if "access" in data and "refresh" in data:
            st.session_state["access_token"] = data["access"]
            st.session_state["refresh_token"] = data["refresh"]
            return True
        return False
    
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred during authentication: {e}")
        return False