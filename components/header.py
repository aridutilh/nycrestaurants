import streamlit as st

def render_header():
    """Render the app header with minimalist styling"""
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

    # Use Streamlit's native text input for search
    search_query = st.text_input(
        label="",
        value=st.session_state.get('search_query', ''),
        placeholder="Search any restaurant in NYC...",
        key="search_input"
    )

    # Update session state when search input changes
    if search_query != st.session_state.get('search_query', ''):
        st.session_state.search_query = search_query
        st.session_state.search_triggered = True

def render_loading():
    """Display minimal loading animation"""
    st.markdown(
        """
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p class="loading-text">Loading restaurants...</p>
            <div class="loading-emoji-container">
                <span class="loading-emoji">🍜</span>
                <span class="loading-emoji">🍕</span>
                <span class="loading-emoji">🍱</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )