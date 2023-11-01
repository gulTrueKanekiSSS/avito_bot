from marshmallow import Schema, fields
from config import db, app

class User_good(db.Model):
    __tablename__ = 'goods'
    trader = db.Column(db.String)
    trader_id = db.Column(db.Integer)
    category = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    good_name = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Integer)
    photo = db.Column(db.Integer)
    is_goods_not_dangerous = db.Column(db.Boolean)




class User_good_schema(Schema):
    id = fields.Int()
    trader = fields.Str()
    trader_id = fields.Str()
    category = fields.Str()
    good_name = fields.Str()
    description = fields.Str()
    price = fields.Int()
    photo = fields.Str()
    is_goods_not_dangerous = fields.Bool()


app.app_context().push()
db.create_all()