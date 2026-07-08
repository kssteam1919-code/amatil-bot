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
STOCK_FILE = "stock.json"
PENDING_FILE = "pending.json"

PRIZES = [
    {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 10%", "code": "WHEEL10"},
    {"prize": "Скидка 15%", "code": "WHEEL15"},
    {"prize": "Скидка 20%", "code": "WHEEL20"},
    {"prize": "Бесплатная доставка", "code": "FREEDEL"},
    {"prize": "Пробник в подарок", "code": "SAMPLE"}
]

DEFAULT_STOCK = {
    "rickmorty": 1, "monk": 1, "monk2": 1, "samoubiyca_v2": 2,
    "monstervapor": 2, "annima_apple": 1,
    "h45_green": 1, "pasito2": 1, "pasito3": 1, "hamster1": 1
}

user_wheel_used = {}

def load_json(filename, default):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return default.copy()

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f)

current_stock = load_json(STOCK_FILE, DEFAULT_STOCK)
pending_orders = load_json(PENDING_FILE, {})

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
    await message.answer(
        f"Добро пожаловать в AMATIL VAPE, {user_name}!\n\n"
        "Мы предлагаем оригинальные устройства, авторские жидкости и никотиновые паучи.\n"
        "Ознакомьтесь с категориями ниже и наслаждайтесь качеством.",
        reply_markup=keyboard
    )

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
                save_json(STOCK_FILE, current_stock)
                buyer_info = order.get("user", "Покупатель")
                buyer_link = order.get("userLink", "")
                await bot.send_message(MY_ID, f"✅ Заказ {order_id} подтверждён.\n\n👤 {buyer_info}\n🔗 {buyer_link}")
                del pending_orders[order_id]
                save_json(PENDING_FILE, pending_orders)
                await message.answer(f"✅ Заказ {order_id} подтверждён. Свяжитесь с покупателем.")
            else:
                await message.answer("❌ Заказ с таким ID не найден.")
        else:
            await message.answer("❌ Пожалуйста, укажите ID заказа: /confirm [id]")
        return

    # Обработка заказа из Mini App
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order = data["order"]
        total = data["total"]
        user = message.from_user
        name = user.full_name
        user_link = f"tg://user?id={user.id}"
        if user.username:
            name += f" (@{user.username})"
        else:
            name += f"\n🔗 {user_link}"

        order_id = datetime.now().strftime("%y%m%d%H%M%S") + str(random.randint(100, 999))
        pending_orders[order_id] = {"items": order, "total": total, "user": name, "userId": user.id, "userLink": user_link}
        save_json(PENDING_FILE, pending_orders)

        text = f"🛒 Новый заказ\n\n👤 {name}\n🆔 ID: {user.id}\n📦 ID заказа: {order_id}\n\n"
        for item in order:
            text += f"• {item['name']} × {item['qty']} — {item['price'] * item['qty']} ₽\n"
        text += f"\n💰 Итого: {total} ₽\n\n⚡ Для подтверждения: /confirm {order_id}"
        await bot.send_message(MY_ID, text)
        await message.answer("✅ Ваш заказ принят и ожидает подтверждения менеджера.\n\n📲 Для связи: @Fe3riko")
        return

    # Кнопки меню
    if message.text == "💬 Отзывы":
        await message.answer("💬 Ознакомьтесь с отзывами наших клиентов:\n👉 https://t.me/amatilrev\n\nБудем рады вашему отзыву — напишите @Fe3riko")
    elif message.text == "📞 Поддержка":
        await message.answer("📞 Служба поддержки AMATIL VAPE\n\nПо всем вопросам обращайтесь:\n👉 @Fe3riko\n\nМы оперативно поможем с выбором и оформлением.")
    elif message.text == "❓ FAQ":
        await message.answer(
            "❓ Часто задаваемые вопросы\n\n"
            "🚗 Доставка — по городу, возможен самовывоз.\n"
            "💳 Оплата — банковский перевод или наличные при встрече.\n"
            "🕒 Работаем 24/7.\n\n"
            "Дополнительные вопросы: @Fe3riko"
        )
    elif message.text == "🎁 Акции":
        await message.answer(
            "🎁 Действующие акции\n\n"
            "👥 Пригласите друга — получите оба скидку 25%.\n"
            "🎁 При заказе от 2000 ₽ — случайный подарок.\n"
            "🎰 Ежедневное колесо фортуны — гарантированный приз.\n\n"
            "Подробности: @Fe3riko"
        )
    elif message.text == "🚗 Доставка":
        await message.answer(
            "🚗 Доставка\n\n"
            "📍 Ближняя зона (до 1.5 км) — от 50 ₽\n"
            "📍 Дальняя зона (более 1.5 км) — от 100 ₽\n"
            "🤝 Самовывоз — адрес уточняйте у менеджера.\n"
            "🕒 Доставка 24/7.\n\n"
            "Точную стоимость и время согласовывайте: @Fe3riko"
        )
    elif message.text == "💳 Оплата":
        await message.answer("💳 Способы оплаты\n\n• Банковский перевод\n• Наличные при встрече\n\nРеквизиты и детали: @Fe3riko")
    elif message.text == "🧠 Факт дня":
        facts = [
            "Первый прототип электронной сигареты был запатентован в 1965 году.",
            "Качественная жидкость не содержит диацетила и других вредных примесей.",
            "Мятные вкусы остаются самыми популярными в мире благодаря своей универсальности."
        ]
        await message.answer(f"🧠 Факт дня\n\n{random.choice(facts)}")
    elif message.text == "🎰 Крутить скидку":
        if user_id in user_wheel_used:
            await message.answer("🎰 Вы уже испытывали удачу сегодня. Возвращайтесь завтра за новым призом!")
        else:
            prize = random.choice(PRIZES)
            user_wheel_used[user_id] = True
            await message.answer(f"🎰 Колесо фортуны\n\nВам выпал приз: {prize['prize']}!\nПромокод: {prize['code']}\n\nПредъявите его при заказе: @Fe3riko")
    elif message.text == "📋 История заказов":
        if user_id in user_orders:
            await message.answer("📋 Ваши заказы:\n\n" + "\n".join(user_orders[user_id][-5:]))
        else:
            await message.answer("📋 У вас пока нет завершённых заказов.")
    elif any(phrase in message.text.lower() for phrase in SECRET_PHRASES):
        prize = random.choice(PRIZES)
        await message.answer(f"🔮 Секретная скидка AMATIL VAPE!\n\nПриз: {prize['prize']}\nПромокод: {prize['code']}\n\nПредъявите при общении: @Fe3riko")
    else:
        await message.answer("Пожалуйста, воспользуйтесь кнопками меню для навигации.")

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