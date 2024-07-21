import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Здравствуйте, {message.from_user.full_name}! "
                         f"Этот бот позволяет просмотреть актуальные курсы валют с помощью команды /rates , "
                         f"а так же посчитать обмен между доступными валютами с помощью команды /exchange "
                         f"(например /exchange USD RUB 10)")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
