from os import error
from sqlite3.dbapi2 import Error
from flask_restful import Resource, reqparse
from datetime import datetime
from flask import request
from utils.util import api_key_required
from controllers.dbController import SQLite
from controllers.memoryDb import InMemory
from controllers.firestore import Firestore


BLANK_ERROR = "'{}' cannot be blank or of wrong type."


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
    def post(cls):
        data = _odds_parser.parse_args()
        odds_data = request.get_json()
        league = odds_data["league"]
        date_range = odds_data["date_range"]
        range_from = date_range.split("to")[0].strip()

        range_to = date_range.split("to")[1].strip()

        try:
            print("from reader",range_from,range_to)
            # db = InMemory.getInstance()
            # read, odds = db.read(league, range_from, range_to)
            # use sqlite
            # db = SQLite.getInstance().connect()
            db = Firestore.getInstance().connect()

            read, odds = db.read(league,range_from,range_to)
            if read is False:
                return{"error": odds}, 404
            if len(odds) > 0:
                return {"odds": odds}, 200
            else:
                return{"odds": " No natching odds found in the specified range"}, 404
        except error:
            print(error)
            return {"message": "Error reading data from database"}, 500
