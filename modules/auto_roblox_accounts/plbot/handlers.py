import re
import time
import traceback
from logging import getLogger
from threading import Thread, Event as ThreadingEvent
from datetime import datetime

from playerokapi.enums import ItemDealStatuses
from playerokapi.listener.events import NewDealEvent, NewMessageEvent

from ..meta import PREFIX, NAME
from ..data import Data as data
from ..settings import Settings as sett
from ..settings import DATA as SETTINGS_DATA
from ..lzt_client import LZTMarketClient, LZTMarketError
from plbot.playerokbot import get_playerok_bot


logger = getLogger(f"{NAME}.playerok")

config = sett.get("config")
messages = sett.get("messages")

profiles = data.get("profiles")
purchases = data.get("purchases")
stats = data.get("stats")

stop_cycles_event = ThreadingEvent()
__active_funcs = {}

TAG_RE = re.compile(r"roblox:([A-Za-z0-9_\-]+)", re.IGNORECASE)


def msg(message_name: str, **kwargs) -> str | None:
    return get_playerok_bot().msg(message_name, "messages", SETTINGS_DATA, **kwargs)


def get_profile_for_item(item) -> dict | None:
    """Ищет профиль закупки по тегу roblox:<TAG> в описании/названии товара."""
    text = f"{item.name or ''} {item.description or ''}"
    match = TAG_RE.search(text)
    if not match:
        return None
    tag = match.group(1).lower()
    tag_map = config.get("tag_to_profile", {})
    profile_id = tag_map.get(tag)
    if not profile_id:
        return None
    return profiles.get(profile_id)


def is_purchase_used(item_id: str, profile_id: str) -> bool:
    for p in purchases:
        if p.get("profile_id") == profile_id and str(p.get("lzt_item_id")) == str(item_id):
            return True
    return False


def parse_account_data(raw: dict) -> dict:
    """Извлекает логин/пароль из ответа LZT. Адаптировать под реальный формат."""
    raw_str = str(raw)
    login = raw.get("login") or raw.get("username") or ""
    password = raw.get("password") or raw.get("pass") or ""
    email = raw.get("email") or ""
    if not login and ":" in raw_str:
        parts = raw_str.split(":")
        login = parts[0].strip()
        password = ":".join(parts[1:]).strip()
    return {
        "login": login,
        "password": password,
        "email": email
    }


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
        text = msg("refund_notification", deal_id=deal_id, reason=reason)
        if text:
            plbot.send_message(deal_id, text)
        stats["refunded"] = stats.get("refunded", 0) + 1
        data.set("stats", stats)
    except Exception as e:
        logger.error(f"{PREFIX} Ошибка возврата сделки {deal_id}: {e}")


def deliver_account(plbot, deal, account: dict, bought_for: int | None, profile_id: str, lzt_item_id: str):
    reserve = config.get("reserve_minutes", 10)
    email_password = account.get("email_password")

    if account.get("email") and email_password:
        text = msg(
            "account_delivered_with_email",
            login=account.get("login", ""),
            password=account.get("password", ""),
            email=account.get("email", ""),
            email_password=email_password,
            deal_id=deal.id,
            reserve_minutes=reserve
        )
    else:
        text = msg(
            "account_delivered",
            login=account.get("login", ""),
            password=account.get("password", ""),
            deal_id=deal.id,
            reserve_minutes=reserve
        )

    if text:
        plbot.send_message(deal.chat.id if deal.chat else deal.id, text)

    purchases.append({
        "deal_id": deal.id,
        "profile_id": profile_id,
        "lzt_item_id": str(lzt_item_id),
        "login": account.get("login", ""),
        "password": account.get("password", ""),
        "email": account.get("email", ""),
        "email_password": email_password,
        "bought_for": bought_for,
        "sold_for": deal.item.price,
        "created_at": datetime.now().isoformat(),
        "2fa_codes_left": 3
    })
    data.set("purchases", purchases)

    profit = (deal.item.price or 0) - (bought_for or 0)
    stats["sold"] = stats.get("sold", 0) + 1
    stats["profit"] = stats.get("profit", 0) + profit
    data.set("stats", stats)

    if config.get("profit_notifications", True):
        admin_text = msg(
            "profit_notification",
            deal_id=deal.id,
            profit=profit,
            sold_for=deal.item.price or 0,
            bought_for=bought_for or 0
        )
        if admin_text:
            send_admin_notification(admin_text)

    if config.get("auto_complete_deal", True):
        try:
            time.sleep(1)
            plbot.account.update_deal(deal.id, ItemDealStatuses.SENT)
        except Exception as e:
            logger.error(f"{PREFIX} Ошибка подтверждения сделки {deal.id}: {e}")


def process_new_deal(plbot, event: NewDealEvent):
    deal = event.deal

    profile = get_profile_for_item(deal.item)
    if not profile:
        return

    if not config.get("enabled", True):
        return

    if not config.get("lzt", {}).get("token"):
        logger.warning(f"{PREFIX} LZT токен не задан")
        return

    plbot.send_message(
        deal.chat.id if deal.chat else deal.id,
        msg("order_wait")
    )

    client = LZTMarketClient(
        token=config["lzt"]["token"],
        base_url=config["lzt"].get("base_url", "https://lzt.market"),
        proxy=config["lzt"].get("proxy") or None,
        user_agent=config["lzt"].get("user_agent"),
        timeout=config["lzt"].get("requests_timeout", 30)
    )

    try:
        accounts = client.search_accounts(
            search_url=profile["search_url"],
            max_price=deal.item.price - profile.get("min_profit", 0),
            max_pages=config["lzt"].get("max_search_pages", 3),
            delay=config["lzt"].get("search_delay_seconds", 2),
            blacklist_items=config.get("blacklist", {}).get("items", []),
            blacklist_sellers=config.get("blacklist", {}).get("sellers", [])
        )

        chosen = None
        for acc in accounts:
            if not is_purchase_used(acc["id"], profile["id"]):
                chosen = acc
                break

        if not chosen:
            logger.info(f"{PREFIX} Подходящий аккаунт не найден для сделки {deal.id}")
            text = msg("no_account_found")
            if text:
                plbot.send_message(deal.chat.id if deal.chat else deal.id, text)
            refund_deal(plbot, deal.id, "Не найден подходящий аккаунт на LZT")
            return

        bought = client.buy_account(chosen["id"])
        account_data = parse_account_data(bought)

        if config.get("temp_email_password_enabled", True):
            try:
                email_password = client.get_email_password(chosen["id"])
                if email_password:
                    account_data["email_password"] = email_password
            except Exception:
                pass

        deliver_account(
            plbot,
            deal,
            account_data,
            bought_for=chosen.get("price"),
            profile_id=profile["id"],
            lzt_item_id=chosen["id"]
        )
        logger.info(
            f"{PREFIX} Аккаунт выдан по сделке {deal.id} (LZT {chosen['id']})"
        )

    except LZTMarketError as e:
        logger.error(f"{PREFIX} LZT ошибка в сделке {deal.id}: {e}")
        refund_deal(plbot, deal.id, f"Ошибка LZT Market: {e}")
    except Exception as e:
        logger.error(f"{PREFIX} Ошибка обработки сделки {deal.id}: {traceback.format_exc()}")
        refund_deal(plbot, deal.id, f"Внутренняя ошибка: {e}")


async def handle_2fa_command(plbot, event: NewMessageEvent):
    text = (event.message.text or "").strip()
    if not text.lower().startswith("!code"):
        return

    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return

    deal_id = parts[1].strip()
    purchase = next((p for p in purchases if p.get("deal_id") == deal_id), None)
    if not purchase:
        return

    if purchase.get("2fa_codes_left", 0) <= 0:
        plbot.send_message(event.chat.id, msg("2fa_limit_reached"))
        return

    # Заглушка: реальный код 2FA Roblox приходит на почту/телефон.
    # Можно интегрировать получение почты, если есть доступ.
    code = "000000"
    purchase["2fa_codes_left"] = purchase.get("2fa_codes_left", 3) - 1
    data.set("purchases", purchases)

    plbot.send_message(
        event.chat.id,
        msg(
            "2fa_code",
            code=code,
            attempts_left=purchase["2fa_codes_left"]
        )
    )


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
                global config, messages, profiles, purchases, stats
                if sett.get("config") != config:
                    config = sett.get("config")
                if sett.get("messages") != messages:
                    messages = sett.get("messages")
                if data.get("profiles") != profiles:
                    profiles = data.get("profiles")
                if data.get("purchases") != purchases:
                    purchases = data.get("purchases")
                if data.get("stats") != stats:
                    stats = data.get("stats")
                time.sleep(cycle_delay)

            while True:
                run_in_thread_safe(_check_configs)
                if stop_cycles_event.wait(3):
                    return

        Thread(target=check_configs_loop, daemon=True).start()

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
    except Exception as e:
        logger.error(f"{PREFIX} Ошибка в on_new_deal: {traceback.format_exc()}")


async def on_new_message(plbot, event: NewMessageEvent):
    if event.message.user.id == plbot.playerok_account.id:
        return
    if not config.get("enabled", True):
        return
    if event.message.text is None:
        return
    await handle_2fa_command(plbot, event)
