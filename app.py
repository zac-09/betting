from flask import Flask,jsonify
from flask_restful import Api
from natsWrapper import run 
from db import db
from resources.create_odds import CreateOdds
from resources.delete_odds import DeleteOdds
from resources.update_odds import UpdateOdds
from resources.read_odds import ReadOdds



from marshmallow import ValidationError
from ma import ma
import asyncio
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
api = Api(app)

# db = SQLAlchemy(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@app.before_first_request 
def create_tables():
    db.create_all() 


api.add_resource(CreateOdds,"/create")
api.add_resource(DeleteOdds,"/delete")
api.add_resource(ReadOdds,"/read")
api.add_resource(UpdateOdds,"/update/<odd_id>")

db.init_app(app)
print("reacehed there")


if __name__ == "__main__":
    ma.init_app(app)
  
   

    app.run(debug=True, host='0.0.0.0',port=5000 )

 

