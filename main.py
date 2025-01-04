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
    initial_sidebar_state="collapsed"
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Render header
render_header()

# Initialize session state for data
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'data' not in st.session_state:
    st.session_state.data = None

# Load data if not already loaded
if not st.session_state.data_loaded:
    try:
        render_loading()
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
    # Main navigation
    tabs = st.tabs(["🗺️ Map View", "🔍 Search", "ℹ️ About"])

    with tabs[0]:
        render_map_view(st.session_state.data)

    with tabs[1]:
        render_search(st.session_state.data)

    with tabs[2]:
        # Calculate interesting statistics
        df = st.session_state.data
        total_inspections = len(df)
        grade_a_count = len(df[df['grade'] == 'A'])
        grade_a_percentage = (grade_a_count / total_inspections) * 100
        avg_score = df['score'].mean()
        worst_score = df['score'].max()
        best_neighborhood = df.groupby('boro')['score'].mean().idxmin()

        st.markdown(
            f"""
            ## About NYC Restaurant Safety

            When analyzing restaurant safety across New York City neighborhoods, we've discovered some 
            fascinating patterns in our data. For instance, {best_neighborhood} leads with the best 
            average safety scores, showing a strong commitment to food safety standards.

            ### By the Numbers
            - **{total_inspections:,}** total inspections conducted
            - **{grade_a_percentage:.1f}%** of restaurants maintain an A grade
            - Average safety score: **{avg_score:.1f}** (lower is better)
            - {worst_score:.0f} points was the highest (worst) score recorded

            ### Understanding Scores
            Restaurant scores are calculated based on violation points:
            - **Grade A**: 0-13 points (Excellent)
            - **Grade B**: 14-27 points (Good)
            - **Grade C**: 28+ points (Poor)

            ### Timing Matters
            - Inspections happen throughout the year
            - Scores can vary by season and inspection type
            - Regular inspections help maintain high safety standards

            ### Data Insights
            - Violations are weighted based on health risk
            - Critical violations carry more points
            - Repeat violations face stricter penalties

            ### About This Tool
            This application visualizes health inspection data from NYC's Department of Health, 
            helping you make informed dining decisions. Data is sourced from the 
            [NYC Open Data API](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j) 
            and updated regularly.

            Created with ❤️ for NYC's diverse food scene
            """
        )

    # Footer
    st.markdown(
        """
        <div style='text-align: center; padding: 20px;'>
            <p>Data provided by NYC Open Data | Last updated: {}</p>
        </div>
        """.format(pd.Timestamp.now().strftime("%B %d, %Y")),
        unsafe_allow_html=True
    )
else:
    st.warning("Please wait while we load the data...")