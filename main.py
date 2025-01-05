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

# Disable session state metrics
if 'metrics' not in st.session_state:
    st.session_state['metrics'] = False

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

    # Search Section (moved directly under header)
    search_query = st.text_input(
        "",  # Remove label
        placeholder="Enter restaurant name or address...",
        help="Find restaurants and view their latest inspection results"
    )

    # Data Visualization Section
    st.markdown("## 📊 Restaurant Safety Overview")

    # Key Statistics Dashboard
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_restaurants = len(df['camis'].unique())
        st.metric("Total Restaurants", f"{total_restaurants:,}", 
                 help="Number of unique restaurants in NYC")

    with col2:
        grade_a_percent = (len(df[df['grade'] == 'A']) / len(df) * 100)
        st.metric("Grade A Restaurants", f"{grade_a_percent:.1f}%",
                 help="Percentage of restaurants with Grade A")

    with col3:
        avg_score = df['score'].mean()
        st.metric("Average Safety Score", f"{avg_score:.1f}",
                 help="Lower score is better")

    with col4:
        recent_inspections = len(df[df['inspection_date'] >= (pd.Timestamp.now() - pd.Timedelta(days=30))])
        st.metric("Recent Inspections", f"{recent_inspections:,}",
                 help="Inspections in the last 30 days")

    # Map View
    render_map_view(st.session_state.data)

    # About Section
    st.markdown(
        """
        ## About NYC Restaurant Safety

        Our platform helps you make informed dining decisions by providing transparent 
        access to NYC's restaurant inspection data. Here's what you need to know:

        ### 🎯 Safety Grades Explained
        - **Grade A (0-13 points)**: Excellent food safety practices
        - **Grade B (14-27 points)**: Good, with some areas for improvement
        - **Grade C (28+ points)**: Significant violations present

        ### 🔍 What We Check
        - Food temperature control
        - Kitchen cleanliness
        - Employee hygiene
        - Pest control
        - Food handling procedures

        ### 📊 Recent Trends
        """
    )

    # Add recent trends visualization
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Most Common Violations")
        violations = df.groupby('violation_description')['camis'].count().nlargest(5)
        st.bar_chart(violations)

    with col2:
        st.markdown("#### Inspection Results by Borough")
        borough_stats = df.groupby('boro')['grade'].value_counts().unstack()
        st.bar_chart(borough_stats)

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