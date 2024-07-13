import streamlit as st

def sidebar():
    if st.session_state.get("logged_in", False):
        with st.sidebar:
            st.title("Navigation")
            
            st.markdown("### Menu")
            if st.button("Home"):
                st.query_params.page = "home"
            if st.button("Page 1"):
                st.query_params.page = "page-1"
            if st.button("Page 2"):
                st.query_params.page = "page-2"
            
            if st.button("Logout"):
                st.session_state["logged_in"] = False
                st.experimental_rerun()

    return None  # We're not returning a page selection anymore