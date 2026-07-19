import re
import time
import json
import traceback
import base64
from logging import getLogger
from threading import Thread, Event as ThreadingEvent
from datetime import datetime, timedelta

from playerokapi.enums import ItemDealStatuses
from playerokapi.listener.events import NewDealEvent, NewMessageEvent, NewReviewEvent

from ..meta import PREFIX, NAME
from ..data import Data as data
from ..settings import Settings as sett
from ..settings import DATA as SETTINGS_DATA
from ..steam_utils import parse_mafile, get_shared_secret, generate_steam_guard_code, change_steam_password
from plbot.playerokbot import get_playerok_bot


logger = getLogger(f"{NAME}.playerok")

config = sett.get("config")
messages = sett.get("messages")

accounts = data.get("accounts")
rentals = data.get("rentals")
stats = data.get("stats")

stop_cycles_event = ThreadingEvent()
__active_funcs = {}

STEAMGUARD_RE = re.compile(r"!steamguard\s+(\S+)", re.IGNORECASE)


def msg(message_name: str, **kwargs) -> str | None:
    return get_playerok_bot().msg(message_name, "messages", SETTINGS_DATA, **kwargs)


def get_free_account() -> dict | None:
    for acc in accounts:
        if acc.get("status") == "free":
            return acc
    return None


def find_rental(deal_id: str) -> dict | None:
    for r in rentals:
        if r.get("deal_id") == deal_id:
            return r
    return None


def send_admin_notification(text: str):
    chat_id = config.get("admin_chat_id", "")
    if not chat_id:
        return
    try:
        plbot = get_playerok_bot()
        plbot.send_message(str(chat_id), text, exclude_watermark=True)
    except Exception as e:
        logger.error(f"{PREFIX} Ошибка уведомления админу: {e}")


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

    account["status"] = "reserved"
    account["deal_id"] = deal.id
    data.set("accounts", accounts)

    rentals.append({
        "deal_id": deal.id,
        "account_login": account.get("login"),
        "started_at": None,
        "expires_at": None,
        "status": "reserved",
        "guard_codes_left": config.get("rental", {}).get("max_guard_codes_per_rental", 5),
        "last_code_time": 0,
        "price": deal.item.price
    })
    data.set("rentals", rentals)

    text = msg(
        "account_delivered",
        login=account.get("login", ""),
        password=account.get("password", ""),
        deal_id=deal.id,
        duration_hours=config.get("rental", {}).get("duration_hours", 24)
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


def handle_steamguard_command(plbot, event: NewMessageEvent):
    text = (event.message.text or "").strip()
    match = STEAMGUARD_RE.search(text)
    if not match:
        return

    deal_id = match.group(1)
    rental = find_rental(deal_id)
    if not rental:
        return

    if rental.get("status") == "reserved":
        rental["status"] = "active"
        rental["started_at"] = datetime.now().isoformat()
        rental["expires_at"] = (
            datetime.now() + timedelta(hours=config.get("rental", {}).get("duration_hours", 24))
        ).isoformat()
        data.set("rentals", rentals)

        account = next((a for a in accounts if a.get("login") == rental.get("account_login")), None)
        if account:
            account["status"] = "rented"
            data.set("accounts", accounts)

        stats["rented"] = stats.get("rented", 0) + 1
        stats["profit"] = stats.get("profit", 0) + (rental.get("price") or 0)
        data.set("stats", stats)

        start_text = msg(
            "rental_started",
            expires_at=rental["expires_at"]
        )
        if start_text:
            plbot.send_message(event.chat.id, start_text)

    if rental.get("guard_codes_left", 0) <= 0:
        plbot.send_message(event.chat.id, msg("steamguard_limit"))
        return

    cooldown = config.get("rental", {}).get("guard_code_cooldown_seconds", 30)
    now = time.time()
    if now - rental.get("last_code_time", 0) < cooldown:
        return

    account = next((a for a in accounts if a.get("login") == rental.get("account_login")), None)
    if not account:
        return

    try:
        mafile = parse_mafile(account.get("mafile", "{}"))
        shared_secret = get_shared_secret(mafile)
        code = generate_steam_guard_code(shared_secret)
    except Exception as e:
        logger.error(f"{PREFIX} Ошибка генерации Steam Guard: {e}")
        return

    rental["guard_codes_left"] = rental.get("guard_codes_left", 5) - 1
    rental["last_code_time"] = now
    data.set("rentals", rentals)

    plbot.send_message(
        event.chat.id,
        msg(
            "steamguard_code",
            code=code,
            codes_left=rental["guard_codes_left"]
        )
    )


def handle_review(plbot, event: NewReviewEvent):
    deal = event.deal
    rental = find_rental(deal.id)
    if not rental:
        return
    if rental.get("status") != "active" or not rental.get("expires_at"):
        return

    bonus = config.get("rental", {}).get("bonus_minutes_for_review", 60)
    expires = datetime.fromisoformat(rental["expires_at"])
    rental["expires_at"] = (expires + timedelta(minutes=bonus)).isoformat()
    data.set("rentals", rentals)

    text = msg(
        "review_bonus",
        bonus_minutes=bonus,
        expires_at=rental["expires_at"]
    )
    if text:
        plbot.send_message(deal.chat.id if deal.chat else deal.id, text)


def expire_rentals():
    """Фоновая проверка истёкших аренд. Возвращает аккаунты в пул и меняет пароль."""
    now = datetime.now()
    for rental in list(rentals):
        if rental.get("status") != "active":
            continue
        expires_at = rental.get("expires_at")
        if not expires_at:
            continue
        try:
            expires = datetime.fromisoformat(expires_at)
        except Exception:
            continue
        if now < expires:
            continue

        account = next((a for a in accounts if a.get("login") == rental.get("account_login")), None)
        if account:
            new_password = f"Pass{int(time.time())}"
            try:
                change_steam_password(
                    account.get("login", ""),
                    account.get("password", ""),
                    new_password,
                    api_key=config.get("steam", {}).get("api_key", ""),
                    proxy=config.get("steam", {}).get("proxy") or None
                )
                account["password"] = new_password
            except Exception as e:
                logger.error(f"{PREFIX} Ошибка смены пароля {account.get('login')}: {e}")
            account["status"] = "free"
            account.pop("deal_id", None)
            data.set("accounts", accounts)

        rental["status"] = "expired"
        data.set("rentals", rentals)

        plbot = get_playerok_bot()
        if plbot:
            text = msg("rental_expired")
            if text:
                try:
                    plbot.send_message(rental.get("deal_id"), text)
                except Exception as e:
                    logger.warning(f"{PREFIX} Не удалось отправить сообщение об окончании аренды: {e}")


def run_in_thread_safe(func: callable, sleep_after_seconds: float = 0,
                       sleep_before_seconds: float = 0):
    global __active_funcs
    if __active_funcs.get(func) is True:
        return

    import time as _time

    def run():
        __active_funcs[func] = True
        if sleep_before_seconds > 0:
            _time.sleep(sleep_before_seconds)
        try:
            func()
        finally:
            if sleep_after_seconds > 0:
                _time.sleep(sleep_after_seconds)
            __active_funcs[func] = False

    Thread(target=run, daemon=True).start()


async def run_cycles(_):
    from .. import get_module

    if not get_module().enabled:
        return

    def run():
        while not hasattr(get_playerok_bot(), "account"):
            time.sleep(1)

        def check_configs_loop(cycle_delay=5):
            def _check_configs():
                global config, messages, accounts, rentals, stats
                if sett.get("config") != config:
                    config = sett.get("config")
                if sett.get("messages") != messages:
                    messages = sett.get("messages")
                if data.get("accounts") != accounts:
                    accounts = data.get("accounts")
                if data.get("rentals") != rentals:
                    rentals = data.get("rentals")
                if data.get("stats") != stats:
                    stats = data.get("stats")
                time.sleep(cycle_delay)

            while True:
                run_in_thread_safe(_check_configs)
                if stop_cycles_event.wait(3):
                    return

        def expire_loop():
            while True:
                try:
                    expire_rentals()
                except Exception as e:
                    logger.error(f"{PREFIX} Ошибка в expire_loop: {e}")
                time.sleep(60)

        Thread(target=check_configs_loop, daemon=True).start()
        Thread(target=expire_loop, daemon=True).start()

    Thread(target=run, daemon=True).start()


async def stop_cycles(_):
    global stop_cycles_event
    stop_cycles_event.set()


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


async def on_new_review(plbot, event: NewReviewEvent):
    if event.deal.user.id == plbot.playerok_account.id:
        return
    if not config.get("enabled", True):
        return
    try:
        handle_review(plbot, event)
    except Exception:
        logger.error(f"{PREFIX} Ошибка в on_new_review: {traceback.format_exc()}")


async def on_module_enabled(module):
    from .. import set_module
    set_module(module)
    logger.info(f"{PREFIX} Модуль подключен и активен")


async def on_module_disabled(_):
    stop_cycles_event.set()


async def on_telegram_bot_init(telegram_bot):
    from ..tgbot._handlers import on_telegram_bot_init as _tg_init
    await _tg_init(telegram_bot)
