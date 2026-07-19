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
    txt = textwrap.dedent(f"""
        🧱 <b>Меню {NAME}</b>

        <b>{NAME}</b> v{VERSION}
        Автоматическая выдача Roblox-аккаунтов через LZT Market.

        <b>Состояние:</b> {enabled}
        <b>Продано:</b> {stats.get('sold', 0)}
        <b>Профит:</b> {stats.get('profit', 0)}₽
        <b>Возвратов:</b> {stats.get('refunded', 0)}

        Перемещайтесь по разделам ниже ↓
    """)
    return txt


def menu_kb():
    rows = [
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data=calls.ROBLOX_MenuNavigation(to="settings").pack())],
        [InlineKeyboardButton(text="📋 Профили закупок", callback_data=calls.ROBLOX_MenuNavigation(to="profiles").pack())],
        [InlineKeyboardButton(text="🚫 Чёрные списки", callback_data=calls.ROBLOX_MenuNavigation(to="blacklist").pack())],
        [InlineKeyboardButton(text="📊 Статистика", callback_data=calls.ROBLOX_MenuNavigation(to="stats").pack())],
        [InlineKeyboardButton(text="❌ Закрыть", callback_data="destroy")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def settings_text():
    config = sett.get("config")
    enabled = "🟢 Включено" if config.get("enabled", True) else "🔴 Выключено"
    auto_complete = "🟢 Включено" if config.get("auto_complete_deal", True) else "🔴 Выключено"
    profit_notif = "🟢 Включено" if config.get("profit_notifications", True) else "🔴 Выключено"
    token = config.get("lzt", {}).get("token", "")
    token_status = "✅ Задан" if token else "❌ Не задан"
    reserve = config.get("reserve_minutes", 10)

    txt = textwrap.dedent(f"""
        ⚙️ <b>Настройки {NAME}</b>

        <b>Состояние модуля:</b> {enabled}
        <b>Токен LZT:</b> {token_status}
        <b>Резерв (мин):</b> {reserve}
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
            callback_data="roblox_switch_enabled"
        )],
        [InlineKeyboardButton(
            text=f"✅ Авто-выполнение: {'🟢' if auto_complete else '🔴'}",
            callback_data="roblox_switch_auto_complete"
        )],
        [InlineKeyboardButton(
            text=f"🔔 Уведомления профита: {'🟢' if profit_notif else '🔴'}",
            callback_data="roblox_switch_profit_notifications"
        )],
        [InlineKeyboardButton(text="🔑 Ввести токен LZT", callback_data="roblox_enter_lzt_token")],
        [InlineKeyboardButton(text="⏱ Ввести резерв (мин)", callback_data="roblox_enter_reserve")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.ROBLOX_MenuNavigation(to="default").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def profiles_text():
    profiles = data.get("profiles")
    txt = textwrap.dedent(f"""
        📋 <b>Профили закупок</b>

        Всего профилей: <b>{len(profiles)}</b>

        Каждый профиль связывает тег <code>roblox:TAG</code> в описании товара с URL поиска на LZT Market.
    """)
    return txt


def profiles_kb(page: int = 0):
    profiles = data.get("profiles")
    rows = []
    items_per_page = 8
    items = list(profiles.items())
    total_pages = math.ceil(len(items) / items_per_page) or 1

    if page < 0:
        page = 0
    elif page >= total_pages:
        page = total_pages - 1

    start = page * items_per_page
    end = start + items_per_page

    for profile_id, profile in items[start:end]:
        rows.append([
            InlineKeyboardButton(
                text=f"{profile.get('name', profile_id)} ({profile_id})",
                callback_data=calls.ROBLOX_ProfilePage(profile_id=profile_id).pack()
            )
        ])

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="←", callback_data=calls.ROBLOX_ProfilesPagination(page=page - 1).pack()))
    else:
        nav_row.append(InlineKeyboardButton(text="🛑", callback_data="null_answer"))
    nav_row.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="null_answer"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="→", callback_data=calls.ROBLOX_ProfilesPagination(page=page + 1).pack()))
    else:
        nav_row.append(InlineKeyboardButton(text="🛑", callback_data="null_answer"))
    rows.append(nav_row)

    rows.append([InlineKeyboardButton(text="➕ Добавить профиль", callback_data="roblox_add_profile")])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.ROBLOX_MenuNavigation(to="default").pack())])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def profile_page_text(profile_id: str):
    profiles = data.get("profiles")
    profile = profiles.get(profile_id, {})
    tags = [
        tag for tag, mapped_id in sett.get("config").get("tag_to_profile", {}).items()
        if mapped_id == profile_id
    ]
    tags_str = ", ".join(f"<code>roblox:{t}</code>" for t in tags) or "—"
    txt = textwrap.dedent(f"""
        📋 <b>Профиль {profile.get('name', profile_id)}</b>

        <b>ID:</b> <code>{profile_id}</code>
        <b>Название:</b> {profile.get('name', '—')}
        <b>URL поиска:</b> <code>{profile.get('search_url', '—')}</code>
        <b>Мин. профит:</b> {profile.get('min_profit', 0)}₽
        <b>Теги:</b> {tags_str}
    """)
    return txt


def profile_page_kb(profile_id: str):
    rows = [
        [InlineKeyboardButton(text="✏️ Изменить", callback_data=f"roblox_edit_profile:{profile_id}")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"roblox_delete_profile:{profile_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.ROBLOX_MenuNavigation(to="profiles").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def blacklist_text():
    txt = textwrap.dedent("""
        🚫 <b>Чёрные списки</b>

        Выберите тип списка для управления.
    """)
    return txt


def blacklist_kb():
    rows = [
        [InlineKeyboardButton(text="🛍 Чёрный список товаров", callback_data=calls.ROBLOX_MenuNavigation(to="blacklist_items").pack())],
        [InlineKeyboardButton(text="👤 Чёрный список продавцов", callback_data=calls.ROBLOX_MenuNavigation(to="blacklist_sellers").pack())],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.ROBLOX_MenuNavigation(to="settings").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def blacklist_list_text(list_type: str):
    config = sett.get("config")
    items = config.get("blacklist", {}).get(list_type, [])
    txt = textwrap.dedent(f"""
        🚫 <b>Чёрный список {'товаров' if list_type == 'items' else 'продавцов'}</b>

        Всего: <b>{len(items)}</b>
    """)
    return txt


def blacklist_list_kb(list_type: str, page: int = 0):
    config = sett.get("config")
    items = config.get("blacklist", {}).get(list_type, [])
    rows = []
    items_per_page = 8
    total_pages = math.ceil(len(items) / items_per_page) or 1

    if page < 0:
        page = 0
    elif page >= total_pages:
        page = total_pages - 1

    for item in items[page * items_per_page:(page + 1) * items_per_page]:
        rows.append([
            InlineKeyboardButton(
                text=str(item),
                callback_data=calls.ROBLOX_BlacklistItemPage(list_type=list_type, item=str(item)).pack()
            )
        ])

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="←", callback_data=calls.ROBLOX_BlacklistPagination(list_type=list_type, page=page - 1).pack()))
    else:
        nav_row.append(InlineKeyboardButton(text="🛑", callback_data="null_answer"))
    nav_row.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="null_answer"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="→", callback_data=calls.ROBLOX_BlacklistPagination(list_type=list_type, page=page + 1).pack()))
    else:
        nav_row.append(InlineKeyboardButton(text="🛑", callback_data="null_answer"))
    rows.append(nav_row)

    action = "roblox_add_blacklist_item" if list_type == "items" else "roblox_add_blacklist_seller"
    rows.append([InlineKeyboardButton(text="➕ Добавить", callback_data=action)])
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.ROBLOX_MenuNavigation(to="blacklist").pack())])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def blacklist_item_page_text(list_type: str, item: str):
    txt = textwrap.dedent(f"""
        🚫 <b>Элемент чёрного списка</b>

        <b>Тип:</b> {'товар' if list_type == 'items' else 'правец'}
        <b>Значение:</b> <code>{item}</code>
    """)
    return txt


def blacklist_item_page_kb(list_type: str, item: str):
    rows = [
        [InlineKeyboardButton(
            text="🗑 Удалить",
            callback_data=f"roblox_delete_blacklist:{list_type}:{item}"
        )],
        [InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=calls.ROBLOX_MenuNavigation(to=f"blacklist_{list_type}").pack()
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def stats_text():
    stats = data.get("stats")
    purchases = data.get("purchases")
    txt = textwrap.dedent(f"""
        📊 <b>Статистика {NAME}</b>

        <b>Продано аккаунтов:</b> {stats.get('sold', 0)}
        <b>Общий профит:</b> {stats.get('profit', 0)}₽
        <b>Возвратов:</b> {stats.get('refunded', 0)}
        <b>Активных выдач:</b> {len(purchases)}
    """)
    return txt


def stats_kb():
    rows = [
        [InlineKeyboardButton(text="🔄 Обновить", callback_data=calls.ROBLOX_MenuNavigation(to="stats").pack())],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.ROBLOX_MenuNavigation(to="default").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        🧱 <b>{NAME}</b>
        \n{placeholder}
    """)
    return txt
