import streamlit as st

def render_header():
    """Render the app header with retro diner styling and neon effects"""
    st.markdown(
        """
        <div class="simple-header">
            <div class="emoji-container">
                <span class="floating-emoji left">🍔</span>
                <h1>NYC DINER SAFETY</h1>
                <span class="floating-emoji right">☕</span>
            </div>
            <p class="garfield-quote">"Life is like a diner... you get what you order!" - NYC Food Safety</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_loading():
    """Display loading animation with diner theme"""
    st.markdown(
        """
        <div style='text-align: center;'>
            <div class='loading-spinner'></div>
            <p style='font-family: "Satisfy", cursive; color: var(--diner-turquoise); font-size: 1.2rem;'>
                Cooking up your results...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )