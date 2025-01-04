import streamlit as st
import pandas as pd
from utils.data_loader import search_restaurants
from components.header import render_loading

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

                for _, row in results.iterrows():
                    st.markdown(
                        f"""
                        <div class='restaurant-card'>
                            <h3>{row['dba']}</h3>
                            <p>📍 {row['building']} {row['street']}</p>
                            <p>🏆 Grade: {row['grade'] if pd.notna(row['grade']) else 'N/A'}</p>
                            <p>📊 Score: {int(row['score']) if pd.notna(row['score']) else 'N/A'}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.warning("No restaurants found matching your search.")

    st.markdown("</div>", unsafe_allow_html=True)