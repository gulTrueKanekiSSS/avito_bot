from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goods.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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



class User_good_schema(Schema):
    id = fields.Int()
    trader = fields.Str()
    trader_id = fields.Str()
    category = fields.Str()
    good_name = fields.Str()
    description = fields.Str()
    price = fields.Int()
    photo = fields.Str()


app.app_context().push()
db.create_all()