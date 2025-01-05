import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants
from components.header import render_loading
from components.restaurant_details import render_restaurant_details

def render_search(df):
    """Render the restaurant search component"""
    # Get search query from main search input
    search_query = st.session_state.get('search_query', '')

    if not search_query:
        # Show recently inspected restaurants
        st.markdown("#### 🕒 Recently Inspected Restaurants")
        recent_restaurants = df.sort_values('inspection_date', ascending=False).drop_duplicates('camis').head(10)

        for _, row in recent_restaurants.iterrows():
            inspection_date = row['inspection_date'].strftime('%B %d, %Y') if pd.notna(row['inspection_date']) else 'N/A'
            with st.expander(
                f"🏪 {row['dba']} - Inspected {inspection_date}", 
                expanded=False
            ):
                render_restaurant_details(row)

    if search_query:
        st.session_state.is_loading = True
        if st.session_state.is_loading:
            render_loading()
        try:
            results = search_restaurants(df, search_query)

            if len(results) > 0:
                st.write(f"Found {len(results)} results:")

                for idx, row in results.iterrows():
                    with st.expander(f"🏪 {row['dba']} - {row['building']} {row['street']}", expanded=False):
                        render_restaurant_details(row)
            else:
                st.warning("No restaurants found matching your search.")
        finally:
            st.session_state.is_loading = False