import streamlit as st
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from utils.db_connection import init_db
from utils.theme import apply_cricket_theme, render_sidebar_branding




# Configure Streamlit Page
st.set_page_config(
    page_title="Cricbuzz LiveStats | Cricket Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Unified Cricket Theme
apply_cricket_theme()

# Initialize Database Engine
init_db()

# Sidebar Setup
render_sidebar_branding()

with st.sidebar:
    if os.getenv("RAPIDAPI_KEY"):
        if st.button("🔄 Sync Live Cricbuzz API Data"):
            with st.spinner("Fetching latest live matches & scorecards from Cricbuzz API..."):
                from utils.api_fetcher import sync_api_to_database
                success = sync_api_to_database()
                if success:
                    st.success("Successfully synced Cricbuzz API data into SQLite DB!")
                    st.rerun()
                else:
                    st.error("Failed to sync API data. Verify RapidAPI quota.")

    with st.expander("⚙️ Key Configuration"):
        custom_key = st.text_input(
            "Update RapidAPI Key",
            value="",
            type="password",
            placeholder="••••••••••••••••••••••••••••••••",
            help="Enter new key to override environment settings"
        )
        if custom_key:
            os.environ["RAPIDAPI_KEY"] = custom_key
            st.success("New API Key set for current session!")

# Main Content Header
st.markdown("<h1 class='gradient-header'>🏏 Welcome to Cricbuzz LiveStats</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.2rem; color: #94a3b8;'>Real-Time Cricket Match Analytics, Multi-Format Leaderboards & SQL Intelligence</p>", unsafe_allow_html=True)
st.divider()

# High-Level Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Teams", value="83 Teams", delta="International & League")
with col2:
    st.metric(label="Total Players", value="160+ Players", delta="API Synced")
with col3:
    st.metric(label="Matches Tracked", value="25+ Matches", delta="Test/ODI/T20")
with col4:
    st.metric(label="SQL Analytics", value="25 Complete", delta="Beginner to Advanced")

st.markdown("""
<br>
<div style="background: linear-gradient(135deg, rgba(22, 101, 52, 0.15) 0%, rgba(15, 23, 42, 0.5) 100%); padding: 28px; border-radius: 16px; border: 1px solid rgba(34, 197, 94, 0.3); backdrop-filter: blur(12px);">
    <h3 style="color: #4ade80;">🏟️ Stadium Navigation Center</h3>
    <p>Select a module from the left sidebar navigation bar to explore the platform:</p>
    <ul>
        <li><b style="color: #facc15;">1_🏠_Home.py</b>: Explore business use cases, architecture, and free API setup.</li>
        <li><b style="color: #facc15;">2_⚡_Live_Matches.py</b>: Inspect live scorecards, batters, bowler stats, and venue details.</li>
        <li><b style="color: #facc15;">3_📊_Top_Stats.py</b>: View format-categorized leaderboards for <b>Test</b>, <b>ODI</b>, and <b>T20</b>.</li>
        <li><b style="color: #facc15;">4_🔍_SQL_Queries.py</b>: Execute 25 pre-built SQL questions or write custom SQL.</li>
        <li><b style="color: #facc15;">5_🛠️_CRUD_Operations.py</b>: Manage players and match data dynamically.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
