import streamlit as st
from utils.theme import apply_cricket_theme, render_sidebar_branding

st.set_page_config(page_title="Home | Cricbuzz LiveStats", page_icon="🏠", layout="wide")

apply_cricket_theme()
render_sidebar_branding()

st.markdown("<h1 class='gradient-header'>🏠 Project Overview & Stadium Architecture</h1>", unsafe_allow_html=True)
st.caption("Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics")
st.divider()

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("""
    ### 🎯 Problem Statement & Goal
    Build a comprehensive cricket analytics dashboard integrating live data from the **Cricbuzz API** (via RapidAPI or fallback simulation engine) with a **SQLite database** to deliver:
    
    1. ⚡ **Real-Time Match Updates**: Live scorecards, status badges, venue details, batter & bowler stats.
    2. 📊 **Multi-Format Player Statistics**: Categorized leaderboards for **Test**, **ODI**, and **T20** with Plotly graphs.
    3. 🔍 **SQL-Driven Analytics**: 25 complete pre-formulated analytical queries across 3 difficulty levels.
    4. 🛠️ **Full CRUD Operations**: Form-based UI to manage players and match records dynamically.
    """)

    st.markdown("""
    ### 💼 Business Use Cases
    - 📺 **Sports Media & Broadcasting**: Real-time match updates and player performance trends for commentary teams.
    - 🏏 **Fantasy Cricket Platforms**: Head-to-head stats, player form tracking, and score updates.
    - 📈 **Cricket Analytics Firms**: Advanced statistical modeling, team evaluation, and partnership analytics.
    - 🎓 **Educational Institutions**: Hands-on SQL practice with engaging, real-world sports datasets.
    """)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(22, 101, 52, 0.2) 0%, rgba(15, 23, 42, 0.4) 100%); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 16px; padding: 24px; margin-bottom: 20px; backdrop-filter: blur(12px);">
        <h3 style="color: #4ade80;">🛠️ Tech Stack</h3>
        <ul>
            <li><b>Language</b>: Python 3.10+</li>
            <li><b>UI Framework</b>: Streamlit</li>
            <li><b>Database Engine</b>: SQLite3</li>
            <li><b>Data Processing</b>: Pandas</li>
            <li><b>Visualization</b>: Plotly Express</li>
            <li><b>API Integration</b>: Requests & REST API</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(22, 101, 52, 0.2) 0%, rgba(15, 23, 42, 0.4) 100%); border: 1px solid rgba(34, 197, 94, 0.3); border-radius: 16px; padding: 24px; margin-bottom: 20px; backdrop-filter: blur(12px);">
        <h3 style="color: #facc15;">🔑 RapidAPI Setup Guide</h3>
        <ol>
            <li>Visit <b><a href="https://rapidapi.com" target="_blank" style="color: #4ade80;">RapidAPI.com</a></b>.</li>
            <li>Search for <b>cricbuzz-cricket</b> or <b>cricket live data</b>.</li>
            <li>Click <b>Subscribe to Test</b> under the <b>BASIC ($0/month) Free Plan</b>.</li>
            <li>Copy your <b>X-RapidAPI-Key</b>.</li>
            <li>Paste it in the sidebar API settings input field!</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("### 📁 Project Architecture & Folder Structure")
st.code("""
cricbuzz_livestats/
├── app.py                      # Main entry point for Streamlit application & Cricket Stadium CSS
├── requirements.txt            # Python package dependencies
├── README.md                   # Complete documentation
├── utils/
│   ├── db_connection.py        # Centralized SQLite connection, schema & 25 SQL queries
│   ├── api_fetcher.py          # RapidAPI Cricbuzz REST API fetcher with mock fallback
│   └── theme.py                # Unified Cricket Stadium theme & navigation bar styling
└── pages/
    ├── 1_🏠_Home.py             # Project overview & documentation
    ├── 2_⚡_Live_Matches.py     # Real-time scorecards & venue stats
    ├── 3_📊_Top_Stats.py        # Test, ODI & T20 leaderboards & Plotly analytics
    ├── 4_🔍_SQL_Queries.py      # 25 Complete SQL practice queries + playground
    └── 5_🛠️_CRUD_Operations.py  # Form-based Create, Read, Update, Delete UI
""", language="text")
