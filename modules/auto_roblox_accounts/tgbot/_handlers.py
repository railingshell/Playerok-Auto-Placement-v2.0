from aiogram.types import BotCommand
from tgbot.telegrambot import TelegramBot
from logging import getLogger

from ..meta import NAME


logger = getLogger(f"{NAME}.telegram")


async def on_telegram_bot_init(tgbot: TelegramBot) -> None:
    try:
        main_menu_commands = await tgbot.bot.get_my_commands()
        roblox_menu_commands = [BotCommand(command=f"/roblox_panel", description=f"🧱 Управление {NAME}")]
        await tgbot.bot.set_my_commands(list(main_menu_commands + roblox_menu_commands))
    except:
        pass
