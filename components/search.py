import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants
from components.restaurant_details import render_restaurant_details
from utils.map_utils import create_restaurant_map

def render_search(df):
    """Render the restaurant search component"""
    try:
        # Initialize search state if not present
        if 'search_query' not in st.session_state:
            st.session_state.search_query = ''
            st.session_state.search_triggered = False

        # Get current search query
        search_query = st.session_state.search_query.strip()

        # Only perform search if triggered by input change
        if search_query and st.session_state.get('search_triggered', False):
            st.session_state.is_loading = True
            try:
                # Perform search with error handling
                results = search_restaurants(df, search_query)

                if results is None or len(results) == 0:
                    st.warning("No restaurants found matching your search.")
                    return

                st.write(f"Found {len(results)} matching restaurants:")

                # Display results in a clean layout
                for idx, row in results.iterrows():
                    try:
                        with st.expander(f"🏪 {row['dba']} - {row['building']} {row['street']}", expanded=True):
                            # Create two columns for layout
                            col1, col2 = st.columns([3, 2])

                            with col1:
                                # Basic restaurant info
                                st.markdown(f"**Address:** {row['building']} {row['street']}, {row['boro']}")
                                st.markdown(f"**Latest Inspection:** {row['inspection_date'].strftime('%B %d, %Y')}")
                                st.markdown(f"**Score:** {int(row['score']) if pd.notna(row['score']) else 'N/A'}")
                                if pd.notna(row['grade']):
                                    st.markdown(f"**Grade:** {row['grade']}")
                                if pd.notna(row['violation_description']):
                                    st.markdown("**Latest Violation:**")
                                    st.markdown(f"_{row['violation_description']}_")

                            with col2:
                                # Display location map
                                st.plotly_chart(create_restaurant_map(row), use_container_width=True)

                    except Exception as e:
                        st.error(f"Error displaying restaurant {row.get('dba', 'Unknown')}: {str(e)}")
                        continue

            except Exception as e:
                st.error(f"Error performing search: {str(e)}")
            finally:
                st.session_state.is_loading = False
                st.session_state.search_triggered = False

        elif not search_query:
            # Show recently inspected restaurants
            st.markdown("#### 🕒 Recently Inspected Restaurants")
            try:
                recent_restaurants = (df.sort_values('inspection_date', ascending=False)
                                   .drop_duplicates('camis')
                                   .head(10))

                for _, row in recent_restaurants.iterrows():
                    inspection_date = (row['inspection_date'].strftime('%B %d, %Y') 
                                    if pd.notna(row['inspection_date']) else 'N/A')
                    with st.expander(f"🏪 {row['dba']} - Inspected {inspection_date}", expanded=False):
                        render_restaurant_details(row)
            except Exception as e:
                st.error(f"Error loading recent restaurants: {str(e)}")
                return

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")