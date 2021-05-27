DROP TABLE IF EXISTS odds;
CREATE TABLE odds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league VARCHAR(80),
    home_team VARCHAR(80),
    away_team VARCHAR(80),
    home_team_win_odds FLOAT,
    away_team_win_odds FLOAT,
    draw_odds FLOAT,
    game_date DATE


)