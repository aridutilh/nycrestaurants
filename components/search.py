import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants
from components.restaurant_details import render_restaurant_details

def render_search(df):
    """Render the restaurant search component"""
    try:
        # Initialize search state if not present
        if 'search_query' not in st.session_state:
            st.session_state.search_query = ''

        # Get current search query
        search_query = st.session_state.search_query.strip()

        if not search_query:
            # Show recently inspected restaurants
            st.markdown("#### 🕒 Recently Inspected Restaurants")
            try:
                recent_restaurants = (df.sort_values('inspection_date', ascending=False)
                                   .drop_duplicates('camis')
                                   .head(10))

                for _, row in recent_restaurants.iterrows():
                    inspection_date = (row['inspection_date'].strftime('%B %d, %Y') 
                                    if pd.notna(row['inspection_date']) else 'N/A')
                    with st.expander(
                        f"🏪 {row['dba']} - Inspected {inspection_date}", 
                        expanded=False
                    ):
                        render_restaurant_details(row)
            except Exception as e:
                st.error(f"Error loading recent restaurants: {str(e)}")
                return

        if search_query:
            # Set loading state
            if 'is_loading' not in st.session_state:
                st.session_state.is_loading = False

            st.session_state.is_loading = True
            try:
                # Perform search with error handling
                results = search_restaurants(df, search_query)

                if results is None or len(results) == 0:
                    st.warning("No restaurants found matching your search.")
                    return

                st.write(f"Found {len(results)} results:")

                for idx, row in results.iterrows():
                    try:
                        with st.expander(f"🏪 {row['dba']} - {row['building']} {row['street']}", expanded=False):
                            render_restaurant_details(row)
                    except Exception as e:
                        st.error(f"Error displaying restaurant {row.get('dba', 'Unknown')}: {str(e)}")
                        continue

            except Exception as e:
                st.error(f"Error performing search: {str(e)}")
            finally:
                st.session_state.is_loading = False

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")