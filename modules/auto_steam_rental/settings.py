import os
from settings import (
    Settings as sett,
    SettingsFile
)


CONFIG = SettingsFile(
    name="config",
    path=os.path.join(os.path.dirname(__file__), "module_settings", "config.json"),
    need_restore=True,
    default={
        "enabled": True,
        "rental": {
            "duration_hours": 24,
            "login_timeout_minutes": 15,
            "bonus_minutes_for_review": 60,
            "max_guard_codes_per_rental": 5,
            "guard_code_cooldown_seconds": 30
        },
        "steam": {
            "api_key": "",
            "proxy": ""
        },
        "auto_complete_deal": True,
        "admin_chat_id": "",
        "profit_notifications": True
    }
)

MESSAGES = SettingsFile(
    name="messages",
    path=os.path.join(os.path.dirname(__file__), "module_settings", "messages.json"),
    need_restore=True,
    default={
        "order_wait": {
            "enabled": True,
            "text": [
                "⏳ Заказ принят. Подготавливаю Steam-аккаунт для аренды..."
            ]
        },
        "account_delivered": {
            "enabled": True,
            "text": [
                "✅ Аккаунт готов к аренде!",
                "",
                "👤 Логин: <code>{login}</code>",
                "🔑 Пароль: <code>{password}</code>",
                "",
                "💡 Инструкция:",
                "1. Скачайте и откройте файл .maFile — в нём данные для входа.",
                "2. Или войдите в Steam клиент по логину и паролю.",
                "3. Для получения кода Steam Guard напишите: <code>!steamguard {deal_id}</code>",
                "",
                "⏳ Аренда начнётся с момента первого запроса Steam Guard.",
                "📅 Длительность аренды: {duration_hours} ч."
            ]
        },
        "steamguard_code": {
            "enabled": True,
            "text": [
                "🔐 Код Steam Guard: <code>{code}</code>",
                "",
                "⏱ Действителен 30 секунд.",
                "Осталось кодов: {codes_left}"
            ]
        },
        "steamguard_limit": {
            "enabled": True,
            "text": [
                "❌ Лимит кодов Steam Guard исчерпан."
            ]
        },
        "rental_started": {
            "enabled": True,
            "text": [
                "🚀 Аренда началась!",
                "📅 Окончание: <code>{expires_at}</code>"
            ]
        },
        "rental_expired": {
            "enabled": True,
            "text": [
                "⏰ Срок аренды истёк. Аккаунт возвращён в пул."
            ]
        },
        "rental_refunded": {
            "enabled": True,
            "text": [
                "📦 Средства по сделке <code>{deal_id}</code> возвращены.",
                "Причина: {reason}"
            ]
        },
        "no_account_available": {
            "enabled": True,
            "text": [
                "😔 К сожалению, сейчас нет свободных Steam-аккаунтов для аренды.",
                "Оформляем возврат средств."
            ]
        },
        "review_bonus": {
            "enabled": True,
            "text": [
                "🌟 Спасибо за отзыв! К аренде добавлено {bonus_minutes} минут.",
                "Новое время окончания: <code>{expires_at}</code>"
            ]
        }
    }
)

DATA = [CONFIG, MESSAGES]


class Settings:

    @staticmethod
    def get(name: str) -> dict:
        return sett.get(name, DATA)

    @staticmethod
    def set(name: str, new: list | dict) -> dict:
        return sett.set(name, new, DATA)
