import html
import textwrap
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uuid import UUID

from core.modules import Module, get_module_by_uuid

from .. import callback_datas as calls


def _escape(value: str) -> str:
    return html.escape(str(value)) if value is not None else ""


def module_page_text(module_uuid: UUID):
    module: Module = get_module_by_uuid(module_uuid)
    if not module:
        raise Exception("Не удалось найти модуль")

    txt = textwrap.dedent(f"""
        🔌 <b>Страница модуля</b>

        <b>Модуль</b> <code>{_escape(module.meta.name)}</code>:
        · UUID: <b>{module.uuid}</b>
        · Версия: <b>{_escape(module.meta.version)}</b>
        · Описание: <blockquote>{_escape(module.meta.description)}</blockquote>
        · Авторы: <b>{_escape(module.meta.authors)}</b>
        · Ссылки: <b>{_escape(module.meta.links)}</b>

        🔌 <b>Состояние:</b> {'🟢 Включен' if module.enabled else '🔴 Выключен'}
    """)
    return txt


def module_page_kb(module_uuid: UUID, page: int = 0):
    module: Module = get_module_by_uuid(module_uuid)
    if not module: 
        raise Exception("Не удалось найти модуль")
    
    rows = [
        [InlineKeyboardButton(text="🔴 Выключить модуль" if module.enabled else "🟢 Включить модуль", callback_data="switch_module_enabled")],
        [InlineKeyboardButton(text="♻️ Перезагрузить", callback_data="reload_module")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.ModulesPagination(page=page).pack())]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


def module_page_float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        🔧 <b>Управление модулем</b>
        \n{placeholder}
    """)
    return txt