from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.helpful import throw_float_message

from .. import templates as templ
from .. import callback_datas as calls


router = Router()


@router.callback_query(calls.ROBLOX_MenuNavigation.filter())
async def callback_menu_navigation(callback: CallbackQuery, callback_data: calls.ROBLOX_MenuNavigation, state: FSMContext):
    await state.set_state(None)
    to = callback_data.to
    if to == "default":
        await throw_float_message(state, callback.message, templ.menu_text(), templ.menu_kb(), callback)
    elif to == "settings":
        await throw_float_message(state, callback.message, templ.settings_text(), templ.settings_kb(), callback)
    elif to == "profiles":
        await throw_float_message(state, callback.message, templ.profiles_text(), templ.profiles_kb(), callback)
    elif to == "blacklist":
        await throw_float_message(state, callback.message, templ.blacklist_text(), templ.blacklist_kb(), callback)
    elif to == "blacklist_items":
        await throw_float_message(state, callback.message, templ.blacklist_list_text("items"), templ.blacklist_list_kb("items"), callback)
    elif to == "blacklist_sellers":
        await throw_float_message(state, callback.message, templ.blacklist_list_text("sellers"), templ.blacklist_list_kb("sellers"), callback)
    elif to == "stats":
        await throw_float_message(state, callback.message, templ.stats_text(), templ.stats_kb(), callback)


@router.callback_query(calls.ROBLOX_ProfilesPagination.filter())
async def callback_profiles_pagination(callback: CallbackQuery, callback_data: calls.ROBLOX_ProfilesPagination, state: FSMContext):
    await state.set_state(None)
    await state.update_data(profiles_page=callback_data.page)
    await throw_float_message(state, callback.message, templ.profiles_text(), templ.profiles_kb(callback_data.page), callback)


@router.callback_query(calls.ROBLOX_ProfilePage.filter())
async def callback_profile_page(callback: CallbackQuery, callback_data: calls.ROBLOX_ProfilePage, state: FSMContext):
    await state.set_state(None)
    profile_id = callback_data.profile_id
    await state.update_data(profile_id=profile_id)
    await throw_float_message(
        state,
        callback.message,
        templ.profile_page_text(profile_id),
        templ.profile_page_kb(profile_id),
        callback
    )


@router.callback_query(calls.ROBLOX_BlacklistPagination.filter())
async def callback_blacklist_pagination(callback: CallbackQuery, callback_data: calls.ROBLOX_BlacklistPagination, state: FSMContext):
    await state.set_state(None)
    list_type = callback_data.list_type
    page = callback_data.page
    await state.update_data(blacklist_page=page)
    await throw_float_message(
        state,
        callback.message,
        templ.blacklist_list_text(list_type),
        templ.blacklist_list_kb(list_type, page),
        callback
    )


@router.callback_query(calls.ROBLOX_BlacklistItemPage.filter())
async def callback_blacklist_item_page(callback: CallbackQuery, callback_data: calls.ROBLOX_BlacklistItemPage, state: FSMContext):
    await state.set_state(None)
    await throw_float_message(
        state,
        callback.message,
        templ.blacklist_item_page_text(callback_data.list_type, callback_data.item),
        templ.blacklist_item_page_kb(callback_data.list_type, callback_data.item),
        callback
    )
