import streamlit as st
import requests

# Function to display the sidebar
def sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Page 1", "Page 2"])
    return page

# Function to display the title menu
def title_menu():
    st.title("My Streamlit App")
    st.subheader("Always visible title menu")

# Function for the login page
def login_page():
    st.title("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid username or password")

# Function to authenticate the user with the API
def authenticate(username, password):
    url = "https://izife981fidwfw-8000.proxy.runpod.net/auth/jwt/create/"  # Replace with your login API URL
    payload = {"email": username, "password": password}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        if "access" in data and "refresh" in data:
            st.session_state["access_token"] = data["access"]
            st.session_state["refresh_token"] = data["refresh"]
            st.info('true')
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return False

# Function for the main content
def main_content(page):
    title_menu()
    if page == "Home":
        st.write("Welcome to the Home page!")
    elif page == "Page 1":
        st.write("This is Page 1")
    elif page == "Page 2":
        st.write("This is Page 2")

# Main function
def main():
    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        page = sidebar()
        main_content(page)

if __name__ == "__main__":
    main()
