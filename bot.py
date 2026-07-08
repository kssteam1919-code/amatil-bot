import os
import asyncio
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
    if message.text and message.text.startswith("/start"):
        await message.answer("Бот работает!")
    elif message.web_app_data:
        await bot.send_message(MY_ID, "Получен заказ!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    await web.TCPSite(runner, "0.0.0.0", port).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())