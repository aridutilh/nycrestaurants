import streamlit as st
from utils.map_utils import create_heatmap
import plotly.express as px

def render_map_view(df):
    """Render the main map view with controls"""
    st.subheader("🗺️ Restaurant Safety Heatmap")
    
    # Year selector for time-lapse
    years = sorted(df['year'].unique())
    selected_year = st.select_slider(
        "Select Year",
        options=years,
        value=years[-1]
    )
    
    # Filter data for selected year
    year_data = df[df['year'] == selected_year]
    
    # Create and display heatmap
    fig = create_heatmap(year_data)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Inspections",
            len(year_data),
            f"{len(year_data) - len(df[df['year'] == selected_year-1])}"
        )
    
    with col2:
        avg_score = year_data['score'].mean()
        st.metric(
            "Average Score",
            f"{avg_score:.1f}",
            f"{avg_score - df[df['year'] == selected_year-1]['score'].mean():.1f}"
        )
    
    with col3:
        grade_a = len(year_data[year_data['grade'] == 'A'])
        st.metric(
            "Grade A Restaurants",
            grade_a,
            f"{grade_a - len(df[(df['year'] == selected_year-1) & (df['grade'] == 'A')])}"
        )
