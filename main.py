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
        st.markdown(
            """
            ## About This App

            Welcome to the NYC Restaurant Safety Explorer! This application visualizes health inspection 
            data from restaurants across New York City, helping you make informed dining decisions.

            ### Data Source
            Data is sourced from the [NYC Open Data API](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j) 
            and is updated regularly.

            ### How to Use
            - Use the Map View to explore restaurant safety scores across NYC
            - Search for specific restaurants by name or address
            - View detailed inspection history and violation information
            - Use the time-lapse feature to see changes over years

            ### Understanding Scores
            - Lower scores are better
            - Grade A: 0-13 points
            - Grade B: 14-27 points
            - Grade C: 28+ points

            Created with ❤️ for NYC's food scene
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