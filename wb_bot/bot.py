import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers import register_handlers # ИЗМЕНЕНО: Импортируем функцию регистрации обработчиков
from config import BOT_TOKEN

# Инициализируем Bot и Dispatcher здесь
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage) # ИЗМЕНЕНО: Передаем bot и storage при инициализации Dispatcher

# Регистрируем все обработчики, передавая dp
register_handlers(dp)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
