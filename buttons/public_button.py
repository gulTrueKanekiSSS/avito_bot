from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from data_base import User_good, db
from states_groups.groups import Good
from keyboards.keyboards import keyboard_with_categories, keyboard
from aiogram.types import ReplyKeyboardMarkup
from aiogram import types, Dispatcher


# @dp.message_handler(Text(equals="Опубликовать"))
async def set_category(message: types.Message, state: FSMContext):
    if message.from_user.username is None:
        await message.answer("Для того чтобы опубликовать товар, пожалуйста, укажите пользовательское имя в своем профиле телеграмм", reply_markup=keyboard)
    else:
        await message.delete()
        await state.set_state(Good.wait_category.state)
        await message.answer('Выбери категорию товара:',
                             reply_markup=keyboard_with_categories)


# @dp.message_handler(content_types=['text'], state=Good.wait_category)
async def public_item(message: types.Message, state: FSMContext):
    if message.text not in ["Личные вещи", "Электроника", "Велосипеды и запчасти", "Автомобили и запчасти", "Вещи для дома", "Аксессуары"]:
        await message.answer("Пожалуйста, выбери категорию из списка)")
    else:
        await state.update_data(choosen_category=message.text)
        await state.set_state(Good.wait_good_name.state)
        await message.answer("Укажите название товара:")


# @dp.message_handler(content_types=['text'], state=Good.wait_good_name)
async def good_name_choosen(message: types.Message, state: FSMContext):
    await state.update_data(choosen_name=message.text)
    await state.set_state(Good.wait_description.state)
    await message.answer('Напиши описание товара:')


# @dp.message_handler(content_types=['text'], state=Good.wait_description)
async def description_choosen(message: types.Message, state: FSMContext):
    await state.update_data(choosen_desription=message.text)
    await state.set_state(Good.wait_photo.state)
    skip_photo = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    skip_photo.add('Пропустить')
    await message.answer('Пришли фото своего товара:', reply_markup=skip_photo)


# @dp.message_handler(content_types=['photo', 'text'], state=Good.wait_photo)
async def photo_choosen(message: types.Message, state: FSMContext):
    if message.text == 'Пропустить':
        await state.update_data(choose_photo=None)
        await state.set_state(Good.wait_price.state)
        await message.answer('Укажи цену своего товара:')
    elif message.text:
        await message.answer("Пожалуйста введите текст или пропустите этап")
    else:
        await state.update_data(choose_photo=message.photo)
        await state.set_state(Good.wait_price.state)
        await message.answer('Укажи цену своего товара:')


# @dp.message_handler(content_types=['text'], state=Good.wait_price)
async def choose_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price_choosen=message.text)
        await state.set_state(Good.wait_price.state)
        data = await state.get_data()
        if data.get('choose_photo') is None:
            data_for_db = {
                'trader': message.from_user.username,
                'trader_id': message.from_user.id,
                'category': data.get('choosen_category'),
                'good_name': data.get('choosen_name'),
                'description': data.get('choosen_desription'),
                'price': data.get('price_choosen'),
            }
        else:
            data_for_db = {
                'trader': message.from_user.username,
                'trader_id': message.from_user.id,
                'category': data.get('choosen_category'),
                'good_name': data.get('choosen_name'),
                'description': data.get('choosen_desription'),
                'price': data.get('price_choosen'),
                'photo': data.get('choose_photo')[-1]['file_id']
            }
        good = User_good(**data_for_db)
        with db.session.begin():
            db.session.add(good)
        await message.answer('Отлично, я все записал',
                             reply_markup=keyboard)
        await state.finish()
    else:
        await message.answer('Укажи цену в цифрах)')

def register_handlers_pub(dp: Dispatcher):
    dp.register_message_handler(set_category, Text(equals='Опубликовать'))
    dp.register_message_handler(public_item, content_types=['text'], state=Good.wait_category)
    dp.register_message_handler(good_name_choosen, content_types=['text'], state=Good.wait_good_name)
    dp.register_message_handler(description_choosen, content_types=['text'], state=Good.wait_description)
    dp.register_message_handler(photo_choosen, content_types=['photo', 'text'], state=Good.wait_photo)
    dp.register_message_handler(choose_price, content_types=['text'], state=Good.wait_price)