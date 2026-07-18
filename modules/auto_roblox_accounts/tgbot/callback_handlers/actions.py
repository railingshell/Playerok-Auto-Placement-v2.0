from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError

from tgbot.helpful import throw_float_message
from tgbot import templates as main_templ

from .. import templates as templ
from .. import callback_datas as calls
from .. import states
from ...settings import Settings as sett
from ...data import Data as data
from .navigation import callback_menu_navigation


router = Router()


@router.callback_query(F.data == "roblox_switch_enabled")
async def callback_switch_enabled(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    config = sett.get("config")
    config["enabled"] = not config.get("enabled", True)
    sett.set("config", config)
    return await callback_menu_navigation(callback, calls.ROBLOX_MenuNavigation(to="settings"), state)


@router.callback_query(F.data == "roblox_switch_auto_complete")
async def callback_switch_auto_complete(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    config = sett.get("config")
    config["auto_complete_deal"] = not config.get("auto_complete_deal", True)
    sett.set("config", config)
    return await callback_menu_navigation(callback, calls.ROBLOX_MenuNavigation(to="settings"), state)


@router.callback_query(F.data == "roblox_switch_profit_notifications")
async def callback_switch_profit_notifications(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    config = sett.get("config")
    config["profit_notifications"] = not config.get("profit_notifications", True)
    sett.set("config", config)
    return await callback_menu_navigation(callback, calls.ROBLOX_MenuNavigation(to="settings"), state)


@router.callback_query(F.data == "roblox_enter_lzt_token")
async def callback_enter_lzt_token(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.ROBLOX_AddProfileStates.entering_search_url)
    await state.update_data(setting_key="lzt_token")
    await throw_float_message(
        state,
        callback.message,
        templ.float_text("🔑 Введите токен LZT Market:"),
        main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="settings").pack())
    )


@router.callback_query(F.data == "roblox_enter_reserve")
async def callback_enter_reserve(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.ROBLOX_AddProfileStates.entering_search_url)
    await state.update_data(setting_key="reserve_minutes")
    await throw_float_message(
        state,
        callback.message,
        templ.float_text("⏱ Введите время резерва в минутах:"),
        main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="settings").pack())
    )


@router.callback_query(F.data == "roblox_add_profile")
async def callback_add_profile(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.ROBLOX_AddProfileStates.entering_id)
    await state.update_data(new_profile={}, edit_mode=False)
    await throw_float_message(
        state,
        callback.message,
        templ.float_text("🆔 Введите ID профиля (латиницей, без пробелов):"),
        main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
    )


@router.callback_query(F.data.startswith("roblox_delete_profile:"))
async def callback_delete_profile(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    profile_id = callback.data.split(":", 1)[1]
    profiles = data.get("profiles")
    if profile_id in profiles:
        del profiles[profile_id]
        data.set("profiles", profiles)

    config = sett.get("config")
    tag_map = config.get("tag_to_profile", {})
    for tag, mapped_id in list(tag_map.items()):
        if mapped_id == profile_id:
            del tag_map[tag]
    config["tag_to_profile"] = tag_map
    sett.set("config", config)

    return await callback_menu_navigation(callback, calls.ROBLOX_MenuNavigation(to="profiles"), state)


@router.callback_query(F.data.startswith("roblox_edit_profile:"))
async def callback_edit_profile(callback: CallbackQuery, state: FSMContext):
    profile_id = callback.data.split(":", 1)[1]
    profiles = data.get("profiles")
    profile = profiles.get(profile_id, {})
    await state.set_state(states.ROBLOX_AddProfileStates.entering_name)
    await state.update_data(
        new_profile=profile.copy(),
        edit_profile_id=profile_id,
        edit_mode=True
    )
    await throw_float_message(
        state,
        callback.message,
        templ.float_text(f"✏️ Редактирование профиля <code>{profile_id}</code>.\\nВведите новое название:"),
        main_templ.back_kb(calls.ROBLOX_ProfilePage(profile_id=profile_id).pack())
    )


@router.callback_query(F.data == "roblox_add_blacklist_item")
async def callback_add_blacklist_item(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.ROBLOX_BlacklistStates.entering_item)
    await throw_float_message(
        state,
        callback.message,
        templ.float_text("🛍 Введите ID товара для добавления в чёрный список:"),
        main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="blacklist_items").pack())
    )


@router.callback_query(F.data == "roblox_add_blacklist_seller")
async def callback_add_blacklist_seller(callback: CallbackQuery, state: FSMContext):
    await state.set_state(states.ROBLOX_BlacklistStates.entering_seller)
    await throw_float_message(
        state,
        callback.message,
        templ.float_text("👤 Введите имя продавца для добавления в чёрный список:"),
        main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="blacklist_sellers").pack())
    )


@router.callback_query(F.data.startswith("roblox_delete_blacklist:"))
async def callback_delete_blacklist(callback: CallbackQuery, state: FSMContext):
    await state.set_state(None)
    parts = callback.data.split(":")
    if len(parts) < 3:
        return
    list_type = parts[1]
    item = ":".join(parts[2:])
    config = sett.get("config")
    blacklist = config.get("blacklist", {})
    items = blacklist.get(list_type, [])
    if item in items:
        items.remove(item)
    blacklist[list_type] = items
    config["blacklist"] = blacklist
    sett.set("config", config)
    return await callback_menu_navigation(callback, calls.ROBLOX_MenuNavigation(to=f"blacklist_{list_type}"), state)


async def handle_action_error(callback: CallbackQuery, state: FSMContext, e: Exception, back_cb: str):
    if e is TelegramAPIError:
        return
    await throw_float_message(
        state,
        callback.message,
        templ.float_text(f"❌ Ошибка: {e}"),
        main_templ.back_kb(back_cb)
    )
