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
    kb = [
        [types.KeyboardButton(text="🛍 Каталог", web_app=types.WebAppInfo(url="https://darling-sable-0c139f.netlify.app"))],
        [types.KeyboardButton(text="💬 Отзывы"), types.KeyboardButton(text="📞 Поддержка")],
        [types.KeyboardButton(text="❓ FAQ"), types.KeyboardButton(text="🎁 Акции")],
        [types.KeyboardButton(text="📦 Доставка"), types.KeyboardButton(text="💳 Оплата")],
        [types.KeyboardButton(text="🔥 Новинки"), types.KeyboardButton(text="🏆 Хиты продаж")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        "💨 <b>Добро пожаловать в AMATIL VAPE!</b>\n\n"
        "🚀 Твой проводник в мир авторских вкусов и оригинальных девайсов.\n\n"
        "Выбери, что тебя интересует:",
        reply_markup=keyboard
    )

@dp.message()
async def handle_all(message: types.Message):
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order = data["order"]
        total = data["total"]
        user = message.from_user
        name = user.full_name
        if user.username:
            name += f" (@{user.username})"
        text = f"🛒 <b>Новый заказ!</b>\n\n👤 {name}\n🆔 ID: {user.id}\n\n"
        for item in order:
            text += f"• {item['name']} x{item['qty']} — {item['price'] * item['qty']}₽\n"
        text += f"\n💰 <b>Итого:</b> {total}₽"
        await bot.send_message(MY_ID, text)
        await message.answer(
            "✅ <b>Заказ принят!</b>\n\n"
            "Скоро свяжусь с вами для уточнения деталей.\n\n"
            "📲 Мой контакт: @Fe3riko"
        )
    elif message.text == "💬 Отзывы":
        await message.answer(
            "💬 <b>Отзывы наших клиентов</b>\n\n"
            "Реальные люди, реальные эмоции:\n"
            "👉 https://t.me/amatilrev\n\n"
            "Хочешь оставить отзыв? Пиши @Fe3riko"
        )
    elif message.text == "📞 Поддержка":
        await message.answer(
            "📞 <b>Связь со мной</b>\n\n"
            "По любым вопросам — пиши:\n"
            "👉 @Fe3riko\n\n"
            "Отвечаю быстро, помогаю с выбором!"
        )
    elif message.text == "❓ FAQ":
        await message.answer(
            "❓ <b>Частые вопросы</b>\n\n"
            "📦 Доставка по РФ — 2-4 дня\n"
            "💳 Оплата — перевод/наличные\n"
            "🛡 Гарантия на устройства — 14 дней\n"
            "🧪 Жижи — только авторские, не Китай\n"
            "🔄 Обмен/возврат — в течение 7 дней"
        )
    elif message.text == "🎁 Акции":
        await message.answer(
            "🎁 <b>Акции и предложения</b>\n\n"
            "🔥 Заказ от 1500₽ — пробник в подарок\n"
            "👥 Приведи друга — скидка 10%\n"
            "🚚 Первый заказ — бесплатная доставка\n"
            "💎 Постоянным клиентам — особые условия"
        )
    elif message.text == "📦 Доставка":
        await message.answer(
            "📦 <b>Доставка</b>\n\n"
            "• Почта России / СДЭК / Boxberry\n"
            "• Отправка день в день\n"
            "• Трек-номер сразу после отправки\n"
            "• Среднее время — 2-4 дня\n\n"
            "По вопросам — @Fe3riko"
        )
    elif message.text == "💳 Оплата":
        await message.answer(
            "💳 <b>Оплата</b>\n\n"
            "• Перевод на карту\n"
            "• Наличные при встрече (Москва)\n"
            "• Безопасная сделка через Telegram\n\n"
            "Подробности — @Fe3riko"
        )
    elif message.text == "🔥 Новинки":
        await message.answer(
            "🔥 <b>Новинки</b>\n\n"
            "Следи за обновлениями в каталоге!\n"
            "🛍 Жми «Каталог», чтобы увидеть актуальные позиции."
        )
    elif message.text == "🏆 Хиты продаж":
        await message.answer(
            "🏆 <b>Хиты продаж</b>\n\n"
            "• XROS 5 — легендарный под-мод\n"
            "• ANNIMA LOVE & ZOMBI — топ-жижа\n\n"
            "🛍 Жми «Каталог», чтобы заказать!"
        )

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