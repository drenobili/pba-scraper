-- PBA Scraper Database Schema
-- Run this file to set up the required tables before running scraper.py
-- Usage: mysql -u your_user -p your_database < schema.sql

CREATE TABLE IF NOT EXISTS players (
    player_id INT          NOT NULL AUTO_INCREMENT,
    name      VARCHAR(100) NOT NULL,
    team      VARCHAR(50)  NOT NULL,
    PRIMARY KEY (player_id),
    KEY idx_name (name)
);

CREATE TABLE IF NOT EXISTS stats (
    stats_id          INT           NOT NULL AUTO_INCREMENT,
    player_id         INT           NOT NULL,
    GP                INT           DEFAULT 0,
    pts               INT           DEFAULT 0,
    fg_made           INT           DEFAULT 0,
    fg_attempted      INT           DEFAULT 0,
    fg_pct            DECIMAL(5,1)  DEFAULT 0.0,
    two_pt_made       INT           DEFAULT 0,
    two_pt_attempted  INT           DEFAULT 0,
    two_pt_pct        DECIMAL(5,1)  DEFAULT 0.0,
    three_pt_made     INT           DEFAULT 0,
    three_pt_attempted INT          DEFAULT 0,
    three_pt_pct      DECIMAL(5,1)  DEFAULT 0.0,
    four_pt_made      INT           DEFAULT 0,
    four_pt_attempted INT           DEFAULT 0,
    four_pt_pct       DECIMAL(5,1)  DEFAULT 0.0,
    ft_made           INT           DEFAULT 0,
    ft_attempted      INT           DEFAULT 0,
    ft_pct            DECIMAL(5,1)  DEFAULT 0.0,
    minutes           FLOAT         DEFAULT 0,
    off               INT           DEFAULT 0,
    def               INT           DEFAULT 0,
    reb               INT           DEFAULT 0,
    ast               INT           DEFAULT 0,
    to_stat           INT           DEFAULT 0,
    stl               INT           DEFAULT 0,
    blk               INT           DEFAULT 0,
    pf                INT           DEFAULT 0,
    plus_minus        INT           DEFAULT 0,
    PRIMARY KEY (stats_id),
    KEY idx_player_id (player_id),
    CONSTRAINT fk_player FOREIGN KEY (player_id) REFERENCES players (player_id)
);

