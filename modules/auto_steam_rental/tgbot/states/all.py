from aiogram.fsm.state import State, StatesGroup


class STEAMRENT_AddAccountStates(StatesGroup):
    entering_login = State()
    entering_password = State()
    entering_mafile = State()


class STEAMRENT_SettingsStates(StatesGroup):
    entering_duration = State()
    entering_login_timeout = State()
    entering_bonus = State()
    entering_api_key = State()
