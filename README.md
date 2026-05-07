# PBA Box Score Scraper

A Python scraper that pulls player box score data from the PBA's public stats site and stores cumulative season stats in a MySQL database.

Built to support basketball analytics work on Philippine professional league data.

---

## What it does

- Scrapes player-level box scores from [stats-api-01.pba.ph](https://stats-api-01.pba.ph) for a given tournament and game range
- Parses shooting splits (2P, 3P, 4P, FT), rebounds, assists, turnovers, and other standard stats
- Accumulates per-game data into running season totals per player
- Recomputes FG totals from shot breakdowns for accuracy

## Stack

- Python, BeautifulSoup, mysql-connector-python, python-dotenv

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/drenobili/pba-scraper.git
cd pba-scraper
```

### 2. Install dependencies

```bash
pip install requests beautifulsoup4 mysql-connector-python python-dotenv
```

### 3. Set up your database

Create a MySQL database, then run the schema:

```bash
mysql -u your_user -p your_database < schema.sql
```

### 4. Configure your credentials

```bash
cp .env.example .env
```

Open `.env` and fill in your MySQL credentials:

```
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

---

## Usage

Open `scraper.py` and set the tournament URL and game range near the bottom of the file:

```python
BASE_URL   = "https://stats-api-01.pba.ph/tournaments/pba-50th-season-philippine-cup"
START_GAME = 1
END_GAME   = 86
```

Tournament URLs follow the pattern:
```
https://stats-api-01.pba.ph/tournaments/{tournament-slug}
```

You can find available tournaments by browsing [stats-api-01.pba.ph](https://stats-api-01.pba.ph).

Then run:

```bash
python scraper.py
```

The script will print progress per game and skip any game IDs that fail without stopping the run.

---

## Database schema

Two tables are created by `schema.sql`:

**`players`** — one row per player per team

| Column | Type | Description |
|---|---|---|
| player_id | INT (PK) | Auto-incremented ID |
| name | VARCHAR(100) | Player name |
| team | VARCHAR(50) | Team name |

**`stats`** — cumulative season stats per player

Tracks GP, PTS, FG/2P/3P/4P/FT (made, attempted, pct), MIN, REB (OFF/DEF), AST, TO, STL, BLK, PF, and +/-.

---

## Notes

- The PBA uses a 4-point line, which this scraper handles as a separate shot category
- FG totals are recomputed from 2P + 3P + 4P breakdowns rather than trusting the FG column directly
- Running the scraper on a game that was already scraped will double-count stats — designed for a single full-season run

---

## Author

Andre Bautista — [LinkedIn](https://www.linkedin.com/in/drenobili/) · [drenobili@gmail.com](mailto:drenobili@gmail.com)

