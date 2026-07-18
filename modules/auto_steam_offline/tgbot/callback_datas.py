from aiogram.filters.callback_data import CallbackData


class STEAMOFF_MenuNavigation(CallbackData, prefix="steamoff_nav"):
    to: str


class STEAMOFF_AccountPage(CallbackData, prefix="steamoff_account"):
    login: str


class STEAMOFF_AccountsPagination(CallbackData, prefix="steamoff_page"):
    page: int
    status: str
