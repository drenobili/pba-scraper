-- =========================
-- Database Schema
-- PBA Box Score Stats
-- =========================

-- =========================
-- Table: players
-- =========================
CREATE TABLE players (
    player_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    team VARCHAR(50) NOT NULL,
    PRIMARY KEY (player_id),
    INDEX idx_player_name (name)
);

-- =========================
-- Table: stats
-- =========================
CREATE TABLE stats (
    stats_id INT NOT NULL AUTO_INCREMENT,
    player_id INT NOT NULL,

    GP INT DEFAULT 0,
    pts INT DEFAULT 0,

    fg_made INT DEFAULT 0,
    fg_attempted INT DEFAULT 0,
    fg_pct DECIMAL(5,1) DEFAULT 0.0,

    two_pt_made INT DEFAULT 0,
    two_pt_attempted INT DEFAULT 0,
    two_pt_pct DECIMAL(5,1) DEFAULT 0.0,

    three_pt_made INT DEFAULT 0,
    three_pt_attempted INT DEFAULT 0,
    three_pt_pct DECIMAL(5,1) DEFAULT 0.0,

    four_pt_made INT DEFAULT 0,
    four_pt_attempted INT DEFAULT 0,
    four_pt_pct DECIMAL(5,1) DEFAULT 0.0,

    ft_made INT DEFAULT 0,
    ft_attempted INT DEFAULT 0,
    ft_pct DECIMAL(5,1) DEFAULT 0.0,

    minutes FLOAT DEFAULT 0,

    off INT DEFAULT 0,
    def INT DEFAULT 0,
    reb INT DEFAULT 0,

    ast INT DEFAULT 0,
    to_stat INT DEFAULT 0,
    stl INT DEFAULT 0,
    blk INT DEFAULT 0,
    pf INT DEFAULT 0,

    plus_minus INT DEFAULT 0,

    PRIMARY KEY (stats_id),

    INDEX idx_player_id (player_id),

    CONSTRAINT fk_stats_player
        FOREIGN KEY (player_id)
        REFERENCES players(player_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
