import streamlit as st

def render_header():
    """Render the app header with minimalist styling"""
    st.markdown(
        """
        <div class="simple-header">
            <h1>NYC Restaurant Safety</h1>
            <p class="subheader">
                Explore food safety ratings and inspection results across New York City
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_loading():
    """Display minimal loading animation"""
    st.markdown(
        """
        <div style='text-align: center;'>
            <div class='loading-spinner'></div>
            <p style='color: var(--text-secondary); font-size: 0.9rem; margin-top: 1rem;'>
                Loading data...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )