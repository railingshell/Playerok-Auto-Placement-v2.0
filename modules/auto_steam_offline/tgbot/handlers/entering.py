import json
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


@router.message(states.STEAMOFF_AddAccountStates.entering_login, F.text)
async def handler_entering_login(message: types.Message, state: FSMContext):
    try:
        login = message.text.strip()
        if not login:
            raise Exception("❌ Логин не может быть пустым")
        await state.update_data(new_account={"login": login})
        await state.set_state(states.STEAMOFF_AddAccountStates.entering_password)
        await throw_float_message(
            state,
            message,
            templ.float_text("🔑 Введите пароль Steam-аккаунта:"),
            main_templ.back_kb(calls.STEAMOFF_MenuNavigation(to="accounts").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.STEAMOFF_MenuNavigation(to="accounts").pack())
            )


@router.message(states.STEAMOFF_AddAccountStates.entering_password, F.text)
async def handler_entering_password(message: types.Message, state: FSMContext):
    try:
        password = message.text.strip()
        if not password:
            raise Exception("❌ Пароль не может быть пустым")
        state_data = await state.get_data()
        new_account = state_data.get("new_account", {})
        new_account["password"] = password
        await state.update_data(new_account=new_account)
        await state.set_state(states.STEAMOFF_AddAccountStates.entering_mafile)
        await throw_float_message(
            state,
            message,
            templ.float_text("📎 Пришлите файл .maFile или вставьте его содержимое сообщением:"),
            main_templ.back_kb(calls.STEAMOFF_MenuNavigation(to="accounts").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.STEAMOFF_MenuNavigation(to="accounts").pack())
            )


@router.message(states.STEAMOFF_AddAccountStates.entering_mafile)
async def handler_entering_mafile(message: types.Message, state: FSMContext):
    try:
        mafile_data = None
        if message.document:
            file_id = message.document.file_id
            from tgbot.telegrambot import get_telegram_bot
            bot = get_telegram_bot().bot
            file = await bot.download(file_id)
            mafile_data = file.read().decode("utf-8", errors="ignore")
        elif message.text:
            mafile_data = message.text.strip()
        else:
            raise Exception("❌ Пришлите файл .maFile или его содержимое")

        try:
            parsed = json.loads(mafile_data)
        except Exception:
            raise Exception("❌ Невалидный JSON в maFile") from None

        state_data = await state.get_data()
        new_account = state_data.get("new_account", {})
        new_account["mafile"] = parsed
        new_account["status"] = "free"

        accounts = data.get("accounts")
        if any(a.get("login") == new_account["login"] for a in accounts):
            raise Exception("❌ Аккаунт с таким логином уже существует")

        accounts.append(new_account)
        data.set("accounts", accounts)

        await state.set_state(None)
        await throw_float_message(
            state,
            message,
            templ.float_text(f"✅ Аккаунт <code>{new_account['login']}</code> добавлен"),
            main_templ.back_kb(calls.STEAMOFF_MenuNavigation(to="accounts").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.STEAMOFF_MenuNavigation(to="accounts").pack())
            )


@router.message(states.STEAMOFF_SettingsStates.entering_max_codes, F.text)
async def handler_entering_max_codes(message: types.Message, state: FSMContext):
    try:
        value = message.text.strip()
        if not value.isdigit() or int(value) < 1:
            raise Exception("❌ Введите целое число больше 0")
        config = sett.get("config")
        config["max_codes_per_activation"] = int(value)
        sett.set("config", config)
        await state.set_state(None)
        await throw_float_message(
            state,
            message,
            templ.float_text("✅ Максимальное количество кодов обновлено"),
            main_templ.back_kb(calls.STEAMOFF_MenuNavigation(to="settings").pack())
        )
    except Exception as e:
        if e is not TelegramAPIError:
            await throw_float_message(
                state,
                message,
                templ.float_text(str(e)),
                main_templ.back_kb(calls.STEAMOFF_MenuNavigation(to="settings").pack())
            )
