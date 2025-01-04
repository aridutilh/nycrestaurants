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

                # Create columns for the grid layout
                cols = st.columns(2)
                for idx, row in results.iterrows():
                    col_idx = idx % 2
                    with cols[col_idx]:
                        with st.expander(f"🏪 {row['dba']} - {row['building']} {row['street']}"):
                            render_restaurant_details(row)
            else:
                st.warning("No restaurants found matching your search.")

    st.markdown("</div>", unsafe_allow_html=True)