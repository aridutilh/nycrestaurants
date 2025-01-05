import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants
from components.restaurant_details import render_restaurant_details

def render_search(df):
    """Render the restaurant search component"""
    try:
        # Get current search state
        search_query = st.session_state.get('search_query', '').strip()

        # Debug logging
        st.write("Debug - Current search query:", search_query)
        st.write("Debug - Search triggered:", st.session_state.get('search_triggered', False))

        # Check if we have a valid search query
        if search_query:
            try:
                # Perform search
                results = search_restaurants(df, search_query)

                if results is None or results.empty:
                    st.warning("No restaurants found matching your search.")
                else:
                    # Display results
                    st.success(f"Found {len(results)} matching restaurants:")

                    # Display each result in an expander
                    for _, row in results.iterrows():
                        # Create expander label with key info
                        expander_label = (
                            f"🏪 {row['dba']} - "
                            f"{row['building']} {row['street']}, {row['boro']}"
                        )

                        # Display restaurant details in expander
                        with st.expander(expander_label, expanded=False):
                            render_restaurant_details(row)

            except Exception as e:
                st.error(f"Error performing search: {str(e)}")

        else:
            # Show recently inspected restaurants
            st.subheader("🕒 Recently Inspected Restaurants")
            recent = df.sort_values('inspection_date', ascending=False).head(10)

            for _, row in recent.iterrows():
                expander_label = (
                    f"🏪 {row['dba']} - "
                    f"{row['building']} {row['street']}, {row['boro']}"
                )
                with st.expander(expander_label, expanded=False):
                    render_restaurant_details(row)

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.write("Debug - Error details:", str(e))

    # Always reset search triggered flag after rendering
    st.session_state.search_triggered = False