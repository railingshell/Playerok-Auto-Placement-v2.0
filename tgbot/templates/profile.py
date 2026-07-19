import textwrap
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from .. import callback_datas as calls


def profile_text():
    from plbot.playerokbot import get_playerok_bot
    
    plbot = get_playerok_bot()
    plbot.refresh_account()
    
    acc = plbot.account
    profile = acc.profile
    
    txt = textwrap.dedent(f"""
        👤 <b>Профиль</b>

        <b>🧑 Никнейм:</b> {profile.username}
        <b>🆔 ID:</b> <code>{profile.id}</code>
        <b>📪 Email:</b> {profile.email}
        <b>⭐ Рейтинг:</b> {profile.rating} · {profile.reviews_count} отзыв.

        💰 <b>Баланс:</b> {profile.balance.value if profile.balance else 0}₽
        <blockquote>👜 Доступно: {profile.balance.available if profile.balance else 0}₽
        ⌛ В процессе: {profile.balance.pending_income if profile.balance else 0}₽
        ❄️ Заморожено: {profile.balance.frozen if profile.balance else 0}₽</blockquote>

        📦 <b>Предметы:</b> {profile.stats.items.total - profile.stats.items.finished} активн. · {profile.stats.items.total} всего
        🛒 <b>Продажи:</b> {profile.stats.deals.outgoing.total - profile.stats.deals.outgoing.finished} активн. · {profile.stats.deals.outgoing.total} всего
        🛍 <b>Покупки:</b> {profile.stats.deals.incoming.total - profile.stats.deals.incoming.finished} активн. · {profile.stats.deals.incoming.total} всего

        <b>🗓 На Playerok с</b> {datetime.fromisoformat(profile.created_at.replace('Z', '+00:00')).strftime('%d.%m.%Y')}
    """)
    return txt


def profile_kb():
    rows = [
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=calls.MenuNavigation(to="default").pack()),]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return kb