from aiogram import executor
from config import dp
from buttons import buy_button, help_button, public_button, user_goods_button, start_button

public_button.register_handlers_pub(dp)
buy_button.register_handlers_buy(dp)
help_button.register_handler_help(dp)
user_goods_button.register_handlers_goods(dp)
start_button.register_handler_start(dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
