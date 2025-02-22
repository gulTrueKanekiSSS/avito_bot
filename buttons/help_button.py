from keyboards.keyboards import keyboard
from aiogram import types, Dispatcher


# @dp.message_handler(commands=['help'])
async def show_help_message(message: types.Message):
    await message.answer(help,
                         reply_markup=keyboard,
                         parse_mode='html')

def register_handler_help(dp: Dispatcher):
    dp.register_message_handler(show_help_message, commands=['help'])