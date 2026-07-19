"""Тесты прозрачного шифрования секретов (core/secrets.py)."""
import pytest

from core import secrets


@pytest.fixture
def cipher_key(monkeypatch):
    """Изолированный ключ шифрования на время теста."""
    from cryptography.fernet import Fernet

    monkeypatch.setenv("PAP_SECRET_KEY", Fernet.generate_key().decode())
    monkeypatch.delenv("PAP_DISABLE_ENCRYPTION", raising=False)
    secrets.reset_cipher()
    yield
    secrets.reset_cipher()


def test_encrypt_decrypt_round_trip(cipher_key):
    value = "token=abc123; sid=xyz"
    encrypted = secrets.encrypt_value(value)

    assert encrypted.startswith(secrets.ENC_PREFIX)
    assert encrypted != value
    assert secrets.decrypt_value(encrypted) == value


def test_empty_value_is_not_encrypted(cipher_key):
    assert secrets.encrypt_value("") == ""
    assert secrets.decrypt_value("") == ""


def test_double_encryption_is_noop(cipher_key):
    once = secrets.encrypt_value("secret")
    twice = secrets.encrypt_value(once)
    assert once == twice


def test_legacy_plaintext_passthrough(cipher_key):
    # Значение без префикса enc:: считается legacy и возвращается как есть
    assert secrets.decrypt_value("plain-cookie-value") == "plain-cookie-value"


def test_config_only_sensitive_fields_encrypted(cipher_key):
    config = {
        "playerok": {
            "api": {"cookies": "token=abc", "proxy": ""},
            "watermark": {"value": "public-watermark"},
        },
        "telegram": {
            "api": {"token": "123:AAA"},
            "bot": {"password": "hunter2"},
        },
    }
    on_disk = secrets.encrypt_config("config", config)

    assert on_disk["playerok"]["api"]["cookies"].startswith(secrets.ENC_PREFIX)
    assert on_disk["telegram"]["api"]["token"].startswith(secrets.ENC_PREFIX)
    assert on_disk["telegram"]["bot"]["password"].startswith(secrets.ENC_PREFIX)
    # Несекретные поля остаются в открытом виде
    assert on_disk["playerok"]["watermark"]["value"] == "public-watermark"
    # Исходный словарь не мутируется
    assert config["playerok"]["api"]["cookies"] == "token=abc"

    restored = secrets.decrypt_config("config", secrets.encrypt_config("config", config))
    assert restored["playerok"]["api"]["cookies"] == "token=abc"
    assert restored["telegram"]["bot"]["password"] == "hunter2"


def test_unknown_file_is_untouched(cipher_key):
    data = {"password": "secret"}
    assert secrets.encrypt_config("some_module_config", data) == data


def test_disabled_encryption_is_noop(monkeypatch):
    monkeypatch.setenv("PAP_DISABLE_ENCRYPTION", "1")
    secrets.reset_cipher()
    try:
        assert secrets.encrypt_value("secret") == "secret"
        assert secrets.get_cipher() is None
    finally:
        secrets.reset_cipher()
