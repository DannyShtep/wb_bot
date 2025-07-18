import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import dp
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp.storage = storage

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())