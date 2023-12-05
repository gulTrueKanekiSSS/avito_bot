from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from states_groups.groups import GoodsMode
from data_base import User_good, db
from keyboards.keyboards import keyboard, keyboard_with_moves
from config import bot


# @dp.message_handler(Text(equals='Мои Товары'))
async def show_owners_goods(message: types.Message, state: FSMContext):
    with db.session.begin():
        goods = db.session.query(User_good).filter(User_good.trader_id == message.from_user.id).all()
        db.session.close()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if len(goods) == 0:
        await message.answer('У тебя пока что нету товаров, создай его',
                             reply_markup=keyboard)
    else:
        for good in goods:
            good_for_user = KeyboardButton(text=good.good_name)
            kb.add(good_for_user)
        await message.answer('Вот такие товары у тебя сейчас имеются',
                             reply_markup=kb)
        await state.set_state(GoodsMode.wait_good.state)


# @dp.message_handler(content_types=['text'], state=GoodsMode.wait_good)
async def waiting_good(message: types.Message, state: FSMContext):
    await state.update_data(choosen_good_name=message.text)
    await message.answer('Выбери что хочешь сделать с товаром',
                         reply_markup=keyboard_with_moves)
    await state.set_state(GoodsMode.wait_move.state)


# @dp.message_handler(content_types=['text'], state=GoodsMode.wait_move)
async def choose_move(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Посмотреть':
        with db.session.begin():
            good = db.session.query(User_good).filter(User_good.good_name == data.get('choosen_good_name') and User_good.trader_id == message.from_user.id).all()
            try:
                if good[0].photo is not None:
                    await bot.send_photo(message.from_user.id, good[0].photo,
                                         caption=f'Название: {good[0].good_name}\nОписание: {good[0].description}\nЦена: {good[0].price}\nПродавец: @{good[0].trader}')
                else:
                    await message.answer(f'Название: {good[0].good_name}\nОписание: {good[0].description}\nЦена: {good[0].price}руб.\nПродавец: @{good[0].trader}')
            except Exception:
                await message.answer('Произошла какая-то ошибка(((',
                                     reply_markup=keyboard)

    elif message.text == 'Товар продан':
        with db.session.begin():
            db.session.delete(db.session.query(User_good).filter(User_good.good_name == data.get('choosen_good_name'))[0])
            db.session.commit()

        await message.answer('Готово',
                             reply_markup=keyboard)
        await state.finish()

    elif message.text == 'Вернуться на главную':
        await message.answer('Возвращаем на главную...',
                             reply_markup=keyboard)
        await message.delete()
        await state.finish()

    else:
        await message.answer('Такого действия мы еще не предусмотрели)')

def register_handlers_goods(dp: Dispatcher):
    dp.register_message_handler(show_owners_goods, Text(equals='Мои Товары'))
    dp.register_message_handler(waiting_good, content_types=['text'], state=GoodsMode.wait_good)
    dp.register_message_handler(choose_move, content_types=['text'], state=GoodsMode.wait_move)
