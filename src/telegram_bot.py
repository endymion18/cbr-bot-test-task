import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from daily_currency import client
from utils import parse_args

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

rates = {key.decode('utf-8'): value.decode('utf-8')
         for key, value in asyncio.get_event_loop().run_until_complete(client.hgetall("currencies:rates")).items()}
currencies_codes = list(rates.keys())
currencies_codes.append("RUB")
names = {key.decode('utf-8'): value.decode('utf-8')
         for key, value in asyncio.get_event_loop().run_until_complete(client.hgetall("currencies:names")).items()}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Здравствуйте, {message.from_user.full_name}! "
                         f"Этот бот позволяет просмотреть актуальные курсы валют с помощью команды /rates , "
                         f"а так же посчитать обмен между доступными валютами с помощью команды /exchange "
                         f"(например /exchange USD RUB 10)")


@dp.message(Command('exchange'))
async def command_exchange_handler(message: Message, command: CommandObject) -> None:
    try:
        args = await parse_args(command.args, currencies_codes)
        if args[0] == "RUB":
            await message.answer(f"{args[2]} {args[0]} = {str(args[2] / float(rates[args[1]]))} {args[1]}")
            return
        answer_rub = float(rates[args[0]]) * args[2]
        if args[1] == "RUB":
            await message.answer(f"{args[2]} {args[0]} = {str(answer_rub)} RUB")
        else:
            answer_other = answer_rub / float(rates[args[1]])
            await message.answer(f"{args[2]} {args[0]} = {str(answer_other)} {args[1]}")

    except AttributeError as err:
        await message.answer(err.__str__())


@dp.message(Command('rates'))
async def command_rates_handler(message: Message) -> None:
    rates_msg = "\n".join(
        f"{names[key]} ({key}) - {value} руб."
        for key, value in rates.items())
    await message.answer(rates_msg)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
