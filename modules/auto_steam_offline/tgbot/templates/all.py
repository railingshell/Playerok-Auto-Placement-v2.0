import math
import textwrap
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ...settings import Settings as sett
from ...data import Data as data
from .. import callback_datas as calls
from ...meta import NAME, VERSION


def menu_text():
    config = sett.get("config")
    enabled = "🟢 Включено" if config.get("enabled", True) else "🔴 Выключено"
    stats = data.get("stats")
    accounts = data.get("accounts")
    free = sum(1 for a in accounts if a.get("status") == "free")
    used = sum(1 for a in accounts if a.get("status") == "used")

    txt = textwrap.dedent(f"""
        🎮 <b>Меню {NAME}</b>

        <b>{NAME}</b> v{VERSION}
        Автоматическая офлайн-активация Steam.

        <b>Состояние:</b> {enabled}
        <b>Свободно:</b> {free}
        <b>Выдано:</b> {used}
        <b>Активировано:</b> {stats.get('activated', 0)}
        <b>Профит:</b> {stats.get('profit', 0)}₽
        <b>Возвратов:</b> {stats.get('refunded', 0)}

        Перемещайтесь по разделам ниже ↓
    """)
    return txt


def menu_kb():
    rows = [
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data=calls.STEAMOFF_MenuNavigation(to="settings").pack())],
        [InlineKeyboardButton(text="📋 Аккаунты", callback_data=calls.STEAMOFF_MenuNavigation(to="accounts").pack())],
        [InlineKeyboardButton(text="📊 Статистика", callback_data=calls.STEAMOFF_MenuNavigation(to="stats").pack())],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="destroy")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def settings_text():
    config = sett.get("config")
    enabled = "🟢 Включено" if config.get("enabled", True) else "🔴 Выключено"
    auto_complete = "🟢 Включено" if config.get("auto_complete_deal", True) else "🔴 Выключено"
    profit_notif = "🟢 Включено" if config.get("profit_notifications", True) else "🔴 Выключено"

    txt = textwrap.dedent(f"""
        ⚙️ <b>Настройки {NAME}</b>

        <b>Состояние модуля:</b> {enabled}
        <b>Кодов Steam Guard:</b> {config.get('max_codes_per_activation', 3)}
        <b>Таймаут кодов:</b> {config.get('code_cooldown_seconds', 30)} сек.
        <b>Авто-выполнение сделки:</b> {auto_complete}
        <b>Уведомления о профите:</b> {profit_notif}
    """)
    return txt


def settings_kb():
    config = sett.get("config")
    enabled = config.get("enabled", True)
    auto_complete = config.get("auto_complete_deal", True)
    profit_notif = config.get("profit_notifications", True)

    rows = [
        [InlineKeyboardButton(
            text=f"{'🔴 Выключить' if enabled else '🟢 Включить'} модуль",
            callback_data="steamoff_switch_enabled"
        )],
        [InlineKeyboardButton(
            text=f"✅ Авто-выполнение: {'🟢' if auto_complete else '🔴'}",
            callback_data="steamoff_switch_auto_complete"
        )],
        [InlineKeyboardButton(
            text=f"🔔 Уведомления профита: {'🟢' if profit_notif else '🔴'}",
            callback_data="steamoff_switch_profit_notifications"
        )],
        [InlineKeyboardButton(text="🔢 Макс. кодов Steam Guard", callback_data="steamoff_enter_max_codes")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.STEAMOFF_MenuNavigation(to="default").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def accounts_text(status: str = ""):
    accounts = data.get("accounts")
    filtered = [a for a in accounts if not status or a.get("status") == status]
    txt = textwrap.dedent(f"""
        📋 <b>Аккаунты</b>

        Всего: <b>{len(accounts)}</b>
        {f'Статус: <code>{status}</code>' if status else ''}
        Отображено: <b>{len(filtered)}</b>
    """)
    return txt


def accounts_kb(status: str = "", page: int = 0):
    accounts = data.get("accounts")
    filtered = [a for a in accounts if not status or a.get("status") == status]
    rows = []
    items_per_page = 8
    total_pages = math.ceil(len(filtered) / items_per_page) or 1

    if page < 0:
        page = 0
    elif page >= total_pages:
        page = total_pages - 1

    start = page * items_per_page
    end = start + items_per_page

    for account in filtered[start:end]:
        login = account.get("login", "—")
        status_icon = "🟢" if account.get("status") == "free" else "🔴" if account.get("status") == "used" else "🟡"
        rows.append([
            InlineKeyboardButton(
                text=f"{status_icon} {login}",
                callback_data=calls.STEAMOFF_AccountPage(login=login).pack()
            )
        ])

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="←", callback_data=calls.STEAMOFF_AccountsPagination(page=page - 1, status=status).pack()))
    else:
        nav_row.append(InlineKeyboardButton(text="🛑", callback_data="null_answer"))
    nav_row.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="null_answer"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="→", callback_data=calls.STEAMOFF_AccountsPagination(page=page + 1, status=status).pack()))
    else:
        nav_row.append(InlineKeyboardButton(text="🛑", callback_data="null_answer"))
    rows.append(nav_row)

    rows.append([
        InlineKeyboardButton(text="🟢 Свободные", callback_data=calls.STEAMOFF_MenuNavigation(to="accounts_free").pack()),
        InlineKeyboardButton(text="🔴 Выданные", callback_data=calls.STEAMOFF_MenuNavigation(to="accounts_used").pack())
    ])
    rows.append([InlineKeyboardButton(text="➕ Добавить аккаунт", callback_data="steamoff_add_account")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.STEAMOFF_MenuNavigation(to="default").pack())])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def account_page_text(login: str):
    accounts = data.get("accounts")
    account = next((a for a in accounts if a.get("login") == login), {})
    activation = next((a for a in data.get("activations") if a.get("account_login") == login), {})
    txt = textwrap.dedent(f"""
        📋 <b>Аккаунт {login}</b>

        <b>Статус:</b> <code>{account.get('status', '—')}</code>
        <b>Пароль:</b> <code>{account.get('password', '—')}</code>
        <b>maFile:</b> {'✅ Загружен' if account.get('mafile') else '❌ Нет'}
        <b>Осталось кодов:</b> {activation.get('codes_left', '—')}
    """)
    return txt


def account_page_kb(login: str):
    rows = [
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"steamoff_delete_account:{login}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.STEAMOFF_MenuNavigation(to="accounts").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def stats_text():
    stats = data.get("stats")
    txt = textwrap.dedent(f"""
        📊 <b>Статистика {NAME}</b>

        <b>Активировано:</b> {stats.get('activated', 0)}
        <b>Общий профит:</b> {stats.get('profit', 0)}₽
        <b>Возвратов:</b> {stats.get('refunded', 0)}
    """)
    return txt


def stats_kb():
    rows = [
        [InlineKeyboardButton(text="🔄 Обновить", callback_data=calls.STEAMOFF_MenuNavigation(to="stats").pack())],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.STEAMOFF_MenuNavigation(to="default").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        🎮 <b>{NAME}</b>
        \n{placeholder}
    """)
    return txt
