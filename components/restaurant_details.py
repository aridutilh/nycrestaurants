import streamlit as st
import pandas as pd
from utils.map_utils import create_restaurant_map

def render_restaurant_details(row):
    """Render detailed view for a single restaurant"""
    violation_details = ""
    if pd.notna(row['violation_code']):
        violation_details = f"""
            <div class='violation-details'>
                <strong>Violation Details</strong>
                <p><strong>Code:</strong> {row['violation_code']}</p>
                <p><strong>Description:</strong> {row['violation_description']}</p>
                <p><strong>Action:</strong> {row['action']}</p>
            </div>
        """

    st.markdown(
        f"""
        <div class='restaurant-card'>
            <h2>{row['dba']}</h2>
            <div class="restaurant-info-grid">
                <div class="restaurant-info-item">
                    <strong>Address</strong>
                    {row['building']} {row['street']}, {row['boro']}
                </div>
                <div class="restaurant-info-item">
                    <strong>Cuisine</strong>
                    {row['cuisine_description']}
                </div>
                <div class="restaurant-info-item">
                    <strong>Grade</strong>
                    {row['grade'] if pd.notna(row['grade']) else 'N/A'}
                </div>
                <div class="restaurant-info-item">
                    <strong>Score</strong>
                    {int(row['score']) if pd.notna(row['score']) else 'N/A'}
                </div>
            </div>

            <div class="restaurant-info-grid">
                <div class="restaurant-info-item">
                    <strong>Last Inspection</strong>
                    {row['inspection_date'].strftime('%B %d, %Y') if pd.notna(row['inspection_date']) else 'N/A'}
                </div>
                <div class="restaurant-info-item">
                    <strong>Critical Flag</strong>
                    {row['critical_flag'] if pd.notna(row['critical_flag']) else 'N/A'}
                </div>
            </div>

            {violation_details}

            <div style="margin-top: 20px;">
                <h3>📍 Location</h3>
                {create_restaurant_map(row).to_html()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )