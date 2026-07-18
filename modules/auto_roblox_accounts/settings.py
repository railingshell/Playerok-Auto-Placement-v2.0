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
        "lzt": {
            "token": "",
            "base_url": "https://lzt.market",
            "proxy": "",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "requests_timeout": 30,
            "max_search_pages": 3,
            "search_delay_seconds": 2
        },
        "tag_to_profile": {},
        "blacklist": {
            "items": [],
            "sellers": []
        },
        "reserve_minutes": 10,
        "auto_complete_deal": True,
        "profit_notifications": True,
        "temp_email_password_enabled": True,
        "admin_chat_id": ""
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
                "⏳ Заказ принят в работу. Ищу подходящий аккаунт на LZT Market..."
            ]
        },
        "account_delivered": {
            "enabled": True,
            "text": [
                "✅ Аккаунт найден и выдан!",
                "",
                "👤 Логин: <code>{login}</code>",
                "🔑 Пароль: <code>{password}</code>",
                "",
                "💡 Инструкция по входу:",
                "1. Перейдите на сайт www.roblox.com",
                "2. Нажмите «Войти» и введите логин и пароль.",
                "3. Если аккаунт запросит код 2FA, напишите в этот чат: <code>!code {deal_id}</code>",
                "",
                "❗ Если не получается войти — сообщите об этом в чат в течение {reserve_minutes} минут."
            ]
        },
        "account_delivered_with_email": {
            "enabled": True,
            "text": [
                "✅ Аккаунт найден и выдан!",
                "",
                "👤 Логин: <code>{login}</code>",
                "🔑 Пароль: <code>{password}</code>",
                "📧 Почта: <code>{email}</code>",
                "🔐 Пароль от почты: <code>{email_password}</code>",
                "",
                "💡 Инструкция по входу:",
                "1. Перейдите на сайт www.roblox.com",
                "2. Нажмите «Войти» и введите логин и пароль.",
                "3. Если аккаунт запросит код 2FA, напишите в этот чат: <code>!code {deal_id}</code>",
                "",
                "❗ Если не получается войти — сообщите об этом в чат в течение {reserve_minutes} минут."
            ]
        },
        "no_account_found": {
            "enabled": True,
            "text": [
                "😔 К сожалению, подходящий аккаунт не найден на LZT Market.",
                "",
                "Мы оформляем возврат средств по сделке."
            ]
        },
        "2fa_code": {
            "enabled": True,
            "text": [
                "🔐 Ваш код подтверждения: <code>{code}</code>",
                "",
                "Введите его в окно авторизации Roblox.",
                "Осталось попыток: {attempts_left}"
            ]
        },
        "2fa_limit_reached": {
            "enabled": True,
            "text": [
                "❌ Лимит кодов исчерпан. Если вход не удался — обратитесь к продавцу."
            ]
        },
        "refund_notification": {
            "enabled": True,
            "text": [
                "📦 Средства по сделке <code>{deal_id}</code> возвращены покупателю.",
                "Причина: {reason}"
            ]
        },
        "profit_notification": {
            "enabled": True,
            "text": [
                "💰 Профит по сделке <code>{deal_id}</code>: <b>{profit}₽</b>",
                "Продано за: {sold_for}₽",
                "Куплено за: {bought_for}₽"
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
