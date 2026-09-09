import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api_fetcher import fetch_format_rankings
from utils.theme import apply_cricket_theme, render_sidebar_branding

st.set_page_config(page_title="Top Player Stats | Cricbuzz LiveStats", page_icon="📊", layout="wide")

apply_cricket_theme()
render_sidebar_branding()

st.markdown("<h1 class='gradient-header'>📊 Official Cricbuzz Leaderboards</h1>", unsafe_allow_html=True)
st.caption("Live ICC Rankings & Player Stats powered directly by Cricbuzz REST API")
st.divider()

# Main Format Category Tabs (Test, ODI, T20)
main_tab_test, main_tab_odi, main_tab_t20 = st.tabs([
    "🔴 Test Cricket Leaderboard",
    "🔵 ODI Cricket Leaderboard",
    "🟢 T20 Cricket Leaderboard"
])

def render_format_leaderboards(format_key, badge_html, color_theme):
    data = fetch_format_rankings(format_key)
    st.markdown(f"### {badge_html} Top Player Rankings", unsafe_allow_html=True)
    st.info(f"Data Source: **{data.get('source', 'Cricbuzz REST API')}**")
    
    sub_batsmen, sub_bowlers, sub_allrounders = st.tabs([
        "🏏 Batting Leaders",
        "🎯 Bowling Leaders",
        "⚡ All-Rounder Leaders"
    ])

    # 1. Batting Leaders
    with sub_batsmen:
        df_bat = pd.DataFrame(data.get("batsmen", []))
        if df_bat.empty:
            st.warning("No batting rankings data available for this format.")
        else:
            col_chart, col_table = st.columns([3, 2])
            with col_chart:
                fig_bat = px.bar(
                    df_bat,
                    x="name",
                    y="rating",
                    color="rating",
                    text="rating",
                    title=f"{format_key.upper()} Top Ranked Batsmen (ICC Rating)",
                    labels={"name": "Player Name", "rating": "Rating Score"},
                    color_continuous_scale=color_theme
                )
                fig_bat.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_bat, width="stretch")

            with col_table:
                st.markdown("#### 📋 Leaderboard Table")
                st.dataframe(
                    df_bat[["rank", "name", "country", "rating", "trend"]],
                    width="stretch",
                    hide_index=True
                )

    # 2. Bowling Leaders
    with sub_bowlers:
        df_bowl = pd.DataFrame(data.get("bowlers", []))
        if df_bowl.empty:
            st.warning("No bowling rankings data available for this format.")
        else:
            col_chart2, col_table2 = st.columns([3, 2])
            with col_chart2:
                fig_bowl = px.bar(
                    df_bowl,
                    x="name",
                    y="rating",
                    color="rating",
                    text="rating",
                    title=f"{format_key.upper()} Top Ranked Bowlers (ICC Rating)",
                    labels={"name": "Player Name", "rating": "Rating Score"},
                    color_continuous_scale=color_theme
                )
                fig_bowl.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_bowl, width="stretch")

            with col_table2:
                st.markdown("#### 📋 Bowling Leaderboard")
                st.dataframe(
                    df_bowl[["rank", "name", "country", "rating", "trend"]],
                    width="stretch",
                    hide_index=True
                )

    # 3. All-Rounder Leaders
    with sub_allrounders:
        df_all = pd.DataFrame(data.get("allrounders", []))
        if df_all.empty:
            st.warning("No all-rounder rankings data available for this format.")
        else:
            col_chart3, col_table3 = st.columns([3, 2])
            with col_chart3:
                fig_all = px.bar(
                    df_all,
                    x="name",
                    y="rating",
                    color="rating",
                    text="rating",
                    title=f"{format_key.upper()} Top Ranked All-Rounders (ICC Rating)",
                    labels={"name": "Player Name", "rating": "Rating Score"},
                    color_continuous_scale=color_theme
                )
                fig_all.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_all, width="stretch")

            with col_table3:
                st.markdown("#### 📋 All-Rounders Leaderboard")
                st.dataframe(
                    df_all[["rank", "name", "country", "rating", "trend"]],
                    width="stretch",
                    hide_index=True
                )

with main_tab_test:
    render_format_leaderboards("test", "<span style='background: rgba(231, 76, 60, 0.2); color: #e74c3c; border: 1px solid #e74c3c; padding: 4px 12px; border-radius: 20px; font-weight: 700;'>🔴 TEST</span>", "Reds")

with main_tab_odi:
    render_format_leaderboards("odi", "<span style='background: rgba(52, 152, 219, 0.2); color: #3498db; border: 1px solid #3498db; padding: 4px 12px; border-radius: 20px; font-weight: 700;'>🔵 ODI</span>", "Blues")

with main_tab_t20:
    render_format_leaderboards("t20", "<span style='background: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; padding: 4px 12px; border-radius: 20px; font-weight: 700;'>🟢 T20</span>", "Greens")
