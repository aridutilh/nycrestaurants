import streamlit as st

def render_header():
    """Render the app header with pizza parlor styling"""
    st.markdown(
        """
        <div class="main-header">
            <h1>🍕 NYC Pizza & Restaurant Safety Explorer 🗽</h1>
            <p style='font-family: Roboto, sans-serif; font-size: 1.2rem;'>
                Discover food safety ratings across the Big Apple
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_loading():
    """Display pizza-themed loading animation"""
    st.markdown(
        """
        <div style='text-align: center;'>
            <div class='loading-pizza'>🍕</div>
            <p>Loading the freshest data...</p>
        </div>
        """,
        unsafe_allow_html=True
    )
