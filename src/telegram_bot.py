import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from daily_currency import client

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

rates = await client.hgetall("currencies:rates")
names = await client.hgetall("currencies:names")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Здравствуйте, {message.from_user.full_name}! "
                         f"Этот бот позволяет просмотреть актуальные курсы валют с помощью команды /rates , "
                         f"а так же посчитать обмен между доступными валютами с помощью команды /exchange "
                         f"(например /exchange USD RUB 10)")


@dp.message(Command('exchange'))
async def command_exchange_handler(message: Message) -> None:
    msg_args = message.text.split()

    await message.answer(message.text)


@dp.message(Command('rates'))
async def command_rates_handler(message: Message) -> None:
    rates_msg = "\n".join(
        f"{names[key].decode('utf-8')} ({key.decode('utf-8')}) - {value.decode('utf-8')} руб."
        for key, value in rates.items())
    await message.answer(rates_msg)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
