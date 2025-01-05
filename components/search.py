import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants

def render_search_section(df):
    """Render the search section including header and results"""
    # Header section
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
        </div>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ''

    # Search input using native Streamlit component
    search_query = st.text_input(
        label="Search restaurants",
        value=st.session_state.search_query,
        placeholder="🔍 Enter restaurant name, address, or borough...",
        key="search_input_field"
    )

    # Update search state
    if search_query != st.session_state.search_query:
        st.session_state.search_query = search_query

    # Display results section
    try:
        if search_query.strip():
            # Perform search
            results = search_restaurants(df, search_query)

            if results is None or results.empty:
                st.warning("No restaurants found matching your search.")
            else:
                st.success(f"Found {len(results)} matching restaurants:")

                # Display each result
                for idx, row in results.iterrows():
                    expander_label = f"🏪 {row['dba']} - {row['building']} {row['street']}, {row['boro']}"

                    with st.expander(expander_label):
                        # Restaurant details
                        st.markdown(f"**Grade:** {row['grade'] if pd.notna(row['grade']) else 'N/A'}")
                        st.markdown(f"**Score:** {int(row['score']) if pd.notna(row['score']) else 'N/A'}")
                        st.markdown(f"**Latest Inspection:** {row['inspection_date'].strftime('%B %d, %Y')}")

                        if pd.notna(row['violation_description']):
                            st.markdown("**Latest Violation:**")
                            st.markdown(f"_{row['violation_description']}_")

                        col1, col2 = st.columns(2)
                        with col1:
                            if pd.notna(row['cuisine_description']):
                                st.markdown(f"**Cuisine:** {row['cuisine_description']}")
                        with col2:
                            if pd.notna(row['critical_flag']):
                                st.markdown(f"**Critical Flag:** {row['critical_flag']}")
        else:
            # Show recently inspected restaurants
            st.subheader("🕒 Recently Inspected Restaurants")
            recent = df.sort_values('inspection_date', ascending=False).head(10)

            for _, row in recent.iterrows():
                with st.expander(f"🏪 {row['dba']} - {row['building']} {row['street']}, {row['boro']}"):
                    st.markdown(f"**Grade:** {row['grade'] if pd.notna(row['grade']) else 'N/A'}")
                    st.markdown(f"**Score:** {int(row['score']) if pd.notna(row['score']) else 'N/A'}")
                    st.markdown(f"**Latest Inspection:** {row['inspection_date'].strftime('%B %d, %Y')}")

                    if pd.notna(row['violation_description']):
                        st.markdown("**Latest Violation:**")
                        st.markdown(f"_{row['violation_description']}_")

    except Exception as e:
        st.error(f"Error displaying search results: {str(e)}")
        st.write("Debug - Error details:", str(e))