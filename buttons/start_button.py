from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards.keyboards import keyboard
from config import bot

# @dp.message_handler(commands=['start'])
async def welcome_message(message: types.Message, state=FSMContext):
    await state.reset_state()
    await bot.send_sticker(message.from_user.id, sticker='CAACAgQAAxkBAAJEYmRgm3wwg-DnBkJFN_gS2hXKlfT9AAJPCgACBkA5Uxyu3L4frJ9ULwQ')
    await message.answer(text='<strong>Здарова, ты хочешь опубликовать товар или купить?</strong>\n\nВоспользуйся кнопкой /help ))',
                         parse_mode='HTML',
                         reply_markup=keyboard)
    await message.delete()


def register_handler_start(dp: Dispatcher):
    dp.register_message_handler(welcome_message, commands=['start'])