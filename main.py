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

    # Footer with personal branding
    st.markdown("""
        <div class="footer">
            <div class="footer-content">
                <div class="footer-links">
                    <span>© 2025 Small Spoon Software by <a href="https://aridutilh.com" target="_blank" rel="noopener noreferrer">Ari</a></span>
                    <a href="https://github.com/aridutilh/nycrestaurants" target="_blank" rel="noopener noreferrer" class="github-link">
                        <svg height="24" width="24" viewBox="0 0 16 16" version="1.1">
                            <path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Please wait while we load the data...")