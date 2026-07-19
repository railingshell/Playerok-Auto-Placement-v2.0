"""Тесты чистых функций steam_utils (модуль auto_steam_rental).

Загружаем файл напрямую через importlib, чтобы не выполнять тяжёлый
`__init__.py` модуля (который тянет aiogram/playerokapi). Сами функции
используют только stdlib.
"""
import importlib.util
import os

import pytest

_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "modules", "auto_steam_rental", "steam_utils.py",
)
_spec = importlib.util.spec_from_file_location("steam_utils_standalone", _PATH)
steam_utils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(steam_utils)


# --- parse_mafile ---

def test_parse_mafile_dict_passthrough():
    d = {"shared_secret": "abc"}
    assert steam_utils.parse_mafile(d) is d


def test_parse_mafile_from_str():
    assert steam_utils.parse_mafile('{"a": 1}') == {"a": 1}


def test_parse_mafile_from_bytes():
    assert steam_utils.parse_mafile(b'{"a": 2}') == {"a": 2}


def test_parse_mafile_invalid_raises():
    with pytest.raises(ValueError):
        steam_utils.parse_mafile("{ broken")


# --- get_shared_secret ---

def test_get_shared_secret_missing_returns_none():
    assert steam_utils.get_shared_secret({}) is None
    assert steam_utils.get_shared_secret({"shared_secret": ""}) is None


def test_get_shared_secret_valid_base64_normalized():
    import base64
    raw = b"0123456789"
    secret = base64.b64encode(raw).decode()
    # нормализуется через decode->encode, значение сохраняется
    assert steam_utils.get_shared_secret({"shared_secret": secret}) == secret


# --- generate_steam_guard_code ---

STEAM_ALPHABET = "23456789BCDFGHJKMNPQRTVWXY"


def test_generate_code_empty_raises():
    with pytest.raises(ValueError):
        steam_utils.generate_steam_guard_code("")


def test_generate_code_format():
    import base64
    secret = base64.b64encode(b"my-steam-shared-secret").decode()
    code = steam_utils.generate_steam_guard_code(secret)
    assert len(code) == 5
    assert all(ch in STEAM_ALPHABET for ch in code)


def test_generate_code_is_deterministic_for_fixed_time(monkeypatch):
    import base64
    secret = base64.b64encode(b"my-steam-shared-secret").decode()
    monkeypatch.setattr(steam_utils.time, "time", lambda: 1_700_000_000)
    first = steam_utils.generate_steam_guard_code(secret)
    second = steam_utils.generate_steam_guard_code(secret)
    assert first == second
    assert len(first) == 5


def test_generate_code_changes_with_time_window(monkeypatch):
    import base64
    secret = base64.b64encode(b"another-secret-value-123").decode()
    monkeypatch.setattr(steam_utils.time, "time", lambda: 1_700_000_000)
    code_a = steam_utils.generate_steam_guard_code(secret)
    # следующее 30-секундное окно, как правило, даёт другой код
    monkeypatch.setattr(steam_utils.time, "time", lambda: 1_700_000_000 + 3000)
    code_b = steam_utils.generate_steam_guard_code(secret)
    assert code_a != code_b
