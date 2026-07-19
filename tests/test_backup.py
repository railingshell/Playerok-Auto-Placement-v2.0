"""Тесты локального бэкапа/восстановления (backup.py)."""
import os
import zipfile

import backup


def _make_tree(base):
    os.makedirs(os.path.join(base, "bot_settings"), exist_ok=True)
    os.makedirs(os.path.join(base, "bot_data"), exist_ok=True)
    with open(os.path.join(base, "bot_settings", "config.json"), "w", encoding="utf-8") as f:
        f.write('{"cookies": "enc::secret"}')
    with open(os.path.join(base, "bot_settings", ".secret_key"), "w", encoding="utf-8") as f:
        f.write("my-fernet-key")
    with open(os.path.join(base, "bot_data", "stats.json"), "w", encoding="utf-8") as f:
        f.write("{}")


def test_create_and_list(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _make_tree(tmp_path)

    archive = backup.create_backup()
    assert archive is not None
    assert os.path.isfile(archive)

    # В архиве есть и настройки (включая ключ), и данные
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
    assert any(n.endswith("config.json") for n in names)
    assert any(n.endswith(".secret_key") for n in names)
    assert any(n.endswith("stats.json") for n in names)

    assert len(backup.list_backups()) == 1


def test_get_backups_returns_sorted(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert backup.get_backups() == []

    _make_tree(tmp_path)
    backup.create_backup()
    names = backup.get_backups()
    assert len(names) == 1
    assert names[0].endswith(".zip")


def test_create_with_nothing_to_backup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert backup.create_backup() is None


def test_restore_round_trip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _make_tree(tmp_path)
    archive = backup.create_backup()

    # Удаляем настройки и восстанавливаем из архива
    os.remove(os.path.join(tmp_path, "bot_settings", "config.json"))
    os.remove(os.path.join(tmp_path, "bot_settings", ".secret_key"))

    assert backup.restore_backup(archive) is True
    with open(os.path.join(tmp_path, "bot_settings", "config.json"), encoding="utf-8") as f:
        assert f.read() == '{"cookies": "enc::secret"}'
    with open(os.path.join(tmp_path, "bot_settings", ".secret_key"), encoding="utf-8") as f:
        assert f.read() == "my-fernet-key"


def test_restore_missing_archive(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert backup.restore_backup("nope.zip") is False


def test_restore_rejects_unsafe_paths(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    malicious = tmp_path / "evil.zip"
    with zipfile.ZipFile(malicious, "w") as zf:
        zf.writestr("../escape.txt", "pwned")

    assert backup.restore_backup(str(malicious)) is False
    assert not (tmp_path.parent / "escape.txt").exists()
