import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants
from components.header import render_loading
from components.restaurant_details import render_restaurant_details

def render_search(df):
    """Render the restaurant search component"""
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)

    search_query = st.text_input(
        "Search restaurants by name or address",
        placeholder="Enter restaurant name or address..."
    )

    if search_query:
        with st.spinner("🍕 Searching restaurants..."):
            results = search_restaurants(df, search_query)

            if len(results) > 0:
                st.write(f"Found {len(results)} results:")

                # Create a container for search results
                st.markdown("""
                    <style>
                    .search-results {
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
                        gap: 20px;
                        padding: 10px;
                    }
                    </style>
                    <div class='search-results'>
                """, unsafe_allow_html=True)

                # Calculate optimal number of columns based on screen width
                
                for idx, row in results.iterrows():
                    with st.expander(f"🏪 {row['dba']} - {row['building']} {row['street']}", expanded=False):
                        render_restaurant_details(row)

                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No restaurants found matching your search.")

    st.markdown("</div>", unsafe_allow_html=True)