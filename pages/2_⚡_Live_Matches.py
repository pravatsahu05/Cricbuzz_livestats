import streamlit as st
import pandas as pd
from utils.api_fetcher import fetch_live_matches
from utils.theme import apply_cricket_theme, render_sidebar_branding

st.set_page_config(page_title="Live Matches | Cricbuzz LiveStats", page_icon="⚡", layout="wide")

apply_cricket_theme()
render_sidebar_branding()

st.markdown("<h1 class='gradient-header'>⚡ Real-Time Live Cricket Scorecards</h1>", unsafe_allow_html=True)
st.caption("Live Match Scores & Commentary powered by Cricbuzz API Engine")

col_ref, col_src = st.columns([1, 4])
with col_ref:
    if st.button("🔄 Refresh Live Scores"):
        st.rerun()

matches = fetch_live_matches()

with col_src:
    source_name = matches[0].get("source", "REST API") if matches else "REST API"
    if "Simulation" in source_name or "Quota" in source_name:
        st.warning(f"📡 Data Engine: **{source_name}** (RapidAPI Key Rate-Limited or Quota Reached)")
    else:
        st.success(f"🟢 Data Engine: **{source_name}**")

st.divider()

if not matches:
    st.warning("No live matches available at the moment.")
else:
    for m in matches:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(22, 101, 52, 0.25) 0%, rgba(15, 23, 42, 0.5) 100%); border: 1px solid rgba(34, 197, 94, 0.4); border-radius: 16px; padding: 24px; margin-bottom: 24px; backdrop-filter: blur(12px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #94a3b8; font-weight: 700;">🏆 {m['series']} • {m['match_desc']}</span>
                <span style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; padding: 4px 14px; border-radius: 20px; font-size: 0.9rem; font-weight: 700;">🔴 {m['status']}</span>
            </div>
            <hr style="border-color: rgba(34, 197, 94, 0.2); margin: 16px 0;">
            <div style="display: flex; justify-content: space-around; text-align: center; margin: 20px 0;">
                <div>
                    <div style="font-size: 1.4rem; font-weight: 800; color: #ffffff;">{m['team1']}</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #4ade80; text-shadow: 0 0 10px rgba(74, 222, 128, 0.3);">{m['team1_score']}/{m['team1_wickets']}</div>
                    <div style="color: #94a3b8; font-weight: 600;">({m['team1_overs']} ov)</div>
                </div>
                <div style="font-size: 1.8rem; font-weight: 900; color: #facc15; align-self: center;">vs</div>
                <div>
                    <div style="font-size: 1.4rem; font-weight: 800; color: #ffffff;">{m['team2']}</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #4ade80; text-shadow: 0 0 10px rgba(74, 222, 128, 0.3);">{m['team2_score']}/{m['team2_wickets']}</div>
                    <div style="color: #94a3b8; font-weight: 600;">({m['team2_overs']} ov)</div>
                </div>
            </div>
            <div style="color: #94a3b8; font-size: 0.95rem; text-align: center;">
                📍 <b>Venue</b>: {m['venue']}, {m['city']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if "batsmen" in m and m["batsmen"]:
            col_bat, col_bowl = st.columns(2)
            with col_bat:
                st.markdown("<h4 style='color: #4ade80;'>🏏 Current Batsmen</h4>", unsafe_allow_html=True)
                df_bat = pd.DataFrame(m["batsmen"])
                df_bat.columns = ["Batter", "Runs", "Balls", "4s", "6s", "SR"]
                st.dataframe(df_bat, width="stretch", hide_index=True)
            with col_bowl:
                st.markdown("<h4 style='color: #4ade80;'>🎯 Current Bowler</h4>", unsafe_allow_html=True)
                b = m["bowler"] if "bowler" in m else {"name": "Jasprit Bumrah", "overs": 3.4, "runs": 22, "wickets": 3, "economy": 6.0}
                df_bowl = pd.DataFrame([b])
                df_bowl.columns = ["Bowler", "Overs", "Runs", "Wickets", "Economy"]
                st.dataframe(df_bowl, width="stretch", hide_index=True)
        st.divider()
