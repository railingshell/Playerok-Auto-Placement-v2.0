from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from tgbot.helpful import throw_float_message
from tgbot import templates as main_templ

from .. import templates as templ
from .. import callback_datas as calls
from .. import states
from ...settings import Settings as sett
from ...data import Data as data
from .navigation import callback_menu_navigation


router = Router()


@router.callback_query(F.data == "steamrent_switch_enabled")
async def callback_switch_enabled(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    config = sett.get("config")
    config["enabled"] = not config.get("enabled", True)
    sett.set("config", config)
    return await callback_menu_navigation(callback, calls.STEAMRENT_MenuNavigation(to="settings"), state)


@router.callback_query(F.data == "steamrent_switch_auto_complete")
async def callback_switch_auto_complete(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    config = sett.get("config")
    config["auto_complete_deal"] = not config.get("auto_complete_deal", True)
    sett.set("config", config)
    return await callback_menu_navigation(callback, calls.STEAMRENT_MenuNavigation(to="settings"), state)


@router.callback_query(F.data == "steamrent_switch_profit_notifications")
async def callback_switch_profit_notifications(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    config = sett.get("config")
    config["profit_notifications"] = not config.get("profit_notifications", True)
    sett.set("config", config)
    return await callback_menu_navigation(callback, calls.STEAMRENT_MenuNavigation(to="settings"), state)


@router.callback_query(F.data == "steamrent_enter_duration")
async def callback_enter_duration(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.STEAMRENT_SettingsStates.entering_duration)
    await throw_float_message(
        state,
        callback.message,
        templ.float_text("⏱ Введите длительность аренды в часах:"),
        main_templ.back_kb(calls.STEAMRENT_MenuNavigation(to="settings").pack())
    )


@router.callback_query(F.data == "steamrent_enter_api_key")
async def callback_enter_api_key(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.STEAMRENT_SettingsStates.entering_api_key)
    await throw_float_message(
        state,
        callback.message,
        templ.float_text("🔑 Введите Steam API ключ (для смены пароля):"),
        main_templ.back_kb(calls.STEAMRENT_MenuNavigation(to="settings").pack())
    )


@router.callback_query(F.data == "steamrent_add_account")
async def callback_add_account(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.STEAMRENT_AddAccountStates.entering_login)
    await state.update_data(new_account={})
    await throw_float_message(
        state,
        callback.message,
        templ.float_text("🆔 Введите логин Steam-аккаунта:"),
        main_templ.back_kb(calls.STEAMRENT_MenuNavigation(to="accounts").pack())
    )


@router.callback_query(F.data.startswith("steamrent_delete_account:"))
async def callback_delete_account(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    login = callback.data.split(":", 1)[1]
    accounts = data.get("accounts")
    accounts = [a for a in accounts if a.get("login") != login]
    data.set("accounts", accounts)
    return await callback_menu_navigation(callback, calls.STEAMRENT_MenuNavigation(to="accounts"), state)
