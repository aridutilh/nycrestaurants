import streamlit as st
import pandas as pd
import plotly.express as px
from components.header import render_header
from utils.data_loader import load_nyc_restaurant_data, search_restaurants

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

    # Render header with integrated search
    render_header()

    # Handle search results if there's a query
    search_query = st.session_state.get('search_query', '').strip()
    if search_query:
        results = search_restaurants(df, search_query)
        if results is None or results.empty:
            st.warning("No restaurants found matching your search.")
        else:
            st.markdown(f"##### Found {len(results)} matching restaurants:")
            st.markdown("<div class='search-results'>", unsafe_allow_html=True)

            for idx, row in results.iterrows():
                expander_label = (
                    f"🏪 {row['dba']} - "
                    f"{row['grade'] if pd.notna(row['grade']) else 'Grade N/A'} "
                    f"(Score: {int(row['score']) if pd.notna(row['score']) else 'N/A'})"
                )

                with st.expander(expander_label, expanded=False):
                    st.markdown(f"""
                    <div class='restaurant-result'>
                        <p>📍 {row['building']} {row['street']}, {row['boro']}</p>
                        <p>📅 Inspected: {row['inspection_date'].strftime('%B %d, %Y')}</p>
                        {f"<p class='violation'>❗ {row['violation_description']}</p>" if pd.notna(row['violation_description']) else ""}
                        <div class='restaurant-details'>
                            <span>🍽️ {row['cuisine_description'] if pd.notna(row['cuisine_description']) else 'N/A'}</span>
                            {f"<span class='critical'>⚠️ {row['critical_flag']}</span>" if pd.notna(row['critical_flag']) else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # Add spacing between search results and main content
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

    # Grade Distribution Chart
    grade_dist = filtered_df[filtered_df['grade'].isin(['A', 'B', 'C'])]['grade'].value_counts()
    fig_grades = px.pie(
        values=grade_dist.values,
        names=grade_dist.index,
        title=f'Restaurant Grades Distribution in {selected_boro}',
        color_discrete_sequence=['#2ECC71', '#F1C40F', '#E74C3C']
    )

    # Update layout for transparent background
    fig_grades.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=20, l=20, r=20)
    )

    st.plotly_chart(fig_grades, use_container_width=True)

    # Pest Violations Section
    st.markdown("<h3 style='text-align: center; margin: 2rem 0;'>🪳 Top Icks Report</h3>", unsafe_allow_html=True)

    # Filter for pest-related violations in the past year
    one_year_ago = pd.Timestamp.now() - pd.Timedelta(days=365)
    pest_df = filtered_df[
        (filtered_df['inspection_date'] >= one_year_ago) &
        (filtered_df['violation_description'].notna())
    ]

    # Define pest-related keywords
    pest_keywords = {
        'rats/mice': ['rat', 'mouse', 'mice', 'rodent'],
        'cockroaches': ['roach', 'cockroach'],
        'flies': ['flies', 'flying insects'],
        'vermin': ['vermin', 'pest']
    }

    # Calculate statistics for each pest type
    pest_stats = {}
    for pest_type, keywords in pest_keywords.items():
        mask = pest_df['violation_description'].str.lower().str.contains('|'.join(keywords), na=False)
        pest_stats[pest_type] = len(pest_df[mask])

    # Create two columns for the stats
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🐀 Rats/Mice Reports",
            pest_stats['rats/mice'],
            help="Number of rat or mice related violations"
        )
        st.metric(
            "🪰 Fly Infestations",
            pest_stats['flies'],
            help="Number of fly-related violations"
        )

    with col2:
        st.metric(
            "🪳 Cockroach Reports",
            pest_stats['cockroaches'],
            help="Number of cockroach-related violations"
        )
        st.metric(
            "🐜 Other Vermin",
            pest_stats['vermin'],
            help="Number of other pest-related violations"
        )

    # Add explanation text
    st.markdown(
        """
        <div style='text-align: center; font-size: 0.9rem; color: #666; margin-top: 1rem;'>
            These statistics show reported violations involving pests during health inspections.
            Multiple violations may be reported for the same establishment.
        </div>
        """,
        unsafe_allow_html=True
    )

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
                </div>
                <div style="font-size: 0.8rem; color: #666;">
                    All data on this website is from <a href="https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/43nn-pn8j/data_preview" target="_blank" rel="noopener noreferrer">Open Data NYC</a> | Find this website's code <a href="https://github.com/aridutilh/nycrestaurants" target="_blank" rel="noopener noreferrer">here</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    st.warning("Please wait while we load the data...")