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

SECRET_PHRASES = ["amatil лучший", "миша amatil"]

PRIZES = [
    {"prize": "Скидка 5%", "code": "WHEEL5"}, {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 5%", "code": "WHEEL5"}, {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 5%", "code": "WHEEL5"}, {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 5%", "code": "WHEEL5"}, {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 5%", "code": "WHEEL5"}, {"prize": "Скидка 5%", "code": "WHEEL5"},
    {"prize": "Скидка 10%", "code": "WHEEL10"}, {"prize": "Скидка 10%", "code": "WHEEL10"},
    {"prize": "Скидка 10%", "code": "WHEEL10"}, {"prize": "Скидка 10%", "code": "WHEEL10"},
    {"prize": "Скидка 10%", "code": "WHEEL10"}, {"prize": "Скидка 10%", "code": "WHEEL10"},
    {"prize": "Скидка 10%", "code": "WHEEL10"}, {"prize": "Скидка 15%", "code": "WHEEL15"},
    {"prize": "Скидка 15%", "code": "WHEEL15"}, {"prize": "Скидка 15%", "code": "WHEEL15"},
    {"prize": "Скидка 15%", "code": "WHEEL15"}, {"prize": "Скидка 15%", "code": "WHEEL15"},
    {"prize": "Скидка 20%", "code": "WHEEL20"}, {"prize": "Скидка 20%", "code": "WHEEL20"},
    {"prize": "Скидка 20%", "code": "WHEEL20"}, {"prize": "Скидка 25%", "code": "WHEEL25"},
    {"prize": "Скидка 25%", "code": "WHEEL25"}, {"prize": "Скидка 30%", "code": "WHEEL30"},
    {"prize": "Бесплатная доставка", "code": "FREEDEL"},
    {"prize": "Дополнительная жижа на выбор", "code": "FREEJUICE"},
    {"prize": "Картридж в подарок", "code": "FREECART"},
    {"prize": "Удвоение заказа", "code": "DOUBLE"},
    {"prize": "Ранний доступ к новинкам", "code": "EARLY"},
    {"prize": "Пожизненная скидка 5%", "code": "LIFETIME5"},
    {"prize": "VIP-статус (скидка 10% навсегда)", "code": "VIP"},
    {"prize": "🔥 ДЖЕКПОТ: Бесплатный XROS! 🔥", "code": "FREEXROS"}
]

FLAVORS = {
    "вишня": "Скидка 10% — WHEEL10", "мята": "Скидка 15% — WHEEL15",
    "ананас": "Скидка 5% — WHEEL5", "грейпфрут": "Бесплатная доставка — FREEDEL",
    "банан": "Скидка 20% — WHEEL20", "яблоко": "Скидка 10% — WHEEL10",
    "персик": "Скидка 5% — WHEEL5", "гранат": "Скидка 15% — WHEEL15"
}

current_stock = {
    "rickmorty": 1, "monk": 1, "monk2": 1, "samoubiyca_v2": 2,
    "monstervapor": 2, "annima_apple": 0, "h45_green": 1,
    "pasito2": 1, "pasito3": 1, "hamster1": 0
}

pending_orders = {}
user_wheel_used = {}
user_game_state = {}
subscribers = set()
referrals = {}
total_revenue = 0

async def handle(request):
    return web.Response(text="OK")

async def reset_wheel():
    while True:
        await asyncio.sleep(86400)
        user_wheel_used.clear()

@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    kb = [
        [types.KeyboardButton(text="🛍 Каталог", web_app=types.WebAppInfo(url="https://darling-sable-0c139f.netlify.app"))],
        [types.KeyboardButton(text="💬 Отзывы"), types.KeyboardButton(text="📞 Поддержка")],
        [types.KeyboardButton(text="❓ FAQ"), types.KeyboardButton(text="🎁 Акции")],
        [types.KeyboardButton(text="🚗 Доставка"), types.KeyboardButton(text="💳 Оплата")],
        [types.KeyboardButton(text="🎰 Крутить скидку"), types.KeyboardButton(text="🧠 Факт дня")],
        [types.KeyboardButton(text="🎮 Угадай вкус"), types.KeyboardButton(text="🔔 Новинки")],
        [types.KeyboardButton(text="👥 Реферал"), types.KeyboardButton(text="📋 История заказов")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        f"Добро пожаловать в AMATIL VAPE, {user_name}!\n\n"
        "Мы предлагаем оригинальные устройства, авторские жидкости и никотиновые паучи.\n"
        "Ознакомьтесь с возможностями ниже и наслаждайтесь качеством.",
        reply_markup=keyboard
    )

@dp.message()
async def handle_all(message: types.Message):
    global current_stock, pending_orders, total_revenue
    user_id = message.from_user.id

    # Подтверждение заказа
    if message.text and message.text.startswith("/confirm"):
        parts = message.text.split(" ")
        if len(parts) > 1:
            order_id = parts[1]
            if order_id in pending_orders:
                order = pending_orders[order_id]
                total_revenue += order["total"]
                for item in order["items"]:
                    item_id = item.get("id", item["name"].lower().replace(" ", "_"))
                    if item_id in current_stock and current_stock[item_id] >= item["qty"]:
                        current_stock[item_id] -= item["qty"]
                buyer_info = order.get("user", "Покупатель")
                buyer_link = order.get("userLink", "")
                await bot.send_message(MY_ID, f"✅ Заказ {order_id} подтверждён!\n\n👤 {buyer_info}\n🔗 {buyer_link}")
                del pending_orders[order_id]
                await message.answer(f"✅ Заказ {order_id} успешно подтверждён. Свяжитесь с покупателем для уточнения деталей.")
            else:
                await message.answer("❌ К сожалению, заказ с таким ID не найден. Проверьте правильность ID и попробуйте снова.")
        else:
            await message.answer("❌ Пожалуйста, укажите ID заказа после команды. Например: /confirm abc123")
        return

    # Выручка
    if message.text and message.text.startswith("/profit"):
        await message.answer(f"💰 Общая выручка: {total_revenue} ₽\n\nСпасибо, что развиваете AMATIL VAPE вместе с нами!")
        return

    # Реферал
    if message.text and message.text.startswith("/ref"):
        code = str(user_id)[:6]
        referrals[code] = user_id
        await message.answer(
            f"👥 Ваша персональная реферальная ссылка:\n\n"
            f"https://t.me/amatil_bot?start={code}\n\n"
            f"Отправьте её другу, и когда он сделает первый заказ — вы оба получите скидку 10%!"
        )
        return

    # Заказ из Mini App
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
        text = f"🛒 Новый заказ\n\n👤 {name}\n🆔 ID: {user.id}\n📦 ID заказа: {order_id}\n\n"
        for item in order:
            text += f"• {item['name']} × {item['qty']} — {item['price'] * item['qty']} ₽\n"
        text += f"\n💰 Итого: {total} ₽\n\n⚡ Для подтверждения отправьте: /confirm {order_id}"
        await bot.send_message(MY_ID, text)
        await message.answer(
            "✅ Ваш заказ успешно принят и ожидает подтверждения менеджера.\n\n"
            "В ближайшее время с вами свяжутся для уточнения деталей.\n\n"
            "📲 Контакт для связи: @Fe3riko"
        )
        return

    # Мини-игра "Угадай вкус"
    if message.text == "🎮 Угадай вкус":
        flavor = random.choice(list(FLAVORS.keys()))
        user_game_state[user_id] = flavor
        await message.answer(
            "🎮 Добро пожаловать в мини-игру «Угадай вкус»!\n\n"
            "Я загадал один из вкусов нашей линейки. Это фрукт или ягода.\n"
            "Напишите свой вариант в чат, и если угадаете — получите приз!\n\n"
            "Доступные подсказки: вишня, мята, ананас, грейпфрут, банан, яблоко, персик, гранат."
        )
        return

    # Проверка ответа в игре
    if user_id in user_game_state:
        if message.text and message.text.lower() == user_game_state[user_id]:
            prize = FLAVORS[user_game_state[user_id]]
            await message.answer(
                f"🎉 Поздравляем! Вы угадали!\n\n"
                f"Загаданный вкус: {user_game_state[user_id]}\n"
                f"Ваш приз: {prize}\n\n"
                f"Предъявите этот промокод при заказе: @Fe3riko"
            )
        else:
            await message.answer(
                "❌ К сожалению, вы не угадали. Попробуйте ещё раз!\n\n"
                "Напишите другой вариант вкуса."
            )
        return

    # Кнопки меню
    if message.text == "💬 Отзывы":
        await message.answer(
            "💬 Отзывы наших клиентов\n\n"
            "Ознакомьтесь с реальными впечатлениями покупателей о продукции и обслуживании:\n"
            "👉 https://t.me/amatilrev\n\n"
            "Будем рады вашему отзыву — напишите @Fe3riko"
        )
    elif message.text == "📞 Поддержка":
        await message.answer(
            "📞 Служба поддержки AMATIL VAPE\n\n"
            "По всем вопросам, включая подбор устройств и жидкостей, обращайтесь:\n"
            "👉 @Fe3riko\n\n"
            "Мы отвечаем оперативно и предоставляем профессиональную консультацию."
        )
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
            "🎁 Действующие акции и специальные предложения\n\n"
            "👥 Пригласите друга — получите оба скидку 25% на следующий заказ.\n"
            "🎁 При заказе от 2000 ₽ — случайный подарок.\n"
            "🎰 Ежедневное колесо фортуны — гарантированный приз.\n"
            "🎮 Угадайте вкус дня — получите дополнительную скидку.\n\n"
            "Подробности уточняйте в поддержке: @Fe3riko"
        )
    elif message.text == "🚗 Доставка":
        await message.answer(
            "🚗 Условия доставки\n\n"
            "Мы осуществляем доставку исключительно по городу.\n\n"
            "📍 Ближняя зона (до 1,5 км от склада):\n"
            "• Бесплатно при заказе от 1000 ₽\n"
            "• При заказе менее 1000 ₽ — 50 ₽\n\n"
            "📍 Дальняя зона (более 1,5 км):\n"
            "• Стоимость рассчитывается индивидуально — от 100 ₽\n"
            "• Чем дальше адрес, тем выше стоимость доставки\n\n"
            "🕒 Доставка день в день при оформлении до 18:00.\n"
            "🤝 Возможен самовывоз — адрес уточняйте у менеджера.\n\n"
            "Все детали и точную стоимость доставки обговаривайте с менеджером:\n"
            "👉 @Fe3riko"
        )
    elif message.text == "💳 Оплата":
        await message.answer(
            "💳 Способы оплаты\n\n"
            "• Банковский перевод на карту.\n"
            "• Наличный расчёт при личной встрече.\n"
            "• Безопасная сделка через Telegram.\n\n"
            "Реквизиты и детали — @Fe3riko"
        )
    elif message.text == "🧠 Факт дня":
        facts = [
            "Первый прототип электронной сигареты был запатентован в 1965 году — задолго до массового распространения.",
            "Качественная жидкость не содержит диацетила и других вредных примесей, в отличие от массового ширпотреба.",
            "Мятные вкусы остаются самыми популярными в мире благодаря своей универсальности."
        ]
        await message.answer(f"🧠 Факт дня\n\n{random.choice(facts)}")
    elif message.text == "🎰 Крутить скидку":
        if user_id in user_wheel_used:
            await message.answer("🎰 Вы уже испытывали удачу сегодня. Возвращайтесь завтра за новым призом!")
        else:
            prize = random.choice(PRIZES)
            user_wheel_used[user_id] = True
            await message.answer(
                f"🎰 Колесо фортуны\n\n"
                f"Вам выпал приз: {prize['prize']}!\n"
                f"Промокод: {prize['code']}\n\n"
                f"Предъявите его при заказе: @Fe3riko"
            )
    elif message.text == "🔔 Новинки":
        subscribers.add(user_id)
        await message.answer("🔔 Вы успешно подписались на уведомления о новинках! Мы сообщим вам, как только появится что-то новое.")
    elif message.text == "👥 Реферал":
        code = str(user_id)[:6]
        referrals[code] = user_id
        await message.answer(
            f"👥 Ваша персональная реферальная ссылка:\n\n"
            f"https://t.me/amatil_bot?start={code}\n\n"
            f"Отправьте её другу, и когда он сделает первый заказ — вы оба получите скидку 10%!"
        )
    elif message.text == "📋 История заказов":
        await message.answer("📋 История ваших заказов находится в разработке. Скоро она появится!")
    elif any(phrase in message.text.lower() for phrase in SECRET_PHRASES):
        prize = random.choice(PRIZES)
        await message.answer(
            f"🔮 Вы обнаружили секретную пасхалку AMATIL VAPE!\n\n"
            f"Вам выпал приз: {prize['prize']}\n"
            f"Промокод: {prize['code']}\n\n"
            f"Предъявите его при общении с @Fe3riko"
        )
    else:
        await message.answer("Пожалуйста, воспользуйтесь кнопками меню для навигации.")

async def main():
    asyncio.create_task(reset_wheel())
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