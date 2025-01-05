import streamlit as st

def render_header():
    """Render the app header with simplified styling and floating emojis"""
    st.markdown(
        """
        <div class="simple-header">
            <div class="emoji-container">
                <span class="floating-emoji left">🍕</span>
                <h1>NYC Food Safety</h1>
                <span class="floating-emoji right">🗽</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_loading():
    """Display loading animation"""
    st.markdown(
        """
        <div style='text-align: center;'>
            <div class='loading-icon'>🍝</div>
            <p style='font-family: "Comic Neue", cursive; color: #FF6B00;'>
                Hunting down the tastiest spots...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )