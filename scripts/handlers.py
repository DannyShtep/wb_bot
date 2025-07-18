from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher # ИЗМЕНЕНО: Импортируем Dispatcher
from states import BookingState
from scheduler import start_monitoring
from wb_api import get_available_draft_supplies

# ИЗМЕНЕНО: Удаляем глобальную инициализацию dp здесь.
# Вместо этого, создаем функцию, которая будет принимать dp.

def register_handlers(dp: Dispatcher): # ИЗМЕНЕНО: Создаем функцию для регистрации обработчиков
    @dp.message_handler(commands=['start'], state='*')
    async def start_cmd(message: types.Message, state: FSMContext):
        await message.answer("Привет, я бот автобронирования поставок на WB по твоим критериям - введи свой токен WB API, укажи необходимую информацию и ожидай бронирования! Бот обязательно пришлет тебе уведомление об успешном бронировании.")
        await BookingState.waiting_for_token.set()

    @dp.message_handler(state=BookingState.waiting_for_token)
    async def process_token(message: types.Message, state: FSMContext):
        await state.update_data(token=message.text.strip())
        try:
            supplies = await get_available_draft_supplies(message.text.strip())
            if not supplies:
                await message.answer("❌ У вас нет черновиков поставок.")
                await state.finish()
                return
            text = "📦 Найдены черновики поставок:\n\n"
            buttons = []
            for s in supplies:
                text += f"• {s['id']} — создан: {s['createdAt'][:10]}\n"
                buttons.append(types.InlineKeyboardButton(f"{s['id']}", callback_data=f"choose_supply:{s['id']}"))
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            await message.answer(text + "\n👉 Выбери нужную поставку:", reply_markup=keyboard)
            await BookingState.waiting_for_supply_choice.set()
        except Exception as e:
            await message.answer(f"❌ Ошибка: {str(e)}")
            await state.finish()

    @dp.callback_query_handler(lambda c: c.data.startswith("choose_supply:"), state=BookingState.waiting_for_supply_choice)
    async def process_supply_choice(callback_query: types.CallbackQuery, state: FSMContext):
        supply_id = callback_query.data.split(":")[1]
        await state.update_data(supply_id=supply_id)
        await callback_query.message.edit_reply_markup()

        # Показываем кнопки типов приёмки
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("Бесплатно", callback_data="type:x0"),
            types.InlineKeyboardButton("x1", callback_data="type:x1"),
            types.InlineKeyboardButton("x2", callback_data="type:x2"),
            types.InlineKeyboardButton("x3", callback_data="type:x3")
        )
        await callback_query.message.answer("Выберите тип приёмки:", reply_markup=keyboard)
        await BookingState.waiting_for_type.set()

    @dp.callback_query_handler(lambda c: c.data.startswith("type:"), state=BookingState.waiting_for_type)
    async def process_type_choice(callback_query: types.CallbackQuery, state: FSMContext):
        selected_type = callback_query.data.split(":")[1]
        await state.update_data(type=selected_type)
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer("📅 Введите интервал дат (например, 2025-07-20,2025-07-25):")
        await BookingState.waiting_for_date_range.set()

    @dp.message_handler(state=BookingState.waiting_for_date_range)
    async def process_date_range(message: types.Message, state: FSMContext):
        try:
            start_str, end_str = map(str.strip, message.text.split(','))
            await state.update_data(start_date=start_str, end_date=end_str)
            # Кнопка "Отменить"
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add("🚫 Отменить планирование")
            await message.answer("🔍 Начинаю мониторинг слотов...", reply_markup=keyboard)
            data = await state.get_data()
            await state.finish()
            await start_monitoring(message.chat.id, data, message)
        except:
            await message.answer("⚠️ Неверный формат. Введите как: 2025-07-20,2025-07-25")

    @dp.message_handler(lambda msg: "отменить" in msg.text.lower(), state="*")
    async def cancel_planning(message: types.Message, state: FSMContext):
        await state.finish()
        keyboard = types.ReplyKeyboardRemove()
        await message.answer("❌ Планирование отменено.", reply_markup=keyboard)
