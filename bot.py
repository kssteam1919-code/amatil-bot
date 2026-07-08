import os
import asyncio
import json
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

TOKEN = "8534597622:AAGy2BFWxae892IghQylbkCoxjGdHvNrq0g"
MY_ID = 8389699824

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранилище заказов для истории (в памяти, сбрасывается при перезапуске бота)
user_orders = {}

# Секретная фраза
SECRET_PHRASE = "amatil секрет"

# Интересные факты о вейпинге
FACTS = [
    "🧪 Первый электронный испаритель был изобретён в 1965 году, но мир узнал о нём только в 2000-х.",
    "💨 Самое большое облако пара — более 2 метров в диаметре!",
    "🌍 В Японии вейпинг популярнее курения — там ценят чистоту и отсутствие запаха.",
    "🎨 Авторские жижи — это как крафтовое пиво: каждый вкус уникален.",
    "⚡ XROS 5 держит заряд до 2 дней активного парения.",
    "🧊 Мятные жижи — самые популярные в мире, и ANNIMA LOVE & ZOMBI это доказывает!",
    "🔬 Качественная жижа не оставляет нагара на испарителе.",
    "💎 Оригинальные девайсы служат в 3 раза дольше реплик."
]

# Мини-игра: подбор вкуса
MOOD_FLAVORS = {
    "🍓": "Фруктовый микс — сочный и яркий!",
    "🧊": "Мятный коктейль — свежесть и прохлада!",
    "🍰": "Десертный — сладкий и уютный!",
    "🌿": "Табачный — классика и благородство!"
}

async def handle(request):
    return web.Response(text="OK")

@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    kb = [
        [types.KeyboardButton(text="🛍 Каталог", web_app=types.WebAppInfo(url="https://darling-sable-0c139f.netlify.app"))],
        [types.KeyboardButton(text="💬 Отзывы"), types.KeyboardButton(text="📞 Поддержка")],
        [types.KeyboardButton(text="❓ FAQ"), types.KeyboardButton(text="🎁 Акции")],
        [types.KeyboardButton(text="📦 Доставка"), types.KeyboardButton(text="💳 Оплата")],
        [types.KeyboardButton(text="🎰 Подобрать вкус"), types.KeyboardButton(text="🧠 Факт дня")],
        [types.KeyboardButton(text="📋 История заказов")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        f"💨 {user_name}, добро пожаловать в AMATIL VAPE!\n\n"
        "🚀 Твой персональный проводник в мир авторских вкусов и премиальных девайсов.\n\n"
        "Выбери, что тебя интересует:",
        reply_markup=keyboard
    )

@dp.message()
async def handle_all(message: types.Message):
    user_id = message.from_user.id

    # --- Обработка заказа из Mini App ---
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order = data["order"]
        total = data["total"]
        user = message.from_user
        name = user.full_name
        if user.username:
            name += f" (@{user.username})"

        # Сохраняем заказ в историю
        if user_id not in user_orders:
            user_orders[user_id] = []
        user_orders[user_id].append({
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "items": order,
            "total": total
        })

        # Уведомление тебе
        text = f"🛒 Новый заказ!\n\n👤 {name}\n🆔 ID: {user.id}\n\n"
        for item in order:
            text += f"• {item['name']} x{item['qty']} — {item['price'] * item['qty']}₽\n"
        text += f"\n💰 Итого: {total}₽"
        await bot.send_message(MY_ID, text)
        await message.answer(
            "✅ Заказ принят!\n\n"
            "Скоро свяжусь с вами для уточнения деталей.\n\n"
            "📲 Мой контакт: @Fe3riko"
        )
        return

    # --- Кнопки меню ---
    if message.text == "💬 Отзывы":
        await message.answer(
            "💬 Отзывы наших клиентов\n\n"
            "Реальные люди, реальные эмоции:\n"
            "👉 https://t.me/amatilrev\n\n"
            "Хочешь оставить отзыв? Пиши @Fe3riko"
        )
    elif message.text == "📞 Поддержка":
        await message.answer(
            "📞 Связь со мной\n\n"
            "По любым вопросам — пиши:\n"
            "👉 @Fe3riko\n\n"
            "Отвечаю быстро, помогаю с выбором!"
        )
    elif message.text == "❓ FAQ":
        await message.answer(
            "❓ Частые вопросы\n\n"
            "📦 Доставка по РФ — 2-4 дня\n"
            "💳 Оплата — перевод/наличные\n"
            "🛡 Гарантия на устройства — 14 дней\n"
            "🧪 Жижи — только авторские, не Китай\n"
            "🔄 Обмен/возврат — в течение 7 дней"
        )
    elif message.text == "🎁 Акции":
        await message.answer(
            "🎁 Акции и предложения\n\n"
            "🔥 Заказ от 1500₽ — пробник в подарок\n"
            "👥 Приведи друга — скидка 10%\n"
            "🚚 Первый заказ — бесплатная доставка\n"
            "💎 Постоянным клиентам — особые условия"
        )
    elif message.text == "📦 Доставка":
        await message.answer(
            "📦 Доставка\n\n"
            "• Почта России / СДЭК / Boxberry\n"
            "• Отправка день в день\n"
            "• Трек-номер сразу после отправки\n"
            "• Среднее время — 2-4 дня\n\n"
            "По вопросам — @Fe3riko"
        )
    elif message.text == "💳 Оплата":
        await message.answer(
            "💳 Оплата\n\n"
            "• Перевод на карту\n"
            "• Наличные при встрече (Москва)\n"
            "• Безопасная сделка через Telegram\n\n"
            "Подробности — @Fe3riko"
        )

    # --- 🆕 Фишки ---
    elif message.text == "🧠 Факт дня":
        fact = random.choice(FACTS)
        await message.answer(f"🧠 Факт дня\n\n{fact}")

    elif message.text == "🎰 Подобрать вкус":
        emoji = random.choice(list(MOOD_FLAVORS.keys()))
        flavor = MOOD_FLAVORS[emoji]
        await message.answer(
            f"🎰 Твой вкус сегодня — {emoji}\n\n"
            f"{flavor}\n\n"
            "🛍 Жми «Каталог», чтобы найти свою идеальную жижу!"
        )

    elif message.text == "📋 История заказов":
        if user_id in user_orders and user_orders[user_id]:
            text = "📋 Твои заказы:\n\n"
            for i, order in enumerate(user_orders[user_id][-5:], 1):
                items_text = ", ".join([f"{item['name']} x{item['qty']}" for item in order['items']])
                text += f"{i}. {order['date']}\n{items_text}\n💰 {order['total']}₽\n\n"
            text += "Хочешь повторить заказ? Жми «Каталог»!"
        else:
            text = "📋 У тебя пока нет заказов.\n\n🛍 Жми «Каталог», чтобы сделать первый!"
        await message.answer(text)

    # --- Пасхалка ---
    elif SECRET_PHRASE in message.text.lower():
        await message.answer(
            "🔮 Ты нашёл секретную пасхалку AMATIL VAPE!\n\n"
            "Ты — особенный клиент, и я это ценю. Держи промокод на скидку 5%: SECRET5\n"
            "Покажи это сообщение при заказе @Fe3riko"
        )

    else:
        await message.answer("Используй кнопки меню для навигации 👇")

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