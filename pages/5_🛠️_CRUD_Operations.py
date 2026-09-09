import streamlit as st
import pandas as pd
from utils.db_connection import (
    get_all_players_df,
    insert_player,
    update_player,
    delete_player,
    get_db_connection,
    execute_sql_query
)
from utils.theme import apply_cricket_theme, render_sidebar_branding

st.set_page_config(page_title="CRUD Operations | Cricbuzz LiveStats", page_icon="🛠️", layout="wide")

apply_cricket_theme()
render_sidebar_branding()

st.markdown("<h1 class='gradient-header'>🛠️ Data Management Console (CRUD)</h1>", unsafe_allow_html=True)
st.caption("Full Administrative UI for Player Records & Match Stats Operations")
st.divider()

# Get Teams for Selectboxes
conn = get_db_connection()
teams_df = pd.read_sql_query("SELECT team_id, name FROM teams;", conn)
conn.close()

team_dict = dict(zip(teams_df["name"], teams_df["team_id"])) if not teams_df.empty else {"India": 1}

main_crud_tabs = st.tabs(["🏏 Player Records CRUD", "🏟️ Match Records CRUD"])

# ==================== TAB 1: PLAYER RECORDS CRUD ====================
with main_crud_tabs[0]:
    p_tab1, p_tab2, p_tab3, p_tab4 = st.tabs([
        "📋 View All Players",
        "➕ Add New Player",
        "✏️ Edit Player",
        "🗑️ Remove Player"
    ])

    with p_tab1:
        st.subheader("📋 Registered Player Database Records")
        df_players = get_all_players_df()
        st.dataframe(df_players, width="stretch", hide_index=True)
        st.info(f"Total Registered Players in Database: **{len(df_players)}**")

    with p_tab2:
        st.subheader("➕ Register New Player Record")
        with st.form("create_player_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *", placeholder="e.g. Yashasvi Jaiswal")
                team_name = st.selectbox("Team *", list(team_dict.keys()))
                role = st.selectbox("Playing Role *", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
                country = st.text_input("Country *", value="India")
                batting_style = st.selectbox("Batting Style", ["Right-hand bat", "Left-hand bat"])
                bowling_style = st.text_input("Bowling Style", value="Right-arm medium")

            with col2:
                matches = st.number_input("Matches Played", min_value=0, value=15)
                runs = st.number_input("Total Career Runs", min_value=0, value=750)
                avg = st.number_input("Batting Average", min_value=0.0, value=48.5)
                sr = st.number_input("Strike Rate", min_value=0.0, value=92.5)
                centuries = st.number_input("Centuries", min_value=0, value=2)
                fifties = st.number_input("Fifties", min_value=0, value=4)
                wickets = st.number_input("Wickets Taken", min_value=0, value=0)

            submit_create = st.form_submit_button("➕ Save Player Record")
            if submit_create:
                if name.strip():
                    t_id = team_dict.get(team_name, 1)
                    insert_player(
                        name.strip(), t_id, role, batting_style,
                        bowling_style, country.strip(), matches, runs, avg, sr,
                        centuries, fifties, wickets
                    )
                    st.success(f"Player '{name}' registered successfully!")
                    st.rerun()
                else:
                    st.error("Player Name cannot be empty.")

    with p_tab3:
        st.subheader("✏️ Edit Existing Player Record")
        df_players = get_all_players_df()
        if df_players.empty:
            st.warning("No players found in database.")
        else:
            player_options = {f"{row['full_name']} (ID: {row['player_id']})": row['player_id'] for _, row in df_players.iterrows()}
            selected_label = st.selectbox("Select Player to Edit:", list(player_options.keys()))
            selected_p_id = player_options[selected_label]
            p_row = df_players[df_players["player_id"] == selected_p_id].iloc[0]

            with st.form("update_player_form"):
                u_name = st.text_input("Full Name", value=str(p_row["full_name"]))
                roles = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
                cur_role_idx = roles.index(p_row["role"]) if p_row["role"] in roles else 0
                u_role = st.selectbox("Role", roles, index=cur_role_idx)
                u_country = st.text_input("Country", value=str(p_row["country"]))
                u_matches = st.number_input("Matches Played", min_value=0, value=int(p_row["matches_played"]))
                u_runs = st.number_input("Total Runs", min_value=0, value=int(p_row["total_runs"]))
                u_avg = st.number_input("Batting Avg", min_value=0.0, value=float(p_row["batting_avg"]))
                u_sr = st.number_input("Strike Rate", min_value=0.0, value=float(p_row["strike_rate"]))
                u_wickets = st.number_input("Wickets Taken", min_value=0, value=int(p_row["wickets_taken"]))

                submit_update = st.form_submit_button("💾 Save Player Updates")
                if submit_update:
                    update_player(selected_p_id, u_name, u_role, u_country, u_matches, u_runs, u_avg, u_sr, u_wickets)
                    st.success(f"Player '{u_name}' record updated successfully!")
                    st.rerun()

    with p_tab4:
        st.subheader("🗑️ Delete Player Record")
        df_players = get_all_players_df()
        if df_players.empty:
            st.warning("No players found in database.")
        else:
            player_options = {f"{row['full_name']} (ID: {row['player_id']})": row['player_id'] for _, row in df_players.iterrows()}
            del_label = st.selectbox("Select Player to Delete:", list(player_options.keys()), key="del_player_sel")
            del_p_id = player_options[del_label]

            st.warning(f"⚠️ Are you sure you want to permanently delete **{del_label}**?")
            if st.button("🗑️ Confirm Delete Player", type="primary"):
                delete_player(del_p_id)
                st.success(f"Player ID {del_p_id} removed successfully!")
                st.rerun()

# ==================== TAB 2: MATCH RECORDS CRUD ====================
with main_crud_tabs[1]:
    m_tab1, m_tab2, m_tab3 = st.tabs([
        "📋 View Matches",
        "➕ Schedule New Match",
        "🗑️ Delete Match"
    ])

    with m_tab1:
        st.subheader("📋 Scheduled & Completed Match Records")
        df_matches, _ = execute_sql_query("""
        SELECT 
            m.match_id, 
            m.description, 
            t1.name AS team1, 
            t2.name AS team2, 
            v.name AS venue, 
            m.match_date, 
            m.format, 
            m.status 
        FROM matches m 
        JOIN teams t1 ON m.team1_id = t1.team_id 
        JOIN teams t2 ON m.team2_id = t2.team_id 
        JOIN venues v ON m.venue_id = v.venue_id 
        ORDER BY m.match_date DESC;
        """)
        if df_matches is not None and not df_matches.empty:
            st.dataframe(df_matches, width="stretch", hide_index=True)
            st.info(f"Total Matches Recorded: **{len(df_matches)}**")
        else:
            st.warning("No match records found.")

    with m_tab2:
        st.subheader("➕ Schedule New Match Record")
        with st.form("create_match_form", clear_on_submit=True):
            m_desc = st.text_input("Match Description *", value="India vs Australia 4th T20I")
            c_m1, c_m2 = st.columns(2)
            with c_m1:
                m_t1 = st.selectbox("Team 1 *", list(team_dict.keys()), key="m_t1_sel")
                m_fmt = st.selectbox("Match Format *", ["T20I", "ODI", "Test", "T20"])
                m_date = st.date_input("Match Date")
            with c_m2:
                m_t2 = st.selectbox("Team 2 *", list(team_dict.keys()), index=min(1, len(team_dict)-1), key="m_t2_sel")
                m_status = st.selectbox("Status", ["Scheduled", "In Progress", "Completed"])

            submit_m_create = st.form_submit_button("➕ Save Match Record")
            if submit_m_create:
                if m_desc.strip():
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                    INSERT INTO matches (description, series_id, team1_id, team2_id, venue_id, match_date, winner_team_id, victory_margin, victory_type, toss_winner_id, toss_decision, format, status)
                    VALUES (?, 1, ?, ?, 1, ?, ?, 25, 'runs', ?, 'bat', ?, ?);
                    """, (
                        m_desc.strip(), team_dict[m_t1], team_dict[m_t2], str(m_date),
                        team_dict[m_t1], team_dict[m_t1], m_fmt, m_status
                    ))
                    conn.commit()
                    conn.close()
                    st.success("New match scheduled successfully!")
                    st.rerun()

    with m_tab3:
        st.subheader("🗑️ Remove Match Record")
        if df_matches is not None and not df_matches.empty:
            match_options = {f"Match #{row['match_id']}: {row['description']} ({row['match_date']})": row['match_id'] for _, row in df_matches.iterrows()}
            del_m_label = st.selectbox("Select Match to Delete:", list(match_options.keys()))
            del_m_id = match_options[del_m_label]

            st.warning(f"⚠️ Confirm deletion of **{del_m_label}**?")
            if st.button("🗑️ Confirm Delete Match", type="primary"):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM matches WHERE match_id = ?;", (del_m_id,))
                conn.commit()
                conn.close()
                st.success(f"Match ID {del_m_id} removed successfully!")
                st.rerun()
