from ma import ma
from models.odds import OddsModel
from marshmallow_sqlalchemy import ModelSchema


class OddSchema(ModelSchema):
    class Meta:
        model = OddsModel
        load_only = ("odd",)
        dump_only = ("id",)
        include_fk = True