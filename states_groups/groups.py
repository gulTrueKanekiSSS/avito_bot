from aiogram.dispatcher.filters.state import State, StatesGroup

class Good(StatesGroup):
    wait_category = State()
    wait_good_name = State()
    wait_description = State()
    wait_photo = State()
    wait_price = State()


class BuyGood(StatesGroup):
    wait_category = State()
    wait_good_to_buy = State()


class GoodsMode(StatesGroup):
    wait_good = State()
    wait_move = State()