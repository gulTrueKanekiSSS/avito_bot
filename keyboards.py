from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data_base import User_good, db


def count_items():
    with db.session.begin():
        local_goods = len(db.session.query(User_good).filter(User_good.category == 'Личные вещи').all())
        electronic = len(db.session.query(User_good).filter(User_good.category == 'Электроника').all())
        bikes_and_tools = len(db.session.query(User_good).filter(User_good.category == 'Велосипеды и запчасти').all())
        vehicle_and_tools = len(db.session.query(User_good).filter(User_good.category == 'Автомобили и запчасти').all())
        items_for_home = len(db.session.query(User_good).filter(User_good.category == 'Вещи для дома').all())
        accesories = len(db.session.query(User_good).filter(User_good.category == 'Аксессуары').all())
        db.session.close()
    return [local_goods, electronic, bikes_and_tools, vehicle_and_tools, items_for_home, accesories]

items = count_items()


keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_1 = KeyboardButton(text='Опубликовать')
button_2 = KeyboardButton(text='Купить')
button_3 = KeyboardButton(text='Мои Товары')
button_4 = KeyboardButton(text='/help')

keyboard.add(button_1, button_2).add(button_3).add(button_4)

keyboard_with_categories = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
category_1 = KeyboardButton(text=f'Личные вещи')
category_2 = KeyboardButton(text=f'Электроника')
category_3 = KeyboardButton(text=f'Велосипеды и запчасти')
category_4 = KeyboardButton(text=f'Автомобили и запчасти')
category_5 = KeyboardButton(text=f'Вещи для дома')
category_6 = KeyboardButton(text=f'Аксессуары')

keyboard_with_categories.add(category_1, category_2, category_3).add(category_4, category_5, category_6)

is_it_clear = ReplyKeyboardMarkup(resize_keyboard=True)
answer_1 = KeyboardButton(text='/Да')
answer_2 = KeyboardButton(text='/Нет')

is_it_clear.add(answer_1).add(answer_2)

keyboard_with_moves = ReplyKeyboardMarkup(resize_keyboard=True)
item_1 = 'Посмотреть'
item_3 = 'Товар продан'
item_4 = 'Вернуться на главную'
keyboard_with_moves.add(item_3, item_4).add(item_1)

characters = ReplyKeyboardMarkup(resize_keyboard=True)
character_1 = KeyboardButton(text='Название')
character_2 = KeyboardButton(text='Описание')
character_3 = KeyboardButton(text='Цена')
character_4 = KeyboardButton(text='Фотография')
characters.add(character_1, character_2, character_3).add(character_4)
