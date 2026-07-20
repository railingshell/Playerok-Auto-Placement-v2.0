import textwrap
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from __init__ import VERSION

from .. import callback_datas as calls


# ─────────────────────────  ГЛАВНОЕ МЕНЮ  ─────────────────────────

def menu_text():
    txt = textwrap.dedent(f"""
        🤖 <b>PAP</b> · авто-помощник для Playerok
        🟢 Онлайн · {VERSION}

        Выберите раздел 👇
    """)
    return txt


def menu_kb():
    rows = [
        [
        InlineKeyboardButton(text="⚙️ Настройки", callback_data=calls.MenuNavigation(to="settings").pack()),
        InlineKeyboardButton(text="🎛 Управление", callback_data=calls.MenuNavigation(to="management").pack()),
        ],
        [
        InlineKeyboardButton(text="🧩 Система", callback_data=calls.MenuNavigation(to="system").pack()),
        InlineKeyboardButton(text="👤 Профиль", callback_data=calls.MenuNavigation(to="profile").pack()),
        ],
        [InlineKeyboardButton(text="━━━━━━━━━━━━━━━━", callback_data="null_answer")],
        [
        InlineKeyboardButton(text="📣 Новости", url="https://t.me/rogaartproduction"),
        InlineKeyboardButton(text="🧩 Плагины", url="https://t.me/lovesort"),
        ],
        [
        InlineKeyboardButton(text="👨‍💻 Разработчик", url="https://t.me/lovesort"),
        InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/lovesort"),
        ]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


# ─────────────────────────  ⚙️ НАСТРОЙКИ  ─────────────────────────

def settings_menu_text():
    txt = textwrap.dedent("""
        ⚙️ <b>Настройки</b>

        Выберите пункт 👇
    """)
    return txt


def settings_menu_kb():
    rows = [
        [
        InlineKeyboardButton(text="🔒 Авторизация", callback_data=calls.MenuNavigation(to="auth").pack()),
        InlineKeyboardButton(text="🌐 Соединение", callback_data=calls.MenuNavigation(to="conn").pack()),
        ],
        [
        InlineKeyboardButton(text="💬 Сообщения", callback_data=calls.MessagesPagination(page=0).pack()),
        InlineKeyboardButton(text="⌨️ Команды", callback_data=calls.CustomCommandsPagination(page=0).pack()),
        ],
        [
        InlineKeyboardButton(text="🚀 Авто-выдача", callback_data=calls.AutoDeliveriesPagination(page=0).pack()),
        InlineKeyboardButton(text="⬆️ Авто-поднятие", callback_data=calls.MenuNavigation(to="bump").pack()),
        ],
        [
        InlineKeyboardButton(text="♻️ Восстановление", callback_data=calls.MenuNavigation(to="restore").pack()),
        InlineKeyboardButton(text="✅ Подтверждение", callback_data=calls.MenuNavigation(to="complete").pack()),
        ],
        [
        InlineKeyboardButton(text="💸 Авто-вывод", callback_data=calls.MenuNavigation(to="withdrawal").pack()),
        InlineKeyboardButton(text="⚡ Быстрые ответы", callback_data=calls.FastRepliesPagination(page=0).pack()),
        ],
        [
        InlineKeyboardButton(text="🔔 Уведомления", callback_data=calls.MenuNavigation(to="notifications").pack()),
        InlineKeyboardButton(text="🔧 Прочее", callback_data=calls.MenuNavigation(to="other").pack()),
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.MenuNavigation(to="default").pack())]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


# ─────────────────────────  🎛 УПРАВЛЕНИЕ  ─────────────────────────

def management_menu_text():
    txt = textwrap.dedent("""
        🎛 <b>Управление</b>

        Выберите пункт 👇
    """)
    return txt


def management_menu_kb():
    rows = [
        [
        InlineKeyboardButton(text="📊 Статистика", callback_data=calls.StatsNavigation(to="day").pack()),
        InlineKeyboardButton(text="🌟 Отзывы", callback_data=calls.ReviewsPagination(page=0).pack()),
        ],
        [
        InlineKeyboardButton(text="💬 Чаты", callback_data=calls.ChatsPagination(page=0).pack()),
        InlineKeyboardButton(text="📋 Сделки", callback_data=calls.DealsPagination(page=0).pack()),
        ],
        [
        InlineKeyboardButton(text="🛍 Товары", callback_data=calls.ItemsPagination(page=0).pack()),
        InlineKeyboardButton(text="💳 Транзакции", callback_data=calls.TransactionsPagination(page=0).pack()),
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.MenuNavigation(to="default").pack())]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


# ─────────────────────────  🧩 СИСТЕМА  ─────────────────────────

def system_menu_text():
    txt = textwrap.dedent("""
        🧩 <b>Система</b>

        Выберите пункт 👇
    """)
    return txt


def system_menu_kb():
    rows = [
        [
        InlineKeyboardButton(text="🔄 Обновления", callback_data=calls.MenuNavigation(to="updates").pack()),
        InlineKeyboardButton(text="📄 Логи", callback_data=calls.MenuNavigation(to="logs").pack()),
        ],
        [
        InlineKeyboardButton(text="🧩 Модули", callback_data=calls.ModulesPagination(page=0).pack()),
        InlineKeyboardButton(text="🔑 Доступы", callback_data=calls.SignedUsersPagination(page=0).pack()),
        ],
        [InlineKeyboardButton(text="💾 Бэкап", callback_data=calls.MenuNavigation(to="backup").pack())],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.MenuNavigation(to="default").pack())]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb
