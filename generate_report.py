import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level):
    p = doc.add_heading(text, level=level)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    for run in p.runs:
        run.font.name = 'Calibri'
        if level == 1:
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 81, 50) # Cricket Dark Green
        elif level == 2:
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(24, 119, 242) # Royal Blue Accent
        elif level == 3:
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(40, 40, 40)
    return p

def create_report():
    doc = Document()

    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base style adjustment
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 30, 30)

    # --- COVER / TITLE HEADER ---
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(20)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("CRICBUZZ LIVESTATS")
    run_title.font.size = Pt(28)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 81, 50)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(20)
    run_sub = sub_p.add_run("Real-Time Cricket Insights & SQL Analytics Platform\nComprehensive Technical & Business Project Report")
    run_sub.font.size = Pt(14)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(100, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --- PROJECT ACCESS LINKS SECTION (HIGHLIGHTED BOX) ---
    add_heading_styled(doc, "1. Project Access & Repository Links", level=1)

    table_links = doc.add_table(rows=2, cols=2)
    table_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_links.autofit = False

    widths = [Inches(2.2), Inches(4.3)]
    
    headers = ["Resource Type", "URL / Link Location"]
    hdr_cells = table_links.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].width = widths[i]
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(hdr_cells[i], "0F5132")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=150, right=150)

    link_data = [
        ("Web Application (Local)", "http://localhost:8501"),
        ("GitHub Repository", "https://github.com/pravatsahu05/Cricbuzz_livestats.git")
    ]

    for row_idx, (res, url) in enumerate(link_data):
        row_cells = table_links.rows[row_idx].cells
        # Fill row 1 data
        if row_idx == 0:
            pass # row 0 is header, so row_idx + 1 in standard loop, but let's add rows properly
    
    # Re-build table cleanly
    doc.paragraphs[-1]._element.getparent().remove(table_links._element) # remove old table

    table_links = doc.add_table(rows=3, cols=2)
    table_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table_links.rows[0].cells
    hdr_cells[0].width = Inches(2.2)
    hdr_cells[1].width = Inches(4.3)
    for i, title in enumerate(["Resource Name", "Access URL / Repository Link"]):
        p = hdr_cells[i].paragraphs[0]
        run = p.add_run(title)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(hdr_cells[i], "0F5132")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=150, right=150)

    row1 = table_links.rows[1].cells
    row1[0].width = Inches(2.2)
    row1[1].width = Inches(4.3)
    p1 = row1[0].paragraphs[0]
    r1 = p1.add_run("🚀 Live Web Application")
    r1.font.bold = True
    p2 = row1[1].paragraphs[0]
    r2 = p2.add_run("http://localhost:8501")
    r2.font.color.rgb = RGBColor(24, 119, 242)
    r2.font.underline = True
    set_cell_background(row1[0], "F8F9FA")
    set_cell_background(row1[1], "F8F9FA")
    set_cell_margins(row1[0], top=100, bottom=100, left=150, right=150)
    set_cell_margins(row1[1], top=100, bottom=100, left=150, right=150)

    row2 = table_links.rows[2].cells
    row2[0].width = Inches(2.2)
    row2[1].width = Inches(4.3)
    p3 = row2[0].paragraphs[0]
    r3 = p3.add_run("💻 GitHub Repository")
    r3.font.bold = True
    p4 = row2[1].paragraphs[0]
    r4 = p4.add_run("https://github.com/pravatsahu05/Cricbuzz_livestats.git")
    r4.font.color.rgb = RGBColor(24, 119, 242)
    r4.font.underline = True
    set_cell_background(row2[0], "FFFFFF")
    set_cell_background(row2[1], "FFFFFF")
    set_cell_margins(row2[0], top=100, bottom=100, left=150, right=150)
    set_cell_margins(row2[1], top=100, bottom=100, left=150, right=150)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- EXECUTIVE SUMMARY ---
    add_heading_styled(doc, "2. Executive Summary", level=1)
    p = doc.add_paragraph(
        "Cricbuzz LiveStats is an end-to-end interactive web application and relational data platform designed for cricket enthusiasts, sports analysts, and database learners. "
        "The application integrates real-time cricket data via the Cricbuzz RapidAPI with a robust local SQLite database (cricbuzz_analytics.db). "
        "Built on Streamlit with a custom Cricketing Turf Green design theme, Cricbuzz LiveStats offers detailed live match scorecards, series standings, player profile analytics, "
        "a full-fledged CRUD operations management center, and an interactive SQL Query Hub featuring 25 categorized practice queries."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    # --- PROBLEM STATEMENT & BUSINESS USE CASES ---
    add_heading_styled(doc, "3. Problem Statement & Business Use Cases", level=1)
    
    add_heading_styled(doc, "3.1 Problem Statement", level=2)
    doc.add_paragraph(
        "Modern sports analytics requires seamlessly merging fast live updates with historic analytical querying. Existing platforms suffer from several limitations:\n"
        "1. Fragmented Experience: Fans must navigate between live score websites and statistical databases.\n"
        "2. Lack of Practical SQL Learning: SQL learners lack sports datasets with rich multi-table relationships (teams, players, venues, performances).\n"
        "3. API Constraints: Public sports APIs often hit strict rate limits, causing dashboard breaking errors unless backed by clean fallback strategies."
    )

    add_heading_styled(doc, "3.2 Business Use Cases", level=2)
    use_cases = [
        ("Real-Time Fan Engagement Dashboard: ", "Delivers instantaneous match updates, ball-by-ball commentary, dynamic venue conditions, and win probabilities."),
        ("Sports Analytics & Performance Tracking: ", "Enables team strategists and analysts to evaluate player batting strike rates, bowling economies across formats (Test, ODI, T20I), and partnership dynamics."),
        ("Interactive Database Training: ", "Serves as an educational laboratory for executing complex SQL joins, aggregations, window functions (RANK, DENSE_RANK), and Subqueries on real cricket data."),
        ("Full-Lifecycle Data Management: ", "Provides administrators with CRUD control to adjust match logs, team compositions, and player bios effortlessly.")
    ]
    for bold_prefix, desc in use_cases:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        r = bp.add_run(bold_prefix)
        r.font.bold = True
        bp.add_run(desc)

    # --- TECH STACK & ARCHITECTURE ---
    add_heading_styled(doc, "4. Technology Stack & System Architecture", level=1)
    
    tech_table = doc.add_table(rows=6, cols=2)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hdr = tech_table.rows[0].cells
    t_hdr[0].width = Inches(2.0)
    t_hdr[1].width = Inches(4.5)
    for i, text in enumerate(["Layer / Component", "Technology & Libraries Used"]):
        p = t_hdr[i].paragraphs[0]
        run = p.add_run(text)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(t_hdr[i], "0F5132")
        set_cell_margins(t_hdr[i], top=100, bottom=100, left=150, right=150)

    stack_items = [
        ("Frontend UI Framework", "Streamlit (Python-based interactive web framework)"),
        ("UI Styling & Theme", "Vanilla CSS Custom Injector (Cricketing Turf Green Palette, Glassmorphism Cards, Dynamic Nav Bar)"),
        ("Database Engine", "SQLite3 (cricbuzz_analytics.db relational database)"),
        ("API Integration & HTTP", "RapidAPI Cricbuzz API, Python requests module, python-dotenv"),
        ("Data Wrangling & Processing", "Pandas, NumPy, Python Built-in json & datetime modules")
    ]
    for idx, (layer, tech) in enumerate(stack_items):
        cells = tech_table.rows[idx+1].cells
        cells[0].width = Inches(2.0)
        cells[1].width = Inches(4.5)
        p0 = cells[0].paragraphs[0]
        r0 = p0.add_run(layer)
        r0.font.bold = True
        p1 = cells[1].paragraphs[0]
        p1.add_run(tech)
        bg = "F8F9FA" if idx % 2 == 0 else "FFFFFF"
        set_cell_background(cells[0], bg)
        set_cell_background(cells[1], bg)
        set_cell_margins(cells[0], top=80, bottom=80, left=120, right=120)
        set_cell_margins(cells[1], top=80, bottom=80, left=120, right=120)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- DATABASE SCHEMA & RELATIONAL DESIGN ---
    add_heading_styled(doc, "5. Relational Database Schema (8 Core Tables)", level=1)
    doc.add_paragraph(
        "The project leverages an 8-table normalized database schema in SQLite to power analytics and CRUD operations. Below are the key entity tables:"
    )

    db_tables = [
        ("teams", "team_id (PK), team_name, short_name, country, flag_url", "Stores national and franchise team metadata."),
        ("players", "player_id (PK), player_name, role, batting_style, bowling_style, country, matches_played, runs_scored, wickets_taken", "Player bios and aggregated statistics across formats."),
        ("venues", "venue_id (PK), venue_name, city, country, capacity", "Stadium and ground venue details."),
        ("series", "series_id (PK), series_name, host_country, start_date, end_date, total_matches", "Tournament and bilateral series info."),
        ("matches", "match_id (PK), series_id (FK), venue_id (FK), team1_id (FK), team2_id (FK), winner_team_id (FK), match_date, format, result_margin", "Core match outcome records."),
        ("batting_performances", "performance_id (PK), match_id (FK), player_id (FK), runs, balls, fours, sixes, strike_rate, is_out", "Individual innings batting performance breakdown."),
        ("bowling_performances", "bowling_id (PK), match_id (FK), player_id (FK), overs, runs_conceded, wickets, economy, maidens", "Innings bowling figures per player."),
        ("partnerships", "partnership_id (PK), match_id (FK), player1_id (FK), player2_id (FK), runs, balls", "Wicket-by-wicket partnership runs.")
    ]

    schema_table = doc.add_table(rows=len(db_tables)+1, cols=3)
    schema_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_hdr = schema_table.rows[0].cells
    s_hdr[0].width = Inches(1.5)
    s_hdr[1].width = Inches(3.2)
    s_hdr[2].width = Inches(1.8)
    for i, title in enumerate(["Table Name", "Key Columns & Foreign Keys", "Description"]):
        p = s_hdr[i].paragraphs[0]
        run = p.add_run(title)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(s_hdr[i], "0F5132")
        set_cell_margins(s_hdr[i], top=100, bottom=100, left=100, right=100)

    for idx, (tname, cols, desc) in enumerate(db_tables):
        cells = schema_table.rows[idx+1].cells
        cells[0].width = Inches(1.5)
        cells[1].width = Inches(3.2)
        cells[2].width = Inches(1.8)

        p0 = cells[0].paragraphs[0]
        r0 = p0.add_run(tname)
        r0.font.bold = True

        p1 = cells[1].paragraphs[0]
        p1.add_run(cols)
        p1.runs[0].font.size = Pt(9.5)

        p2 = cells[2].paragraphs[0]
        p2.add_run(desc)
        p2.runs[0].font.size = Pt(9.5)

        bg = "F8F9FA" if idx % 2 == 0 else "FFFFFF"
        set_cell_background(cells[0], bg)
        set_cell_background(cells[1], bg)
        set_cell_background(cells[2], bg)
        set_cell_margins(cells[0], top=60, bottom=60, left=80, right=80)
        set_cell_margins(cells[1], top=60, bottom=60, left=80, right=80)
        set_cell_margins(cells[2], top=60, bottom=60, left=80, right=80)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- PAGE-WISE APPLICATION MODULES ---
    add_heading_styled(doc, "6. Application Pages & Module Breakdown", level=1)
    
    pages = [
        ("Home & Live Dashboard (app.py)", "Serves as the entry point showcasing live match feeds fetched real-time from Cricbuzz API. Displays current match status (Live, Upcoming, Completed), series category filters (International, League, Domestic), dynamic scoreboard highlights, and rapid API health status."),
        ("1. Live Scorecard (pages/1_📊_Live_Scorecard.py)", "Provides granular ball-by-ball commentaries, innings summaries, team lineups, toss decisions, venue stats, and partnership progressions for actively selected matches."),
        ("2. Series & Venues (pages/2_🏆_Series_&_Venues.py)", "Displays upcoming international and league series schedules, tournament formats, venue dimensions, pitch reports, and team point table standings."),
        ("3. Player Search (pages/3_👤_Player_Search.py)", "A comprehensive scouting module allowing search by player name or country. Provides detailed breakdowns of Test, ODI, and T20I career stats including batting averages, strike rates, 100s/50s, 5-wicket hauls, and player profiles."),
        ("4. SQL Query Hub (pages/4_💡_SQL_Query_Hub.py)", "An interactive analytics laboratory featuring 25 predefined SQL questions across Beginner, Intermediate, and Advanced tiers. Users can execute queries, inspect tabular results, view raw SQL syntax, export data to CSV, or test custom SQL queries live."),
        ("5. CRUD Operations (pages/5_🛠️_CRUD_Operations.py)", "A full administrative management portal enabling Create, Read, Update, and Delete operations across Players, Teams, and Matches tables with built-in validation and table browser.")
    ]

    for ptitle, pdesc in pages:
        add_heading_styled(doc, ptitle, level=2)
        p = doc.add_paragraph(pdesc)
        p.paragraph_format.space_after = Pt(6)

    # --- 25 SQL QUESTIONS & ANALYTICAL QUERIES ---
    add_heading_styled(doc, "7. SQL Analytics Hub: 25 Practice Queries", level=1)
    doc.add_paragraph(
        "Below is the complete catalogue of the 25 analytical SQL queries implemented in the application, categorized by complexity level:"
    )

    sql_queries = [
        # Beginner (1-8)
        (1, "Beginner", "List All Players with Roles", "SELECT player_id, player_name, role, country FROM players ORDER BY player_name ASC;"),
        (2, "Beginner", "Find All Matches Played at a Specific Venue", "SELECT match_id, match_date, format FROM matches WHERE venue_id = 1;"),
        (3, "Beginner", "Count Total Players Per Country", "SELECT country, COUNT(*) AS total_players FROM players GROUP BY country ORDER BY total_players DESC;"),
        (4, "Beginner", "List All Left-Handed Batsmen", "SELECT player_name, country, role FROM players WHERE batting_style LIKE '%Left%' ORDER BY country;"),
        (5, "Beginner", "Get Top 5 Highest Run-Scorers Overall", "SELECT player_name, country, runs_scored FROM players ORDER BY runs_scored DESC LIMIT 5;"),
        (6, "Beginner", "Find Matches Won by India", "SELECT m.match_id, m.match_date, m.format, t.team_name FROM matches m JOIN teams t ON m.winner_team_id = t.team_id WHERE t.short_name = 'IND';"),
        (7, "Beginner", "List Venues with Capacity Greater Than 50,000", "SELECT venue_name, city, country, capacity FROM venues WHERE capacity > 50000 ORDER BY capacity DESC;"),
        (8, "Beginner", "Show All All-Rounders in the Database", "SELECT player_name, country, matches_played, runs_scored, wickets_taken FROM players WHERE role LIKE '%All-Rounder%';"),

        # Intermediate (9-16)
        (9, "Intermediate", "Calculate Average Runs Scored Per Match", "SELECT m.match_id, AVG(b.runs) AS avg_runs FROM batting_performances b JOIN matches m ON b.match_id = m.match_id GROUP BY m.match_id;"),
        (10, "Intermediate", "Top Wicket-Takers by Bowling Economy", "SELECT p.player_name, p.country, AVG(bw.economy) AS avg_economy, SUM(bw.wickets) AS total_wickets FROM bowling_performances bw JOIN players p ON bw.player_id = p.player_id GROUP BY p.player_id HAVING SUM(bw.wickets) >= 5 ORDER BY avg_economy ASC;"),
        (11, "Intermediate", "Highest Individual Innings Scores (> 100 Runs)", "SELECT p.player_name, b.runs, b.balls, b.four, b.six, m.match_date FROM batting_performances b JOIN players p ON b.player_id = p.player_id JOIN matches m ON b.match_id = m.match_id WHERE b.runs >= 100 ORDER BY b.runs DESC;"),
        (12, "Intermediate", "Team Head-to-Head Win Counts", "SELECT t1.team_name AS team1, t2.team_name AS team2, COUNT(m.match_id) AS total_matches, SUM(CASE WHEN m.winner_team_id = t1.team_id THEN 1 ELSE 0 END) AS team1_wins FROM matches m JOIN teams t1 ON m.team1_id = t1.team_id JOIN teams t2 ON m.team2_id = t2.team_id GROUP BY t1.team_id, t2.team_id;"),
        (13, "Intermediate", "Find Players with High Strike Rates (> 140 in T20s)", "SELECT p.player_name, p.country, b.runs, b.balls, (CAST(b.runs AS FLOAT)/b.balls)*100 AS strike_rate FROM batting_performances b JOIN players p ON b.player_id = p.player_id JOIN matches m ON b.match_id = m.match_id WHERE m.format = 'T20' AND b.balls >= 15 AND (CAST(b.runs AS FLOAT)/b.balls)*100 > 140;"),
        (14, "Intermediate", "Partnerships Greater Than 100 Runs", "SELECT p1.player_name AS batsman1, p2.player_name AS batsman2, pr.runs, pr.balls FROM partnerships pr JOIN players p1 ON pr.player1_id = p1.player_id JOIN players p2 ON pr.player2_id = p2.player_id WHERE pr.runs >= 100 ORDER BY pr.runs DESC;"),
        (15, "Intermediate", "Venues Hosting the Most Matches", "SELECT v.venue_name, v.city, COUNT(m.match_id) AS matches_hosted FROM venues v LEFT JOIN matches m ON v.venue_id = m.venue_id GROUP BY v.venue_id ORDER BY matches_hosted DESC;"),
        (16, "Intermediate", "Bowlers with 5-Wicket Hauls in a Match", "SELECT p.player_name, bw.wickets, bw.runs_conceded, bw.overs, m.match_date FROM bowling_performances bw JOIN players p ON bw.player_id = p.player_id JOIN matches m ON bw.match_id = m.match_id WHERE bw.wickets >= 5 ORDER BY bw.wickets DESC;"),

        # Advanced (17-25)
        (17, "Advanced", "Player Batting Average Across All Matches", "SELECT p.player_name, p.country, SUM(b.runs) AS total_runs, SUM(CASE WHEN b.is_out = 1 THEN 1 ELSE 0 END) AS times_out, CASE WHEN SUM(CASE WHEN b.is_out = 1 THEN 1 ELSE 0 END) = 0 THEN SUM(b.runs) ELSE ROUND(CAST(SUM(b.runs) AS FLOAT) / SUM(CASE WHEN b.is_out = 1 THEN 1 ELSE 0 END), 2) END AS batting_avg FROM batting_performances b JOIN players p ON b.player_id = p.player_id GROUP BY p.player_id ORDER BY batting_avg DESC;"),
        (18, "Advanced", "Rank Players by Runs within Country (Window Function)", "SELECT player_name, country, runs_scored, RANK() OVER (PARTITION BY country ORDER BY runs_scored DESC) AS country_rank FROM players;"),
        (19, "Advanced", "Cumulative Runs Scored by Player Over Time", "SELECT p.player_name, m.match_date, b.runs, SUM(b.runs) OVER (PARTITION BY p.player_id ORDER BY m.match_date ASC) AS cumulative_runs FROM batting_performances b JOIN players p ON b.player_id = p.player_id JOIN matches m ON b.match_id = m.match_id;"),
        (20, "Advanced", "Players Who Have Scored Centuries & Taken 3+ Wickets in Same Series", "SELECT DISTINCT p.player_name FROM players p WHERE p.player_id IN (SELECT player_id FROM batting_performances WHERE runs >= 100) AND p.player_id IN (SELECT player_id FROM bowling_performances WHERE wickets >= 3);"),
        (21, "Advanced", "Team Win Percentage Calculation", "SELECT t.team_name, COUNT(m.match_id) AS total_matches, SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS wins, ROUND(CAST(SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS FLOAT) / COUNT(m.match_id) * 100, 2) AS win_percentage FROM teams t JOIN matches m ON t.team_id = m.team1_id OR t.team_id = m.team2_id GROUP BY t.team_id HAVING total_matches >= 3 ORDER BY win_percentage DESC;"),
        (22, "Advanced", "Boundary Run Contribution Percentage Per Player", "SELECT p.player_name, SUM(b.runs) AS total_runs, SUM(b.four * 4 + b.six * 6) AS boundary_runs, ROUND(CAST(SUM(b.four * 4 + b.six * 6) AS FLOAT) / NULLIF(SUM(b.runs), 0) * 100, 2) AS boundary_pct FROM batting_performances b JOIN players p ON b.player_id = p.player_id GROUP BY p.player_id HAVING total_runs > 50 ORDER BY boundary_pct DESC;"),
        (23, "Advanced", "Most Economical Bowlers in Death Overs (High Run Matches)", "SELECT p.player_name, ROUND(AVG(bw.economy), 2) AS avg_econ FROM bowling_performances bw JOIN players p ON bw.player_id = p.player_id WHERE bw.match_id IN (SELECT match_id FROM batting_performances GROUP BY match_id HAVING SUM(runs) > 300) GROUP BY p.player_id ORDER BY avg_econ ASC;"),
        (24, "Advanced", "Identify Dynamic All-Rounder Performance Index", "SELECT p.player_name, p.country, (SUM(b.runs) * 0.5 + SUM(bw.wickets) * 20) AS performance_index FROM players p LEFT JOIN batting_performances b ON p.player_id = b.player_id LEFT JOIN bowling_performances bw ON p.player_id = bw.player_id GROUP BY p.player_id ORDER BY performance_index DESC LIMIT 10;"),
        (25, "Advanced", "Venues with Highest Average 1st Innings Scores", "SELECT v.venue_name, v.city, ROUND(AVG(b.runs), 2) AS avg_match_runs FROM venues v JOIN matches m ON v.venue_id = m.venue_id JOIN batting_performances b ON m.match_id = b.match_id GROUP BY v.venue_id ORDER BY avg_match_runs DESC;")
    ]

    sql_table = doc.add_table(rows=len(sql_queries)+1, cols=4)
    sql_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sq_hdr = sql_table.rows[0].cells
    sq_hdr[0].width = Inches(0.6)
    sq_hdr[1].width = Inches(1.1)
    sq_hdr[2].width = Inches(1.8)
    sq_hdr[3].width = Inches(3.0)
    for i, title in enumerate(["#", "Tier", "Question Summary", "SQL Query Syntax"]):
        p = sq_hdr[i].paragraphs[0]
        run = p.add_run(title)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(sq_hdr[i], "0F5132")
        set_cell_margins(sq_hdr[i], top=80, bottom=80, left=60, right=60)

    for idx, (num, tier, qtitle, query) in enumerate(sql_queries):
        cells = sql_table.rows[idx+1].cells
        cells[0].width = Inches(0.6)
        cells[1].width = Inches(1.1)
        cells[2].width = Inches(1.8)
        cells[3].width = Inches(3.0)

        p0 = cells[0].paragraphs[0]
        p0.add_run(str(num))

        p1 = cells[1].paragraphs[0]
        r1 = p1.add_run(tier)
        if tier == "Beginner":
            r1.font.color.rgb = RGBColor(40, 167, 69)
        elif tier == "Intermediate":
            r1.font.color.rgb = RGBColor(24, 119, 242)
        else:
            r1.font.color.rgb = RGBColor(220, 53, 69)
        r1.font.bold = True

        p2 = cells[2].paragraphs[0]
        r2 = p2.add_run(qtitle)
        r2.font.bold = True
        r2.font.size = Pt(9.5)

        p3 = cells[3].paragraphs[0]
        r3 = p3.add_run(query)
        r3.font.name = 'Consolas'
        r3.font.size = Pt(8.5)

        bg = "F8F9FA" if idx % 2 == 0 else "FFFFFF"
        for c in cells:
            set_cell_background(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=60, right=60)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- API KEY CONFIGURATION & SETUP GUIDE ---
    add_heading_styled(doc, "8. Configuration & API Setup Guide", level=1)
    
    add_heading_styled(doc, "8.1 Environment (.env) Setup", level=2)
    doc.add_paragraph(
        "The application reads configuration settings securely from a local .env file. "
        "To configure or update the RapidAPI key for Cricbuzz live stats, follow these steps:"
    )

    env_instructions = [
        ("Step 1: Open Environment Configuration", "Navigate to the project root directory and locate or create the file named '.env'."),
        ("Step 2: Add RapidAPI Key Credentials", "Set the RAPIDAPI_KEY variable inside '.env':\n   RAPIDAPI_KEY=519fc6c7ccmsh390678d06370cd9p1002b7jsn3b387a389ffa\n   RAPIDAPI_HOST=cricbuzz-cricket-v1.p.rapidapi.com"),
        ("Step 3: Verification", "Restart the Streamlit application using 'streamlit run app.py'. The home dashboard will automatically fetch live scorecards using the updated key.")
    ]

    for title, desc in env_instructions:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(4)
        r = bp.add_run(title + ": ")
        r.font.bold = True
        bp.add_run(desc)

    add_heading_styled(doc, "8.2 Automatic Fallback Strategy", level=2)
    doc.add_paragraph(
        "To guarantee high availability and uninterrupted user experience during API rate limiting or connectivity outages, "
        "the application features an intelligent fallback mechanism. If the live API call fails or returns non-200 responses, "
        "the system seamlessly switches to local mock cricket datasets and cached SQLite records without crashing the Streamlit UI."
    )

    # --- CONCLUSION ---
    add_heading_styled(doc, "9. Conclusion & Future Enhancements", level=1)
    doc.add_paragraph(
        "Cricbuzz LiveStats successfully bridges real-time live match statistics with in-depth SQL analytical querying. "
        "Future roadmaps for the application include adding ML-powered win prediction models, ball-by-ball heatmaps, and multi-user authentication for saved query bookmarks."
    )

    # Save document
    output_path = r"c:\Users\Pravat\OneDrive\Desktop\Coding Programs\Cricbuzz_livestats\Cricbuzz_LiveStats_Project_Report.docx"
    doc.save(output_path)
    print(f"Report successfully saved to: {output_path}")

if __name__ == "__main__":
    create_report()
