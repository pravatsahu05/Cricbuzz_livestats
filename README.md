# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A comprehensive, multi-page Streamlit web application integrating real-time match data from the **Cricbuzz REST API** (via RapidAPI or free live simulation fallback) with an interactive **SQLite database engine**, featuring **25 complete SQL analytical queries** and **full CRUD administrative operations**.

---

## 🌟 Key Features

1. ⚡ **Real-Time Live Match Scorecards**: Live match status, venue info, ball-by-ball score updates, current batsmen, and bowler stats.
2. 📊 **Top Player Stats & Visual Leaderboards**: Interactive Plotly charts for highest run scorers, leading wicket takers, batting averages, and player comparison matrices.
3. 🔍 **25 Complete SQL Analytics Queries**: Pre-built questions across Beginner (1-8), Intermediate (9-16), and Advanced (17-25) levels with instant tabular output, CSV export, and an interactive **Custom SQL Console**.
4. 🛠️ **Administrative CRUD Operations**: Form-based UI for creating, reading, updating, and deleting team and player records.
5. 🔑 **Dual API Engine**: Connects to RapidAPI Cricbuzz API when an API key is provided, and automatically falls back to realistic live data when no key is set.

---

## ☁️ Streamlit Cloud Deployment & API Key Rotation Guide

### 1. Deploying to Streamlit Cloud
1. Push your project repository to GitHub.
2. Go to **[Streamlit Community Cloud](https://share.streamlit.io/)** and log in.
3. Click **New app**, choose your repo, branch (`main`), and set **Main file path** to `app.py`.
4. Click **Advanced settings... -> Secrets** and add your key:
   ```toml
   RAPIDAPI_KEY = "your_rapidapi_key_here"
   ```
5. Click **Deploy!**

### 2. Updating API Key on a Regular Basis & Auto-Reboot
- **Streamlit Cloud Dashboard**: When you update your `RAPIDAPI_KEY` under Streamlit Cloud app settings -> Secrets, Streamlit automatically reboots your application!
- **In-App Sidebar Rotation**: Alternatively, paste your new API key into the sidebar under **🔑 RapidAPI Key & Sync Controls** and click **⚡ Save & Reboot**. This saves your key, clears cached calls, and reboots the session.

### 3. Extracting Live API Data into Web App
- Click **"🔄 Sync Live Cricbuzz API Data"** in the sidebar.
- The web app extracts live match scorecards, series, teams, and venue data from Cricbuzz REST API and saves them directly into your SQLite database (`cricbuzz_analytics.db`).

---


## 🛠️ Installation & Setup Guide

### 1. Clone & Navigate to Project Directory
```bash
cd "c:\Users\Pravat\OneDrive\Desktop\Coding Programs\Cricbuzz_livestats"
```

### 2. Install Required Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit Dashboard
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser!

---

## 📁 Project Folder Structure

```
cricbuzz_livestats/
├── app.py                      # Main entry point, Glassmorphism UI & Navigation
├── requirements.txt            # Python dependencies (streamlit, pandas, plotly, requests)
├── README.md                   # Full documentation & setup guide
├── .env.example                # API key configuration template
├── utils/
│   ├── db_connection.py        # SQLite database connection, schema setup & 25 SQL queries
│   └── api_fetcher.py          # RapidAPI Cricbuzz API client with live fallback engine
└── pages/
    ├── 1_🏠_Home.py             # Overview, problem statement, business use cases & guide
    ├── 2_⚡_Live_Matches.py     # Live scorecards, venue info & batter/bowler tables
    ├── 3_📊_Top_Stats.py        # Visual leaderboards with Plotly graphs
    ├── 4_🔍_SQL_Queries.py      # 25 Complete practice queries & SQL Playground
    └── 5_🛠️_CRUD_Operations.py  # Create, Read, Update, Delete UI for players
```

---

## 🗄️ Database Schema & SQL Questions

The SQLite database (`cricbuzz_analytics.db`) includes tables: `teams`, `players`, `venues`, `series`, `matches`, `batting_performances`, `bowling_performances`, and `partnerships`.

All **25 SQL practice questions** from beginner SELECT queries to complex window functions, CTEs, standard deviation consistency metrics, toss advantage analysis, weighted player ranking scores, and career trajectory time-series are fully implemented in `pages/4_🔍_SQL_Queries.py`.
