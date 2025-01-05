import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants
from components.header import render_loading
from components.restaurant_details import render_restaurant_details

def render_search(df):
    """Render the restaurant search component"""
    # Popular neighborhood suggestions
    popular_neighborhoods = [
        "Manhattan", "Brooklyn", "Queens",
        "Staten Island", "Bronx"
    ]

    popular_cuisines = [
        "Italian", "Chinese", "Japanese",
        "Mexican", "American"
    ]

    st.markdown("""
        <style>
        .suggestion-tag {
            display: inline-block;
            padding: 6px 12px;
            margin: 4px;
            background: rgba(250, 145, 29, 0.1);
            border: 1px solid rgba(250, 145, 29, 0.2);
            border-radius: 20px;
            color: #1A1A1A;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .suggestion-tag:hover {
            background: rgba(250, 145, 29, 0.2);
            transform: translateY(-2px);
        }
        .suggestions-container {
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Search input
    search_query = st.text_input(
        "Search restaurants by name or address",
        placeholder="Enter restaurant name or address..."
    )

    if not search_query:
        st.markdown("<div class='suggestions-container'>", unsafe_allow_html=True)
        st.markdown("#### 🏙️ Popular Neighborhoods")

        # Display neighborhood suggestions
        suggestions_html = "".join([
            f"<span class='suggestion-tag'>{neighborhood}</span>"
            for neighborhood in popular_neighborhoods
        ])
        st.markdown(f"<div>{suggestions_html}</div>", unsafe_allow_html=True)

        st.markdown("#### 🍽️ Popular Cuisines")
        # Display cuisine suggestions
        suggestions_html = "".join([
            f"<span class='suggestion-tag'>{cuisine}</span>"
            for cuisine in popular_cuisines
        ])
        st.markdown(f"<div>{suggestions_html}</div>", unsafe_allow_html=True)

        # Show top-rated restaurants
        st.markdown("#### ⭐ Top Rated Restaurants")
        top_restaurants = df[df['grade'] == 'A'].nlargest(5, 'score')
        for _, row in top_restaurants.iterrows():
            with st.expander(f"🏪 {row['dba']} - {row['building']} {row['street']}", expanded=False):
                render_restaurant_details(row)

        st.markdown("</div>", unsafe_allow_html=True)

    if search_query:
        with st.spinner("🍕 Searching restaurants..."):
            results = search_restaurants(df, search_query)

            if len(results) > 0:
                st.write(f"Found {len(results)} results:")

                for idx, row in results.iterrows():
                    with st.expander(f"🏪 {row['dba']} - {row['building']} {row['street']}", expanded=False):
                        render_restaurant_details(row)
            else:
                st.warning("No restaurants found matching your search.")