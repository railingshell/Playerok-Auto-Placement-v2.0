from aiogram.fsm.state import State, StatesGroup


class ROBLOX_AddProfileStates(StatesGroup):
    entering_id = State()
    entering_name = State()
    entering_search_url = State()
    entering_min_profit = State()
    entering_tag = State()


class ROBLOX_BlacklistStates(StatesGroup):
    entering_item = State()
    entering_seller = State()
