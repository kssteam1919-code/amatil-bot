import os
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

TOKEN = "8534597622:AAGy2BFWxae892IghQylbkCoxjGdHvNrq0g"
MY_ID = 8389699824

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def handle(request):
    return web.Response(text="OK")

@dp.message(CommandStart())
async def start(message: types.Message):
    kb = [[types.KeyboardButton(text="🛍 Каталог", web_app=types.WebAppInfo(url="https://darling-sable-0c139f.netlify.app"))]]
    kb.append([types.KeyboardButton(text="💬 Отзывы"), types.KeyboardButton(text="📞 Связаться")])
    kb.append([types.KeyboardButton(text="❓ FAQ"), types.KeyboardButton(text="🎁 Акции")])
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите действие...")
    await message.answer("💨 Добро пожаловать в AMATIL VAPE!\n\nВыбирай, что тебя интересует:", reply_markup=keyboard)

@dp.message()
async def handle_all(message: types.Message):
    if message.web_app_data:
        try:
            data = json.loads(message.web_app_data.data)
            order = data["order"]
            total = data["total"]
            user = message.from_user
            name = user.full_name
            if user.username:
                name += f" (@{user.username})"
            text = f"🛒 Новый заказ!\n\n👤 {name}\nID: {user.id}\n\n"
            for item in order:
                text += f"• {item['name']} x{item['qty']} — {item['price'] * item['qty']}₽\n"
            text += f"\n💰 Итого: {total}₽"
            await bot.send_message(MY_ID, text)
            await message.answer("✅ Заказ принят! Скоро свяжусь с вами.\n\n📲 Мой контакт: @Fe3riko")
        except Exception as e:
            await bot.send_message(MY_ID, f"Ошибка разбора заказа: {e}")
            await message.answer("⚠️ Ошибка. Свяжитесь напрямую: @Fe3riko")
    elif message.text == "💬 Отзывы":
        await message.answer("💬 Наши отзывы: https://t.me/amatilrevtest2")
    elif message.text == "📞 Связаться":
        await message.answer("📞 Связь со мной: @Fe3riko")
    elif message.text == "❓ FAQ":
        await message.answer("❓ FAQ:\n\n• Доставка по РФ — 2-4 дня\n• Оплата — перевод/наличные\n• Гарантия — 14 дней\n• Жижи — только авторские")
    elif message.text == "🎁 Акции":
        await message.answer("🎁 Акции:\n\n• Заказ от 1500₽ — пробник в подарок\n• Приведи друга — скидка 10%\n• Первый заказ — бесплатная доставка")
    else:
        await message.answer("Используйте кнопки меню 👇")

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