import re
import time
import json
import traceback
import base64
from logging import getLogger

from playerokapi.enums import ItemDealStatuses
from playerokapi.listener.events import NewDealEvent, NewMessageEvent

from ..meta import PREFIX, NAME
from ..data import Data as data
from ..settings import Settings as sett
from ..settings import DATA as SETTINGS_DATA
from ..steam_utils import parse_mafile, get_shared_secret, generate_steam_guard_code
from plbot.playerokbot import get_playerok_bot


logger = getLogger(f"{NAME}.playerok")

config = sett.get("config")
messages = sett.get("messages")

accounts = data.get("accounts")
activations = data.get("activations")
stats = data.get("stats")

STEAMGUARD_RE = re.compile(r"!sg\s+(\S+)", re.IGNORECASE)


def msg(message_name: str, **kwargs) -> str | None:
    return get_playerok_bot().msg(message_name, "messages", SETTINGS_DATA, **kwargs)


def get_free_account() -> dict | None:
    for acc in accounts:
        if acc.get("status") == "free":
            return acc
    return None


def find_activation(deal_id: str) -> dict | None:
    for a in activations:
        if a.get("deal_id") == deal_id:
            return a
    return None


def send_mafile_as_document(plbot, chat_id: str, account: dict):
    """Отправляет maFile как документ в чат Playerok, если возможно."""
    mafile_raw = account.get("mafile", "")
    if not mafile_raw:
        return None
    if isinstance(mafile_raw, dict):
        mafile_bytes = json.dumps(mafile_raw, ensure_ascii=False, indent=2).encode("utf-8")
    elif isinstance(mafile_raw, str):
        try:
            mafile_bytes = base64.b64decode(mafile_raw)
        except Exception:
            mafile_bytes = mafile_raw.encode("utf-8")
    else:
        mafile_bytes = mafile_raw

    filename = f"{account.get('login', 'account')}.maFile"
    try:
        return plbot.send_message(chat_id, text=None, images=[(filename, mafile_bytes)])
    except Exception as e:
        logger.error(f"{PREFIX} Не удалось отправить maFile: {e}")
        return None


def process_new_deal(plbot, event: NewDealEvent):
    deal = event.deal
    if not config.get("enabled", True):
        return

    plbot.send_message(
        deal.chat.id if deal.chat else deal.id,
        msg("order_wait")
    )

    account = get_free_account()
    if not account:
        logger.info(f"{PREFIX} Нет свободных аккаунтов для сделки {deal.id}")
        text = msg("no_account_available")
        if text:
            plbot.send_message(deal.chat.id if deal.chat else deal.id, text)
        refund_deal(plbot, deal.id, "Нет свободных аккаунтов")
        return

    existing = find_activation(deal.id)
    if existing:
        text = msg("already_activated")
        if text:
            plbot.send_message(deal.chat.id if deal.chat else deal.id, text)
        return

    account["status"] = "used"
    account["deal_id"] = deal.id
    data.set("accounts", accounts)

    max_codes = config.get("max_codes_per_activation", 3)
    activations.append({
        "deal_id": deal.id,
        "account_login": account.get("login"),
        "codes_left": max_codes,
        "last_code_time": 0,
        "price": deal.item.price
    })
    data.set("activations", activations)

    text = msg(
        "activation_delivered",
        login=account.get("login", ""),
        password=account.get("password", ""),
        deal_id=deal.id,
        codes_left=max_codes
    )
    if text:
        plbot.send_message(deal.chat.id if deal.chat else deal.id, text)

    send_mafile_as_document(plbot, deal.chat.id if deal.chat else deal.id, account)

    if config.get("auto_complete_deal", True):
        try:
            time.sleep(1)
            plbot.account.update_deal(deal.id, ItemDealStatuses.SENT)
        except Exception as e:
            logger.error(f"{PREFIX} Ошибка подтверждения сделки {deal.id}: {e}")

    stats["activated"] = stats.get("activated", 0) + 1
    stats["profit"] = stats.get("profit", 0) + (deal.item.price or 0)
    data.set("stats", stats)


def handle_steamguard_command(plbot, event: NewMessageEvent):
    text = (event.message.text or "").strip()
    match = STEAMGUARD_RE.search(text)
    if not match:
        return

    deal_id = match.group(1)
    activation = find_activation(deal_id)
    if not activation:
        return

    if activation.get("codes_left", 0) <= 0:
        plbot.send_message(event.chat.id, msg("steamguard_limit"))
        return

    cooldown = config.get("code_cooldown_seconds", 30)
    now = time.time()
    if now - activation.get("last_code_time", 0) < cooldown:
        return

    account = next((a for a in accounts if a.get("login") == activation.get("account_login")), None)
    if not account:
        return

    try:
        mafile = parse_mafile(account.get("mafile", "{}"))
        shared_secret = get_shared_secret(mafile)
        code = generate_steam_guard_code(shared_secret)
    except Exception as e:
        logger.error(f"{PREFIX} Ошибка генерации Steam Guard: {e}")
        return

    activation["codes_left"] = activation.get("codes_left", 3) - 1
    activation["last_code_time"] = now
    data.set("activations", activations)

    plbot.send_message(
        event.chat.id,
        msg(
            "steamguard_code",
            code=code,
            codes_left=activation["codes_left"]
        )
    )


def refund_deal(plbot, deal_id: str, reason: str):
    try:
        plbot.account.update_deal(deal_id, ItemDealStatuses.ROLLED_BACK)
        logger.info(f"{PREFIX} Сделка {deal_id} возвращена. Причина: {reason}")
        text = msg("rental_refunded", deal_id=deal_id, reason=reason)
        if text:
            plbot.send_message(deal_id, text)
        stats["refunded"] = stats.get("refunded", 0) + 1
        data.set("stats", stats)
    except Exception as e:
        logger.error(f"{PREFIX} Ошибка возврата сделки {deal_id}: {e}")


def run_cycles(_):
    pass


def stop_cycles(_):
    pass


async def on_new_deal(plbot, event: NewDealEvent):
    try:
        if event.deal.user.id == plbot.playerok_account.id:
            return
        if not config.get("enabled", True):
            return
        process_new_deal(plbot, event)
    except Exception:
        logger.error(f"{PREFIX} Ошибка в on_new_deal: {traceback.format_exc()}")


async def on_new_message(plbot, event: NewMessageEvent):
    if event.message.user.id == plbot.playerok_account.id:
        return
    if not config.get("enabled", True):
        return
    if event.message.text is None:
        return
    try:
        handle_steamguard_command(plbot, event)
    except Exception:
        logger.error(f"{PREFIX} Ошибка в on_new_message: {traceback.format_exc()}")


async def on_module_enabled(module):
    from .. import set_module
    set_module(module)
    logger.info(f"{PREFIX} Модуль подключен и активен")


async def on_module_disabled(_):
    pass


async def on_telegram_bot_init(telegram_bot):
    from ..tgbot._handlers import on_telegram_bot_init as _tg_init
    await _tg_init(telegram_bot)
