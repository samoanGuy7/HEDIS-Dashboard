import streamlit as st
from auth import login_page, authenticate
from components.sidebar import sidebar

# Import page functions directly
from pages.home import show as home_show
from pages.page1 import show as page1_show
from pages.page2 import show as page2_show

def inject_custom_css():
    css = """
    <style>
        /* Your custom CSS goes here */
        .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #f0f0f0;
        }
        /* CSS to hide sidebar when not logged in */
        .stApp.not-logged-in > div:nth-child(1) > div > div > div > div > section:nth-child(1) {
            display: none;
        }
        .stApp.not-logged-in > div:nth-child(1) > div > div > div > div > section.main {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1gv3huu.eczjsme18 > div.st-emotion-cache-6qob1r.eczjsme11 > div.st-emotion-cache-79elbk.eczjsme17 {
            display:none;
        }
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1gv3huu.eczjsme18 > div.st-emotion-cache-6qob1r.eczjsme11 > div.st-emotion-cache-1mi2ry5.eczjsme9 {
            display: none;
            }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_page()
    else:
        sidebar()  # Call sidebar but don't expect a return value
        
        # Get the current URL path using st.query_params
        query_params = st.query_params
        path = query_params.get("page", "home").lower()
        
        if path == "home":
            home_show()
        elif path == "page-1":
            page1_show()
        elif path == "page-2":
            page2_show()
        else:
            st.error("Page not found")

if __name__ == "__main__":
    main()