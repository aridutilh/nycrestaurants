import streamlit as st
import pandas as pd
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
            <p><strong>Last Inspection:</strong> {row['inspection_date'].strftime('%B %d, %Y') if pd.notna(row['inspection_date']) else 'N/A'}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Violations and Notes Section
    if pd.notna(row['violation_code']) or pd.notna(row['violation_description']):
        st.markdown("### 📋 Violation Details")
        st.markdown(
            f"""
            <div class='violation-details'>
                <p><strong>Violation Code:</strong> {row['violation_code'] if pd.notna(row['violation_code']) else 'N/A'}</p>
                <p><strong>Description:</strong> {row['violation_description'] if pd.notna(row['violation_description']) else 'No description available'}</p>
                <p><strong>Critical Flag:</strong> {row['critical_flag'] if pd.notna(row['critical_flag']) else 'N/A'}</p>
                <p><strong>Action:</strong> {row['action'] if pd.notna(row['action']) else 'N/A'}</p>
                <p><strong>Inspection Type:</strong> {row['inspection_type'] if pd.notna(row['inspection_type']) else 'N/A'}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Display restaurant location on map
    st.subheader("📍 Location")
    fig = create_restaurant_map(row)
    st.plotly_chart(fig, use_container_width=True)