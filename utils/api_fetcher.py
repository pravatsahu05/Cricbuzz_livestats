import requests
import os
import sqlite3
import pandas as pd
import streamlit as st

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cricbuzz_analytics.db")
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

def get_api_key():
    """
    Retrieve active RapidAPI Key.
    Checks in priority order:
    1. st.session_state["RAPIDAPI_KEY"] (UI dynamic update)
    2. os.getenv("RAPIDAPI_KEY") (Environment variable / .env)
    3. st.secrets["RAPIDAPI_KEY"] (Streamlit Cloud Secrets deployment)
    """
    if st.session_state.get("RAPIDAPI_KEY"):
        return st.session_state["RAPIDAPI_KEY"]

    env_key = os.getenv("RAPIDAPI_KEY")
    if env_key:
        return env_key

    try:
        if hasattr(st, "secrets") and "RAPIDAPI_KEY" in st.secrets:
            return st.secrets["RAPIDAPI_KEY"]
    except Exception:
        pass

    return None

def get_headers():
    api_key = get_api_key()
    if not api_key:
        return None
    return {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

def check_api_quota():
    """Check remaining API requests and hard limits directly from RapidAPI HTTP response headers."""
    headers = get_headers()
    if not headers:
        return {"status": "No API Key Set", "remaining": None, "limit": None}

    try:
        res = requests.get(f"https://{RAPIDAPI_HOST}/matches/v1/live", headers=headers, timeout=5)
        if res.status_code == 200:
            rem = res.headers.get("X-RateLimit-Requests-Remaining") or res.headers.get("X-RateLimit-rapid-free-plans-hard-limit-Remaining")
            lim = res.headers.get("X-RateLimit-Requests-Limit") or res.headers.get("X-RateLimit-rapid-free-plans-hard-limit-Limit")
            hard_rem = res.headers.get("X-RateLimit-rapid-free-plans-hard-limit-Remaining")
            return {
                "status": "Active",
                "remaining": rem,
                "limit": lim,
                "hard_remaining": hard_rem,
                "http_status": 200
            }
        elif res.status_code == 429:
            return {"status": "Quota Exceeded (429)", "remaining": 0, "limit": None}
        elif res.status_code in (401, 403):
            return {"status": "Invalid API Key (401/403)", "remaining": 0, "limit": None}
        else:
            return {"status": f"HTTP {res.status_code}", "remaining": None, "limit": None}
    except Exception as e:
        return {"status": f"Error: {str(e)}", "remaining": None, "limit": None}



@st.cache_data(ttl=60, show_spinner=False)
def fetch_live_matches():
    """Fetch live and recent match scorecards directly from RapidAPI Cricbuzz API with fallback."""
    headers = get_headers()
    if not headers:
        return get_fallback_matches()

    try:
        # Check live matches first
        url_live = f"https://{RAPIDAPI_HOST}/matches/v1/live"
        response = requests.get(url_live, headers=headers, timeout=6)
        
        # If live matches endpoint returns 429 or fails, try recent matches
        if response.status_code != 200:
            url_recent = f"https://{RAPIDAPI_HOST}/matches/v1/recent"
            response = requests.get(url_recent, headers=headers, timeout=6)

        if response.status_code == 200:
            data = response.json()
            matches_list = []
            for match_type in data.get("typeMatches", []):
                for series in match_type.get("seriesMatches", []):
                    wrapper = series.get("seriesAdWrapper", {})
                    series_name = wrapper.get("seriesName", "Cricbuzz Series")
                    for match in wrapper.get("matches", []):
                        m_info = match.get("matchInfo", {})
                        m_score = match.get("matchScore", {})

                        t1 = m_info.get("team1", {})
                        t2 = m_info.get("team2", {})
                        t1_s = m_score.get("team1Score", {}).get("inngs1", {})
                        t2_s = m_score.get("team2Score", {}).get("inngs1", {})

                        match_id = m_info.get("matchId")
                        match_obj = {
                            "id": match_id,
                            "series": series_name,
                            "match_desc": m_info.get("matchDesc", "Live Match"),
                            "format": m_info.get("matchFormat", "T20"),
                            "team1": t1.get("teamName", "Team A"),
                            "team1_id": t1.get("teamId"),
                            "team1_score": t1_s.get("runs", 0),
                            "team1_wickets": t1_s.get("wickets", 0),
                            "team1_overs": t1_s.get("overs", 0.0),
                            "team2": t2.get("teamName", "Team B"),
                            "team2_id": t2.get("teamId"),
                            "team2_score": t2_s.get("runs", 0),
                            "team2_wickets": t2_s.get("wickets", 0),
                            "team2_overs": t2_s.get("overs", 0.0),
                            "status": m_info.get("status", "In Progress"),
                            "state": m_info.get("state", "In Progress"),
                            "venue": m_info.get("venueInfo", {}).get("ground", "International Stadium"),
                            "city": m_info.get("venueInfo", {}).get("city", "Host City"),
                            "source": "Cricbuzz REST API (Live)"
                        }

                        # Parse any batters/bowler in matchScore directly if available
                        batsmen = []
                        if "batsman1" in m_score:
                            b1 = m_score["batsman1"]
                            batsmen.append({"name": b1.get("name", "Batter 1"), "runs": b1.get("runs", 0), "balls": b1.get("balls", 0), "fours": b1.get("fours", 0), "sixes": b1.get("sixes", 0), "sr": float(b1.get("strikeRate", 0))})
                        if "batsman2" in m_score:
                            b2 = m_score["batsman2"]
                            batsmen.append({"name": b2.get("name", "Batter 2"), "runs": b2.get("runs", 0), "balls": b2.get("balls", 0), "fours": b2.get("fours", 0), "sixes": b2.get("sixes", 0), "sr": float(b2.get("strikeRate", 0))})

                        if batsmen:
                            match_obj["batsmen"] = batsmen
                        
                        if "bowler1" in m_score:
                            bw = m_score["bowler1"]
                            match_obj["bowler"] = {"name": bw.get("name", "Bowler 1"), "overs": float(bw.get("overs", 0)), "runs": bw.get("runs", 0), "wickets": bw.get("wickets", 0), "economy": float(bw.get("economy", 0))}

                        matches_list.append(match_obj)

            if matches_list:
                return matches_list

    except Exception:
        pass

    return get_fallback_matches()

@st.cache_data(ttl=120, show_spinner=False)
def fetch_format_rankings(format_type="test"):
    """Fetch ICC rankings for batsmen, bowlers, allrounders directly from Cricbuzz API for test, odi, or t20."""
    headers = get_headers()
    fmt = format_type.lower().strip()
    if fmt not in ["test", "odi", "t20"]:
        fmt = "test"

    results = {"batsmen": [], "bowlers": [], "allrounders": [], "format": fmt.upper(), "source": "Cricbuzz REST API"}

    if not headers:
        return get_fallback_format_rankings(fmt)

    categories = ["batsmen", "bowlers", "allrounders"]
    try:
        for cat in categories:
            url = f"https://{RAPIDAPI_HOST}/stats/v1/rankings/{cat}?formatType={fmt}"
            res = requests.get(url, headers=headers, timeout=6)
            if res.status_code == 200:
                data = res.json()
                raw_list = data.get("rank", [])
                parsed_list = []
                for item in raw_list:
                    parsed_list.append({
                        "rank": int(item.get("rank", 0)),
                        "name": item.get("name", "Unknown Player"),
                        "country": item.get("country", "International"),
                        "rating": int(item.get("rating", 0)),
                        "trend": item.get("trend", "Flat")
                    })
                results[cat] = parsed_list

        if any(results[cat] for cat in categories):
            return results
    except Exception:
        pass

    return get_fallback_format_rankings(fmt)

def sync_api_to_database(db_path=DB_PATH):
    """Fetch live and recent match & player data from Cricbuzz API and sync into SQLite DB."""
    headers = get_headers()
    if not headers:
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        endpoints = ["matches/v1/live", "matches/v1/recent"]
        teams_map = {}
        venues_map = {}
        series_map = {}

        for ep in endpoints:
            r = requests.get(f"https://{RAPIDAPI_HOST}/{ep}", headers=headers, timeout=6)
            if r.status_code == 200:
                data = r.json()
                for match_type in data.get("typeMatches", []):
                    m_type_name = match_type.get("matchType", "International")
                    for series in match_type.get("seriesMatches", []):
                        wrapper = series.get("seriesAdWrapper", {})
                        s_name = wrapper.get("seriesName", "Cricbuzz Championship")
                        series_map[s_name] = (m_type_name, "2026-08-01")

                        for match in wrapper.get("matches", []):
                            info = match.get("matchInfo", {})
                            t1 = info.get("team1", {})
                            t2 = info.get("team2", {})
                            if t1.get("teamName"):
                                teams_map[t1["teamName"]] = t1.get("teamName")
                            if t2.get("teamName"):
                                teams_map[t2["teamName"]] = t2.get("teamName")

                            v_info = info.get("venueInfo", {})
                            if v_info.get("ground"):
                                venues_map[v_info["ground"]] = (v_info.get("city", "Host City"), "India", 55000)

        for t_name in teams_map.keys():
            cursor.execute("""
            INSERT OR IGNORE INTO teams (name, country, matches_played, wins, losses)
            VALUES (?, ?, ?, ?, ?);
            """, (t_name, "India" if "India" in t_name or "Punjab" in t_name else "International", 20, 12, 8))

        for v_name, (city, country, cap) in venues_map.items():
            cursor.execute("""
            INSERT OR IGNORE INTO venues (name, city, country, capacity)
            VALUES (?, ?, ?, ?);
            """, (v_name, city, country, cap))

        for s_name, (m_type, s_date) in series_map.items():
            cursor.execute("""
            INSERT OR IGNORE INTO series (name, host_country, match_type, start_date, total_matches)
            VALUES (?, ?, ?, ?, ?);
            """, (s_name, "India", m_type, s_date, 10))

        conn.commit()
        conn.close()
        return True
    except Exception:
        return False

def get_fallback_format_rankings(format_type):
    fmt = format_type.upper()
    if fmt == "TEST":
        return {
            "format": "TEST",
            "source": "Simulation Engine (Fallback)",
            "batsmen": [
                {"rank": 1, "name": "Harry Brook", "country": "England", "rating": 856, "trend": "Flat"},
                {"rank": 2, "name": "Steven Smith", "country": "Australia", "rating": 840, "trend": "Up"},
                {"rank": 3, "name": "Joe Root", "country": "England", "rating": 820, "trend": "Down"},
                {"rank": 4, "name": "Yashasvi Jaiswal", "country": "India", "rating": 792, "trend": "Up"},
                {"rank": 5, "name": "Virat Kohli", "country": "India", "rating": 775, "trend": "Flat"}
            ],
            "bowlers": [
                {"rank": 1, "name": "Mitchell Starc", "country": "Australia", "rating": 865, "trend": "Up"},
                {"rank": 2, "name": "Jasprit Bumrah", "country": "India", "rating": 852, "trend": "Flat"},
                {"rank": 3, "name": "Pat Cummins", "country": "Australia", "rating": 830, "trend": "Down"},
                {"rank": 4, "name": "Kagiso Rabada", "country": "South Africa", "rating": 815, "trend": "Up"},
                {"rank": 5, "name": "Ravichandran Ashwin", "country": "India", "rating": 802, "trend": "Flat"}
            ],
            "allrounders": [
                {"rank": 1, "name": "Ravindra Jadeja", "country": "India", "rating": 450, "trend": "Flat"},
                {"rank": 2, "name": "Ben Stokes", "country": "England", "rating": 390, "trend": "Up"},
                {"rank": 3, "name": "Axar Patel", "country": "India", "rating": 320, "trend": "Flat"}
            ]
        }
    elif fmt == "ODI":
        return {
            "format": "ODI",
            "source": "Simulation Engine (Fallback)",
            "batsmen": [
                {"rank": 1, "name": "Shubman Gill", "country": "India", "rating": 826, "trend": "Flat"},
                {"rank": 2, "name": "Babar Azam", "country": "Pakistan", "rating": 810, "trend": "Down"},
                {"rank": 3, "name": "Rohit Sharma", "country": "India", "rating": 785, "trend": "Up"},
                {"rank": 4, "name": "Virat Kohli", "country": "India", "rating": 772, "trend": "Up"},
                {"rank": 5, "name": "Daryl Mitchell", "country": "New Zealand", "rating": 750, "trend": "Flat"}
            ],
            "bowlers": [
                {"rank": 1, "name": "Rashid Khan", "country": "Afghanistan", "rating": 720, "trend": "Up"},
                {"rank": 2, "name": "Kuldeep Yadav", "country": "India", "rating": 705, "trend": "Flat"},
                {"rank": 3, "name": "Shaheen Afridi", "country": "Pakistan", "rating": 690, "trend": "Down"},
                {"rank": 4, "name": "Jasprit Bumrah", "country": "India", "rating": 685, "trend": "Up"}
            ],
            "allrounders": [
                {"rank": 1, "name": "Azmatullah Omarzai", "country": "Afghanistan", "rating": 340, "trend": "Up"},
                {"rank": 2, "name": "Shakib Al Hasan", "country": "Bangladesh", "rating": 310, "trend": "Down"},
                {"rank": 3, "name": "Ravindra Jadeja", "country": "India", "rating": 295, "trend": "Flat"}
            ]
        }
    else: # T20
        return {
            "format": "T20",
            "source": "Simulation Engine (Fallback)",
            "batsmen": [
                {"rank": 1, "name": "Ishan Kishan", "country": "India", "rating": 845, "trend": "Up"},
                {"rank": 2, "name": "Suryakumar Yadav", "country": "India", "rating": 832, "trend": "Flat"},
                {"rank": 3, "name": "Phil Salt", "country": "England", "rating": 805, "trend": "Up"},
                {"rank": 4, "name": "Travis Head", "country": "Australia", "rating": 790, "trend": "Up"},
                {"rank": 5, "name": "Yashasvi Jaiswal", "country": "India", "rating": 770, "trend": "Flat"}
            ],
            "bowlers": [
                {"rank": 1, "name": "Rashid Khan", "country": "Afghanistan", "rating": 740, "trend": "Flat"},
                {"rank": 2, "name": "Adil Rashid", "country": "England", "rating": 715, "trend": "Up"},
                {"rank": 3, "name": "Arshdeep Singh", "country": "India", "rating": 695, "trend": "Up"},
                {"rank": 4, "name": "Anrich Nortje", "country": "South Africa", "rating": 680, "trend": "Flat"}
            ],
            "allrounders": [
                {"rank": 1, "name": "Sikandar Raza", "country": "Zimbabwe", "rating": 320, "trend": "Up"},
                {"rank": 2, "name": "Hardik Pandya", "country": "India", "rating": 305, "trend": "Flat"},
                {"rank": 3, "name": "Marcus Stoinis", "country": "Australia", "rating": 290, "trend": "Down"}
            ]
        }

def get_fallback_matches():
    """Realistic fallback live match dataset."""
    return [
        {
            "id": 101,
            "series": "India vs Australia T20I Series 2026",
            "match_desc": "3rd T20I (N)",
            "team1": "India",
            "team1_score": 198,
            "team1_wickets": 4,
            "team1_overs": 20.0,
            "team2": "Australia",
            "team2_score": 164,
            "team2_wickets": 7,
            "team2_overs": 17.4,
            "status": "Australia need 35 runs in 14 balls",
            "venue": "Narendra Modi Stadium",
            "city": "Ahmedabad",
            "source": "Live Simulation Engine (Free Source)",
            "batsmen": [
                {"name": "Travis Head", "runs": 68, "balls": 38, "fours": 7, "sixes": 4, "sr": 178.95},
                {"name": "Glenn Maxwell", "runs": 34, "balls": 19, "fours": 2, "sixes": 3, "sr": 178.95}
            ],
            "bowler": {"name": "Jasprit Bumrah", "overs": 3.4, "runs": 22, "wickets": 3, "economy": 6.0}
        },
        {
            "id": 102,
            "series": "England vs South Africa Test Series 2026",
            "match_desc": "1st Test - Day 3",
            "team1": "England",
            "team1_score": 384,
            "team1_wickets": 10,
            "team1_overs": 94.2,
            "team2": "South Africa",
            "team2_score": 210,
            "team2_wickets": 5,
            "team2_overs": 68.0,
            "status": "South Africa trail by 174 runs",
            "venue": "Lord's Cricket Ground",
            "city": "London",
            "source": "Live Simulation Engine (Free Source)",
            "batsmen": [
                {"name": "Aiden Markram", "runs": 82, "balls": 140, "fours": 10, "sixes": 1, "sr": 58.57},
                {"name": "Heinrich Klaasen", "runs": 45, "balls": 62, "fours": 6, "sixes": 1, "sr": 72.58}
            ],
            "bowler": {"name": "Ben Stokes", "overs": 14.0, "runs": 42, "wickets": 2, "economy": 3.0}
        },
        {
            "id": 103,
            "series": "Asia Cup ODI Trophy 2026",
            "match_desc": "Super 4s - Match 5",
            "team1": "Pakistan",
            "team1_score": 278,
            "team1_wickets": 8,
            "team1_overs": 50.0,
            "team2": "Sri Lanka",
            "team2_score": 242,
            "team2_wickets": 9,
            "team2_overs": 47.1,
            "status": "Sri Lanka need 37 runs in 17 balls",
            "venue": "R. Premadasa Stadium",
            "city": "Colombo",
            "source": "Live Simulation Engine (Free Source)",
            "batsmen": [
                {"name": "Charith Asalanka", "runs": 58, "balls": 51, "fours": 4, "sixes": 2, "sr": 113.72},
                {"name": "Dunith Wellalage", "runs": 22, "balls": 18, "fours": 2, "sixes": 0, "sr": 122.22}
            ],
            "bowler": {"name": "Shaheen Afridi", "overs": 9.1, "runs": 48, "wickets": 4, "economy": 5.23}
        }
    ]
