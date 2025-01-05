import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants

def render_search_section(df):
    """Render the search section with a clean, minimal structure"""
    # Create a container for the search functionality
    with st.container():
        # Search input with minimal wrapping
        search_query = st.text_input(
            label="Search restaurants",
            value=st.session_state.get('search_query', ''),
            placeholder="🔍 Search any restaurant in NYC...",
            key="search_input_main",
            label_visibility="collapsed"
        )

        # Title and description below search
        st.markdown(
            """
            <div class="app-header">
                <h1>NYC Restaurant Safety</h1>
                <p class="subtitle">
                    Explore food safety ratings and inspection results across New York City
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Update search state
        if 'search_query' not in st.session_state or search_query != st.session_state.search_query:
            st.session_state.search_query = search_query

        # Display results if there's a search query
        if search_query.strip():
            try:
                results = search_restaurants(df, search_query)

                if results is None or results.empty:
                    st.warning("No restaurants found matching your search.")
                else:
                    st.markdown(
                        f"<div class='results-count'>Found {len(results)} matching restaurants:</div>",
                        unsafe_allow_html=True
                    )

                    for idx, row in results.iterrows():
                        with st.expander(
                            f"🏪 {row['dba']} - "
                            f"{row['grade'] if pd.notna(row['grade']) else 'Grade N/A'} "
                            f"(Score: {int(row['score']) if pd.notna(row['score']) else 'N/A'})"
                        ):
                            st.markdown(
                                f"""
                                <div class='restaurant-card'>
                                    <p>📍 {row['building']} {row['street']}, {row['boro']}</p>
                                    <p>📅 Inspected: {row['inspection_date'].strftime('%B %d, %Y')}</p>
                                    {f"<p class='violation'>❗ {row['violation_description']}</p>" if pd.notna(row['violation_description']) else ""}
                                    <div class='restaurant-meta'>
                                        <span>🍽️ {row['cuisine_description'] if pd.notna(row['cuisine_description']) else 'N/A'}</span>
                                        {f"<span class='critical'>⚠️ {row['critical_flag']}</span>" if pd.notna(row['critical_flag']) else ""}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

            except Exception as e:
                st.error(f"Error displaying search results: {str(e)}")