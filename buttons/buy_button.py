from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from states_groups.groups import BuyGood
from data_base import User_good, db
from keyboards.keyboards import keyboard, keyboard_with_categories
from config import bot


async def show_categories(message: types.Message, state=FSMContext):
    await state.set_state(BuyGood.wait_category.state)
    await message.answer(f'Приветствую в разделе покупок {message.from_user.username}! Выбери интересующую категорию:',
                         reply_markup=keyboard_with_categories)


async def search_goods(message: types.Message, state: FSMContext):
    if message.text not in ["Личные вещи", "Электроника", "Велосипеды и запчасти", "Автомобили и запчасти", "Вещи для дома", "Аксессуары"]:
        await message.answer("Пожалуйста, выбери категорию из списка)")
    else:
        await state.update_data()
        with db.session.begin():
            categories = db.session.query(User_good).filter(User_good.category == message.text).all()
            db.session.close()
        goods = ReplyKeyboardMarkup(resize_keyboard=True)
        goods.add(KeyboardButton(text='Закончить выбор товара'))
        for category in categories:
            good = KeyboardButton(text=category.good_name)
            goods.add(good)

        await message.answer(f'Такие товары сейчас есть по категории - {message.text}',
                             reply_markup=goods)
        await state.set_state(BuyGood.wait_good_to_buy.state)


async def show_good(message: types.Message, state: FSMContext):
    if message.text == 'Закончить выбор товара':
        await state.finish()
        await message.answer('Ок', reply_markup=keyboard)
    else:
        await state.update_data()
        with db.session.begin():
            good = db.session.query(User_good).filter(User_good.good_name == message.text).all()
            db.session.close()
        try:
            if good[0].photo is not None:
                await bot.send_photo(message.from_user.id, good[0].photo, caption=f'Название: {good[0].good_name}\nОписание: {good[0].description}\nЦена: {good[0].price}\nПродавец: @{good[0].trader}')
            else:
                await message.answer(f'Название: {good[0].good_name}\nОписание: {good[0].description}\nЦена: {good[0].price}руб.\nПродавец: @{good[0].trader}')
        except IndexError:
            await bot.send_message(message.from_user.id, 'У нас нету такого товара 😢', reply_markup=keyboard)
            await state.finish()


def register_handlers_buy(dp: Dispatcher):
    dp.register_message_handler(show_categories, Text(equals='Купить'))
    dp.register_message_handler(search_goods, content_types=['text'], state=BuyGood.wait_category)
    dp.register_message_handler(show_good, content_types=['text'], state=BuyGood.wait_good_to_buy)
