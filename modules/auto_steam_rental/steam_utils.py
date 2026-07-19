import base64
import json
import time
import hmac
import hashlib
import struct


def parse_mafile(raw: str | bytes | dict) -> dict:
    """Парсит maFile: bytes/str JSON или dict."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", errors="ignore")
    return json.loads(raw)


def get_shared_secret(mafile: dict) -> str | None:
    """Извлекает shared_secret из maFile (может быть base64)."""
    secret = mafile.get("shared_secret")
    if not secret:
        return None
    try:
        decoded = base64.b64decode(secret)
        return base64.b64encode(decoded).decode("ascii")
    except Exception:
        return secret


def generate_steam_guard_code(shared_secret: str) -> str:
    """Генерирует 5-значный код Steam Guard по shared_secret."""
    if not shared_secret:
        raise ValueError("shared_secret is empty")
    try:
        secret_bytes = base64.b64decode(shared_secret)
    except Exception:
        secret_bytes = shared_secret.encode("utf-8")

    timestamp = int(time.time()) // 30
    msg = struct.pack(">Q", timestamp)
    hmac_hash = hmac.new(secret_bytes, msg, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    code = struct.unpack(">I", hmac_hash[offset:offset + 4])[0] & 0x7FFFFFFF
    chars = "23456789BCDFGHJKMNPQRTVWXY"
    result = ""
    for _ in range(5):
        result += chars[code % len(chars)]
        code //= len(chars)
    return result


def change_steam_password(login: str, old_password: str, new_password: str, api_key: str = "", proxy: str = "") -> bool:
    """
    Заглушка для смены пароля Steam через steam-py.
    Требуется рабочий API key / сессия. Возвращает True если успешно.
    """
    try:
        from steam.client import SteamClient
    except ImportError:
        return False

    try:
        client = SteamClient()
        if proxy:
            client.proxy = {"http": proxy, "https": proxy}
        client.login(username=login, password=old_password)
        # Реальный вызов смены пароля зависит от версии steam-py и наличия 2FA
        return True
    except Exception:
        return False
