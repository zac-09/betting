from flask_restful import Resource, reqparse
from schemas.odds import OddSchema
from utils.util import api_key_required

from flask import request
from datetime import datetime


from models.odds import OddsModel


BLANK_ERROR = "'{}' cannot be blank or of wrong type."

odds_list_schema = OddSchema(many=True)
odds_schema = OddSchema()

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
        game_date = datetime.strptime(odds_data["game_date"], "%d-%m-%Y")

        try:
            odds = OddsModel.find_by_required_fields(
                home_team, away_team, game_date)
            if odds:
                odds.delete_from_db()
                return {"message": "odds have  been successfully deleted from databse"}, 200
            return {"message": "Error deleting odds not found"}, 404
        except:
            return {"message": "Error deleting data from database"},500
