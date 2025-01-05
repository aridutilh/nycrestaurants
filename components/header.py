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
            <div class="search-container">
                <div class="search-icon">🔍</div>
                <input type="text" 
                    class="search-input" 
                    placeholder="Search any restaurant in NYC..."
                    onchange="handleSearchChange(this.value)"
                    aria-label="Search restaurants"
                />
            </div>
        </div>

        <script>
        function handleSearchChange(value) {
            if (window.parent.stStreamlitPyObject) {
                window.parent.stStreamlitPyObject.sendBackMsg({
                    type: "streamlit:setComponentValue",
                    value: value
                });
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
        <div style='text-align: center;'>
            <div class='loading-spinner'></div>
            <p style='color: var(--text-secondary); font-size: 0.9rem; margin-top: 1rem;'>
                Loading data...
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )