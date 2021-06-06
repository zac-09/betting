from flask import Flask,jsonify
from flask_restful import Api
import os

from resources.create_odds import CreateOdds
from resources.delete_odds import DeleteOdds
from resources.update_odds import UpdateOdds
from resources.read_odds import ReadOdds
import sqlite3 


from marshmallow import ValidationError

import sqlite3



app = Flask(__name__)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
api = Api(app)

# db = SQLAlchemy(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


db = sqlite3.connect("data.db")


api.add_resource(CreateOdds,"/create")
api.add_resource(DeleteOdds,"/delete")
api.add_resource(ReadOdds,"/read")
api.add_resource(UpdateOdds,"/update/<odd_id>")


def init_db():
    with app.app_context():
     
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


port = int(os.environ.get('PORT', 8080))

if __name__ == "__main__":
   
  
   

    app.run(debug=True, host='0.0.0.0',port=port )

 

