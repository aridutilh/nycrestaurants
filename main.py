import streamlit as st
import pandas as pd
import plotly.express as px
from components.header import render_header
from components.search import render_search
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

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'data' not in st.session_state:
    st.session_state.data = None

if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

# Load data if not already loaded
if not st.session_state.data_loaded:
    try:
        st.session_state.is_loading = True
        data = load_nyc_restaurant_data()
        if not data.empty:
            st.session_state.data = data
            st.session_state.data_loaded = True
        else:
            st.error("Unable to load restaurant data. Please try refreshing the page.")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.session_state.data_loaded = False
    finally:
        st.session_state.is_loading = False

# Only show content if data is loaded
if st.session_state.data_loaded and st.session_state.data is not None:
    df = st.session_state.data

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
    st.markdown('<div class="neighborhood-toggle">', unsafe_allow_html=True)
    selected_boro = st.selectbox(
        "Select a neighborhood to explore",
        sorted(df['boro'].unique()),
        key="neighborhood_selector",
        help="Choose a borough to see detailed statistics"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    filtered_df = df[df['boro'] == selected_boro]

    # Grade Distribution Section
    st.markdown("<h3 style='text-align: center; margin: 2rem 0;'>📊 Grade Distribution</h3>", unsafe_allow_html=True)
    grade_dist = filtered_df[filtered_df['grade'].isin(['A', 'B', 'C'])]['grade'].value_counts()
    fig_grades = px.pie(
        values=grade_dist.values,
        names=grade_dist.index,
        title=f'Restaurant Grades Distribution in {selected_boro}',
        color_discrete_sequence=['#2ECC71', '#F1C40F', '#E74C3C']
    )
    st.plotly_chart(fig_grades, use_container_width=True)

    # Most Common Issues Section
    st.markdown("<h3 style='text-align: center; margin: 2rem 0;'>⚠️ Most Common Issues</h3>", unsafe_allow_html=True)

    # Group and count violation descriptions for the selected borough
    violation_counts = filtered_df['violation_description'].value_counts().head(5)
    fig_violations = px.bar(
        x=violation_counts.values,
        y=violation_counts.index,
        orientation='h',
        title=f'Top 5 Most Common Violations in {selected_boro}',
        labels={'x': 'Number of Incidents', 'y': ''},
        color_discrete_sequence=['#FFA07A']  # Light salmon color
    )

    # Update layout for better readability
    fig_violations.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        title_x=0.5,
        title_font_size=16,
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            gridcolor='#E5E5E5',
            title_font_size=14,
            tickfont_size=12
        ),
        yaxis=dict(
            categoryorder='total ascending',
            tickfont_size=12,
            tickfont_color='#333333'
        )
    )

    # Add gridlines only for x-axis
    fig_violations.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    fig_violations.update_yaxes(showgrid=False)

    st.plotly_chart(fig_violations, use_container_width=True)

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