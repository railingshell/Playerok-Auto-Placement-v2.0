import textwrap
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from settings import Settings as sett

from .. import callback_datas as calls
    

def other_text():
    config = sett.get("config")
    
    read_chat = "✅" if config["playerok"]["read_chat"] else "❌"
    watermark_enabled = "✅" if config["playerok"]["watermark"]["enabled"] else "❌"
    watermark_value = config["playerok"]["watermark"]["value"] or "❌ Не задано"

    fs = config["telegram"]["bot"].get("forced_subscription", {})
    fs_enabled = "✅" if fs.get("enabled") else "❌"
    fs_channel = fs.get("channel") or "❌ Не задан"
    
    txt = textwrap.dedent(f"""
        🔧 <b>Прочее</b>

        <b>👀 Чтение чата:</b> {read_chat}
        <blockquote><b>(?)</b> Будет помечать чат как прочитанный перед тем, как отправить сообщение.</blockquote>

        <b>©️ Водяной знак:</b> {watermark_enabled}
        <b>🏷️©️ Значение:</b> {watermark_value}

        <b>📣 Обяз. подписка:</b> {fs_enabled}
        <b>🔗 Канал:</b> {fs_channel}
        <blockquote><b>(?)</b> Требует подписки на канал перед использованием бота. Бот должен быть <b>администратором</b> канала. Укажите @юзернейм канала.</blockquote>
    """)
    return txt


def other_kb():
    config = sett.get("config")
    
    read_chat = "✅" if config["playerok"]["read_chat"] else "❌"
    watermark_enabled = "✅" if config["playerok"]["watermark"]["enabled"] else "❌"
    watermark_value = config["playerok"]["watermark"]["value"] or "❌ Не задано"

    fs = config["telegram"]["bot"].get("forced_subscription", {})
    fs_enabled = "✅" if fs.get("enabled") else "❌"
    fs_channel = fs.get("channel") or "❌ Не задан"
    
    rows = [
        [InlineKeyboardButton(text=f"👀 Чтение чата: {read_chat}", callback_data="switch_read_chat_enabled")],
        [InlineKeyboardButton(text=f"©️ Водяной знак: {watermark_enabled}", callback_data="switch_watermark_enabled")],
        [InlineKeyboardButton(text=f"🏷️©️ Значение: {watermark_value}", callback_data="enter_watermark_value")],
        [InlineKeyboardButton(text=f"📣 Обяз. подписка: {fs_enabled}", callback_data="switch_forced_subscription_enabled")],
        [InlineKeyboardButton(text=f"🔗 Канал подписки: {fs_channel}", callback_data="enter_forced_subscription_channel")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.MenuNavigation(to="settings").pack())]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb


def other_float_text(placeholder: str):
    txt = textwrap.dedent(f"""
        🔧 <b>Прочее</b>
        \n{placeholder}
    """)
    return txt