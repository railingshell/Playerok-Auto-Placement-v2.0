from aiogram.fsm.state import State, StatesGroup


class STEAMOFF_AddAccountStates(StatesGroup):
    entering_login = State()
    entering_password = State()
    entering_mafile = State()


class STEAMOFF_SettingsStates(StatesGroup):
    entering_max_codes = State()
