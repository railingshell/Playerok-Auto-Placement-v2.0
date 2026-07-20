import textwrap
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import backup as backup_mod

from .. import callback_datas as calls


def _backups_info() -> tuple[int, str]:
    """Возвращает (кол-во бэкапов, имя последнего или '❌ Нет')."""
    names = backup_mod.get_backups()
    last = names[0] if names else "❌ Нет"
    return len(names), last


def backup_text():
    count, last = _backups_info()

    txt = textwrap.dedent(f"""
        💾 <b>Бэкап</b>

        Резервная копия сохраняет настройки бота (<code>bot_settings/</code>, включая ключ шифрования) и собранные данные (<code>bot_data/</code>).
        <blockquote><b>(?)</b> Архив создаётся на сервере в папке <code>backups/</code>. Он содержит ключ шифрования и токены — храните его в надёжном месте и не пересылайте посторонним.</blockquote>

        <b>📦 Всего бэкапов:</b> {count}
        <b>🕒 Последний:</b> <code>{last}</code>
    """)
    return txt


def backup_kb():
    rows = [
        [InlineKeyboardButton(text="💾 Создать бэкап", callback_data="create_backup")],
        [InlineKeyboardButton(text="📤 Отправить архив в чат", callback_data="send_backup_to_chat")],
        [InlineKeyboardButton(text="📄 Список бэкапов", callback_data="list_backups")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.MenuNavigation(to="system").pack())]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


def backup_float_text(placeholder):
    txt = textwrap.dedent(f"""
        💾 <b>Бэкап</b>
        \n{placeholder}
    """)
    return txt
