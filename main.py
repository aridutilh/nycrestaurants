import streamlit as st
import pandas as pd
from components.header import render_header, render_loading
from components.search import render_search
from components.maps import render_map_view
from components.restaurant_details import render_restaurant_details
from utils.data_loader import load_nyc_restaurant_data

# Page configuration
st.set_page_config(
    page_title="NYC Restaurant Safety Explorer",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Render header
render_header()

# Initialize session state
if 'search_query' not in st.session_state:
    st.session_state.search_query = ''

# Initialize session state for data
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'data' not in st.session_state:
    st.session_state.data = None

# Load data if not already loaded
if not st.session_state.data_loaded:
    try:
        render_loading()  # Show loading animation
        data = load_nyc_restaurant_data()
        if not data.empty:
            st.session_state.data = data
            st.session_state.data_loaded = True
        else:
            st.error("Unable to load restaurant data. Please try refreshing the page.")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.session_state.data_loaded = False

# Only show content if data is loaded
if st.session_state.data_loaded and st.session_state.data is not None:
    df = st.session_state.data

    # Clean Data Overview Section
    st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>🍽️ Restaurant Safety at a Glance</h2>", unsafe_allow_html=True)

    # Simplified metrics in two rows
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Active Restaurants",
            f"{len(df['camis'].unique()):,}",
            help="Total number of restaurants currently operating in NYC"
        )

        recent_inspections = len(df[df['inspection_date'] >= (pd.Timestamp.now() - pd.Timedelta(days=30))])
        st.metric(
            "Recent Inspections",
            f"{recent_inspections:,}",
            help="Inspections conducted in the last 30 days"
        )

    with col2:
        grade_a_percent = (len(df[df['grade'] == 'A']) / len(df) * 100)
        st.metric(
            "Grade A Restaurants",
            f"{grade_a_percent:.1f}%",
            help="Percentage of restaurants with Grade A rating"
        )

        avg_score = df['score'].mean()
        st.metric(
            "Average Safety Score",
            f"{avg_score:.1f}",
            help="Lower score indicates better safety standards"
        )

    # Interactive Map
    st.markdown("<h3 style='text-align: center; margin: 2rem 0;'>📍 Restaurant Locations</h3>", unsafe_allow_html=True)
    render_map_view(df)

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

    # Footer
    st.markdown(
        f"""
        <div style='text-align: center; padding: 20px; color: #6B7280; font-size: 0.9rem;'>
            <p>Data provided by NYC Open Data | Last updated: {pd.Timestamp.now().strftime("%B %d, %Y")}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Please wait while we load the data...")