from flask_restful import Resource, reqparse
from schemas.odds import OddSchema
from flask import request
from datetime import datetime
from utils.util import api_key_required


from models.odds import OddsModel


BLANK_ERROR = "'{}' cannot be blank or of wrong type."


odds_list_schema = OddSchema(many=True)

_odds_parser = reqparse.RequestParser()
_odds_parser.add_argument(
    "league", type=str, required=True, help=BLANK_ERROR.format("league")
)
_odds_parser.add_argument(
    "date_range", type=str, required=True, help=BLANK_ERROR.format("date_range")
)



class ReadOdds(Resource):
    """
    This resource is used to read odds from database within specified range
    """


    @classmethod
    @api_key_required
    def get(cls):
        data = _odds_parser.parse_args()
        odds_data = request.get_json()
        league = odds_data["league"]
        date_range = odds_data["date_range"]
        range_from = datetime.strptime(date_range.split("to")[0].strip(), "%d-%m-%Y") 
        range_to = datetime.strptime(date_range.split("to")[1].strip(), "%d-%m-%Y") 
        try:
            odds = OddsModel.find_witin_range(league,range_from,range_to)
            print("the ranges are",range_from,range_to)
            return {"odds":odds_list_schema.dump(odds)}, 200
        except:
            return {"message":"Error reading data from database"}, 500


      
  