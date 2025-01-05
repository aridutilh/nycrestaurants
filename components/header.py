import streamlit as st

def render_header():
    """Render the app header with minimalist styling"""
    # Initialize search state if not present
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ''
        st.session_state.search_triggered = False

    # Get current search query value
    current_search = st.session_state.get('search_query', '')

    # Create the header HTML with proper string formatting
    header_html = f"""
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
            <div class="search-icon">🔍</div>
            <input type="text" 
                id="restaurant-search"
                class="search-input" 
                placeholder="Search any restaurant in NYC..."
                value="{current_search}"
                onchange="handleSearchChange(event)"
                oninput="handleSearchInput(event)"
                aria-label="Search restaurants"
            />
        </div>
    </div>

    <script>
    function handleSearchInput(event) {{
        handleSearchChange(event);
    }}

    function handleSearchChange(event) {{
        const value = event.target.value;
        window.parent.streamlit.setComponentValue({{
            value: value,
            dataType: "json",
            args: {{ search_query: value, search_triggered: true }},
        }});
    }}
    </script>
    """

    st.markdown(header_html, unsafe_allow_html=True)

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