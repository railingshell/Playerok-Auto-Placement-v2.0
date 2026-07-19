"""Тесты логики валидации и восстановления конфигов (settings.py)."""
from settings import validate_config, restore_config


DEFAULT = {
    "playerok": {"api": {"cookies": "", "timeout": 30}},
    "logs": {"max_file_size": 512},
    "enabled": True,
}


def test_validate_config_accepts_matching_structure():
    assert validate_config(DEFAULT, DEFAULT) is True


def test_validate_config_rejects_missing_key():
    broken = {"playerok": {"api": {"cookies": ""}}, "logs": {"max_file_size": 512}}
    assert validate_config(broken, DEFAULT) is False


def test_validate_config_rejects_wrong_type():
    broken = {
        "playerok": {"api": {"cookies": "", "timeout": 30}},
        "logs": {"max_file_size": "512"},  # строка вместо числа
        "enabled": True,
    }
    assert validate_config(broken, DEFAULT) is False


def test_restore_config_adds_missing_keys():
    partial = {"playerok": {"api": {"cookies": "mycookie"}}}
    restored = restore_config(partial, DEFAULT)

    assert restored["playerok"]["api"]["cookies"] == "mycookie"  # значение сохранено
    assert restored["playerok"]["api"]["timeout"] == 30  # добавлено из шаблона
    assert restored["logs"]["max_file_size"] == 512
    assert restored["enabled"] is True


def test_restore_config_fixes_wrong_types():
    broken = {
        "playerok": {"api": {"cookies": "", "timeout": "oops"}},
        "logs": {"max_file_size": 512},
        "enabled": True,
    }
    restored = restore_config(broken, DEFAULT)
    assert restored["playerok"]["api"]["timeout"] == 30


def test_restore_config_does_not_mutate_input():
    partial = {"playerok": {"api": {"cookies": "x"}}}
    restore_config(partial, DEFAULT)
    assert "timeout" not in partial["playerok"]["api"]
