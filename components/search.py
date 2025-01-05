import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants
from components.restaurant_details import render_restaurant_details

def render_search(df):
    """Render the restaurant search component"""
    try:
        # Get current search state
        search_query = st.session_state.get('search_query', '').strip()
        search_triggered = st.session_state.get('search_triggered', False)

        # Only perform search if triggered and query exists
        if search_query and search_triggered:
            try:
                # Perform search
                results = search_restaurants(df, search_query)

                if results is None or len(results) == 0:
                    st.warning("No restaurants found matching your search.")
                else:
                    st.write(f"Found {len(results)} matching restaurants:")

                    # Display results
                    for _, row in results.iterrows():
                        with st.expander(
                            f"🏪 {row['dba']} - {row['building']} {row['street']}, {row['boro']}",
                            expanded=False
                        ):
                            render_restaurant_details(row)

            except Exception as e:
                st.error(f"Error performing search: {str(e)}")
            finally:
                # Reset search triggered flag
                st.session_state.search_triggered = False

        elif not search_query:
            # Show recently inspected restaurants
            st.markdown("#### 🕒 Recently Inspected Restaurants")
            recent = df.sort_values('inspection_date', ascending=False).head(10)

            for _, row in recent.iterrows():
                with st.expander(
                    f"🏪 {row['dba']} - {row['building']} {row['street']}, {row['boro']}",
                    expanded=False
                ):
                    render_restaurant_details(row)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")