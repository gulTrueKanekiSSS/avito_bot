
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from bot_token import token


from data_base import User_good, db
from keyboards import keyboard, keyboard_with_categories, keyboard_with_moves, characters

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

help = 'В данном боте ты можешь опубликовать товар буквально в пару кликов, тут ты можешь указать что хочешь не только продать товар, но и купить что-то определенное указав название, описание и цену за которую ты готов его купить\nТак же ты можешь купить товар подобрав нужную категорию.\n\n<strong>ВНИМАНИЕ!</strong>\nЕсли ты уже продал товар, не забудь его убрать с продажи в МоиТовары'

class Good(StatesGroup):
    wait_category = State()
    wait_good_name = State()
    wait_description = State()
    wait_photo = State()
    wait_price = State()


class BuyGood(StatesGroup):
    wait_category = State()
    wait_good_to_buy = State()


@dp.message_handler(commands=['start'])
async def welcome_message(message: types.Message, state=FSMContext):
    await state.reset_state()
    await bot.send_sticker(message.from_user.id, sticker='CAACAgQAAxkBAAJEYmRgm3wwg-DnBkJFN_gS2hXKlfT9AAJPCgACBkA5Uxyu3L4frJ9ULwQ')
    await message.answer(text='<strong>Здарова, ты хочешь опубликовать товар или купить?</strong>\n\nВоспользуйся кнопкой /help ))', parse_mode='HTML',
                         reply_markup=keyboard)

    await message.delete()


@dp.message_handler(Text(equals="Опубликовать"))
async def set_category(message: types.Message, state: FSMContext):
    await message.delete()
    await state.set_state(Good.wait_category.state)
    await message.answer('Выбери категорию товара:', reply_markup=keyboard_with_categories)


@dp.message_handler(content_types=['text'], state=Good.wait_category)
async def public_item(message: types.Message, state: FSMContext):
    if message.text not in ["Личные вещи", "Электроника", "Велосипеды и запчасти", "Автомобили и запчасти", "Вещи для дома", "Аксессуары"]:
        await message.answer("Пожалуйста, выбери категорию из списка)")
    else:
        await state.update_data(choosen_category=message.text)
        await state.set_state(Good.wait_good_name.state)
        await message.answer("Укажите название товара:")


@dp.message_handler(content_types=['text'], state=Good.wait_good_name)
async def good_name_choosen(message: types.Message, state: FSMContext):
    await state.update_data(choosen_name=message.text)
    await state.set_state(Good.wait_description.state)
    await message.answer('Напиши описание товара:')


@dp.message_handler(content_types=['text'], state=Good.wait_description)
async def description_choosen(message: types.Message, state: FSMContext):
    await state.update_data(choosen_desription=message.text)
    await state.set_state(Good.wait_photo.state)
    skip_photo = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    skip_photo.add('Пропустить')
    await message.answer('Пришли фото своего товара:', reply_markup=skip_photo)


@dp.message_handler(content_types=['photo', 'text'], state=Good.wait_photo)
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


@dp.message_handler(content_types=['text'], state=Good.wait_price)
async def choose_price(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price_choosen=message.text)
        await state.set_state(Good.wait_price.state)
        data = await state.get_data()
        # data = {
        #     'good_name': state.get_data()
        # }
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
        await message.answer('Отлично, я все записал', reply_markup=keyboard)
        await state.finish()
    else:
        await message.answer('Укажи цену в цифрах)')


@dp.message_handler(Text(equals='Купить'))
async def show_categories(message: types.Message, state=FSMContext):
    await state.set_state(BuyGood.wait_category.state)
    await message.answer(f'Приветствую в разделе покупок {message.from_user.username}! Выбери интересующую категорию:', reply_markup=keyboard_with_categories)


@dp.message_handler(content_types=['text'], state=BuyGood.wait_category)
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

        await message.answer(f'Такие товары сейчас есть по категории - {message.text}', reply_markup=goods)
        await state.set_state(BuyGood.wait_good_to_buy.state)


@dp.message_handler(content_types=['text'], state=BuyGood.wait_good_to_buy)
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
                # await message.answer(f'Название: {good[0].good_name}\nОписание: {good[0].description}\nЦена: {good[0].price}\nПродавец: @{good[0].trader}')
            else:
                await message.answer(f'Название: {good[0].good_name}\nОписание: {good[0].description}\nЦена: {good[0].price}руб.\nПродавец: @{good[0].trader}')
        except IndexError:
            await bot.send_message(message.from_user.id, 'У нас нету такого товара 😢', reply_markup=keyboard)
            await state.finish()

class GoodsMode(StatesGroup):
    wait_good = State()
    wait_move = State()


@dp.message_handler(Text(equals='Мои Товары'))
async def show_owners_goods(message: types.Message, state: FSMContext):
    with db.session.begin():
        goods = db.session.query(User_good).filter(User_good.trader_id == message.from_user.id).all()
        db.session.close()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if len(goods) == 0:
        await message.answer('У тебя пока что нету товаров, создай его', reply_markup=keyboard)
    else:
        for good in goods:
            good_for_user = KeyboardButton(text=good.good_name)
            kb.add(good_for_user)
        await message.answer('Вот такие товары у тебя сейчас имеются', reply_markup=kb)
        await state.set_state(GoodsMode.wait_good.state)


@dp.message_handler(content_types=['text'], state=GoodsMode.wait_good)
async def waiting_good(message: types.Message, state: FSMContext):
    await state.update_data(choosen_good_name=message.text)
    await message.answer('Выбери что хочешь сделать с товаром', reply_markup=keyboard_with_moves)
    await state.set_state(GoodsMode.wait_move.state)


@dp.message_handler(content_types=['text'], state=GoodsMode.wait_move)
async def choose_move(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Посмотреть':
        with db.session.begin():
            good = db.session.query(User_good).filter(User_good.good_name == data.get('choosen_good_name') and User_good.trader_id == message.from_user.id).all()
            try:
                if good[0].photo is not None:
                    await bot.send_photo(message.from_user.id, good[0].photo, caption=f'Название: {good[0].good_name}\nОписание: {good[0].description}\nЦена: {good[0].price}\nПродавец: @{good[0].trader}')
                else:
                    await message.answer(f'Название: {good[0].good_name}\nОписание: {good[0].description}\nЦена: {good[0].price}руб.\nПродавец: @{good[0].trader}')
            except Exception:
                await message.answer('Произошла какая-то ошибка(((', reply_markup=keyboard)

    elif message.text == 'Товар продан':

        with db.session.begin():
            db.session.delete(db.session.query(User_good).filter(User_good.good_name == data.get('choosen_good_name'))[0])
            db.session.commit()

        await message.answer('Готово', reply_markup=keyboard)
        await state.finish()
    elif message.text == 'Вернуться на главную':
        await message.answer('Возвращаем на главную...', reply_markup=keyboard)
        await state.finish()

    else:
        await message.answer('Такого действия мы еще не предусмотрели)')


@dp.message_handler(commands=['help'])
async def show_help_message(message: types.Message):
    await message.answer(help, reply_markup=keyboard, parse_mode='html')

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
