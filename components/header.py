import streamlit as st

def render_header():
    """Render the app header with Garfield-themed styling"""
    st.markdown(
        """
        <div class="main-header">
            <h1>🍕 NYC Restaurant Explorer 🗽</h1>
            <p>
                Discover the Best Eats in the Big Apple!<br>
                <span style="font-size: 0.9rem; color: #FF6B00;">
                    "I've never met a lasagna I didn't like" - Not just Garfield
                </span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_loading():
    """Display Garfield-themed loading animation"""
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