#!/usr/bin/env python3
"""
💾 Локальный бэкап и восстановление настроек и данных PAP.

Создаёт zip-архив с папками ``bot_settings/`` (включая ключ шифрования
``.secret_key``) и ``bot_data/``. Архивы складываются в ``backups/`` и не
попадают в git.

⚠️ Архив содержит ключ шифрования, cookies и токены. Храните его в надёжном
приватном месте и НИКОГДА не загружайте в публичные репозитории или сторонние
сервисы.

Использование:
    python backup.py create              # создать бэкап
    python backup.py list                # показать список бэкапов
    python backup.py restore <архив>     # восстановить из архива
"""
from __future__ import annotations

import argparse
import os
import sys
import zipfile
from datetime import datetime

# Папки, которые попадают в бэкап (относительно корня проекта)
BACKUP_TARGETS = ["bot_settings", "bot_data"]
BACKUP_DIR = "backups"


def create_backup(targets: list[str] = BACKUP_TARGETS, backup_dir: str = BACKUP_DIR) -> str | None:
    """Создаёт zip-архив с указанными папками. Возвращает путь к архиву или None."""
    existing = [t for t in targets if os.path.isdir(t)]
    if not existing:
        print("⚠️  Нечего бэкапить: папки настроек и данных не найдены.")
        return None

    os.makedirs(backup_dir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_path = os.path.join(backup_dir, f"pap-backup-{stamp}.zip")

    file_count = 0
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for target in existing:
            for root, _dirs, files in os.walk(target):
                for name in files:
                    full = os.path.join(root, name)
                    zf.write(full, arcname=os.path.relpath(full, "."))
                    file_count += 1

    size_kb = os.path.getsize(archive_path) / 1024
    print(f"✅ Бэкап создан: {archive_path} ({file_count} файлов, {size_kb:.1f} КБ)")
    print("⚠️  Архив содержит ключ шифрования и токены — храните его в надёжном месте.")
    return archive_path


def get_backups(backup_dir: str = BACKUP_DIR) -> list[str]:
    """Возвращает список файлов-бэкапов (от новых к старым) без вывода в консоль."""
    if not os.path.isdir(backup_dir):
        return []
    return sorted(
        (f for f in os.listdir(backup_dir) if f.endswith(".zip")),
        reverse=True,
    )


def list_backups(backup_dir: str = BACKUP_DIR) -> list[str]:
    """Возвращает список архивов бэкапов, от новых к старым."""
    archives = get_backups(backup_dir)
    if not archives:
        print("ℹ️  Бэкапов пока нет.")
        return []

    print(f"📦 Найдено бэкапов: {len(archives)}")
    for name in archives:
        path = os.path.join(backup_dir, name)
        size_kb = os.path.getsize(path) / 1024
        print(f"  · {name} ({size_kb:.1f} КБ)")
    return archives


def _is_safe_member(member: str) -> bool:
    """Защита от zip-slip: запрещаем абсолютные пути и выход за пределы папки."""
    if os.path.isabs(member) or member.startswith(("/", "\\")):
        return False
    norm = os.path.normpath(member)
    return not norm.startswith("..")


def restore_backup(archive_path: str, dest: str = ".") -> bool:
    """Восстанавливает файлы из архива в папку назначения (по умолчанию — корень)."""
    if not os.path.isfile(archive_path):
        print(f"❌ Архив не найден: {archive_path}")
        return False

    with zipfile.ZipFile(archive_path, "r") as zf:
        members = zf.namelist()
        unsafe = [m for m in members if not _is_safe_member(m)]
        if unsafe:
            print(f"❌ Архив содержит небезопасные пути, восстановление отменено: {unsafe[:3]}")
            return False
        zf.extractall(dest)

    print(f"✅ Восстановлено из {archive_path} ({len(members)} файлов).")
    print("🔄 Перезапустите бота, чтобы применить восстановленные настройки.")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Бэкап и восстановление настроек и данных PAP.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("create", help="создать бэкап")
    sub.add_parser("list", help="показать список бэкапов")
    restore_p = sub.add_parser("restore", help="восстановить из архива")
    restore_p.add_argument("archive", help="путь к zip-архиву бэкапа")

    args = parser.parse_args(argv)

    if args.command == "create":
        return 0 if create_backup() else 1
    if args.command == "list":
        list_backups()
        return 0
    if args.command == "restore":
        return 0 if restore_backup(args.archive) else 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
