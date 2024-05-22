import asyncio
import json
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from utils import get_aggregated_data

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}!")


@dp.message()
async def get_json(message: types.Message):
    try:
        received_json = json.loads(message.text)
        dt_from = datetime.strptime(received_json['dt_from'], '%Y-%m-%dT%H:%M:%S')
        dt_upto = datetime.strptime(received_json['dt_upto'], '%Y-%m-%dT%H:%M:%S')
        group_type = received_json['group_type']
        answer = get_aggregated_data(dt_from, dt_upto, group_type)
        await message.answer(json.dumps(answer))

    except (ValueError, TypeError):
        await message.answer('Невалидный запрос. Пример запроса:\n '
                             '{"dt_from": "2022-09-01T00:00:00", '
                             '"dt_upto": "2022-12-31T23:59:00", '
                             '"group_type": "month"}')


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
