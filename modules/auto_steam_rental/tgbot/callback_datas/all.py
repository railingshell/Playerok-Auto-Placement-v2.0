from aiogram.filters.callback_data import CallbackData


class STEAMRENT_MenuNavigation(CallbackData, prefix="steamrent_mennav"):
    to: str


class STEAMRENT_AccountPage(CallbackData, prefix="steamrent_accpage"):
    login: str


class STEAMRENT_AccountsPagination(CallbackData, prefix="steamrent_accpag"):
    page: int
    status: str
