import os
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiohttp import web

TOKEN = "8534597622:AAGy2BFWxae892IghQylbkCoxjGdHvNrq0g"
MY_ID = 8389699824

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="OK")

@dp.message()
async def catch_all(message: types.Message):
    await bot.send_message(MY_ID, f"Сообщение от {message.from_user.id}: {message.content_type}")
    if message.text and message.text.startswith("/start"):
        info = await bot.get_me()
        await message.answer(f"Бот @{info.username}")
    elif message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order = data["order"]
        total = data["total"]
        text = "🛒 Заказ:\n\n"
        for item in order:
            text += f"• {item['name']} x{item['qty']} — {item['price']}₽\n"
        text += f"\n💰 Итого: {total}₽"
        await bot.send_message(MY_ID, text)
        await message.answer("✅ Принято!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())