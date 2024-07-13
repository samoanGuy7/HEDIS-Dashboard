import streamlit as st
from pages.payer_demo import payer_demo
from pages.provider_demo import provider_demo
import plotly.express as px
import pandas as pd

# Function to display the home page
def home_page():
    st.title("Welcome to the HEDIS RAG-Based Pipeline Demo")
    
    st.markdown("""
        This demo showcases how health plans and providers can use our HEDIS RAG-based pipeline to identify and address care gaps in real-time.
        Use the navigation on the left to explore the Payer Demo and Provider Demo sections.
    """)
    
    st.markdown("### Features:")
    st.markdown("""
        - **Real-time member information**: Access up-to-date information about members.
        - **Identification of care gaps**: Easily identify gaps in care that need attention.
        - **Historical data analysis**: Analyze historical data to track progress and trends.
        - **Interactive charts and tables**: Use interactive visualizations for better insights.
    """)
    
    st.markdown("### HEDIS Overview")
    st.markdown("""
        The Healthcare Effectiveness Data and Information Set (HEDIS) is a widely used set of performance measures in the healthcare industry. It is designed to allow consumers to compare the performance of health plans easily. HEDIS includes measures for many different domains of care, including:
        - Effectiveness of Care
        - Access/Availability of Care
        - Experience of Care
        - Utilization and Risk Adjusted Utilization
        - Health Plan Descriptive Information
        - Measures Collected Using Electronic Clinical Data Systems
    """)

    # Example chart: HEDIS Measure Compliance Rates
    st.markdown("### Example Chart: HEDIS Measure Compliance Rates")
    example_data = {
        "Measure": ["AWV", "CBP", "CDC"],
        "Compliance Rate": [82, 75, 88]
    }
    df = pd.DataFrame(example_data)
    fig = px.bar(df, x="Measure", y="Compliance Rate", title="HEDIS Measure Compliance Rates", color="Measure")
    st.plotly_chart(fig)

    # Example facts about HEDIS
    st.markdown("### Did You Know?")
    st.markdown("""
        - **Over 190 million people** are enrolled in plans that report HEDIS results.
        - HEDIS consists of **90 measures** across 6 domains of care.
        - HEDIS results are used by more than **90% of America's health plans** to measure performance on important dimensions of care and service.
    """)

# Function to display the title and menu
def title_menu():
    st.title("HEDIS RAG-Based Pipeline")
    st.subheader("Care Gap Identification")

# Main content function to manage the page transitions
def main_content():
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    title_menu()

    # Custom navigation menu in sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Payer Demo", "Provider Demo"],
        index=["Home", "Payer Demo", "Provider Demo"].index(st.session_state.page),
        key="navigation_radio"
    )

    # Update the session state with the selected page
    st.session_state.page = page

    # Page content based on the selected page
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Payer Demo":
        payer_demo()
    elif st.session_state.page == "Provider Demo":
        provider_demo()

# Main function to run the app
def main():
    # Hide the default Streamlit navigation
    st.set_page_config(
        page_title="HEDIS RAG-Based Pipeline",
        page_icon=":hospital:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main_content()

if __name__ == "__main__":
    main()
##