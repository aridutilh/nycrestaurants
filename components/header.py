import streamlit as st

def render_header():
    """Render the app header with minimalist styling"""
    # Initialize search query in session state if not present
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ''

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
                <div class="search-icon">🔍</div>
                <input type="text" 
                    class="search-input" 
                    placeholder="Search any restaurant in NYC..."
                    value=""
                    onchange="handleSearchChange(this.value)"
                    oninput="this.dispatchEvent(new Event('change'))"
                    aria-label="Search restaurants"
                />
            </div>
        </div>

        <script>
        function handleSearchChange(value) {
            // Send the value to Streamlit using the correct event format
            const data = {
                search_query: value
            };

            if (window.parent.streamlit) {
                window.parent.streamlit.setComponentValue(data);
            }
        }
        </script>
        """,
        unsafe_allow_html=True
    )

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