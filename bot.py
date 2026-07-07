import os
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiohttp import web

TOKEN = "8534597622:AAEZFSvryRX_6m03Mkcr_FAbOZ2tBPFz0sg"
MY_ID = 8389699824

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="OK")

# Обрабатываем ВСЕ сообщения
@dp.message()
async def catch_all(message: types.Message):
    # Пересылаем сообщение тебе в личку (чтобы убедиться, что бот работает)
    await bot.send_message(MY_ID, f"Получено сообщение от {message.from_user.id}\nТип: {message.content_type}\nДанные: {message.web_app_data}")

    # Если это заказ – оформляем
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order = data['order']
        total = data['total']
        text = "🛒 Новый заказ!\n\n"
        for item in order:
            text += f"• {item['name']} x{item['qty']} — {item['price']}₽\n"
        text += f"\n💰 Итого: {total}₽"
        await bot.send_message(MY_ID, text)
        await message.answer("✅ Заказ принят! Скоро свяжусь с вами.")
    elif message.text == "/start":
        await message.answer("Привет! Открой магазин через кнопку Меню 👇")
    else:
        await message.answer("Сообщение получено")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())