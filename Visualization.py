# visualization.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_style import hide_streamlit_style

def app():
    hide_streamlit_style()
    st.title("Exploratory Data Analysis (EDA) Visualizations")

    # Check if data is available in session state
    if 'cleaned_data' not in st.session_state:
        st.error("No data available. Please go to the Data Cleaning Page and upload your file.")
        st.stop()

    # Retrieve the cleaned data from session state
    df = st.session_state['cleaned_data']

    # Add a "Reset Data" button to reset the data
    if st.button("Reset Data"):
        del st.session_state['cleaned_data']  # Remove the data from session state
        st.success("Data has been reset! Please go back to the Data Cleaning Page to upload a new file.")
        st.stop()

    # Data Preview
    with st.expander("Data Preview"):
        st.dataframe(df)

    st.markdown("## Basic Visualizations")

    #######################################
    # VISUALIZATION METHODS
    #######################################

    def plot_histogram(df, column):
        fig = px.histogram(df, x=column, title=f"Distribution of {column}", marginal="box", nbins=30)
        st.plotly_chart(fig, use_container_width=True)

    def plot_scatter(df, x_col, y_col, color_col=None):
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{x_col} vs {y_col}", opacity=0.7)
        st.plotly_chart(fig, use_container_width=True)

    def plot_correlation_heatmap(df):
        # Select only the numeric columns
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        corr =numeric_df.corr()
        fig = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
        st.plotly_chart(fig, use_container_width=True)

    #######################################
    # MAIN EDA LAYOUT
    #######################################

    # Column Selections
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    # Distribution Plot
    st.subheader("1. Distribution Plot")
    column = st.selectbox("Select a numeric column for distribution:", numeric_columns)
    if column:
        plot_histogram(df, column)

    # Scatter Plot for Numeric Variables
    st.subheader("2. Scatter Plot")
    col1 = st.selectbox("Select X-axis column:", numeric_columns)
    col2 = st.selectbox("Select Y-axis column:", numeric_columns)
    color_col = st.selectbox("Select column for color grouping (optional):", [None] + list(categorical_columns))
    if col1 and col2:
        plot_scatter(df, col1, col2, color_col)

    # Correlation Heatmap
    st.subheader("3. Correlation Heatmap")
    plot_correlation_heatmap(df)

    #######################################
    # ADVANCED VISUALIZATIONS (Optional)
    #######################################

    st.markdown("## Advanced Visualizations")

    # Interactive Bar Chart
    st.subheader("4. Interactive Bar Chart")
    bar_column = st.selectbox("Select a categorical column for bar chart:", categorical_columns)
    numeric_column = st.selectbox("Select a numeric column for aggregation:", numeric_columns)
    if bar_column and numeric_column:
        fig = px.bar(df, x=bar_column, y=numeric_column, color=bar_column, title=f"Aggregated {numeric_column} by {bar_column}")
        st.plotly_chart(fig, use_container_width=True)

    # Time Series Plot (if applicable)
    if 'Date' in df.columns:
        st.subheader("5. Time Series Plot")
        date_column = 'Date'
        value_column = st.selectbox("Select a value column for time series:", numeric_columns)
        fig = px.line(df, x=date_column, y=value_column, title=f"{value_column} Over Time")
        st.plotly_chart(fig, use_container_width=True)

    # Gauge and Indicator Example (Metrics Overview)
    st.subheader("6. Metrics Overview")
    metrics_col1, metrics_col2 = st.columns(2)

    with metrics_col1:
        fig = go.Figure(go.Indicator(
            mode="number+gauge+delta", value=df[numeric_columns[0]].mean(),
            title={'text': f"Average of {numeric_columns[0]}"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        st.plotly_chart(fig, use_container_width=True)

    with metrics_col2:
        fig = go.Figure(go.Indicator(
            mode="number+gauge+delta", value=df[numeric_columns[1]].mean(),
            title={'text': f"Average of {numeric_columns[1]}"},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    app()
