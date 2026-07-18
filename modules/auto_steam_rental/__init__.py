from core.modules import Module
from logging import getLogger

from playerokapi.enums import EventTypes

from .plbot.handlers import (
    on_new_deal,
    on_new_review,
    run_cycles,
    stop_cycles,
    on_module_enabled,
    on_module_disabled,
    on_telegram_bot_init
)
from .tgbot import router
from .meta import *
from .data import Data
from .settings import Settings


logger = getLogger(NAME)
_module: Module = None


def set_module(new: Module):
    global _module
    _module = new


def get_module():
    return _module


class AutoSteamRental(Module):
    """Автоматическая аренда Steam-аккаунтов."""

    NAME = "auto_steam_rental"
    VERSION = "1.0.0"

    def on_init(self):
        Data.init()
        Settings.init()

    def on_enable(self):
        pass

    def on_disable(self):
        pass


BOT_EVENT_HANDLERS = {
    "ON_MODULE_ENABLED": [on_module_enabled, run_cycles],
    "ON_MODULE_DISABLED": [stop_cycles],
    "ON_TELEGRAM_BOT_INIT": [on_telegram_bot_init]
}

PLAYEROK_EVENT_HANDLERS = {
    EventTypes.NEW_DEAL: [on_new_deal],
    EventTypes.NEW_REVIEW: [on_new_review]
}

TELEGRAM_BOT_ROUTERS = [router]
