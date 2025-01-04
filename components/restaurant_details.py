import streamlit as st
import pandas as pd
from utils.map_utils import create_restaurant_map

def get_rating_class_and_message(score):
    """Get rating class and Garfield message based on score"""
    if score <= 13:
        return {
            'class': 'rating-excellent',
            'icon': '😺',
            'text': 'Excellent!',
            'message': "Mmm... This place is purrfect! I'd share my lasagna with them!"
        }
    elif score <= 27:
        return {
            'class': 'rating-good',
            'icon': '😸',
            'text': 'Good',
            'message': "Not bad! Almost as good as my Monday meals!"
        }
    elif score <= 40:
        return {
            'class': 'rating-fine',
            'icon': '😾',
            'text': 'Fine',
            'message': "It's acceptable... but I've had better naps!"
        }
    else:
        return {
            'class': 'rating-poor',
            'icon': '🙀',
            'text': 'Poor',
            'message': "Odie wouldn't even eat here... and that's saying something!"
        }

def render_restaurant_details(row):
    """Render detailed view for a single restaurant"""
    # Get rating information
    rating_info = get_rating_class_and_message(row['score'] if pd.notna(row['score']) else 100)

    # Create the rating component
    st.markdown(
        f"""
        <div class='rating-container {rating_info["class"]}'>
            <div class='rating-icon'>{rating_info["icon"]}</div>
            <div class='rating-text'>{rating_info["text"]}</div>
            <div class='rating-message'>{rating_info["message"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create restaurant info grid
    st.markdown(
        f"""
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
        """,
        unsafe_allow_html=True
    )

    # Create inspection info grid
    st.markdown(
        f"""
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
        """,
        unsafe_allow_html=True
    )

    # Add violation details if present
    if pd.notna(row['violation_code']):
        st.markdown(
            f"""
            <div class='violation-details'>
                <strong>Violation Details</strong>
                <p><strong>Code:</strong> {row['violation_code']}</p>
                <p><strong>Description:</strong> {row['violation_description']}</p>
                <p><strong>Action:</strong> {row['action']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Add map
    st.markdown("### 📍 Location")
    st.plotly_chart(create_restaurant_map(row), use_container_width=True)