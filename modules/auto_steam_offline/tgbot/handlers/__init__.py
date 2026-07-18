from aiogram import Router

from . import entering
from . import commands

router = Router()
router.include_router(entering.router)
router.include_router(commands.router)
