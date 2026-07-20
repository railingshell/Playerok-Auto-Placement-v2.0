from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup, 
    Message, 
    CallbackQuery, 
    InputMediaPhoto, 
    FSInputFile
)
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest

from logging import getLogger

from settings import Settings as sett

from . import templates as templ


logger = getLogger("universal.telegram")


async def is_subscribed(user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на обязательный канал.

    - Если функция выключена или канал не задан — доступ открыт.
    - Авторизованные пользователи (signed_users, т.е. владелец) НЕ гейтятся —
      чтобы не запереть себя даже при неверной настройке.
    - Для остальных: при ошибке проверки (бот не админ канала, неверный @канал)
      доступ закрыт (fail-closed) — гейт показывается. Для прохождения гейта бот
      должен быть администратором канала.
    """
    config = sett.get("config")
    fs = config["telegram"]["bot"].get("forced_subscription", {})
    if not fs.get("enabled") or not fs.get("channel"):
        logger.info(
            f"[подписка] пропуск user={user_id}: функция выключена или канал не задан "
            f"(enabled={fs.get('enabled')}, channel={fs.get('channel')!r})"
        )
        return True

    # Владелец/авторизованные — всегда пропускаем (нет риска самоблокировки)
    if user_id in config["telegram"]["bot"].get("signed_users", []):
        logger.info(f"[подписка] пропуск user={user_id}: авторизован (signed_users)")
        return True

    from .telegrambot import get_telegram_bot
    bot = get_telegram_bot().bot
    try:
        member = await bot.get_chat_member(fs["channel"], user_id)
        subscribed = member.status not in ("left", "kicked")
        logger.info(
            f"[подписка] user={user_id} канал={fs['channel']} статус={member.status} "
            f"подписан={subscribed}"
        )
        return subscribed
    except Exception as e:
        logger.warning(
            f"[подписка] НЕ удалось проверить {fs['channel']} для user={user_id} — "
            f"бот должен быть администратором канала, а канал указан как @юзернейм: {e}"
        )
        return False


async def _subscription_channel_info() -> tuple[str, str]:
    """Возвращает (название, ссылка) обязательного канала для отображения."""
    config = sett.get("config")
    channel = config["telegram"]["bot"]["forced_subscription"].get("channel", "")
    username = channel.lstrip("@")
    name = username or "канал"
    url = f"https://t.me/{username}" if username and not channel.startswith("-") else ""

    from .telegrambot import get_telegram_bot
    try:
        chat = await get_telegram_bot().bot.get_chat(channel)
        name = chat.title or name
        if chat.username:
            url = f"https://t.me/{chat.username}"
    except Exception:
        pass
    return name, url


async def show_subscription_gate(message: Message, state: FSMContext, callback: CallbackQuery = None) -> Message | None:
    """Показывает экран «Требуется подписка»."""
    name, url = await _subscription_channel_info()
    return await throw_float_message(
        state=state,
        message=message,
        text=templ.subscription_required_text(name),
        reply_markup=templ.subscription_required_kb(name, url),
        callback=callback
    )


async def do_auth(message: Message, state: FSMContext) -> Message | None:
    from . import states

    await state.set_state(states.SystemStates.waiting_for_password)
    return await throw_float_message(
        state=state,
        message=message,
        text=templ.sign_text(
            "🔑 Введите <b>ключ-пароль</b>, указанный вами в конфиге бота:"
            '\n\n<span class="tg-spoiler">Если вы забыли, его можно посмотреть напрямую в конфиге по пути bot_settings/config.json, параметр password в разделе telegram.bot</span>'
        ),
        reply_markup=templ.destroy_kb()
    )


async def get_accent_message_id(state: FSMContext, message: Message, bot) -> int | None:
    data = await state.get_data()

    if message.from_user and message.from_user.id != bot.id:
        return data.get("accent_message_id")

    return message.message_id


def need_new_message(message: Message, bot, send: bool) -> bool:
    if send:
        return True
    
    if message.text and message.from_user.id != bot.id:
        return message.text.startswith('/')

    return False


async def try_edit_message(bot, chat_id, message_id, text, photo, reply_markup, callback, **kwargs):
    try:
        if photo:
            media = InputMediaPhoto(
                media=FSInputFile(photo),
                caption=text,
                parse_mode="HTML"
            )
            return await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=reply_markup,
                **kwargs
            )
        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
            **kwargs
        )

    except TelegramAPIError as e:
        msg = e.message.lower()

        if "message to edit not found" in msg:
            return None

        if "message is not modified" in msg:
            if callback:
                await bot.answer_callback_query(callback.id, cache_time=0)
            return "not_modified"

        if "query is too old" in msg:
            return "callback_expired"

        raise


async def send_new_message(bot, chat_id, text, photo, reply_markup, reply_to, **kwargs):
    if photo:
        return await bot.send_photo(
            chat_id=chat_id,
            photo=FSInputFile(photo),
            caption=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
            **kwargs
        )
    return await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML",
        reply_to_message_id=reply_to,
        **kwargs
    )


async def throw_float_message(
    state: FSMContext,
    message: Message,
    text: str = None,
    reply_markup: InlineKeyboardMarkup = None,
    callback: CallbackQuery = None,
    photo: str = None,
    send: bool = False,
    reply_to: int = None,
    **kwargs
) -> Message | None:
    
    if not text and not photo:
        return None

    from .telegrambot import get_telegram_bot
    bot = get_telegram_bot().bot

    accent_id = await get_accent_message_id(state, message, bot)
    new_message_needed = need_new_message(message, bot, bool(send or reply_to))

    mess = None

    if accent_id and not new_message_needed:
        mess = await try_edit_message(
            bot=bot,
            chat_id=message.chat.id,
            message_id=accent_id,
            text=text,
            photo=photo,
            reply_markup=reply_markup,
            callback=callback,
            **kwargs
        )

        if message.from_user.id != bot.id: 
            try: 
                await bot.delete_message(message.chat.id, message.message_id)
            except TelegramBadRequest: 
                pass

        if mess in ("not_modified", "callback_expired"):
            return None

    if not mess:
        mess = await send_new_message(
            bot=bot,
            chat_id=message.chat.id,
            text=text,
            photo=photo,
            reply_markup=reply_markup,
            reply_to=reply_to,
            **kwargs
        )

    if callback:
        await bot.answer_callback_query(callback.id, cache_time=0)

    if mess:
        await state.update_data(accent_message_id=mess.message_id)

    return mess