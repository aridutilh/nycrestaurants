import streamlit as st
from utils.map_utils import create_restaurant_map

def render_restaurant_details(row):
    """Render detailed view for a single restaurant"""
    st.markdown(
        f"""
        <div class='restaurant-card'>
            <h2>{row['dba']}</h2>
            <hr>
            <p><strong>Address:</strong> {row['building']} {row['street']}, {row['boro']}</p>
            <p><strong>Cuisine:</strong> {row['cuisine_description']}</p>
            <p><strong>Latest Grade:</strong> {row['grade'] if pd.notna(row['grade']) else 'N/A'}</p>
            <p><strong>Score:</strong> {int(row['score']) if pd.notna(row['score']) else 'N/A'}</p>
            <p><strong>Last Inspection:</strong> {row['inspection_date'].strftime('%B %d, %Y')}</p>
            <p><strong>Violation Description:</strong> {row['violation_description'] if pd.notna(row['violation_description']) else 'No violations found'}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display restaurant location on map
    st.subheader("📍 Location")
    fig = create_restaurant_map(row)
    st.plotly_chart(fig, use_container_width=True)
