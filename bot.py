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

@dp.message()
async def catch_all(message: types.Message):
    if message.content_type == "web_app_data":
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