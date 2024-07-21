import asyncio

import aiohttp
import xml.etree.ElementTree as et
import redis.asyncio as redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler

client = redis.Redis(host="redis", port=6379)


async def get_currencies() -> dict[str, tuple]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cbr.ru/scripts/XML_daily.asp") as response:
            if response.status == 200:
                currencies_raw = await response.text()
            else:
                raise ConnectionError("Can't get currencies from server")

    element_tree = et.fromstring(currencies_raw)
    currencies_elements = element_tree.findall("Valute")
    currencies_dict = {}
    for currency in currencies_elements:
        currencies_dict[currency.find("CharCode").text] = (
            float(currency.find("VunitRate").text.replace(',', '.')), currency.find("Name").text)
    return currencies_dict


async def upload_data():
    currencies = await get_currencies()

    await client.hset("currencies:names", mapping={item[0]: item[1][1] for item in currencies.items()})
    await client.hset("currencies:rates", mapping={item[0]: item[1][0] for item in currencies.items()})


async def main_worker():
    await upload_data()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(upload_data, 'cron', hour=15, minute=0)
    scheduler.start()
    while True:
        await asyncio.sleep(1000)


asyncio.run(main_worker())
