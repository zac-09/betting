from interfaces.db import DB

import sqlite3


class SQLite(DB):
    _instance = None

    def __init__(self):
        self.db = sqlite3

    def connect(self):
        try:
            self.db = self.db.connect("data.db")
            print("successfully connected to db")
        except:
            print("an error occured connecting to database")

        return self

    def insert(self, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        try:

            sql = "INSERT INTO odds (league, home_team,away_team,home_team_win_odds,away_team_win_odds,draw_odds,game_date) values(?,?,?,?,?,?,?)"
            odds = self.db.cursor().execute(sql, (league, home_team, away_team,
                                                  home_team_win_odds, away_team_win_odds, draw_odds, game_date))
            self.db.commit()
            sql = "SELECT * FROM odds WHERE id = ?"
            odds = self.db.execute(sql, (odds.lastrowid,))

            odds_list = self.convertToDict(odds.fetchall())

            return True, odds_list
        except sqlite3.Error as e:
            return False, e.args[0]

    def update(self, id, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        try:
            sql = "UPDATE odds set league = ?, home_team = ?,away_team = ?,home_team_win_odds = ?,away_team_win_odds = ?,draw_odds = ?,game_date = ? where id = ?"
            odds = self.db.execute(sql, (league, home_team, away_team,
                                         home_team_win_odds, away_team_win_odds, draw_odds, game_date, id))
            self.db.commit()
            return True, odds
        except sqlite3.Error as e:
            return False, e.args[0]

    def error():
        pass

    def delete(self, home_team, away_team, game_date):
        try:
            sql = "DELETE FROM odds WHERE  home_team = ? AND away_team = ? AND game_date = ? "
            odds = self.db.execute(sql, (home_team, away_team, game_date))
            self.db.commit()

            return True, odds
        except sqlite3.Error as e:
            print("an error occured", e.args[0]) 
            return False, e.args[0]

    def read(self, league, date_from, date_to):
        try:
            sql = "SELECT * FROM odds WHERE league = ? AND game_date >= ? AND game_date <= ? "
            odds = self.db.execute(sql, (league, date_from, date_to))
            odds = self.convertToDict(odds.fetchall())
            return True, odds
        except sqlite3.Error as e:
            return False, e.args[0]

    def get(self, id):
        try:
            sql = "SELECT * FROM odds WHERE id = ?"
            odds = self.db.execute(sql, (id,))

            odds_list = self.convertToDict(odds.fetchall())
            print("after get", odds_list)
            return True, odds_list
        except sqlite3.Error as e:
            return False, e.args[0]

    def find_by_required_field(self, home_team, away_team, game_date):
        try:
            sql = "SELECT * FROM odds WHERE home_team = ? AND away_team = ? AND game_date = ?"
            odds = self.db.execute(sql, (home_team, away_team, game_date))

            odds_list = self.convertToDict(odds.fetchall())
            print("after get", odds_list)
            return True, odds_list
        except sqlite3.Error as e:
            return False, e.args[0]

    def convertToDict(self, tuples):
        odds = []

        for row in tuples:
            odd = {
                "id": row[0],
                "league": row[1],
                "home_team": row[2],
                "away_team": row[3],
                "home_team_win_odds": row[4],
                "away_team_win_odds": row[5],
                "draw_odds": row[6],
                "game_date": row[7],
            }
            odds.append(odd)
        return odds

    def close_connection(self):
        self.db.close()

    @staticmethod
    def getInstance(re_init=False):
        """ get instance of the class """
        if SQLite._instance is None or re_init is True:
            return SQLite()

        return SQLite._instance
