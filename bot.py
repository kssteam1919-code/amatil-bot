import os
import asyncio
import json
import sys
import traceback
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# === НАСТРОЙКИ ===
TOKEN = "8534597622:AAEZFSvryRX_6m03Mkcr_FAbOZ2tBPFz0sg"       # токен от BotFather
MY_ID = 8389699824                        # твой Telegram ID (число)

# === БОТ ===
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Простой веб-сервер для UptimeRobot
async def handle(request):
    return web.Response(text="OK")

# Команда /start
@dp.message(CommandStart())
async def start(message: types.Message):
    print(f">>> /start от {message.from_user.id}")
    await message.answer("Привет! Открой магазин через кнопку Меню 👇")

# Приём данных из Mini App
@dp.message()
async def catch_all(message: types.Message):
    print("=== ВХОДЯЩЕЕ СООБЩЕНИЕ ===")
    print(f"От: {message.from_user.id}")
    print(f"Тип контента: {message.content_type}")
    print(f"Есть web_app_data: {message.web_app_data is not None}")

    if message.web_app_data:
        try:
            data = json.loads(message.web_app_data.data)
            order = data['order']
            total = data['total']
            text = "🛒 Новый заказ!\n\n"
            for item in order:
                text += f"• {item['name']} x{item['qty']} — {item['price']}₽\n"
            text += f"\n💰 Итого: {total}₽"
            await bot.send_message(MY_ID, text)
            await message.answer("✅ Заказ принят! Скоро свяжусь с вами.")
            print(">>> Заказ обработан успешно")
        except Exception as e:
            print(f"!!! Ошибка обработки заказа: {e}")
            traceback.print_exc()
            await message.answer("⚠️ Произошла ошибка. Попробуйте позже.")
    else:
        await message.answer("Сообщение получено, но это не заказ.")

    print("=========================")

async def main():
    # Запуск веб-сервера
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f">>> Веб-сервер запущен на порту {port}")

    # Запуск поллинга
    print(">>> Бот начал слушать сообщения...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print("!!! КРИТИЧЕСКАЯ ОШИБКА:")
        traceback.print_exc()
        sys.exit(1)