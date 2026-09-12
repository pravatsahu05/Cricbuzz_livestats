import streamlit as st
import os

CRICKET_THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&display=swap');

    /* Global Dark Stadium Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #112d1f 0%, #0a1912 60%, #050d09 100%);
        color: #e2e8f0;
        font-family: 'Outfit', 'Inter', system-ui, sans-serif;
    }

    /* Top Header Bar Styling */
    [data-testid="stHeader"] {
        background: rgba(10, 25, 18, 0.8) !important;
        backdrop-filter: blur(12px);
    }

    /* Sidebar Cricket Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(10, 25, 18, 0.9) !important;
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(34, 197, 94, 0.25);
    }

    /* Sidebar Navigation Links Theme - Consistent Across All Pages */
    [data-testid="stSidebarNav"] {
        background: rgba(15, 23, 42, 0.5) !important;
        border-radius: 14px;
        padding: 12px;
        border: 1px solid rgba(34, 197, 94, 0.2);
        margin-bottom: 20px;
    }
    [data-testid="stSidebarNav"] ul {
        gap: 8px;
    }
    [data-testid="stSidebarNav"] a {
        background: rgba(22, 101, 52, 0.15) !important;
        color: #cbd5e1 !important;
        border-radius: 10px !important;
        border: 1px solid rgba(34, 197, 94, 0.15) !important;
        font-weight: 600 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 10px 14px !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        background: rgba(34, 197, 94, 0.25) !important;
        color: #4ade80 !important;
        border-color: #22c55e !important;
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: linear-gradient(135deg, #15803d 0%, #22c55e 100%) !important;
        color: #052e16 !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 18px rgba(34, 197, 94, 0.45) !important;
    }

    /* Metric Cards - Cricket Pitch Style */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(22, 101, 52, 0.2) 0%, rgba(15, 23, 42, 0.4) 100%);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 16px;
        padding: 18px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: #22c55e;
        box-shadow: 0 12px 32px rgba(34, 197, 94, 0.25);
    }

    /* Cricket Headers Gradient */
    .gradient-header {
        background: linear-gradient(90deg, #4ade80 0%, #facc15 50%, #22c55e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    /* Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: #052e16;
        font-weight: 800;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(74, 222, 128, 0.6);
        transform: scale(1.02);
    }

    /* Tab Headers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #15803d 0%, #22c55e 100%) !important;
        color: #052e16 !important;
        font-weight: 800;
    }
</style>
"""

def apply_cricket_theme():
    """Apply unified Cricket Stadium theme and Navigation Bar CSS across all pages."""
    st.markdown(CRICKET_THEME_CSS, unsafe_allow_html=True)

def render_sidebar_branding():
    """Render consistent sidebar branding, dynamic API Key controls, reboot trigger, quota tracker, and Sync API button across all pages."""
    from utils.api_fetcher import get_api_key, sync_api_to_database, check_api_quota

    with st.sidebar:
        st.image("https://img.icons8.com/color/96/cricket.png", width=65)
        st.markdown("<h2 class='gradient-header'>Cricbuzz LiveStats</h2>", unsafe_allow_html=True)
        st.caption("🏟️ Real-Time Cricket Stadium Insights & SQL Engine")
        st.divider()

        active_key = get_api_key()
        if st.session_state.get("RAPIDAPI_KEY"):
            st.success("🟢 RapidAPI Key Active (UI Session)")
        elif os.getenv("RAPIDAPI_KEY"):
            st.success("🟢 RapidAPI Key Active (.env)")
        elif hasattr(st, "secrets") and "RAPIDAPI_KEY" in st.secrets:
            st.success("🟢 RapidAPI Key Active (Streamlit Secrets)")
        else:
            st.info("💡 Running on Free Live Simulation Engine")

        with st.expander("🔑 RapidAPI Key & Sync Controls", expanded=False):
            st.markdown("<small style='color: #94a3b8;'>Enter key below or set <code>RAPIDAPI_KEY</code> in Streamlit Cloud Secrets dashboard.</small>", unsafe_allow_html=True)
            
            custom_key = st.text_input(
                "Update RapidAPI Key",
                value=st.session_state.get("RAPIDAPI_KEY", ""),
                type="password",
                placeholder="••••••••••••••••••••••••••••••••",
                key="sidebar_custom_key_input",
                help="Key updates automatically reboot session and refresh data."
            )

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("⚡ Save & Reboot", key="sidebar_save_reboot_btn", help="Save new key, clear cache, and reboot app session"):
                    if custom_key.strip():
                        st.session_state["RAPIDAPI_KEY"] = custom_key.strip()
                        os.environ["RAPIDAPI_KEY"] = custom_key.strip()
                        st.cache_data.clear()
                        st.success("API Key updated! Rebooting session...")
                        st.rerun()
                    else:
                        st.warning("Please enter a key.")

            with col_b:
                if st.button("🔄 Clear Cache", key="sidebar_clear_cache_btn", help="Clear app cache and rerun session"):
                    st.cache_data.clear()
                    st.success("Cache cleared!")
                    st.rerun()

            if st.button("📊 Check Key Quota & Usage", key="sidebar_check_quota_btn", help="Check remaining API searches/quota directly from RapidAPI headers"):
                quota = check_api_quota()
                if quota.get("remaining") is not None:
                    st.info(f"📊 **Remaining Searches**: `{quota['remaining']}` / `{quota.get('limit', 'N/A')}`")
                    if quota.get("hard_remaining"):
                        st.caption(f"Monthly Hard Limit Remaining: **{quota['hard_remaining']}**")
                else:
                    st.warning(f"Status: **{quota.get('status', 'Unknown')}**")

            st.divider()

            if st.button("🔄 Sync Live Cricbuzz API Data", key="sidebar_sync_api_btn", help="Fetch live matches, series, teams & venues from RapidAPI into SQLite DB"):
                if not active_key and not custom_key.strip():
                    st.warning("⚠️ Please enter a RapidAPI Key or configure Streamlit Secrets before syncing.")
                else:
                    if custom_key.strip() and custom_key.strip() != active_key:
                        st.session_state["RAPIDAPI_KEY"] = custom_key.strip()
                        os.environ["RAPIDAPI_KEY"] = custom_key.strip()

                    with st.spinner("Extracting live Cricbuzz API data into SQLite database..."):
                        success = sync_api_to_database()
                        if success:
                            st.cache_data.clear()
                            st.success("✅ Successfully synced Cricbuzz API data into SQLite DB!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to sync API data. Verify RapidAPI key & quota.")


