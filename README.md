<div align="center">

# 🟦 PAP — Playerok Auto Placement

### 🤖 Умный бот-помощник для маркетплейса **Playerok** с полным управлением из Telegram

*Ваш магазин работает 24/7 — авто-выдача, авто-поднятие, авто-подтверждение и десятки других фишек, пока вы отдыхаете* ✨

<br/>

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-31210/)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](#-docker)
[![CI](https://img.shields.io/github/actions/workflow/status/railingshell/Playerok-Auto-Placement-v2.0/ci.yml?style=for-the-badge&label=CI&logo=githubactions&logoColor=white)](../../actions)
[![License](https://img.shields.io/badge/License-Custom-important?style=for-the-badge)](LICENSE.txt)

<br/>

**[⚙️ Функционал](#️-функционал)** ·
**[⬇️ Установка](#️-установка)** ·
**[🔐 Безопасность](#-безопасность)** ·
**[💾 Бэкап](#-бэкап-и-восстановление)** ·
**[🐳 Docker](#-docker)** ·
**[📚 Разработчикам](#-разработчикам)** ·
**[🔗 Ссылки](#-ссылки)**

</div>

---

## 💡 Что это такое?

**PAP (Playerok Auto Placement)** — многофункциональный бот, который автоматизирует
рутину продавца на [Playerok](https://playerok.com): сам выдаёт товары, поднимает
лоты в топ, отвечает покупателям, подтверждает сделки и присылает уведомления —
всё это управляется из удобного **Telegram-бота**.

> 🧩 Гибкая **система модулей** позволяет расширять возможности бота готовыми
> плагинами (Roblox, Steam) или писать свои.

---

## ⚙️ Функционал

### 🤖 Полное управление в Telegram-боте
| | |
|---|---|
| 🎪 Удобное меню | 💬 Просмотр и ответы в чатах |
| 🖼️ Отправка изображений | 🌟 Просмотр отзывов с фильтрами |
| 📋 Управление сделками | 🛍️ Управление товарами |
| 🛠️ Настройка конфигов | 📊 Статистика (24 ч / неделя / месяц / всё время) |
| 👤 Подробный профиль | 🗒️ Просмотр логов из консоли |
| 🔔 Уведомления о событиях | ⚡ Быстрые ответы одной кнопкой |

### ✨ Автоматизация и возможности
- 🧩 **Система модулей** — подключаемые плагины
- 🟢 **Вечный онлайн** на сайте
- 🎈 **Сообщения на события** (приветствие, новая продажа…)
- ❗ **Собственные команды**
- 🚀 **Авто-выдача товаров** (поштучно и сообщением)
- ⬆️ **Авто-поднятие товаров** в топ
- ♻️ **Восстановление товаров** (проданных и истёкших)
- ☑️ **Авто-подтверждение сделок**
- 💸 **Авто-вывод средств**
- 🌐 **Подключение прокси**
- …и многое другое

### 🎮 Готовые модули
| Модуль | Что делает | Панель |
|--------|-----------|--------|
| 🎲 **Roblox** | Дропшиппинг-выдача Roblox-аккаунтов через LZT Market по тегу сделки | `/roblox_panel` |
| 🕹️ **Steam Offline** | Офлайн-активация Steam с выдачей кодов Steam Guard | `/autosteamoffline` |
| 🔑 **Steam Rental** | Аренда Steam-аккаунтов с maFile, таймерами и сменой пароля | `/autosteamrental` |

---

## ⬇️ Установка

> 🐍 Требуется **Python 3.12.x** — на других версиях работа не гарантируется.

<details open>
<summary><strong>🔷 Windows</strong></summary>

<br/>

1. Установите **Python 3.12.x** с [python.org](https://www.python.org/downloads/release/python-31210/) (отметьте галочку `Add to PATH`).
2. Скачайте последний [Release](../../releases) и распакуйте в удобное место.
3. Запустите `install.bat` и дождитесь установки зависимостей.
4. Запустите бота через `start.bat`.
5. После первого запуска следуйте инструкциям в консоли.

</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

<br/>

1. Установите **Python 3.12.x** с [официального сайта](https://www.python.org/downloads/release/python-31210/) или через Homebrew:
   ```bash
   brew install python@3.12
   ```
2. Скачайте последний [Release](../../releases) и распакуйте.
3. Дважды кликните `install_mac.command` — дождитесь установки зависимостей.
4. Запустите бота двойным кликом по `start_mac.command`.
5. Следуйте инструкциям в консоли.

</details>

<details>
<summary><strong>♨️ Linux (Ubuntu 24)</strong></summary>

<br/>

Выполните одну команду — установщик сам поставит всё необходимое:

```bash
bash <(curl -s https://raw.githubusercontent.com/lovesort/playerok-auto-placement/main/install.sh)
```

**🕹️ Команды управления:**

| Команда | Действие |
|---------|----------|
| `plpap` | 🕹️ Меню с командами |
| `plpap setup` | ⚙️ Первичная настройка |
| `plpap start` | 🟢 Запуск бота |
| `plpap stop` | ⛔ Остановка бота |
| `plpap restart` | 🔄️ Перезапуск бота |
| `plpap status` | 📈 Статус бота |
| `plpap log` | 🗒️ Логи бота |
| `plpap log100` | 📃 Последние 100 логов |
| `plpap update` | 🔵 Обновление бота |
| `plpap backup` | 💾 Бэкап настроек и данных |
| `plpap restore <архив>` | ♻️ Восстановление из бэкапа |
| `plpap enable` | ☑️ Включить авто-запуск |
| `plpap disable` | ❌ Выключить авто-запуск |

</details>

---

## 🐳 Docker

Самый простой способ запустить бота в изоляции — через Docker.

```bash
# 1. Сгенерируйте ключ шифрования секретов (см. раздел «Безопасность»)
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 2. Пропишите ключ в docker-compose.yml (PAP_SECRET_KEY) и запустите
docker compose up -d --build

# 3. Первичная настройка — в интерактивном режиме
docker compose run --rm pap python bot.py
```

Настройки, данные и логи сохраняются в томах `bot_settings/`, `bot_data/`, `logs/`
и переживают пересоздание контейнера. 🗂️

> 💡 В Docker рекомендуется отключить авто-обновление (`updates.auto_update = false`
> в конфиге) и обновлять образ пересборкой.

---

## 🔐 Безопасность

Чувствительные данные (**cookies** Playerok, **токен** Telegram, реквизиты для
вывода средств) теперь хранятся на диске **в зашифрованном виде** —
с префиксом `enc::`. Код при этом продолжает работать с обычными строками:
шифрование и расшифровка происходят прозрачно.

- 🔑 **Ключ шифрования** берётся из переменной окружения `PAP_SECRET_KEY` либо
  автоматически создаётся в `bot_settings/.secret_key` (файл в `.gitignore` —
  в репозиторий не попадёт).
- ♻️ **Бесшовная миграция:** старые конфиги в открытом виде продолжают работать и
  шифруются автоматически при следующем сохранении.
- 🧯 **Отказоустойчивость:** если библиотека `cryptography` не установлена или задан
  `PAP_DISABLE_ENCRYPTION=1`, бот продолжит работать без шифрования.

> ⚠️ **Сделайте резервную копию `bot_settings/.secret_key`!** Без него зашифрованные
> данные восстановить нельзя. При переносе бота на другой сервер перенесите и ключ
> (или задайте один и тот же `PAP_SECRET_KEY`).

---

## 💾 Бэкап и восстановление

Встроенный кросс-платформенный скрипт сохраняет настройки и данные (включая ключ
шифрования) в локальный архив.

```bash
python backup.py create            # создать бэкап в папке backups/
python backup.py list              # показать список бэкапов
python backup.py restore <архив>   # восстановить из архива
```

Бэкап включает `bot_settings/` (конфиги + `.secret_key`) и `bot_data/`.
На Linux доступны быстрые команды `plpap backup` и `plpap restore <архив>`, в
Windows-меню — пункт **«Sozdat bekap»**, а в самом Telegram-боте — раздел
**💾 Бэкап** (кнопки «Создать бэкап» и «Список бэкапов»).

> 🔒 **Почему не на GitHub?** Архив содержит ключ шифрования и токены — вместе они
> равносильны данным в открытом виде. Храните бэкапы в **надёжном приватном месте**
> (зашифрованный диск, менеджер секретов) и никогда не загружайте их в публичные
> репозитории или сторонние сервисы. Папка `backups/` добавлена в `.gitignore`.

---

## 📚 Разработчикам

Модульная система помогает добавлять в бота новый функционал в удобном формате
(по сути — плагины). Свой модуль можно собрать по [шаблону](.templates/forms_module).

### 🧪 Тесты, линтинг и качество кода

```bash
# Установка dev-зависимостей
pip install -r requirements-dev.txt

# Запуск тестов
pytest

# Проверка стиля кода
ruff check .

# Авто-исправление и хуки перед коммитом
pre-commit install
```

CI на GitHub Actions автоматически прогоняет **ruff** и **pytest** на каждый
push и pull request. ✅

<details>
<summary><strong>📌 Основные ивенты</strong></summary>

<br/>

**Ивенты бота (`BOT_EVENT_HANDLERS`)** — выполняются при действиях самого бота:

| Ивент | Когда вызывается | Аргументы |
|-------|------------------|-----------|
| `ON_MODULE_ENABLED` | При включении модуля | `Module` |
| `ON_MODULE_DISABLED` | При выключении модуля | `Module` |
| `ON_INIT` | При инициализации бота | `-` |
| `ON_PLAYEROK_BOT_INIT` | При запуске Playerok-бота | `PlayerokBot` |
| `ON_TELEGRAM_BOT_INIT` | При запуске Telegram-бота | `TelegramBot` |

**Ивенты Playerok (`PLAYEROK_EVENT_HANDLERS`)** — из слушателя событий:

| Ивент | Когда вызывается | Аргументы |
|-------|------------------|-----------|
| `CHAT_INITIALIZED` | Чат инициализирован | `PlayerokBot`, `ChatInitializedEvent` |
| `NEW_MESSAGE` | Новое сообщение в чате | `PlayerokBot`, `NewMessageEvent` |
| `NEW_DEAL` | Создана новая сделка (покупатель оплатил) | `PlayerokBot`, `NewDealEvent` |
| `NEW_REVIEW` | Новый отзыв по сделке | `PlayerokBot`, `NewReviewEvent` |
| `DEAL_CONFIRMED` | Сделка подтверждена | `PlayerokBot`, `DealConfirmedEvent` |
| `DEAL_ROLLED_BACK` | Продавец оформил возврат | `PlayerokBot`, `DealRolledBackEvent` |
| `DEAL_HAS_PROBLEM` | Пользователь сообщил о проблеме | `PlayerokBot`, `DealHasProblemEvent` |
| `DEAL_PROBLEM_RESOLVED` | Проблема решена | `PlayerokBot`, `DealProblemResolvedEvent` |
| `DEAL_STATUS_CHANGED` | Статус сделки изменён | `PlayerokBot`, `DealStatusChangedEvent` |
| `ITEM_PAID` | Пользователь оплатил предмет | `PlayerokBot`, `ItemPaidEvent` |
| `ITEM_SENT` | Предмет отправлен | `PlayerokBot`, `ItemSentEvent` |

</details>

<details>
<summary><strong>📁 Строение модуля</strong></summary>

<br/>

Модуль — это папка с важными компонентами. За основу можно взять
[шаблонный модуль](.templates/forms_module).

**Обязательные константы хендлеров:**
| Константа | Тип | Описание |
|-----------|-----|----------|
| `BOT_EVENT_HANDLERS` | `dict[str, list[Any]]` | Хендлеры ивентов бота |
| `PLAYEROK_EVENT_HANDLERS` | `dict[EventTypes, list[Any]]` | Хендлеры ивентов Playerok |
| `TELEGRAM_BOT_ROUTERS` | `list[Router]` | Роутеры Telegram-бота модуля |

**Обязательные константы метаданных:**
| Константа | Тип | Описание |
|-----------|-----|----------|
| `PREFIX` | `str` | Префикс |
| `VERSION` | `str` | Версия |
| `NAME` | `str` | Название |
| `DESCRIPTION` | `str` | Описание |
| `AUTHORS` | `str` | Авторы |
| `LINKS` | `str` | Ссылки на авторов |

Если модуль требует дополнительных зависимостей — добавьте `requirements.txt` в его
папку, они установятся автоматически при загрузке модулей.

#### 🔧 Пример `meta.py`:
```python
from colorama import Fore

PREFIX = f"{Fore.LIGHTCYAN_EX}[test module]{Fore.WHITE}"
VERSION = "0.1"
NAME = "test_module"
DESCRIPTION = "Тестовый модуль. /test_module в Telegram боте для управления"
AUTHORS = "@rogaart"
LINKS = "https://t.me/lovesort"
```

#### 🔧 Пример `__init__.py`:
```python
from playerokapi.listener.events import EventTypes
from core.modules_manager import Module, disable_module

from .plbot.handlers import on_playerok_bot_init, on_new_message, on_new_deal
from .tgbot import router
from .tgbot._handlers import on_telegram_bot_init
from .meta import *


_module: Module = None


def set_module(module: Module):
    global _module
    _module = module

def get_module():
    return _module

async def on_module_enabled(module: Module):
    try:
        set_module(module)
        print(f"{PREFIX} Модуль подключен и активен")
    except Exception:
        await disable_module(_module.uuid)


BOT_EVENT_HANDLERS = {
    "ON_MODULE_ENABLED": [on_module_enabled],
    "ON_PLAYEROK_BOT_INIT": [on_playerok_bot_init],
    "ON_TELEGRAM_BOT_INIT": [on_telegram_bot_init]
}
PLAYEROK_EVENT_HANDLERS = {
    EventTypes.NEW_MESSAGE: [on_new_message],
    EventTypes.NEW_DEAL: [on_new_deal],
    # ...
}
TELEGRAM_BOT_ROUTERS = [router]
```

</details>

<details>
<summary><strong>🛠️ Полезные инструменты</strong></summary>

<br/>

### 📝 Готовые врапперы файлов конфигурации и данных
Вместо ручной работы с JSON-файлами используйте готовые классы из
[`settings.py`](settings.py) и [`data.py`](data.py).

Создайте `settings.py` в корне модуля:
```python
import os
from settings import Settings as sett, SettingsFile

CONFIG = SettingsFile(
    name="config",
    path=os.path.join(os.path.dirname(__file__), "module_settings", "config.json"),
    need_restore=True,
    default={"bool_param": True, "str_param": "qwerty", "int_param": 123}
)

DATA = [CONFIG]


class Settings:
    @staticmethod
    def get(name: str) -> dict:
        return sett.get(name, DATA)

    @staticmethod
    def set(name: str, new: list | dict) -> dict:
        return sett.set(name, new, DATA)
```

Чтение и запись:
```python
from . import settings as sett

config = sett.get("config")
print(config["bool_param"])  # -> True
config["bool_param"] = False
sett.set("config", config)   # сразу пишется в файл
```

| Аргумент `SettingsFile` | Описание |
|----------|----------|
| `name` | Имя конфига для чтения/записи |
| `path` | Путь к файлу |
| `need_restore` | Автовосстановление недостающих/некорректных ключей из шаблона |
| `default` | Стандартное значение |

Файл данных (`data.py`) устроен аналогично, но хранит информацию, собранную самим
скриптом, а не заданную пользователем.

### 🔌 Управление состоянием модуля
```python
from core.modules import enable_module, disable_module, reload_module
from . import get_module

await disable_module(get_module().uuid)  # выключить
await enable_module(get_module().uuid)   # включить
await reload_module(get_module().uuid)   # перезагрузить
```

</details>

<details>
<summary><strong>❗ Примечания</strong></summary>

<br/>

Telegram-бот написан на **aiogram 3**; пользовательский функционал внедряется через
роутеры, которые сливаются с главным роутером. Из-за слияния возможны конфликты, если
`callback`-данные имеют одинаковые названия. Поэтому давайте им уникальные имена,
чтобы они не совпадали с основным ботом или другими модулями.

</details>

---

## 🗂️ Структура проекта

```
├── 🤖 bot.py              # точка входа
├── ⚙️ settings.py / data.py  # врапперы конфигов и данных (+ шифрование секретов)
├── 🔧 utils.py            # утилиты и валидаторы
├── 🔄 updater.py          # авто-обновление через GitHub Releases
├── 📦 core/               # ядро: модули, хендлеры, утилиты, шифрование (secrets.py)
├── 🟦 playerokapi/        # самописная обёртка над API Playerok
├── 💬 tgbot/              # Telegram-бот (хендлеры, состояния, шаблоны)
├── 🛰️ plbot/              # логика на стороне Playerok
├── 🧩 modules/            # подключаемые модули (roblox, steam…)
├── 🧪 tests/              # автотесты (pytest)
└── 🐳 Dockerfile / docker-compose.yml
```

---

## 🔗 Ссылки
- 👨‍💻 **Разработчик:** [@lovesort](https://t.me/lovesort) (rogaart)
- 📰 **Новости:** [@rogaartproduction](https://t.me/rogaartproduction)
- 🧩 **Плагины:** [@lovesort](https://t.me/lovesort)

<div align="center">

<br/>

⭐ **Понравился проект? Поставьте звезду!** ⭐

*Сделано с ❤️ для сообщества Playerok*

</div>
