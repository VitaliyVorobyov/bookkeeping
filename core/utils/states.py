from aiogram.fsm.state import State, StatesGroup


class AddDataState(StatesGroup):
    category = State()
    sub_category = State()
    amount = State()
    new_sub_category = State()


class StatisticsState(StatesGroup):
    category = State()
    sub_category = State()
    start_day = State()
    start_month = State()
    start_year = State()
    end_day = State()
    end_mount = State()
    end_year = State()
    add_name_button = State()
