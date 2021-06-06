from sqlite3.dbapi2 import Error
from flask_restful import Resource, reqparse

from utils.util import api_key_required
from controllers.dbController import SQLite
from controllers.memoryDb import InMemory
from controllers.firestore import Firestore
from flask import request
from datetime import datetime


BLANK_ERROR = "'{}' cannot be blank or of wrong type."
CREATED_SUCCESSFULLY = " Odds created successfully."


_odds_parser = reqparse.RequestParser()
_odds_parser.add_argument(
    "league", type=str, required=True, help=BLANK_ERROR.format("league")
)
_odds_parser.add_argument(
    "home_team", type=str, required=True, help=BLANK_ERROR.format("home_team")
)
_odds_parser.add_argument(
    "away_team", type=str, required=True, help=BLANK_ERROR.format("away_team")
)
_odds_parser.add_argument(
    "home_team_win_odds", type=float, required=True, help=BLANK_ERROR.format("home_team_win_odds")
)
_odds_parser.add_argument(
    "away_team_win_odds", type=float, required=True, help=BLANK_ERROR.format("away_team_win_odds")
)
_odds_parser.add_argument(
    "draw_odds", type=float, required=True, help=BLANK_ERROR.format("draw_odds")
)
_odds_parser.add_argument(
    "game_date", type=str, required=True, help=BLANK_ERROR.format("game_date")
)


class UpdateOdds(Resource):
    """
    This resource is used to update odds with in database
    """
    @classmethod
    @api_key_required
    def put(cls, odd_id):
        data = _odds_parser.parse_args()

        odds_data = request.get_json()
        home_team = odds_data["home_team"]
        league = odds_data["league"]

        away_team = odds_data["away_team"]
        away_team_win_odds = odds_data["away_team_win_odds"]
        home_team_win_odds = odds_data["home_team_win_odds"]
        draw_odds = odds_data["draw_odds"]

        game_date = odds_data["game_date"]

        try:
            # db = SQLite.getInstance().connect()
            db = Firestore.getInstance().connect()

            # db = InMemory.getInstance()

            read, odds = db.get(odd_id)

            if read is False:
                return {"message": "Error reading from db"}, 404
            if odds:
                db.update(odd_id, league, home_team, away_team, home_team_win_odds,
                          away_team_win_odds, draw_odds, game_date)

                return {"message": "odds have  been successfully updated from databse"}, 200
            return {"message": "Error updating odds not found"}, 404
        except Error:
            print(Error)
            return{"message": "Error updating odds"}, 500
