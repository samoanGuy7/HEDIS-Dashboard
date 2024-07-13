import streamlit as st
import pandas as pd
import numpy as np

def show():
    st.title("Page 1: Data Visualization")
    
    st.write("This page demonstrates some basic data visualization capabilities.")

    # Generate some random data
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C'])

    # Line chart
    st.subheader("Line Chart")
    st.line_chart(chart_data)

    # Bar chart
    st.subheader("Bar Chart")
    st.bar_chart(chart_data)

    # Area chart
    st.subheader("Area Chart")
    st.area_chart(chart_data)

    # Allow user to display the raw data
    if st.checkbox("Show raw data"):
        st.subheader("Raw data")
        st.write(chart_data)