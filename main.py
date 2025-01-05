import streamlit as st
import pandas as pd
import plotly.express as px
from components.search import render_search_section
from utils.data_loader import load_nyc_restaurant_data

# Page configuration
st.set_page_config(
    page_title="NYC Restaurant Safety Explorer",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state for data loading
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'data' not in st.session_state:
    st.session_state.data = None

# Load data if not already loaded
if not st.session_state.data_loaded:
    try:
        data = load_nyc_restaurant_data()
        if not data.empty:
            st.session_state.data = data
            st.session_state.data_loaded = True
        else:
            st.error("Unable to load restaurant data. Please try refreshing the page.")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

# Render content if data is loaded
if st.session_state.data_loaded and st.session_state.data is not None:
    df = st.session_state.data

    # Render search section at the top
    render_search_section(df)

    # Add spacing between search and main content
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    # Restaurant Safety at a Glance Section
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>🍽️ Restaurant Safety at a Glance</h2>", unsafe_allow_html=True)

    # Metrics in two rows
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Active Restaurants",
            f"{len(df['camis'].unique()):,}",
            help="Total number of restaurants currently operating in NYC"
        )
        grade_a_percent = (len(df[df['grade'] == 'A']) / len(df) * 100)
        st.metric(
            "Grade A Restaurants",
            f"{grade_a_percent:.1f}%",
            help="Percentage of restaurants with Grade A rating"
        )

    with col2:
        recent_inspections = len(df[df['inspection_date'] >= (pd.Timestamp.now() - pd.Timedelta(days=30))])
        st.metric(
            "Recent Inspections",
            f"{recent_inspections:,}",
            help="Inspections conducted in the last 30 days"
        )
        avg_score = df['score'].mean()
        st.metric(
            "Average Safety Score",
            f"{avg_score:.1f}",
            help="Lower score indicates better safety standards"
        )

    # Neighborhood Toggle Section
    st.markdown("<h3 style='text-align: center; margin: 2rem 0;'>🏘️ Neighborhood View</h3>", unsafe_allow_html=True)

    # Add "All NYC" as the first option
    borough_options = ["All NYC"] + sorted(df['boro'].unique().tolist())
    selected_boro = st.selectbox(
        label="Select a neighborhood to explore",
        options=borough_options,
        key="neighborhood_selector",
        label_visibility="collapsed"
    )

    # Filter data based on selection
    filtered_df = df if selected_boro == "All NYC" else df[df['boro'] == selected_boro]

    # Grade Distribution Section
    st.markdown("<h3 style='text-align: center; margin: 2rem 0;'>Grade Distribution</h3>", unsafe_allow_html=True)
    grade_dist = filtered_df[filtered_df['grade'].isin(['A', 'B', 'C'])]['grade'].value_counts()
    fig_grades = px.pie(
        values=grade_dist.values,
        names=grade_dist.index,
        title=f'Restaurant Grades Distribution in {selected_boro}',
        color_discrete_sequence=['#2ECC71', '#F1C40F', '#E74C3C']
    )

    # Update layout for clean background
    fig_grades.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=40, b=20, l=20, r=20)
    )

    st.plotly_chart(fig_grades, use_container_width=True)

    # Simple Safety Guide
    st.markdown("""
        <div style='text-align: center; margin: 3rem 0; padding: 2rem; background-color: #f8f9fa; border-radius: 8px;'>
            <h3>🎯 Understanding Safety Grades</h3>
            <p style='margin: 1rem 0;'>
                <strong>A (0-13 points)</strong> - Excellent food safety standards<br>
                <strong>B (14-27 points)</strong> - Good, with some areas for improvement<br>
                <strong>C (28+ points)</strong> - Significant violations present
            </p>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Please wait while we load the data...")