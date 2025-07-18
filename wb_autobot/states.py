from aiogram.dispatcher.filters.state import State, StatesGroup

class BookingState(StatesGroup):
    waiting_for_token = State()
    waiting_for_supply_choice = State()
    waiting_for_date_range = State()
    waiting_for_type = State()