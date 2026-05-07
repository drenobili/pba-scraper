import requests
from bs4 import BeautifulSoup
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# ------------------- MySQL CONFIG -------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

# ------------------- HELPERS -------------------
def parse_shot_value(value):
    """Convert '5-12' or '5/12' into (made, attempted) as integers."""
    if not value:
        return 0, 0
    value = value.replace("-", "/")
    if "/" not in value:
        return 0, 0
    try:
        made, att = value.split("/")
        return int(made), int(att)
    except:
        return 0, 0

def compute_pct(made, attempted):
    if attempted == 0:
        return 0.0
    return round((made / attempted) * 100, 1)

def safe_int(v):
    try:
        return int(v)
    except:
        return 0

def parse_minutes(text):
    """Convert '21:44' into minutes as a float (21 + 44/60)."""
    if ":" not in text:
        return 0
    try:
        m, s = text.split(":")
        return int(m) + int(s) / 60
    except:
        return 0

# ------------------- SCRAPER -------------------
def is_boxscore_table(table):
    header_text = " ".join(th.get_text(strip=True).upper() for th in table.find_all("th"))
    return "PLAYER" in header_text and "PTS" in header_text

def scrape_box_score(url):
    """Scrape player stats from a single game page. Returns a list of stat dicts."""
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    all_stats = []
    team_names = [t.get_text(strip=True) for t in soup.select(".team_name span")]

    tables = soup.find_all("table")
    tables = [t for t in tables if is_boxscore_table(t)]

    for idx, table in enumerate(tables):
        team_name = team_names[idx] if idx < len(team_names) else "Unknown"
        headers = [th.get_text(strip=True).upper() for th in table.find_all("th")]

        for tr in table.find_all("tr"):
            cells = tr.find_all("td")
            if not cells:
                continue

            row = [c.get_text(strip=True) for c in cells]
            stat = {"team": team_name}

            for h, v in zip(headers, row):
                stat[h] = v

            player_name = stat.get("PLAYER", "")
            if player_name.upper() in ("TEAM TOTALS", "TEAM / COACH", ""):
                continue

            all_stats.append(stat)

    return all_stats

# ------------------- DATABASE -------------------
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def get_or_create_player(cursor, name, team):
    cursor.execute(
        "SELECT player_id FROM players WHERE name=%s AND team=%s",
        (name, team)
    )
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute(
        "INSERT INTO players (name, team) VALUES (%s, %s)",
        (name, team)
    )
    return cursor.lastrowid

def get_existing_stats(cursor, player_id):
    cursor.execute("""
        SELECT GP, pts,
               fg_made, fg_attempted,
               two_pt_made, two_pt_attempted,
               three_pt_made, three_pt_attempted,
               four_pt_made, four_pt_attempted,
               ft_made, ft_attempted,
               minutes, off, def, reb,
               ast, to_stat, stl, blk, pf,
               plus_minus
        FROM stats WHERE player_id = %s
    """, (player_id,))
    return cursor.fetchone()

def create_empty_stats(cursor, player_id):
    cursor.execute("INSERT INTO stats (player_id) VALUES (%s)", (player_id,))

def update_stats(cursor, player_id, stat):
    mins  = parse_minutes(stat.get("MINS", "0:00"))
    pts   = safe_int(stat.get("PTS", 0))

    fg_m,   fg_a   = parse_shot_value(stat.get("FG", "0/0"))
    two_m,  two_a  = parse_shot_value(stat.get("2P", "0/0"))
    thr_m,  thr_a  = parse_shot_value(stat.get("3P", "0/0"))
    four_m, four_a = parse_shot_value(stat.get("4P", "0/0"))
    ft_m,   ft_a   = parse_shot_value(stat.get("FT", "0/0"))

    off       = safe_int(stat.get("OFF", 0))
    deff      = safe_int(stat.get("DEF", 0))
    reb       = off + deff
    ast       = safe_int(stat.get("AST", 0))
    to_stat   = safe_int(stat.get("TO", 0))
    stl       = safe_int(stat.get("STL", 0))
    blk       = safe_int(stat.get("BLK", 0))
    pf        = safe_int(stat.get("PF", 0))
    plus_minus = safe_int(stat.get("+/-", 0))

    row = get_existing_stats(cursor, player_id)
    if not row:
        create_empty_stats(cursor, player_id)
        row = get_existing_stats(cursor, player_id)

    (
        old_gp, old_pts,
        old_fgm, old_fga,
        old_2pm, old_2pa,
        old_3pm, old_3pa,
        old_4pm, old_4pa,
        old_ftm, old_fta,
        old_min, old_off, old_def, old_reb,
        old_ast, old_to, old_stl, old_blk, old_pf,
        old_pm
    ) = row

    GP = old_gp + 1

    new_2pm  = old_2pm  + two_m
    new_2pa  = old_2pa  + two_a
    new_3pm  = old_3pm  + thr_m
    new_3pa  = old_3pa  + thr_a
    new_4pm  = old_4pm  + four_m
    new_4pa  = old_4pa  + four_a
    new_ftm  = old_ftm  + ft_m
    new_fta  = old_fta  + ft_a

    # Recompute FG totals from shot breakdowns (more reliable than the FG column)
    new_fgm = new_2pm + new_3pm + new_4pm
    new_fga = new_2pa + new_3pa + new_4pa

    new_fg_pct  = compute_pct(new_fgm, new_fga)
    new_2p_pct  = compute_pct(new_2pm, new_2pa)
    new_3p_pct  = compute_pct(new_3pm, new_3pa)
    new_4p_pct  = compute_pct(new_4pm, new_4pa)
    new_ft_pct  = compute_pct(new_ftm, new_fta)

    cursor.execute("""
        UPDATE stats SET
            GP=%s, pts=%s,
            fg_made=%s, fg_attempted=%s, fg_pct=%s,
            two_pt_made=%s, two_pt_attempted=%s, two_pt_pct=%s,
            three_pt_made=%s, three_pt_attempted=%s, three_pt_pct=%s,
            four_pt_made=%s, four_pt_attempted=%s, four_pt_pct=%s,
            ft_made=%s, ft_attempted=%s, ft_pct=%s,
            minutes=%s, off=%s, def=%s, reb=%s,
            ast=%s, to_stat=%s, stl=%s, blk=%s, pf=%s,
            plus_minus=%s
        WHERE player_id=%s
    """, (
        GP, old_pts + pts,
        new_fgm, new_fga, new_fg_pct,
        new_2pm, new_2pa, new_2p_pct,
        new_3pm, new_3pa, new_3p_pct,
        new_4pm, new_4pa, new_4p_pct,
        new_ftm, new_fta, new_ft_pct,
        old_min + mins, old_off + off, old_def + deff, old_reb + reb,
        old_ast + ast, old_to + to_stat, old_stl + stl, old_blk + blk, old_pf + pf,
        old_pm + plus_minus,
        player_id
    ))

# ------------------- MAIN -------------------
if __name__ == "__main__":
    # Set the base URL for the tournament you want to scrape.
    # Find tournament URLs at: https://stats-api-01.pba.ph
    # Example: https://stats-api-01.pba.ph/tournaments/pba-50th-season-philippine-cup
    BASE_URL = "https://stats-api-01.pba.ph/tournaments/pba-50th-season-philippine-cup"

    # Set the range of game IDs to scrape.
    # Game IDs are appended as ?game_id=N. Adjust the range to match the tournament.
    START_GAME = 1
    END_GAME   = 86

    for game_id in range(START_GAME, END_GAME):
        url = f"{BASE_URL}?game_id={game_id}"
        print(f"Scraping game {game_id}...")

        try:
            stats = scrape_box_score(url)
            print(f"  {len(stats)} player rows scraped")

            conn   = connect_db()
            cursor = conn.cursor()

            for s in stats:
                player_name = s["PLAYER"]
                team        = s["team"]
                player_id   = get_or_create_player(cursor, player_name, team)
                update_stats(cursor, player_id, s)

            conn.commit()
            cursor.close()
            conn.close()

            print(f"  Game {game_id} saved successfully\n")

        except Exception as e:
            print(f"  Failed on game {game_id}: {e}\n")
