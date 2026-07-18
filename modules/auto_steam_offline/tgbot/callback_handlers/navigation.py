from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.helpful import throw_float_message

from .. import templates as templ
from .. import callback_datas as calls


router = Router()


@router.callback_query(calls.STEAMOFF_MenuNavigation.filter())
async def callback_menu_navigation(callback: CallbackQuery, callback_data: calls.STEAMOFF_MenuNavigation, state: FSMContext):
    await state.set_state(None)
    to = callback_data.to
    if to == "default":
        await throw_float_message(state, callback.message, templ.menu_text(), templ.menu_kb(), callback)
    elif to == "settings":
        await throw_float_message(state, callback.message, templ.settings_text(), templ.settings_kb(), callback)
    elif to == "accounts":
        await throw_float_message(state, callback.message, templ.accounts_text(), templ.accounts_kb(), callback)
    elif to == "accounts_free":
        await throw_float_message(state, callback.message, templ.accounts_text("free"), templ.accounts_kb("free"), callback)
    elif to == "accounts_used":
        await throw_float_message(state, callback.message, templ.accounts_text("used"), templ.accounts_kb("used"), callback)
    elif to == "stats":
        await throw_float_message(state, callback.message, templ.stats_text(), templ.stats_kb(), callback)


@router.callback_query(calls.STEAMOFF_AccountsPagination.filter())
async def callback_accounts_pagination(callback: CallbackQuery, callback_data: calls.STEAMOFF_AccountsPagination, state: FSMContext):
    await throw_float_message(
        state,
        callback.message,
        templ.accounts_text(callback_data.status),
        templ.accounts_kb(callback_data.status, callback_data.page),
        callback
    )


@router.callback_query(calls.STEAMOFF_AccountPage.filter())
async def callback_account_page(callback: CallbackQuery, callback_data: calls.STEAMOFF_AccountPage, state: FSMContext):
    await state.set_state(None)
    await throw_float_message(
        state,
        callback.message,
        templ.account_page_text(callback_data.login),
        templ.account_page_kb(callback_data.login),
        callback
    )
