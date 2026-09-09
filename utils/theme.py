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
    """Render consistent sidebar branding & status across all pages."""
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/cricket.png", width=65)
        st.markdown("<h2 class='gradient-header'>Cricbuzz LiveStats</h2>", unsafe_allow_html=True)
        st.caption("🏟️ Real-Time Cricket Stadium Insights & SQL Engine")
        st.divider()

        current_key = os.getenv("RAPIDAPI_KEY", "")
        if current_key:
            st.success("🔒 RapidAPI Key Active (`.env`)")
        else:
            st.info("💡 Running on Free Live Simulation Engine")
