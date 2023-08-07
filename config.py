from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_token import token
from aiogram import Bot, Dispatcher

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goods.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

help = '''
В данном боте ты можешь опубликовать товар буквально в пару кликов, тут ты можешь указать что хочешь не только продать товар, но и купить что-то определенное указав название, описание и цену за которую ты готов его купить\nТак же ты можешь купить товар подобрав нужную категорию.\n\n<strong>ВНИМАНИЕ!</strong>\nЕсли ты уже продал товар, не забудь его убрать с продажи в МоиТовары
'''