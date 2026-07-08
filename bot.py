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
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🛍 Каталог", web_app=types.WebAppInfo(url="https://darling-sable-0c139f.netlify.app"))],
            [types.KeyboardButton(text="💬 Отзывы"), types.KeyboardButton(text="📞 Связаться")],
            [types.KeyboardButton(text="❓ FAQ"), types.KeyboardButton(text="🎁 Акции")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    await message.answer(
        "💨 Добро пожаловать в AMATIL VAPE!\n\nВыбирай, что тебя интересует:",
        reply_markup=keyboard
    )

@dp.message()
async def handle_buttons(message: types.Message):
    # Обрабатываем кнопки
    if message.text == "💬 Отзывы":
        await message.answer("💬 Наши отзывы: https://t.me/amatilrevtest2")
    elif message.text == "📞 Связаться":
        await message.answer("📞 Связь со мной: @Fe3riko")
    elif message.text == "❓ FAQ":
        await message.answer(
            "❓ Часто задаваемые вопросы:\n\n"
            "• Доставка по России — 2-4 дня\n"
            "• Оплата — переводом/наличными\n"
            "• Гарантия на устройства — 14 дней\n"
            "• Жижи только авторские, не Китай"
        )
    elif message.text == "🎁 Акции":
        await message.answer(
            "🎁 Текущие акции:\n\n"
            "• При заказе от 1500₽ — пробник в подарок\n"
            "• Приведи друга — скидка 10%\n"
            "• Первый заказ — бесплатная доставка"
        )
    # Обрабатываем заказ из Mini App
    elif message.web_app_data:
        try:
            data = json.loads(message.web_app_data.data)
            order = data['order']
            total = data['total']
            
            # Формируем уведомление тебе
            user_info = f"👤 Покупатель: {message.from_user.full_name}"
            if message.from_user.username:
                user_info += f" (@{message.from_user.username})"
            user_info += f"\nID: {message.from_user.id}"
            
            order_text = "🛒 Новый заказ!\n\n" + user_info + "\n\n"
            for item in order:
                order_text += f"• {item['name']} x{item['qty']} — {item['price'] * item['qty']}₽\n"
            order_text += f"\n💰 Итого: {total}₽"
            
            # Отправляем уведомление тебе
            await bot.send_message(MY_ID, order_text)
            # Отвечаем покупателю
            await message.answer("✅ Заказ принят! Скоро свяжусь с вами.\n\n📲 Мой контакт: @Fe3riko")
        except Exception as e:
            await bot.send_message(MY_ID, f"❌ Ошибка при разборе заказа: {e}")
            await message.answer("⚠️ Произошла ошибка. Пожалуйста, свяжитесь со мной напрямую: @Fe3riko")
    else:
        # На случай текстовых сообщений, которые не являются кнопками
        await message.answer("Используйте кнопки меню для навигации 👇")

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