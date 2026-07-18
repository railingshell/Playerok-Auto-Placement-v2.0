from aiogram.filters.callback_data import CallbackData


class ROBLOX_MenuNavigation(CallbackData, prefix="roblox_mennav"):
    to: str


class ROBLOX_ProfilePage(CallbackData, prefix="roblox_profpage"):
    profile_id: str


class ROBLOX_ProfilesPagination(CallbackData, prefix="roblox_profspag"):
    page: int


class ROBLOX_BlacklistPagination(CallbackData, prefix="roblox_blspag"):
    list_type: str
    page: int


class ROBLOX_BlacklistItemPage(CallbackData, prefix="roblox_blitempage"):
    list_type: str
    item: str
