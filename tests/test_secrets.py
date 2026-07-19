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


CORE_CONFIG = "bot_settings/config.json"


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
    on_disk = secrets.encrypt_config(CORE_CONFIG, config)

    assert on_disk["playerok"]["api"]["cookies"].startswith(secrets.ENC_PREFIX)
    assert on_disk["telegram"]["api"]["token"].startswith(secrets.ENC_PREFIX)
    # Пароль бота намеренно НЕ шифруется (нужен для восстановления доступа)
    assert on_disk["telegram"]["bot"]["password"] == "hunter2"
    # Несекретные поля остаются в открытом виде
    assert on_disk["playerok"]["watermark"]["value"] == "public-watermark"
    # Исходный словарь не мутируется
    assert config["playerok"]["api"]["cookies"] == "token=abc"

    restored = secrets.decrypt_config(CORE_CONFIG, secrets.encrypt_config(CORE_CONFIG, config))
    assert restored["playerok"]["api"]["cookies"] == "token=abc"
    assert restored["telegram"]["api"]["token"] == "123:AAA"


def test_module_config_is_not_encrypted(cipher_key):
    # Модули тоже используют name="config", но со своим путём — их данные
    # не должны шифроваться, даже если структура случайно пересекается.
    module_path = "/app/modules/auto_steam_rental/module_settings/config.json"
    data = {
        "enabled": True,
        "telegram": {"bot": {"password": "module-secret"}},
        "playerok": {"api": {"cookies": "should-stay-plain"}},
    }
    result = secrets.encrypt_config(module_path, data)
    assert result == data
    assert result["playerok"]["api"]["cookies"] == "should-stay-plain"


def test_unknown_file_is_untouched(cipher_key):
    data = {"password": "secret"}
    assert secrets.encrypt_config("bot_settings/messages.json", data) == data


def test_disabled_encryption_is_noop(monkeypatch):
    monkeypatch.setenv("PAP_DISABLE_ENCRYPTION", "1")
    secrets.reset_cipher()
    try:
        assert secrets.encrypt_value("secret") == "secret"
        assert secrets.get_cipher() is None
    finally:
        secrets.reset_cipher()


def test_settings_end_to_end(cipher_key, tmp_path, monkeypatch):
    """Реальный Settings: секреты шифруются на диске и прозрачно читаются обратно."""
    import json

    monkeypatch.chdir(tmp_path)
    from settings import Settings

    cfg = Settings.get("config")
    cfg["playerok"]["api"]["cookies"] = "token=abc; sid=xyz"
    cfg["telegram"]["api"]["token"] = "123456789:AAExampleTokenValueForUnitTest1234"
    Settings.set("config", cfg)

    disk = json.loads((tmp_path / "bot_settings" / "config.json").read_text(encoding="utf-8"))
    assert disk["playerok"]["api"]["cookies"].startswith(secrets.ENC_PREFIX)
    assert disk["telegram"]["api"]["token"].startswith(secrets.ENC_PREFIX)

    back = Settings.get("config")
    assert back["playerok"]["api"]["cookies"] == "token=abc; sid=xyz"
    assert back["telegram"]["api"]["token"] == "123456789:AAExampleTokenValueForUnitTest1234"


def test_settings_reads_legacy_plaintext_config(cipher_key, tmp_path, monkeypatch):
    """Старый конфиг в открытом виде должен читаться без ошибок (обратная совместимость)."""
    import json

    monkeypatch.chdir(tmp_path)
    (tmp_path / "bot_settings").mkdir()
    legacy = {
        "playerok": {"api": {"cookies": "legacy-plain-cookie"}},
        "telegram": {"api": {"token": "legacy-plain-token"}},
    }
    (tmp_path / "bot_settings" / "config.json").write_text(
        json.dumps(legacy), encoding="utf-8"
    )

    from settings import Settings

    back = Settings.get("config")
    # Legacy-значения в открытом виде возвращаются как есть
    assert back["playerok"]["api"]["cookies"] == "legacy-plain-cookie"
    assert back["telegram"]["api"]["token"] == "legacy-plain-token"
