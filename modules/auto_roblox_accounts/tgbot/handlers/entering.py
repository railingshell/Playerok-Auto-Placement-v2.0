from aiogram import F, types, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext

from tgbot.helpful import throw_float_message
from tgbot import templates as main_templ

from .. import templates as templ
from .. import states
from .. import callback_datas as calls
from ...settings import Settings as sett
from ...data import Data as data


router = Router()


@router.message(states.ROBLOX_AddProfileStates.entering_id, F.text)
async def handler_entering_profile_id(message: types.Message, state: FSMContext):
    try:
        profile_id = message.text.strip().lower().replace(" ", "_")
        if not profile_id:
            raise Exception("❌ ID не может быть пустым")
        profiles = data.get("profiles")
        if profile_id in profiles:
            raise Exception("❌ Профиль с таким ID уже существует")

        await state.update_data(new_profile={"id": profile_id}, edit_profile_id=profile_id)
        await state.set_state(states.ROBLOX_AddProfileStates.entering_name)
        await throw_float_message(
            state,
            message,
            templ.float_text("📝 Введите название профиля:"),
            main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
            )


@router.message(states.ROBLOX_AddProfileStates.entering_name, F.text)
async def handler_entering_profile_name(message: types.Message, state: FSMContext):
    try:
        name = message.text.strip()
        if not name:
            raise Exception("❌ Название не может быть пустым")
        state_data = await state.get_data()
        new_profile = state_data.get("new_profile", {})
        new_profile["name"] = name
        await state.update_data(new_profile=new_profile)
        await state.set_state(states.ROBLOX_AddProfileStates.entering_search_url)
        await throw_float_message(
            state,
            message,
            templ.float_text("🔗 Введите URL поиска LZT Market для этого профиля:"),
            main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
            )


@router.message(states.ROBLOX_AddProfileStates.entering_search_url, F.text)
async def handler_entering_profile_url(message: types.Message, state: FSMContext):
    try:
        url = message.text.strip()
        if not url.startswith("http"):
            raise Exception("❌ URL должен начинаться с http/https")
        state_data = await state.get_data()
        new_profile = state_data.get("new_profile", {})
        new_profile["search_url"] = url
        await state.update_data(new_profile=new_profile)

        setting_key = state_data.get("setting_key")
        if setting_key == "lzt_token":
            config = sett.get("config")
            config["lzt"]["token"] = url
            sett.set("config", config)
            await state.set_state(None)
            return await throw_float_message(
                state,
                message,
                templ.float_text("✅ Токен LZT сохранён"),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="settings").pack())
            )
        elif setting_key == "reserve_minutes":
            if not url.isdigit():
                raise Exception("❌ Введите число")
            config = sett.get("config")
            config["reserve_minutes"] = int(url)
            sett.set("config", config)
            await state.set_state(None)
            return await throw_float_message(
                state,
                message,
                templ.float_text("✅ Резерв обновлён"),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="settings").pack())
            )

        await state.set_state(states.ROBLOX_AddProfileStates.entering_min_profit)
        await throw_float_message(
            state,
            message,
            templ.float_text("💰 Введите минимальный профит в ₽ (цена Playerok минус цена LZT):"),
            main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
            )


@router.message(states.ROBLOX_AddProfileStates.entering_min_profit, F.text)
async def handler_entering_profile_profit(message: types.Message, state: FSMContext):
    try:
        profit = message.text.strip()
        if not profit.isdigit():
            raise Exception("❌ Введите число")
        state_data = await state.get_data()
        new_profile = state_data.get("new_profile", {})
        new_profile["min_profit"] = int(profit)
        await state.update_data(new_profile=new_profile)
        await state.set_state(states.ROBLOX_AddProfileStates.entering_tag)
        await throw_float_message(
            state,
            message,
            templ.float_text("🏷 Введите тег(и) через запятую без <code>roblox:</code> (например: tag1, tag2):"),
            main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
            )


@router.message(states.ROBLOX_AddProfileStates.entering_tag, F.text)
async def handler_entering_profile_tag(message: types.Message, state: FSMContext):
    try:
        tags_text = message.text.strip()
        tags = [t.strip().lower() for t in tags_text.split(",") if t.strip()]
        if not tags:
            raise Exception("❌ Введите хотя бы один тег")

        state_data = await state.get_data()
        new_profile = state_data.get("new_profile", {})
        profile_id = state_data.get("edit_profile_id", new_profile.get("id"))
        edit_mode = state_data.get("edit_mode", False)

        profiles = data.get("profiles")
        if edit_mode and profile_id in profiles:
            old_profile = profiles[profile_id]
            new_profile["id"] = profile_id
            new_profile.setdefault("login", old_profile.get("login", ""))
            new_profile.setdefault("password", old_profile.get("password", ""))
        profiles[profile_id] = new_profile
        data.set("profiles", profiles)

        config = sett.get("config")
        tag_map = config.get("tag_to_profile", {})
        for tag in tags:
            tag_map[tag] = profile_id
        config["tag_to_profile"] = tag_map
        sett.set("config", config)

        await state.set_state(None)
        await throw_float_message(
            state,
            message,
            templ.float_text(f"✅ Профиль <code>{profile_id}</code> сохранён.\nТеги: {', '.join(tags)}"),
            main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="profiles").pack())
            )


@router.message(states.ROBLOX_BlacklistStates.entering_item, F.text)
async def handler_entering_blacklist_item(message: types.Message, state: FSMContext):
    try:
        item = message.text.strip()
        if not item:
            raise Exception("❌ ID товара не может быть пустым")
        config = sett.get("config")
        blacklist = config.setdefault("blacklist", {})
        items = set(blacklist.get("items", []))
        items.add(item)
        blacklist["items"] = list(items)
        config["blacklist"] = blacklist
        sett.set("config", config)
        await state.set_state(None)
        await throw_float_message(
            state,
            message,
            templ.float_text(f"✅ Товар <code>{item}</code> добавлен в чёрный список"),
            main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="blacklist_items").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="blacklist_items").pack())
            )


@router.message(states.ROBLOX_BlacklistStates.entering_seller, F.text)
async def handler_entering_blacklist_seller(message: types.Message, state: FSMContext):
    try:
        seller = message.text.strip()
        if not seller:
            raise Exception("❌ Имя продавца не может быть пустым")
        config = sett.get("config")
        blacklist = config.setdefault("blacklist", {})
        sellers = set(blacklist.get("sellers", []))
        sellers.add(seller)
        blacklist["sellers"] = list(sellers)
        config["blacklist"] = blacklist
        sett.set("config", config)
        await state.set_state(None)
        await throw_float_message(
            state,
            message,
            templ.float_text(f"✅ Продавец <code>{seller}</code> добавлен в чёрный список"),
            main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="blacklist_sellers").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.ROBLOX_MenuNavigation(to="blacklist_sellers").pack())
            )
