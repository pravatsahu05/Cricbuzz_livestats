import sqlite3
import pandas as pd
import os
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cricbuzz_analytics.db")

def get_db_connection():
    """Establish connection to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_resource
def init_db():
    """Create all required tables and populate seed data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Teams Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        country TEXT NOT NULL,
        matches_played INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0
    );
    """)

    # 2. Venues Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS venues (
        venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        city TEXT NOT NULL,
        country TEXT NOT NULL,
        capacity INTEGER NOT NULL
    );
    """)

    # 3. Series Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS series (
        series_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        host_country TEXT NOT NULL,
        match_type TEXT NOT NULL,
        start_date TEXT NOT NULL,
        total_matches INTEGER NOT NULL
    );
    """)

    # 4. Players Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        team_id INTEGER,
        role TEXT NOT NULL,
        batting_style TEXT,
        bowling_style TEXT,
        country TEXT NOT NULL,
        matches_played INTEGER DEFAULT 0,
        total_runs INTEGER DEFAULT 0,
        batting_avg REAL DEFAULT 0.0,
        strike_rate REAL DEFAULT 0.0,
        centuries INTEGER DEFAULT 0,
        fifties INTEGER DEFAULT 0,
        wickets_taken INTEGER DEFAULT 0,
        bowling_avg REAL DEFAULT 0.0,
        economy_rate REAL DEFAULT 0.0,
        catches INTEGER DEFAULT 0,
        stumpings INTEGER DEFAULT 0,
        FOREIGN KEY (team_id) REFERENCES teams (team_id) ON DELETE SET NULL
    );
    """)

    # 5. Matches Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        series_id INTEGER,
        team1_id INTEGER,
        team2_id INTEGER,
        venue_id INTEGER,
        match_date TEXT NOT NULL,
        winner_team_id INTEGER,
        victory_margin INTEGER,
        victory_type TEXT,
        toss_winner_id INTEGER,
        toss_decision TEXT,
        format TEXT NOT NULL,
        status TEXT DEFAULT 'Completed',
        FOREIGN KEY (series_id) REFERENCES series (series_id),
        FOREIGN KEY (team1_id) REFERENCES teams (team_id),
        FOREIGN KEY (team2_id) REFERENCES teams (team_id),
        FOREIGN KEY (winner_team_id) REFERENCES teams (team_id),
        FOREIGN KEY (toss_winner_id) REFERENCES teams (team_id),
        FOREIGN KEY (venue_id) REFERENCES venues (venue_id)
    );
    """)

    # 6. Batting Performances Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS batting_performances (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        player_id INTEGER,
        runs_scored INTEGER NOT NULL,
        balls_faced INTEGER NOT NULL,
        fours INTEGER DEFAULT 0,
        sixes INTEGER DEFAULT 0,
        strike_rate REAL,
        match_date TEXT NOT NULL,
        quarter TEXT NOT NULL,
        year INTEGER NOT NULL,
        batting_position INTEGER NOT NULL,
        FOREIGN KEY (match_id) REFERENCES matches (match_id),
        FOREIGN KEY (player_id) REFERENCES players (player_id) ON DELETE CASCADE
    );
    """)

    # 7. Bowling Performances Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bowling_performances (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        player_id INTEGER,
        overs_bowled REAL NOT NULL,
        runs_conceded INTEGER NOT NULL,
        wickets_taken INTEGER NOT NULL,
        economy_rate REAL NOT NULL,
        FOREIGN KEY (match_id) REFERENCES matches (match_id),
        FOREIGN KEY (player_id) REFERENCES players (player_id) ON DELETE CASCADE
    );
    """)

    # 8. Partnerships Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS partnerships (
        partnership_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        innings INTEGER NOT NULL,
        player1_id INTEGER,
        player2_id INTEGER,
        combined_runs INTEGER NOT NULL,
        position_differ INTEGER DEFAULT 1,
        FOREIGN KEY (match_id) REFERENCES matches (match_id),
        FOREIGN KEY (player1_id) REFERENCES players (player_id) ON DELETE CASCADE,
        FOREIGN KEY (player2_id) REFERENCES players (player_id) ON DELETE CASCADE
    );
    """)

    conn.commit()

    # Seed initial data if teams table is empty
    cursor.execute("SELECT COUNT(*) FROM teams;")
    if cursor.fetchone()[0] == 0:
        seed_database(conn)

    conn.close()

    # Automatically sync live Cricbuzz API data if API key is present
    try:
        from utils.api_fetcher import sync_api_to_database
        sync_api_to_database(DB_PATH)
    except Exception:
        pass


def seed_database(conn):
    """Seed comprehensive initial cricket dataset into the SQLite database."""
    cursor = conn.cursor()

    # Seed Teams
    teams_data = [
        ("India", "India", 120, 85, 35),
        ("Australia", "Australia", 115, 78, 37),
        ("England", "England", 110, 65, 45),
        ("South Africa", "South Africa", 100, 58, 42),
        ("Pakistan", "Pakistan", 95, 50, 45),
        ("New Zealand", "New Zealand", 98, 56, 42)
    ]
    cursor.executemany("INSERT INTO teams (name, country, matches_played, wins, losses) VALUES (?, ?, ?, ?, ?);", teams_data)

    # Seed Venues
    venues_data = [
        ("Narendra Modi Stadium", "Ahmedabad", "India", 132000),
        ("Eden Gardens", "Kolkata", "India", 68000),
        ("Wankhede Stadium", "Mumbai", "India", 33000),
        ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
        ("Sydney Cricket Ground", "Sydney", "Australia", 48000),
        ("Lord's Cricket Ground", "London", "England", 31100),
        ("The Oval", "London", "England", 27500),
        ("M. Chinnaswamy Stadium", "Bengaluru", "India", 40000)
    ]
    cursor.executemany("INSERT INTO venues (name, city, country, capacity) VALUES (?, ?, ?, ?);", venues_data)

    # Seed Series
    series_data = [
        ("ICC Cricket World Cup 2023", "India", "ODI", "2023-10-05", 48),
        ("Border-Gavaskar Trophy 2024", "Australia", "Test", "2024-11-22", 5),
        ("T20 World Cup 2024", "USA/West Indies", "T20I", "2024-06-01", 55),
        ("India vs England Series 2024", "India", "Test", "2024-01-25", 5),
        ("Asia Cup 2023", "Sri Lanka", "ODI", "2023-08-30", 13)
    ]
    cursor.executemany("INSERT INTO series (name, host_country, match_type, start_date, total_matches) VALUES (?, ?, ?, ?, ?);", series_data)

    # Seed Players (id: 1..12)
    players_data = [
        # (full_name, team_id, role, batting_style, bowling_style, country, matches_played, total_runs, batting_avg, strike_rate, centuries, fifties, wickets_taken, bowling_avg, economy_rate, catches, stumpings)
        ("Virat Kohli", 1, "Batsman", "Right-hand bat", "Right-arm medium", "India", 295, 13848, 58.67, 93.5, 50, 72, 5, 166.2, 5.4, 150, 0),
        ("Rohit Sharma", 1, "Batsman", "Right-hand bat", "Right-arm offbreak", "India", 262, 10709, 49.12, 91.8, 31, 55, 8, 62.1, 5.2, 105, 0),
        ("Ravindra Jadeja", 1, "All-rounder", "Left-hand bat", "Slow left-arm orthodox", "India", 197, 2756, 32.8, 85.2, 0, 13, 220, 35.8, 4.9, 82, 0),
        ("Jasprit Bumrah", 1, "Bowler", "Right-hand bat", "Right-arm fast", "India", 89, 210, 8.5, 60.1, 0, 0, 149, 23.55, 4.6, 25, 0),
        ("Steve Smith", 2, "Batsman", "Right-hand bat", "Right-arm legbreak", "Australia", 158, 5534, 43.5, 87.2, 12, 33, 28, 34.6, 5.4, 90, 0),
        ("Travis Head", 2, "Batsman", "Left-hand bat", "Right-arm offbreak", "Australia", 65, 2397, 42.8, 101.4, 6, 16, 18, 42.1, 5.8, 38, 0),
        ("Glenn Maxwell", 2, "All-rounder", "Right-hand bat", "Right-arm offbreak", "Australia", 138, 3890, 35.4, 126.9, 4, 23, 70, 48.2, 5.6, 85, 0),
        ("Pat Cummins", 2, "Bowler", "Right-hand bat", "Right-arm fast", "Australia", 88, 450, 12.3, 75.0, 0, 0, 141, 28.1, 5.1, 30, 0),
        ("Joe Root", 3, "Batsman", "Right-hand bat", "Right-arm offbreak", "England", 171, 6522, 47.6, 86.9, 16, 39, 27, 56.4, 5.7, 88, 0),
        ("Ben Stokes", 3, "All-rounder", "Left-hand bat", "Right-arm fast-medium", "England", 114, 3328, 38.7, 95.3, 5, 22, 74, 42.3, 6.1, 54, 0),
        ("Babar Azam", 5, "Batsman", "Right-hand bat", "Right-arm offbreak", "Pakistan", 117, 5729, 56.7, 88.2, 19, 32, 0, 0.0, 0.0, 50, 0),
        ("KL Rahul", 1, "Wicket-keeper", "Right-hand bat", "None", "India", 75, 2820, 49.4, 87.6, 7, 18, 0, 0.0, 0.0, 60, 12)
    ]
    cursor.executemany("""
    INSERT INTO players (full_name, team_id, role, batting_style, bowling_style, country, matches_played, total_runs, batting_avg, strike_rate, centuries, fifties, wickets_taken, bowling_avg, economy_rate, catches, stumpings)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, players_data)

    # Seed Matches (Match IDs 1..25)
    matches_data = []
    # Dates spanning recent months and years 2020 to 2026
    sample_dates = [
        "2026-08-15", "2026-08-20", "2026-08-28", "2026-09-01", "2024-11-25",
        "2024-12-05", "2024-06-15", "2024-06-29", "2024-02-10", "2024-03-02",
        "2023-11-19", "2023-11-15", "2023-10-14", "2023-09-17", "2023-09-10",
        "2022-10-23", "2022-11-10", "2022-07-14", "2021-10-24", "2021-06-18",
        "2020-11-27", "2020-12-02", "2020-01-19", "2024-08-10", "2024-08-18"
    ]
    
    formats = ["ODI", "ODI", "T20I", "T20I", "Test", "Test", "T20I", "T20I", "Test", "Test", "ODI", "ODI", "ODI", "ODI", "ODI", "T20I", "T20I", "ODI", "T20I", "Test", "ODI", "ODI", "ODI", "ODI", "T20I"]

    for i in range(1, 26):
        t1 = 1 if i % 2 == 1 else 2
        t2 = 2 if t1 == 1 else (3 if i % 3 == 0 else 5)
        winner = t1 if (i % 5 != 0) else t2
        margin = 35 if i % 2 == 0 else 4  # Close match if margin < 50 runs or < 5 wickets
        vtype = "runs" if i % 2 == 0 else "wickets"
        v_id = (i % 8) + 1
        series_id = (i % 5) + 1
        toss_w = t1 if i % 3 != 0 else t2
        toss_dec = "bat" if i % 2 == 0 else "bowl"
        dt = sample_dates[i - 1]
        fmt = formats[i - 1]

        matches_data.append((
            f"Match #{i}: Team {t1} vs Team {t2} - {fmt}",
            series_id, t1, t2, v_id, dt, winner, margin, vtype, toss_w, toss_dec, fmt, "Completed"
        ))

    cursor.executemany("""
    INSERT INTO matches (description, series_id, team1_id, team2_id, venue_id, match_date, winner_team_id, victory_margin, victory_type, toss_winner_id, toss_decision, format, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, matches_data)

    # Seed Batting & Bowling Performances & Partnerships
    batting_perf = []
    bowling_perf = []
    partnerships_data = []

    # Map dates to quarters
    def get_quarter(date_str):
        month = int(date_str.split("-")[1])
        if month <= 3: return "Q1"
        elif month <= 6: return "Q2"
        elif month <= 9: return "Q3"
        else: return "Q4"

    perf_id = 1
    part_id = 1

    for match_id in range(1, 26):
        m_date = sample_dates[match_id - 1]
        m_year = int(m_date.split("-")[0])
        m_qtr = get_quarter(m_date)

        # Batting performances for player 1 (Virat Kohli) and player 2 (Rohit Sharma)
        runs_vk = 85 if match_id % 3 == 0 else (45 if match_id % 2 == 0 else 62)
        runs_rs = 54 if match_id % 3 == 0 else (72 if match_id % 2 == 0 else 38)
        runs_rj = 35 if match_id % 2 == 0 else 22
        runs_sh = 68 if match_id % 3 == 0 else 15

        batting_perf.append((match_id, 1, runs_vk, 68, 8, 2, round(runs_vk / 68 * 100, 2), m_date, m_qtr, m_year, 3))
        batting_perf.append((match_id, 2, runs_rs, 45, 6, 3, round(runs_rs / 45 * 100, 2), m_date, m_qtr, m_year, 1))
        batting_perf.append((match_id, 3, runs_rj, 25, 3, 1, round(runs_rj / 25 * 100, 2), m_date, m_qtr, m_year, 7))
        batting_perf.append((match_id, 5, runs_sh, 55, 7, 2, round(runs_sh / 55 * 100, 2), m_date, m_qtr, m_year, 4))
        batting_perf.append((match_id, 10, 42, 30, 4, 2, 140.0, m_date, m_qtr, m_year, 6))
        batting_perf.append((match_id, 11, 55, 48, 5, 1, 114.58, m_date, m_qtr, m_year, 3))

        # Bowling performances
        bowling_perf.append((match_id, 4, 10.0 if match_id % 2 == 0 else 4.0, 38, 3 if match_id % 2 == 0 else 2, 3.8))
        bowling_perf.append((match_id, 3, 8.0, 42, 2, 5.25))
        bowling_perf.append((match_id, 8, 9.0, 45, 2, 5.0))
        bowling_perf.append((match_id, 7, 4.0, 28, 1, 7.0))
        bowling_perf.append((match_id, 10, 6.0, 36, 2, 6.0))

        # Partnerships (Kohli & Sharma at position 1 and 2)
        comb_runs = runs_vk + runs_rs
        partnerships_data.append((match_id, 1, 1, 2, comb_runs, 1))

    cursor.executemany("""
    INSERT INTO batting_performances (match_id, player_id, runs_scored, balls_faced, fours, sixes, strike_rate, match_date, quarter, year, batting_position)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, batting_perf)

    cursor.executemany("""
    INSERT INTO bowling_performances (match_id, player_id, overs_bowled, runs_conceded, wickets_taken, economy_rate)
    VALUES (?, ?, ?, ?, ?, ?);
    """, bowling_perf)

    cursor.executemany("""
    INSERT INTO partnerships (match_id, innings, player1_id, player2_id, combined_runs, position_differ)
    VALUES (?, ?, ?, ?, ?, ?);
    """, partnerships_data)

    conn.commit()

# SQL Questions Dictionary (All 25 queries)
SQL_QUESTIONS = {
    1: {
        "title": "Question 1: Players Representing India",
        "level": "Beginner",
        "description": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "sql": """
SELECT full_name, role, batting_style, bowling_style 
FROM players 
WHERE country = 'India';
"""
    },
    2: {
        "title": "Question 2: Recent Matches in Last 30 Days",
        "level": "Beginner",
        "description": "Show all cricket matches played in the last 30 days with description, team names, venue with city, and match date.",
        "sql": """
SELECT 
    m.description, 
    t1.name AS team1, 
    t2.name AS team2, 
    v.name || ', ' || v.city AS venue, 
    m.match_date 
FROM matches m 
JOIN teams t1 ON m.team1_id = t1.team_id 
JOIN teams t2 ON m.team2_id = t2.team_id 
JOIN venues v ON m.venue_id = v.venue_id 
WHERE JULIANDAY('now') - JULIANDAY(m.match_date) <= 30 
ORDER BY m.match_date DESC;
"""
    },
    3: {
        "title": "Question 3: Top 10 ODI Run Scorers",
        "level": "Beginner",
        "description": "List top 10 highest run scorers in ODI cricket showing player name, total runs, batting average, and centuries.",
        "sql": """
SELECT full_name, total_runs, batting_avg, centuries 
FROM players 
WHERE role IN ('Batsman', 'All-rounder', 'Wicket-keeper') 
ORDER BY total_runs DESC 
LIMIT 10;
"""
    },
    4: {
        "title": "Question 4: Venues with Capacity > 50,000",
        "level": "Beginner",
        "description": "Display venues with capacity greater than 50,000 spectators ordered by largest capacity.",
        "sql": """
SELECT name, city, country, capacity 
FROM venues 
WHERE capacity > 50000 
ORDER BY capacity DESC;
"""
    },
    5: {
        "title": "Question 5: Total Wins per Team",
        "level": "Beginner",
        "description": "Calculate how many matches each team has won. Display teams with most wins first.",
        "sql": """
SELECT t.name AS team_name, COUNT(m.match_id) AS total_wins 
FROM teams t 
JOIN matches m ON t.team_id = m.winner_team_id 
GROUP BY t.team_id, t.name 
ORDER BY total_wins DESC;
"""
    },
    6: {
        "title": "Question 6: Player Count by Role",
        "level": "Beginner",
        "description": "Count how many players belong to each playing role.",
        "sql": """
SELECT role, COUNT(player_id) AS player_count 
FROM players 
GROUP BY role 
ORDER BY player_count DESC;
"""
    },
    7: {
        "title": "Question 7: Highest Score per Format",
        "level": "Beginner",
        "description": "Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I).",
        "sql": """
SELECT format, MAX(runs_scored) AS highest_individual_score 
FROM (
    SELECT m.format, bp.runs_scored 
    FROM batting_performances bp 
    JOIN matches m ON bp.match_id = m.match_id
) 
GROUP BY format;
"""
    },
    8: {
        "title": "Question 8: Series Started in 2024",
        "level": "Beginner",
        "description": "Show all cricket series that started in the year 2024.",
        "sql": """
SELECT name, host_country, match_type, start_date, total_matches 
FROM series 
WHERE strftime('%Y', start_date) = '2024';
"""
    },
    9: {
        "title": "Question 9: All-Rounders (>1000 Runs & >50 Wickets)",
        "level": "Intermediate",
        "description": "Find all-rounder players who have scored >1000 runs AND taken >50 wickets in their career.",
        "sql": """
SELECT full_name, total_runs, wickets_taken, 'All Formats' AS cricket_format 
FROM players 
WHERE role = 'All-rounder' AND total_runs > 1000 AND wickets_taken > 50;
"""
    },
    10: {
        "title": "Question 10: Details of Last 20 Completed Matches",
        "level": "Intermediate",
        "description": "Get details of last 20 completed matches with teams, winner, margin, type, and venue.",
        "sql": """
SELECT 
    m.description, 
    t1.name AS team1, 
    t2.name AS team2, 
    tw.name AS winning_team, 
    m.victory_margin, 
    m.victory_type, 
    v.name AS venue_name 
FROM matches m 
JOIN teams t1 ON m.team1_id = t1.team_id 
JOIN teams t2 ON m.team2_id = t2.team_id 
JOIN teams tw ON m.winner_team_id = tw.team_id 
JOIN venues v ON m.venue_id = v.venue_id 
WHERE m.status = 'Completed' 
ORDER BY m.match_date DESC 
LIMIT 20;
"""
    },
    11: {
        "title": "Question 11: Multi-Format Player Breakdown",
        "level": "Intermediate",
        "description": "Compare player performance across Test, ODI, and T20I formats for players playing >= 2 formats.",
        "sql": """
SELECT 
    p.full_name, 
    SUM(CASE WHEN m.format = 'Test' THEN bp.runs_scored ELSE 0 END) AS test_runs, 
    SUM(CASE WHEN m.format = 'ODI' THEN bp.runs_scored ELSE 0 END) AS odi_runs, 
    SUM(CASE WHEN m.format = 'T20I' THEN bp.runs_scored ELSE 0 END) AS t20i_runs, 
    ROUND(AVG(bp.runs_scored), 2) AS overall_batting_avg 
FROM players p 
JOIN batting_performances bp ON p.player_id = bp.player_id 
JOIN matches m ON bp.match_id = m.match_id 
GROUP BY p.player_id, p.full_name 
HAVING COUNT(DISTINCT m.format) >= 2;
"""
    },
    12: {
        "title": "Question 12: Team Performance Home vs Away",
        "level": "Intermediate",
        "description": "Analyze team performance in home vs away conditions based on venue country.",
        "sql": """
SELECT 
    t.name AS team_name, 
    SUM(CASE WHEN v.country = t.country AND m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS home_wins, 
    SUM(CASE WHEN v.country != t.country AND m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS away_wins 
FROM teams t 
JOIN matches m ON t.team_id = m.team1_id OR t.team_id = m.team2_id 
JOIN venues v ON m.venue_id = v.venue_id 
GROUP BY t.team_id, t.name;
"""
    },
    13: {
        "title": "Question 13: 100+ Batting Partnerships",
        "level": "Intermediate",
        "description": "Identify consecutive batting partnerships scoring 100 or more runs in an innings.",
        "sql": """
SELECT 
    p1.full_name AS player1, 
    p2.full_name AS player2, 
    part.combined_runs, 
    part.innings 
FROM partnerships part 
JOIN players p1 ON part.player1_id = p1.player_id 
JOIN players p2 ON part.player2_id = p2.player_id 
WHERE part.combined_runs >= 100 AND part.position_differ = 1;
"""
    },
    14: {
        "title": "Question 14: Bowling Performance by Venue",
        "level": "Intermediate",
        "description": "Calculate bowler stats at venues where they played >= 3 matches with >= 4 overs bowled.",
        "sql": """
SELECT 
    p.full_name, 
    v.name AS venue_name, 
    COUNT(bp.match_id) AS matches_played, 
    SUM(bp.wickets_taken) AS total_wickets, 
    ROUND(AVG(bp.economy_rate), 2) AS avg_economy_rate 
FROM bowling_performances bp 
JOIN matches m ON bp.match_id = m.match_id 
JOIN venues v ON m.venue_id = v.venue_id 
JOIN players p ON bp.player_id = p.player_id 
WHERE bp.overs_bowled >= 4 
GROUP BY p.player_id, v.venue_id 
HAVING COUNT(bp.match_id) >= 3;
"""
    },
    15: {
        "title": "Question 15: Close Match Clutch Performers",
        "level": "Intermediate",
        "description": "Identify players performing in close matches (<50 runs or <5 wickets margin).",
        "sql": """
SELECT 
    p.full_name, 
    COUNT(DISTINCT m.match_id) AS close_matches_played, 
    ROUND(AVG(bp.runs_scored), 2) AS avg_runs_in_close_matches, 
    SUM(CASE WHEN m.winner_team_id = p.team_id THEN 1 ELSE 0 END) AS close_match_wins 
FROM batting_performances bp 
JOIN matches m ON bp.match_id = m.match_id 
JOIN players p ON bp.player_id = p.player_id 
WHERE (m.victory_type = 'runs' AND m.victory_margin < 50) OR (m.victory_type = 'wickets' AND m.victory_margin < 5) 
GROUP BY p.player_id, p.full_name;
"""
    },
    16: {
        "title": "Question 16: Annual Batting Performance Trends",
        "level": "Intermediate",
        "description": "Track player average runs per match and strike rate for each year since 2020.",
        "sql": """
SELECT 
    p.full_name, 
    bp.year, 
    ROUND(AVG(bp.runs_scored), 2) AS avg_runs_per_match, 
    ROUND(AVG(bp.strike_rate), 2) AS avg_strike_rate 
FROM batting_performances bp 
JOIN players p ON bp.player_id = p.player_id 
WHERE bp.year >= 2020 
GROUP BY p.player_id, bp.year 
HAVING COUNT(bp.match_id) >= 5;
"""
    },
    17: {
        "title": "Question 17: Toss Impact on Match Outcome",
        "level": "Advanced",
        "description": "Calculate win percentage for teams winning the toss, broken down by toss decision (bat vs bowl).",
        "sql": """
SELECT 
    toss_decision, 
    COUNT(match_id) AS total_tosses, 
    SUM(CASE WHEN toss_winner_id = winner_team_id THEN 1 ELSE 0 END) AS toss_and_match_wins, 
    ROUND(100.0 * SUM(CASE WHEN toss_winner_id = winner_team_id THEN 1 ELSE 0 END) / COUNT(match_id), 2) AS win_percentage 
FROM matches 
GROUP BY toss_decision;
"""
    },
    18: {
        "title": "Question 18: Economical Bowlers in Limited Overs",
        "level": "Advanced",
        "description": "Find most economical bowlers in ODI & T20 formats with >= 10 matches and >= 2 overs/match.",
        "sql": """
SELECT 
    p.full_name, 
    SUM(bp.wickets_taken) AS total_wickets, 
    ROUND(AVG(bp.economy_rate), 2) AS overall_economy_rate 
FROM bowling_performances bp 
JOIN matches m ON bp.match_id = m.match_id 
JOIN players p ON bp.player_id = p.player_id 
WHERE m.format IN ('ODI', 'T20I', 'T20') 
GROUP BY p.player_id 
HAVING COUNT(bp.match_id) >= 10 AND AVG(bp.overs_bowled) >= 2 
ORDER BY overall_economy_rate ASC;
"""
    },
    19: {
        "title": "Question 19: Batsman Consistency (Standard Deviation)",
        "level": "Advanced",
        "description": "Calculate average runs and standard deviation of runs for batsmen faced >= 10 balls/innings.",
        "sql": """
SELECT 
    p.full_name, 
    ROUND(AVG(bp.runs_scored), 2) AS avg_runs, 
    ROUND(SQRT(AVG(bp.runs_scored * bp.runs_scored) - AVG(bp.runs_scored) * AVG(bp.runs_scored)), 2) AS stddev_runs 
FROM batting_performances bp 
JOIN players p ON bp.player_id = p.player_id 
WHERE bp.balls_faced >= 10 AND bp.year >= 2022 
GROUP BY p.player_id 
HAVING COUNT(bp.performance_id) >= 3 
ORDER BY stddev_runs ASC;
"""
    },
    20: {
        "title": "Question 20: Cross-Format Matches & Batting Averages",
        "level": "Advanced",
        "description": "Show Test, ODI, and T20 match counts and averages for players with >= 20 total matches.",
        "sql": """
SELECT 
    p.full_name, 
    SUM(CASE WHEN m.format = 'Test' THEN 1 ELSE 0 END) AS test_matches, 
    ROUND(AVG(CASE WHEN m.format = 'Test' THEN bp.runs_scored END), 2) AS test_avg, 
    SUM(CASE WHEN m.format = 'ODI' THEN 1 ELSE 0 END) AS odi_matches, 
    ROUND(AVG(CASE WHEN m.format = 'ODI' THEN bp.runs_scored END), 2) AS odi_avg, 
    SUM(CASE WHEN m.format = 'T20I' THEN 1 ELSE 0 END) AS t20_matches, 
    ROUND(AVG(CASE WHEN m.format = 'T20I' THEN bp.runs_scored END), 2) AS t20_avg 
FROM players p 
JOIN batting_performances bp ON p.player_id = bp.player_id 
JOIN matches m ON bp.match_id = m.match_id 
GROUP BY p.player_id 
HAVING p.matches_played >= 20;
"""
    },
    21: {
        "title": "Question 21: Comprehensive Weighted Performance Score",
        "level": "Advanced",
        "description": "Rank players combining batting, bowling, and fielding points into a single weighted score.",
        "sql": """
SELECT 
    full_name, 
    role, 
    country, 
    ROUND(
        (total_runs * 0.01) + (batting_avg * 0.5) + (strike_rate * 0.3) + 
        (wickets_taken * 2) + ((50 - bowling_avg) * 0.5) + ((6 - economy_rate) * 2) + 
        (catches * 3) + (stumpings * 5), 2
    ) AS total_weighted_score 
FROM players 
ORDER BY total_weighted_score DESC;
"""
    },
    22: {
        "title": "Question 22: Head-to-Head Prediction Analysis",
        "level": "Advanced",
        "description": "Analyze head-to-head match records between teams with >= 5 matches played.",
        "sql": """
SELECT 
    t1.name AS team1, 
    t2.name AS team2, 
    COUNT(m.match_id) AS total_matches, 
    SUM(CASE WHEN m.winner_team_id = t1.team_id THEN 1 ELSE 0 END) AS team1_wins, 
    SUM(CASE WHEN m.winner_team_id = t2.team_id THEN 1 ELSE 0 END) AS team2_wins, 
    ROUND(AVG(m.victory_margin), 2) AS avg_victory_margin, 
    ROUND(100.0 * SUM(CASE WHEN m.winner_team_id = t1.team_id THEN 1 ELSE 0 END) / COUNT(m.match_id), 2) AS team1_win_pct 
FROM matches m 
JOIN teams t1 ON m.team1_id = t1.team_id 
JOIN teams t2 ON m.team2_id = t2.team_id 
WHERE m.match_date >= '2023-01-01' 
GROUP BY t1.team_id, t2.team_id 
HAVING COUNT(m.match_id) >= 5;
"""
    },
    23: {
        "title": "Question 23: Player Form & Momentum Categorization",
        "level": "Advanced",
        "description": "Categorize players as 'Excellent Form', 'Good Form', 'Average Form', or 'Poor Form'.",
        "sql": """
SELECT 
    p.full_name, 
    ROUND(AVG(bp.runs_scored), 2) AS avg_runs_last_10, 
    SUM(CASE WHEN bp.runs_scored >= 50 THEN 1 ELSE 0 END) AS fifties_in_last_10, 
    CASE 
        WHEN AVG(bp.runs_scored) >= 50 THEN 'Excellent Form' 
        WHEN AVG(bp.runs_scored) >= 35 THEN 'Good Form' 
        WHEN AVG(bp.runs_scored) >= 20 THEN 'Average Form' 
        ELSE 'Poor Form' 
    END AS form_category 
FROM batting_performances bp 
JOIN players p ON bp.player_id = p.player_id 
GROUP BY p.player_id, p.full_name 
ORDER BY avg_runs_last_10 DESC;
"""
    },
    24: {
        "title": "Question 24: Batting Partnership Combinations",
        "level": "Advanced",
        "description": "Rank consecutive batting partnerships by average runs, 50+ stands, and success rate.",
        "sql": """
SELECT 
    p1.full_name AS partner1, 
    p2.full_name AS partner2, 
    COUNT(part.partnership_id) AS total_partnerships, 
    ROUND(AVG(part.combined_runs), 2) AS avg_partnership_runs, 
    MAX(part.combined_runs) AS highest_partnership, 
    SUM(CASE WHEN part.combined_runs >= 50 THEN 1 ELSE 0 END) AS fifty_plus_partnerships, 
    ROUND(100.0 * SUM(CASE WHEN part.combined_runs >= 50 THEN 1 ELSE 0 END) / COUNT(part.partnership_id), 2) AS success_rate_pct 
FROM partnerships part 
JOIN players p1 ON part.player1_id = p1.player_id 
JOIN players p2 ON part.player2_id = p2.player_id 
WHERE part.position_differ = 1 
GROUP BY part.player1_id, part.player2_id 
HAVING COUNT(part.partnership_id) >= 5 
ORDER BY avg_partnership_runs DESC;
"""
    },
    25: {
        "title": "Question 25: Time-Series Player Trajectory",
        "level": "Advanced",
        "description": "Track quarterly averages to determine career trajectory (Ascending, Declining, Stable).",
        "sql": """
SELECT 
    p.full_name, 
    bp.quarter, 
    ROUND(AVG(bp.runs_scored), 2) AS qtr_avg_runs, 
    ROUND(AVG(bp.strike_rate), 2) AS qtr_avg_sr, 
    COUNT(bp.performance_id) AS qtr_matches, 
    CASE 
        WHEN AVG(bp.runs_scored) > 45 THEN 'Career Ascending' 
        WHEN AVG(bp.runs_scored) < 25 THEN 'Career Declining' 
        ELSE 'Career Stable' 
    END AS career_phase 
FROM batting_performances bp 
JOIN players p ON bp.player_id = p.player_id 
GROUP BY p.player_id, bp.quarter 
HAVING COUNT(bp.performance_id) >= 3 
ORDER BY p.full_name, bp.quarter;
"""
    }
}

@st.cache_data(ttl=60, show_spinner=False)
def execute_sql_query(sql_query_str):
    """Execute raw SQL query and return pandas DataFrame."""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(sql_query_str, conn)
        return df, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

# Helper CRUD functions
@st.cache_data(ttl=60, show_spinner=False)
def get_all_players_df():
    conn = get_db_connection()
    df = pd.read_sql_query("""
    SELECT p.player_id, p.full_name, t.name AS team_name, p.role, p.batting_style, p.bowling_style, p.country, p.matches_played, p.total_runs, p.batting_avg, p.strike_rate, p.centuries, p.fifties, p.wickets_taken
    FROM players p
    LEFT JOIN teams t ON p.team_id = t.team_id;
    """, conn)
    conn.close()
    return df

def insert_player(full_name, team_id, role, batting_style, bowling_style, country, matches, runs, avg, sr, centuries, fifties, wickets):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO players (full_name, team_id, role, batting_style, bowling_style, country, matches_played, total_runs, batting_avg, strike_rate, centuries, fifties, wickets_taken)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (full_name, team_id, role, batting_style, bowling_style, country, matches, runs, avg, sr, centuries, fifties, wickets))
    conn.commit()
    conn.close()
    st.cache_data.clear()

def update_player(player_id, full_name, role, country, matches, runs, avg, sr, wickets):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE players 
    SET full_name = ?, role = ?, country = ?, matches_played = ?, total_runs = ?, batting_avg = ?, strike_rate = ?, wickets_taken = ?
    WHERE player_id = ?;
    """, (full_name, role, country, matches, runs, avg, sr, wickets, int(player_id)))
    conn.commit()
    conn.close()
    st.cache_data.clear()

def delete_player(player_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM players WHERE player_id = ?;", (int(player_id),))
    conn.commit()
    conn.close()
    st.cache_data.clear()


