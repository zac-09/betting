from os import error
from interfaces.db import DB
import random
from datetime import datetime

db =[]


class InMemory(DB):
    _instance = None

    def __init__(self):
      pass

    def connect():
        pass

    def insert(self, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        global db
        try:
            odds = {
                "id": random.randint(1,999),
                "league": league,
                "home_team": home_team,
                "away_team": away_team,
                "home_team_win_odds": home_team_win_odds,
                "away_team_win_odds": away_team_win_odds,
                "draw_odds": draw_odds,
                "game_date": game_date
            }
            db.append(odds)
           
            return True, db
        except error:
            print("An error occured",error)
            return False, "falied to insert into dictionary"

    def update(self, odd_id, league, home_team, away_team, home_team_win_odds, away_team_win_odds, draw_odds, game_date):
        global db
        try:

            for odds in db:
                if odds["id"] == int(odd_id):
                    odds.update({
                        "league": league,
                        "home_team": home_team,
                        "away_team": away_team,
                        "home_team_win_odds": home_team_win_odds,
                        "away_team_win_odds": away_team_win_odds,
                        "draw_odds": draw_odds,
                        "game_date": game_date
                    })
                    return True, odds

        except:
            return False, "failed to Update dictionary"

    def delete(self, home_team, away_team, game_date):
        global db
        
        try:
            for odds in db:
                if odds["home_team"] == home_team and odds["away_team"] == away_team and odds["game_date"] == game_date:
                    index = db.index(odds)
                    
                    db.pop(index)
                return True, odds
        except:
            return False, "failed to delete dictionary"

    def read(self, league, date_from, date_to):
        global db

     
        range_odds = []
        try:
            for odds in db:
                if odds["league"] == league and odds["game_date"] >= datetime.strptime(date_from,"%d-%m-%Y") and odds["game_date"] <= datetime.strptime(date_to,"%d-%m-%Y"):
                    new_odds_dict = odds.copy()
                    range_odds.append(new_odds_dict)
                  
            for odd in range_odds:
                   odd["game_date"] = f"{odd['game_date']}"
            return True, range_odds
        except error:
            print(error)
            return False, "failed to read from db"

    def get(self, odd_id):
        global db
        returned_odds = []
        try:
            for odds in db:
               
                if odds["id"] == int(odd_id):

                    returned_odds.append(odds)
            return True, returned_odds
        except:
            return False, "failed to read from db"

    def find_by_required_field(self, home_team, away_team, game_date):
        returned_odds = []
        global db
        print("From required fields",home_team,away_team,game_date)
        try:
            for odds in db:
                if odds["home_team"] == home_team and odds["away_team"] == away_team and odds["game_date"] == game_date:
                    returned_odds.append(odds)
            return True, returned_odds
        except:
            return False, "failed to read from db"

    @staticmethod
    def getInstance(re_init=False):
        """ get instance of the class """
        if InMemory._instance is None or re_init is True:
            return InMemory()

        return InMemory._instance
