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

user_orders = {}
SECRET_PHRASES = ["amatil лучший", "миша amatil"]

PRIZES = [
    {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 10%", "code": "WHEEL10"},
    {"prize": "Скидка 10%", "code": "WHEEL10"},
    {"prize": "Скидка 10%", "code": "WHEEL10"},
    {"prize": "Скидка 15%", "code": "WHEEL15"},
    {"prize": "Скидка 15%", "code": "WHEEL15"},
    {"prize": "Скидка 20%", "code": "WHEEL20"},
    {"prize": "Скидка 20%", "code": "WHEEL20"},
    {"prize": "Скидка 25%", "code": "WHEEL25"},
    {"prize": "Скидка 30%", "code": "WHEEL30"},
    {"prize": "Бесплатная доставка", "code": "FREEDEL"},
    {"prize": "Бесплатная доставка", "code": "FREEDEL"},
    {"prize": "Бесплатная доставка", "code": "FREEDEL"},
    {"prize": "Дополнительная жижа на выбор", "code": "FREEJUICE"},
    {"prize": "Дополнительная жижа на выбор", "code": "FREEJUICE"},
    {"prize": "Картридж в подарок", "code": "FREECART"},
    {"prize": "Картридж в подарок", "code": "FREECART"},
    {"prize": "Удвоение заказа", "code": "DOUBLE"},
    {"prize": "Удвоение заказа", "code": "DOUBLE"},
    {"prize": "Ранний доступ к новинкам", "code": "EARLY"},
    {"prize": "Ранний доступ к новинкам", "code": "EARLY"},
    {"prize": "Пожизненная скидка 5%", "code": "LIFETIME5"},
    {"prize": "VIP-статус (скидка 10% навсегда)", "code": "VIP"},
    {"prize": "VIP-статус (скидка 10% навсегда)", "code": "VIP"},
    {"prize": "🔥 ДЖЕКПОТ: Бесплатный XROS! 🔥", "code": "FREEXROS"}
]

current_stock = {
    "rickmorty": 1, "monk": 1, "monk2": 1, "samoubiyca_v2": 2,
    "monstervapor": 2, "annima_apple": 1,
    "h45_green": 1, "pasito2": 1, "pasito3": 1, "hamster1": 1
}

pending_orders = {}
user_wheel_used = {}

async def handle(request):
    return web.Response(text="OK")

@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    kb = [
        [types.KeyboardButton(text="🛍 Каталог", web_app=types.WebAppInfo(url="https://darling-sable-0c139f.netlify.app"))],
        [types.KeyboardButton(text="💬 Отзывы"), types.KeyboardButton(text="📞 Поддержка")],
        [types.KeyboardButton(text="❓ FAQ"), types.KeyboardButton(text="🎁 Акции")],
        [types.KeyboardButton(text="🚗 Доставка"), types.KeyboardButton(text="💳 Оплата")],
        [types.KeyboardButton(text="🎰 Крутить скидку"), types.KeyboardButton(text="🧠 Факт дня")],
        [types.KeyboardButton(text="📋 История заказов")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Добро пожаловать в AMATIL VAPE, {user_name}!\n\nВыберите действие:", reply_markup=keyboard)

@dp.message()
async def handle_all(message: types.Message):
    global current_stock, pending_orders
    user_id = message.from_user.id

    # Подтверждение заказа
    if message.text and message.text.startswith("/confirm"):
        parts = message.text.split(" ")
        if len(parts) > 1:
            order_id = parts[1]
            if order_id in pending_orders:
                order = pending_orders[order_id]
                for item in order["items"]:
                    item_id = item.get("id", item["name"].lower().replace(" ", "_"))
                    if item_id in current_stock and current_stock[item_id] >= item["qty"]:
                        current_stock[item_id] -= item["qty"]
                buyer_info = order.get("user", "Покупатель")
                buyer_link = order.get("userLink", "")
                await bot.send_message(MY_ID, f"✅ Заказ {order_id} подтверждён!\n\n👤 {buyer_info}\n🔗 {buyer_link}")
                del pending_orders[order_id]
                await message.answer(f"✅ Заказ {order_id} подтверждён!")
            else:
                ids = list(pending_orders.keys())
                await message.answer(f"❌ Заказ {order_id} не найден.\nАктивные: {ids}")
        else:
            await message.answer("❌ Укажите ID: /confirm [id]")
        return

    # Новый заказ
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order = data["order"]
        total = data["total"]
        user = message.from_user
        name = user.full_name
        user_link = f"tg://user?id={user.id}"
        if user.username:
            name += f" (@{user.username})"
        name += f"\n🔗 {user_link}"

        order_id = datetime.now().strftime("%y%m%d%H%M%S") + str(random.randint(100, 999))
        pending_orders[order_id] = {"items": order, "total": total, "user": name, "userId": user.id, "userLink": user_link}

        text = f"🛒 Новый заказ\n\n👤 {name}\n🆔 ID: {user.id}\n📦 ID: {order_id}\n\n"
        for item in order:
            text += f"• {item['name']} × {item['qty']} — {item['price'] * item['qty']} ₽\n"
        text += f"\n💰 Итого: {total} ₽\n\n⚡ /confirm {order_id}"
        await bot.send_message(MY_ID, text)
        await message.answer("✅ Заказ принят! Ожидайте подтверждения.\n📲 @Fe3riko")
        return

    # Кнопки
    if message.text == "💬 Отзывы":
        await message.answer("💬 https://t.me/amatilrev")
    elif message.text == "📞 Поддержка":
        await message.answer("📞 @Fe3riko")
    elif message.text == "❓ FAQ":
        await message.answer("🚗 Доставка по городу\n💳 Оплата перевод/наличные\n🕒 24/7")
    elif message.text == "🎁 Акции":
        await message.answer("👥 Приведи друга — скидка 25%\n🎁 Заказ от 2000₽ — подарок\n🎰 Крути колесо!")
    elif message.text == "🚗 Доставка":
        await message.answer("🚗 До 1.5 км — от 50₽\n📍 Более 1.5 км — от 100₽\n🤝 Самовывоз\n🕒 24/7")
    elif message.text == "💳 Оплата":
        await message.answer("💳 Перевод на карту / наличные")
    elif message.text == "🧠 Факт дня":
        facts = ["Первый вейп — 1965 год.", "Мятные вкусы — самые популярные.", "Качественная жижа не содержит диацетил."]
        await message.answer(f"🧠 {random.choice(facts)}")
    elif message.text == "🎰 Крутить скидку":
        if user_id in user_wheel_used:
            await message.answer("🎰 Вы уже крутили сегодня!")
        else:
            prize = random.choice(PRIZES)
            user_wheel_used[user_id] = True
            await message.answer(f"🎰 Приз: {prize['prize']}\nПромокод: {prize['code']}\nПредъявите @Fe3riko")
    elif message.text == "📋 История заказов":
        await message.answer("📋 История пока в разработке")
    elif any(phrase in message.text.lower() for phrase in SECRET_PHRASES):
        prize = random.choice(PRIZES)
        await message.answer(f"🔮 Секретная скидка!\nПриз: {prize['prize']}\nПромокод: {prize['code']}")
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