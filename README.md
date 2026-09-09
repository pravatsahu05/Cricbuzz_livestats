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

## 🔑 How to Generate Free Cricbuzz API Key on RapidAPI

Follow these steps to generate your free Cricbuzz API key:

1. Visit **[RapidAPI.com](https://rapidapi.com)** and sign up for a free account.
2. Search for **"Cricbuzz"** or **"cricbuzz-cricket"** in the search bar.
3. Select **Cricbuzz Cricket API** (e.g. `cricbuzz-cricket.p.rapidapi.com`).
4. Click **Subscribe to Test** on the **BASIC (Free)** Plan ($0/month).
5. Copy your **`X-RapidAPI-Key`** from the Code Snippets header.
6. Enter your key directly in the **Sidebar Settings** input field in the Streamlit app or set `RAPIDAPI_KEY=your_key` in a `.env` file.

> [!TIP]
> Even without an API key, Cricbuzz LiveStats runs 100% out-of-the-box using the built-in free live simulation engine!

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
