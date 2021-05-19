from flask_restful import Resource, reqparse
from schemas.odds import OddSchema
from flask import request
from models.odds import OddsModel
from test import CreatOddsPublisher
from utils.util import api_key_required
BLANK_ERROR = "'{}' cannot be blank or of wrong type."
CREATED_SUCCESSFULLY = " Odds created successfully."

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


class CreateOdds(Resource):
    """
    This resource is used to crearte odds and save them to the database
    """

    @classmethod
    @api_key_required
    def post(cls):
        data = _odds_parser.parse_args()
        print("data is:",data)
        try:
            odds = OddsModel(**data)
            odds.save_to_db()
        except:
            return {"message": "Error inserting in database"}, 500
        print(odds)
        publisher = CreatOddsPublisher()
        publisher.publish(request.get_json())
        return {"message": CREATED_SUCCESSFULLY,"odds":odds_schema.dump(odds) }, 200

  
