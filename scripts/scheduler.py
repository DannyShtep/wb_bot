import asyncio
from .wb_api import get_available_slots, book_slot # Modified import for relative path
from aiogram import types

async def start_monitoring(user_id, data, message: types.Message):
    token = data['token']
    start = data['start_date']
    end = data['end_date']
    type_pref = data['type']
    supply_id = data['supply_id']

    interval = 1
    retries = 0

    while True:
        try:
            slots = await get_available_slots(token)
            suitable = [s for s in slots if start <= s['date'] <= end and s['type'] == type_pref]
            if suitable:
                result = await book_slot(token, suitable[0], supply_id)
                await message.answer(
                    f"✅ <b>Поставка забронирована!</b>\n"
                    f"📅 Дата: {suitable[0]['date']}\n"
                    f"🏢 Склад: {suitable[0]['warehouse']}\n"
                    f"📦 Тип приёмки: {suitable[0]['type']}",
                    parse_mode='HTML'
                )
                return
            await asyncio.sleep(interval)
        except Exception as e:
            retries += 1
            wait_time = min(10, 2 * retries)
            await message.answer(f"⚠️ Ошибка при обращении к WB API: {str(e)}\n⏳ Повтор через {wait_time} сек...")
            await asyncio.sleep(wait_time)
