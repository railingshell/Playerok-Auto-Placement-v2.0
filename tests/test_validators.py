"""Тесты чистых функций-валидаторов (utils.py).

utils.py тянет за собой сетевой стек (curl_cffi / tls_requests). Если эти
зависимости не установлены (например, при быстром локальном прогоне) — модуль
тестов аккуратно пропускается, а не падает.
"""
import pytest

pytest.importorskip("curl_cffi")
pytest.importorskip("tls_requests")

from utils import (  # noqa: E402
    is_cookies_valid,
    is_token_valid,
    is_tg_token_valid,
    is_password_valid,
    is_user_agent_valid,
    is_proxy_valid,
    escape_html,
    strip_html,
    parse_date,
)


@pytest.mark.parametrize("cookie,expected", [
    ("token=abc123; sid=xyz", True),
    ("single=value", True),
    ("", False),
    ("noequalsign", False),
    ("key=", False),
    ("=value", False),
])
def test_is_cookies_valid(cookie, expected):
    assert is_cookies_valid(cookie) is expected


@pytest.mark.parametrize("token,expected", [
    ("eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0In0.abc-DEF_123", True),
    ("not-a-jwt", False),
    ("only.two", False),
    ("", False),
])
def test_is_token_valid(token, expected):
    assert is_token_valid(token) is expected


@pytest.mark.parametrize("token,expected", [
    ("123456789:AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQR", True),
    ("123:short", False),
    ("nodigits:AABBCCDDEEFFGGHHIIJJKKLLMMNNOOPPQQR", False),
    ("", False),
])
def test_is_tg_token_valid(token, expected):
    assert is_tg_token_valid(token) is expected


@pytest.mark.parametrize("password,expected", [
    ("StrongPass123", True),
    ("123456", False),      # в чёрном списке
    ("qwerty", False),      # в чёрном списке
    ("abc", False),         # слишком короткий
    ("x" * 65, False),      # слишком длинный
])
def test_is_password_valid(password, expected):
    assert is_password_valid(password) is expected


@pytest.mark.parametrize("proxy,expected", [
    ("127.0.0.1:8080", True),
    ("user:pass@127.0.0.1:8080", True),
    ("127.0.0.1:99999", False),   # порт вне диапазона
    ("not-a-proxy", False),
    ("999.999.999.999:80", False),
])
def test_is_proxy_valid(proxy, expected):
    assert is_proxy_valid(proxy) is expected


def test_is_user_agent_valid():
    assert is_user_agent_valid("Mozilla/5.0 (Windows NT 10.0; Win64; x64)") is True
    assert is_user_agent_valid("short") is False
    assert is_user_agent_valid("") is False


def test_escape_html():
    assert escape_html("<b>a & b</b>") == "&lt;b&gt;a &amp; b&lt;/b&gt;"


def test_strip_html():
    assert strip_html("<p>hello <b>world</b></p>") == "hello world"
    assert strip_html(None) == ""


def test_parse_date():
    assert parse_date("25.12.2024") is not None
    assert parse_date("not-a-date") is None
