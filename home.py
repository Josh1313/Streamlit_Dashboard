import streamlit as st
from streamlit_style import hide_streamlit_style

def app():
    hide_streamlit_style()
    st.title("Welcome to the Data Cleaning & Visualization App")
    st.markdown("""
        This app allows you to:
        - **Clean your data**: Inspect, transform, and handle issues in your dataset.
        - **Visualize your data**: Create interactive visualizations to explore your cleaned data.
        
        Use the sidebar to navigate between pages.
    """)
    st.image("https://venngage-wordpress.s3.amazonaws.com/uploads/2020/06/What-is-Data-Visualization-Blog-Header.jpg", caption="Data Analysis Made Easy", use_column_width=True)
    st.write("Select a page from the sidebar to get started!")