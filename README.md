# 🏀 Basketball Stats Scraper & Database System

This project is a Python-based web scraper that collects basketball box score data from game pages and stores them into a MySQL database for analytics and player performance tracking. It is designed for data science and sports analytics use cases, enabling structured storage of player performance data for further analysis, visualization, or machine learning.

---

## ⚙️ Features

- Scrapes basketball box score data from game URLs  
- Extracts player statistics (points, rebounds, assists, steals, blocks, etc.)  
- Handles multiple shooting formats (2PT, 3PT, 4PT, FT)  
- Automatically computes shooting percentages  
- Stores and updates cumulative player stats in MySQL  
- Prevents duplicate players using name + team matching  
- Robust handling of missing or malformed data  

---

## 🛠️ Requirements

Install dependencies:

pip install requests beautifulsoup4 mysql-connector-python python-dotenv

---

## 🗄️ Database Setup

Create your database:

CREATE DATABASE basketball_stats;

Import schema:

mysql -u your_username -p basketball_stats < schema.sql

This creates:
- players → player information  
- stats → cumulative player performance statistics  

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

DB_HOST=localhost  
DB_USER=your_mysql_username  
DB_PASSWORD=your_mysql_password  
DB_NAME=basketball_stats  

---

## 🚀 How to Run

Run the scraper:

python scraper.py

---

## 🔧 Configuration

Inside `scraper.py`, adjust:

BASE_URL = "https://stats-api-01.pba.ph/tournaments/pba-50th-season-philippine-cup"  
START_GAME = 1  
END_GAME = 86  

Modify depending on:
- Tournament source  
- Number of games available  

---

## 📊 Data Collected

Each player record includes:

- Games Played (GP)  
- Points (PTS)  
- Field Goals (FG)  
- 2PT / 3PT / 4PT shots  
- Free Throws  
- Minutes Played  
- Offensive & Defensive Rebounds  
- Assists, Steals, Blocks  
- Turnovers and Fouls  
- Plus/Minus  
- Shooting Percentages (auto-calculated)  

---

## 🧠 How It Works

- Players are uniquely identified by `name + team`  
- Stats are accumulated across multiple games  
- Shooting percentages are recalculated dynamically  
- Missing values are safely defaulted to zero  
- Each game is scraped and processed sequentially  

---

## 📌 Notes

- Ensure MySQL server is running before execution  
- Script safely skips invalid or missing game pages  
- Designed for scalability and future analytics use  
- Can be extended for ML or dashboard applications  

---

## 📈 Possible Improvements

- Add game-level statistics table  
- Build REST API using Flask or FastAPI  
- Create dashboard (Streamlit / React)  
- Add player efficiency rating (PER)  
- Export dataset for machine learning models  

---

## 🧑‍💻 Author

Built for basketball analytics, data scraping, and machine learning preparation using real-world sports data.
