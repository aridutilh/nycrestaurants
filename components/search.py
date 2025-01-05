import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants

def render_search_section(df):
    """Render the search section including header and results"""
    # Header section with integrated search
    st.markdown(
        """
        <div class="simple-header">
            <div class="floating-emojis">
                <span class="float-left">🍕</span>
                <span class="float-right">👨‍🍳</span>
            </div>
            <h1>NYC Restaurant Safety</h1>
            <p class="subheader">
                Explore food safety ratings and inspection results across New York City
            </p>
            <div class="search-container">
        """,
        unsafe_allow_html=True
    )

    search_query = st.text_input(
        label="",
        value=st.session_state.get('search_query', ''),
        placeholder="🔍 Search any restaurant in NYC...",
        key="search_input_field"
    )

    # Center the search label below the input
    st.markdown(
        """
        <p class="search-label">
            Search restaurants
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Update search state
    if 'search_query' not in st.session_state or search_query != st.session_state.search_query:
        st.session_state.search_query = search_query

    # Display results section only if there's a search query
    if search_query.strip():
        try:
            # Perform search
            results = search_restaurants(df, search_query)

            if results is None or results.empty:
                st.warning("No restaurants found matching your search.")
            else:
                st.markdown(f"##### Found {len(results)} matching restaurants:")
                st.markdown("<div class='search-results'>", unsafe_allow_html=True)

                # Display each result
                for idx, row in results.iterrows():
                    # Create expander label with key info
                    expander_label = (
                        f"🏪 {row['dba']} - "
                        f"{row['grade'] if pd.notna(row['grade']) else 'Grade N/A'} "
                        f"(Score: {int(row['score']) if pd.notna(row['score']) else 'N/A'})"
                    )

                    with st.expander(expander_label, expanded=False):
                        st.markdown(f"""
                        <div class='restaurant-result'>
                            <p>📍 {row['building']} {row['street']}, {row['boro']}</p>
                            <p>📅 Inspected: {row['inspection_date'].strftime('%B %d, %Y')}</p>
                            {f"<p class='violation'>❗ {row['violation_description']}</p>" if pd.notna(row['violation_description']) else ""}
                            <div class='restaurant-details'>
                                <span>🍽️ {row['cuisine_description'] if pd.notna(row['cuisine_description']) else 'N/A'}</span>
                                {f"<span class='critical'>⚠️ {row['critical_flag']}</span>" if pd.notna(row['critical_flag']) else ""}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error displaying search results: {str(e)}")