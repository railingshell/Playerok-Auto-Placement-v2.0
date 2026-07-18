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
        "max_codes_per_activation": 3,
        "code_cooldown_seconds": 30,
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
                "⏳ Заказ принят. Подготавливаю офлайн-активацию Steam..."
            ]
        },
        "activation_delivered": {
            "enabled": True,
            "text": [
                "✅ Активация готова!",
                "",
                "👤 Логин: <code>{login}</code>",
                "🔑 Пароль: <code>{password}</code>",
                "",
                "💡 Инструкция:",
                "1. Войдите в Steam клиент по логину и паролю.",
                "2. Для получения кода Steam Guard напишите: <code>!sg {deal_id}</code>",
                "3. После входа поставьте клиент в офлайн-режим и начинайте играть.",
                "",
                "⏳ Осталось кодов Steam Guard: {codes_left}"
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
        "already_activated": {
            "enabled": True,
            "text": [
                "✅ Активация уже была выдана по этой сделке."
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
                "😔 К сожалению, сейчас нет свободных аккаунтов для активации.",
                "Оформляем возврат средств."
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
