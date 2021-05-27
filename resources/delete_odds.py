from flask_restful import Resource, reqparse

from utils.util import api_key_required

from flask import request


from config.dbController import SQLite




BLANK_ERROR = "'{}' cannot be blank or of wrong type."



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
    "game_date", type=str, required=True, help=BLANK_ERROR.format("game_date")
)


class DeleteOdds(Resource):
    """
    This resource is used to delete odds from the database
    """

    @classmethod
    @api_key_required
    def delete(cls):
        data = _odds_parser.parse_args()
        odds_data = request.get_json()
        home_team = odds_data["home_team"]
        away_team = odds_data["away_team"]
        game_date = odds_data["game_date"]

        try:

            db = SQLite.getInstance().connect()

            read, odds = db.find_by_required_field(
                home_team, away_team, game_date)

            if read is False:
                return {"message": "Error reading from db"}, 500
            if odds:
                db.delete(home_team, away_team, game_date)
                return {"message": "odds have  been successfully deleted from databse"}, 200
            return {"message": "Error deleting odds not found"}, 404
        except:
            return {"message": "Error deleting data from database"}, 500
