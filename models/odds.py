from typing import Dict, List
from db import db
from datetime import datetime



class OddsModel(db.Model):
    __tablename__ = "odds"

    id = db.Column(db.Integer, primary_key=True)
    league = db.Column(db.String(80))
    home_team = db.Column(db.String(80))
    away_team = db.Column(db.String(80))
    home_team_win_odds = db.Column(db.Float)
    away_team_win_odds = db.Column(db.Float)
    draw_odds = db.Column(db.Float)
    game_date = db.Column(db.DateTime)

    def __init__(self, league: str, home_team: str, away_team: str, home_team_win_odds: float, away_team_win_odds: float, draw_odds: float, game_date: str):
        self.league = league
        self.home_team = home_team
        self.away_team = away_team
        self.home_team_win_odds = home_team_win_odds
        self.away_team_win_odds = away_team_win_odds
        self.draw_odds = draw_odds
        self.game_date = datetime.strptime(game_date, "%d-%m-%Y")

    def json(self):
        return {"id": self.id, "home_team": self.home_team,
                "away_team": self.away_team, "home_team_win_odds": self.home_team_win_odds,
                "away_team_win_odds": self.away_team_win_odds, "draw_odds": self.draw_odds}

    @classmethod
    def find_all(cls) -> List["OddsModel"]:
        return cls.query.all()

    @classmethod
    def find_by_id(cls,id:int) -> "OddsModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_witin_range(cls, league: str, range_from: str, range_to: str) -> "OddsModel":
        return cls.query.filter_by(league=league).filter(cls.game_date >= range_from).filter(cls.game_date <= range_to)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
