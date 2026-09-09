import streamlit as st
import time
from utils.db_connection import SQL_QUESTIONS, execute_sql_query
from utils.theme import apply_cricket_theme, render_sidebar_branding

st.set_page_config(page_title="SQL Queries | Cricbuzz LiveStats", page_icon="🔍", layout="wide")

apply_cricket_theme()
render_sidebar_branding()

st.markdown("<h1 class='gradient-header'>🔍 SQL Analytics Console</h1>", unsafe_allow_html=True)
st.caption("25 Complete Analytical Queries across Beginner, Intermediate, and Advanced Levels")
st.divider()

tab_practice, tab_custom = st.tabs(["📚 25 Practice Questions", "💻 Custom SQL Playground"])

with tab_practice:
    col_lvl, col_q = st.columns([1, 2])
    
    with col_lvl:
        level_filter = st.radio("Filter by Level", ["All Levels", "Beginner (1-8)", "Intermediate (9-16)", "Advanced (17-25)"])
    
    filtered_q_ids = []
    for q_id, q_data in SQL_QUESTIONS.items():
        if level_filter == "All Levels":
            filtered_q_ids.append(q_id)
        elif level_filter == "Beginner (1-8)" and q_data["level"] == "Beginner":
            filtered_q_ids.append(q_id)
        elif level_filter == "Intermediate (9-16)" and q_data["level"] == "Intermediate":
            filtered_q_ids.append(q_id)
        elif level_filter == "Advanced (17-25)" and q_data["level"] == "Advanced":
            filtered_q_ids.append(q_id)

    with col_q:
        q_options = [f"Q{q_id}: {SQL_QUESTIONS[q_id]['title']}" for q_id in filtered_q_ids]
        selected_q_text = st.selectbox("Select Question to Execute:", q_options)

    if selected_q_text:
        selected_q_id = int(selected_q_text.split(":")[0].replace("Q", ""))
        q_info = SQL_QUESTIONS[selected_q_id]

        st.subheader(q_info["title"])
        
        lvl = q_info["level"]
        badge_style = "background: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; padding: 4px 14px; border-radius: 20px; font-weight: 700;" if lvl == "Beginner" else ("background: rgba(241, 196, 15, 0.2); color: #f1c40f; border: 1px solid #f1c40f; padding: 4px 14px; border-radius: 20px; font-weight: 700;" if lvl == "Intermediate" else "background: rgba(231, 76, 60, 0.2); color: #e74c3c; border: 1px solid #e74c3c; padding: 4px 14px; border-radius: 20px; font-weight: 700;")
        st.markdown(f"<span style='{badge_style}'>Difficulty: {lvl}</span>", unsafe_allow_html=True)
        
        st.markdown(f"**Description:** {q_info['description']}")
        
        st.markdown("#### 📜 SQL Query Statement")
        st.code(q_info["sql"].strip(), language="sql")

        if st.button(f"▶️ Run Query #{selected_q_id}", key=f"btn_{selected_q_id}"):
            start_time = time.time()
            df, error = execute_sql_query(q_info["sql"])
            exec_time = round((time.time() - start_time) * 1000, 2)

            if error:
                st.error(f"Execution Error: {error}")
            else:
                st.success(f"Execution Successful! ({len(df)} rows returned in {exec_time} ms)")
                st.dataframe(df, width="stretch", hide_index=True)
                
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Results as CSV",
                    data=csv_data,
                    file_name=f"query_{selected_q_id}_results.csv",
                    mime="text/csv"
                )

with tab_custom:
    st.subheader("💻 Interactive Custom SQL Playground")
    st.markdown("Execute custom SQL queries on `cricbuzz_analytics.db` SQLite database.")
    
    st.info("Available Tables: `teams`, `players`, `venues`, `series`, `matches`, `batting_performances`, `bowling_performances`, `partnerships`")
    
    custom_sql = st.text_area("Enter your custom SQL query:", value="SELECT * FROM players WHERE batting_avg > 45 ORDER BY batting_avg DESC;", height=120)
    
    if st.button("🚀 Run Custom SQL"):
        if custom_sql.strip():
            start_time = time.time()
            df_custom, err_custom = execute_sql_query(custom_sql)
            exec_time = round((time.time() - start_time) * 1000, 2)

            if err_custom:
                st.error(f"SQL Error: {err_custom}")
            else:
                st.success(f"Query Executed Successfully! ({len(df_custom)} rows in {exec_time} ms)")
                st.dataframe(df_custom, width="stretch", hide_index=True)
        else:
            st.warning("Please enter a valid SQL query.")
