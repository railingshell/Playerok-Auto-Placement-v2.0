from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.helpful import throw_float_message

from .. import templates as templ
from .. import callback_datas as calls


router = Router()


@router.callback_query(calls.STEAMRENT_MenuNavigation.filter())
async def callback_menu_navigation(callback: CallbackQuery, callback_data: calls.STEAMRENT_MenuNavigation, state: FSMContext):
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
    elif to == "accounts_rented":
        await throw_float_message(state, callback.message, templ.accounts_text("rented"), templ.accounts_kb("rented"), callback)
    elif to == "stats":
        await throw_float_message(state, callback.message, templ.stats_text(), templ.stats_kb(), callback)


@router.callback_query(calls.STEAMRENT_AccountsPagination.filter())
async def callback_accounts_pagination(callback: CallbackQuery, callback_data: calls.STEAMRENT_AccountsPagination, state: FSMContext):
    await state.set_state(None)
    await state.update_data(accounts_page=callback_data.page, accounts_status=callback_data.status)
    await throw_float_message(
        state,
        callback.message,
        templ.accounts_text(callback_data.status),
        templ.accounts_kb(callback_data.status, callback_data.page),
        callback
    )


@router.callback_query(calls.STEAMRENT_AccountPage.filter())
async def callback_account_page(callback: CallbackQuery, callback_data: calls.STEAMRENT_AccountPage, state: FSMContext):
    await state.set_state(None)
    await state.update_data(account_login=callback_data.login)
    await throw_float_message(
        state,
        callback.message,
        templ.account_page_text(callback_data.login),
        templ.account_page_kb(callback_data.login),
        callback
    )
