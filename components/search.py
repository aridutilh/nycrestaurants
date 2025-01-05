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
                        # Create a clickable expander for each restaurant
                        with st.expander(f"🏪 {row['dba']}", expanded=False):
                            # Basic info visible in the collapsed view
                            st.markdown(
                                f"""
                                📍 {row['building']} {row['street']}, {row['boro']}  
                                📅 Latest Inspection: {row['inspection_date'].strftime('%B %d, %Y')}  
                                ⭐ Score: {int(row['score']) if pd.notna(row['score']) else 'N/A'}  
                                {f"📋 Grade: {row['grade']}" if pd.notna(row['grade']) else ""}
                                """
                            )

                            # Create two columns for detailed view
                            col1, col2 = st.columns([3, 2])

                            with col1:
                                if pd.notna(row['violation_description']):
                                    st.markdown("**Latest Violation:**")
                                    st.markdown(f"_{row['violation_description']}_")
                                st.markdown("**Additional Details:**")
                                if pd.notna(row['cuisine_description']):
                                    st.markdown(f"Cuisine: {row['cuisine_description']}")
                                if pd.notna(row['critical_flag']):
                                    st.markdown(f"Critical Flag: {row['critical_flag']}")

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