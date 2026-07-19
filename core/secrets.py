"""
🔐 Прозрачное шифрование чувствительных полей конфигурации.

Модуль хранит в конфигах на диске cookies, токены и пароли в зашифрованном
виде, но код продолжает работать с обычными строками — шифрование и
расшифровка происходят автоматически на уровне `Settings.get/set`.

Как это работает
-----------------
* Ключ шифрования берётся из переменной окружения ``PAP_SECRET_KEY`` либо
  автоматически создаётся и сохраняется в ``bot_settings/.secret_key``
  (эта папка уже в ``.gitignore`` и никогда не попадёт в репозиторий).
* Зашифрованные значения получают префикс ``enc::``. Значения без префикса
  считаются legacy-данными в открытом виде — они продолжают работать и
  шифруются при следующем сохранении конфига (бесшовная миграция).
* Если библиотека ``cryptography`` не установлена или шифрование отключено
  через ``PAP_DISABLE_ENCRYPTION=1`` — модуль работает как no-op и возвращает
  значения без изменений, не ломая бота.
"""
from __future__ import annotations

import os
import copy
from logging import getLogger

logger = getLogger("universal")

ENC_PREFIX = "enc::"
_KEY_ENV = "PAP_SECRET_KEY"
_DISABLE_ENV = "PAP_DISABLE_ENCRYPTION"
_KEY_PATH = os.path.join("bot_settings", ".secret_key")

# Чувствительные пути внутри каждого файла настроек (по его имени).
# Только эти значения шифруются; вся остальная структура остаётся читаемой.
SENSITIVE_PATHS: dict[str, list[tuple[str, ...]]] = {
    "config": [
        ("playerok", "api", "cookies"),
        ("telegram", "api", "token"),
        ("telegram", "bot", "password"),
        ("playerok", "auto_withdrawal", "card_id"),
        ("playerok", "auto_withdrawal", "sbp_phone_number"),
        ("playerok", "auto_withdrawal", "usdt_address"),
    ],
}

_cipher = None
_cipher_ready = False


def _encryption_disabled() -> bool:
    return os.environ.get(_DISABLE_ENV, "").strip().lower() in {"1", "true", "yes"}


def _load_or_create_key() -> bytes | None:
    """Возвращает ключ Fernet из окружения или файла, создавая его при отсутствии."""
    env_key = os.environ.get(_KEY_ENV)
    if env_key:
        return env_key.encode("utf-8")

    try:
        from cryptography.fernet import Fernet
    except ImportError:
        return None

    if os.path.exists(_KEY_PATH):
        with open(_KEY_PATH, "rb") as f:
            return f.read().strip()

    key = Fernet.generate_key()
    os.makedirs(os.path.dirname(_KEY_PATH), exist_ok=True)
    with open(_KEY_PATH, "wb") as f:
        f.write(key)
    try:
        os.chmod(_KEY_PATH, 0o600)
    except OSError:
        pass
    logger.info("🔐 Создан новый ключ шифрования конфигурации: %s", _KEY_PATH)
    return key


def get_cipher():
    """Ленивая инициализация шифра. Возвращает ``Fernet`` или ``None`` (no-op)."""
    global _cipher, _cipher_ready
    if _cipher_ready:
        return _cipher

    _cipher_ready = True
    if _encryption_disabled():
        _cipher = None
        return None

    try:
        from cryptography.fernet import Fernet
    except ImportError:
        logger.warning(
            "🔓 Библиотека 'cryptography' не установлена — секреты хранятся в "
            "открытом виде. Установите зависимости для шифрования конфигов."
        )
        _cipher = None
        return None

    key = _load_or_create_key()
    if not key:
        _cipher = None
        return None
    try:
        _cipher = Fernet(key)
    except (ValueError, TypeError):
        logger.error("🔐 Некорректный ключ шифрования — секреты остаются в открытом виде.")
        _cipher = None
    return _cipher


def reset_cipher() -> None:
    """Сбрасывает кэш шифра (используется в тестах после смены ключа)."""
    global _cipher, _cipher_ready
    _cipher = None
    _cipher_ready = False


def encrypt_value(value: str) -> str:
    """Шифрует строку. Пустые и уже зашифрованные значения возвращаются как есть."""
    if not isinstance(value, str) or not value or value.startswith(ENC_PREFIX):
        return value
    cipher = get_cipher()
    if cipher is None:
        return value
    token = cipher.encrypt(value.encode("utf-8")).decode("utf-8")
    return f"{ENC_PREFIX}{token}"


def decrypt_value(value: str) -> str:
    """Расшифровывает строку. Legacy-значения без префикса возвращаются как есть."""
    if not isinstance(value, str) or not value.startswith(ENC_PREFIX):
        return value
    cipher = get_cipher()
    if cipher is None:
        return value
    try:
        from cryptography.fernet import InvalidToken
    except ImportError:
        return value
    token = value[len(ENC_PREFIX):]
    try:
        return cipher.decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        logger.error(
            "🔐 Не удалось расшифровать значение конфигурации — возможно, "
            "изменился ключ шифрования (bot_settings/.secret_key)."
        )
        return value


def _walk(config: dict, path: tuple[str, ...], transform) -> None:
    node = config
    for key in path[:-1]:
        if not isinstance(node, dict) or key not in node:
            return
        node = node[key]
    last = path[-1]
    if isinstance(node, dict) and isinstance(node.get(last), str):
        node[last] = transform(node[last])


def encrypt_config(name: str, config):
    """Возвращает копию конфига с зашифрованными чувствительными полями."""
    paths = SENSITIVE_PATHS.get(name)
    if not paths or not isinstance(config, dict):
        return config
    result = copy.deepcopy(config)
    for path in paths:
        _walk(result, path, encrypt_value)
    return result


def decrypt_config(name: str, config):
    """Расшифровывает чувствительные поля конфига на месте и возвращает его."""
    paths = SENSITIVE_PATHS.get(name)
    if not paths or not isinstance(config, dict):
        return config
    for path in paths:
        _walk(config, path, decrypt_value)
    return config
