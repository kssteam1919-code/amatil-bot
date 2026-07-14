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
    {"prize": "ДЖЕКПОТ: Бесплатный XROS!", "code": "FREEXROS"}
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

def get_main_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Каталог", web_app=types.WebAppInfo(url="https://darling-sable-0c139f.netlify.app"))],
            [types.KeyboardButton(text="Отзывы"), types.KeyboardButton(text="Поддержка")],
            [types.KeyboardButton(text="FAQ"), types.KeyboardButton(text="Акции")],
            [types.KeyboardButton(text="Доставка"), types.KeyboardButton(text="Оплата")],
            [types.KeyboardButton(text="Крутить скидку"), types.KeyboardButton(text="Факт дня")],
            [types.KeyboardButton(text="Угадай вкус"), types.KeyboardButton(text="Новинки")],
            [types.KeyboardButton(text="Реферал"), types.KeyboardButton(text="История заказов")]
        ],
        resize_keyboard=True
    )

async def handle(request):
    return web.Response(text="OK")

async def reset_wheel():
    while True:
        await asyncio.sleep(86400)
        user_wheel_used.clear()

@dp.message(CommandStart())
async def start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(
        f"Добро пожаловать в AMATIL VAPE, {user_name}!\n\n"
        "Мы предлагаем оригинальные устройства, авторские жидкости и никотиновые паучи.\n"
        "Ознакомьтесь с возможностями ниже.",
        reply_markup=get_main_keyboard()
    )

@dp.message()
async def handle_all(message: types.Message):
    global current_stock, pending_orders, total_revenue
    user_id = message.from_user.id
    text = message.text or ""

    # Выход из игры
    if user_id in user_game_state and text == "Выйти из игры":
        del user_game_state[user_id]
        await message.answer("Вы вышли из игры.", reply_markup=get_main_keyboard())
        return

    # Игра
    if user_id in user_game_state:
        if text.lower() == user_game_state[user_id]:
            prize = FLAVORS[user_game_state[user_id]]
            del user_game_state[user_id]
            await message.answer(
                f"Поздравляем! Вы угадали!\n\n"
                f"Загаданный вкус: {text.lower()}\n"
                f"Ваш приз: {prize}\n\n"
                f"Предъявите промокод при заказе: @Fe3riko",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer("Не угадали. Попробуйте ещё раз или нажмите «Выйти из игры».")
        return

    # Подтверждение заказа
    if text.startswith("/confirm"):
        parts = text.split(" ")
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
                await bot.send_message(MY_ID, f"Заказ {order_id} подтверждён!\n\n{buyer_info}\n{buyer_link}")
                del pending_orders[order_id]
                await message.answer(f"Заказ {order_id} подтверждён.")
            else:
                await message.answer("Заказ с таким ID не найден.")
        else:
            await message.answer("Укажите ID: /confirm [id]")
        return

    if text.startswith("/profit"):
        await message.answer(f"Общая выручка: {total_revenue} руб.")
        return

    if text.startswith("/ref"):
        code = str(user_id)[:6]
        referrals[code] = user_id
        await message.answer(f"Ваша реферальная ссылка:\nhttps://t.me/amatil_bot?start={code}\n\nЗа друга — скидка 10% обоим!")
        return

    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order = data["order"]
        total = data["total"]
        user = message.from_user
        name = user.full_name
        user_link = f"tg://user?id={user.id}"
        if user.username: name += f" (@{user.username})"
        name += f"\n{user_link}"
        order_id = datetime.now().strftime("%y%m%d%H%M%S") + str(random.randint(100, 999))
        pending_orders[order_id] = {"items": order, "total": total, "user": name, "userId": user.id, "userLink": user_link}
        text_msg = f"Новый заказ\n\n{name}\nID: {user.id}\nЗаказ: {order_id}\n\n"
        for item in order:
            text_msg += f"{item['name']} x{item['qty']} — {item['price'] * item['qty']} руб.\n"
        text_msg += f"\nИтого: {total} руб.\n\n/confirm {order_id}"
        await bot.send_message(MY_ID, text_msg)
        await message.answer("Заказ принят! Ожидайте подтверждения.\n@Fe3riko")
        return

    if text == "Угадай вкус":
        flavor = random.choice(list(FLAVORS.keys()))
        user_game_state[user_id] = flavor
        kb = [[types.KeyboardButton(text="Выйти из игры")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Я загадал вкус (фрукт или ягода).\n"
            "Напишите свой вариант.\n\n"
            "Подсказки: вишня, мята, ананас, грейпфрут, банан, яблоко, персик, гранат.\n\n"
            "Для выхода нажмите «Выйти из игры».",
            reply_markup=keyboard
        )
        return

    # КНОПКИ
    if text == "Отзывы":
        await message.answer(
            "Сомневаетесь в выборе?\n\n"
            "Не верьте нам на слово — послушайте тех, кто уже сделал заказ. "
            "В нашей группе отзывов собраны реальные мнения реальных парильщиков.\n\n"
            "Переходите по ссылке, листайте и убедитесь сами. "
            "Если у вас есть что добавить — будем только рады! — @Fe3riko"
        )
    elif text == "Поддержка":
        await message.answer(
            "Поддержка 24/7 (в разумных пределах)\n\n"
            "Напишите нам по любой теме: заказ, доставка, гарантия, подбор вкуса — поможем чем можем.\n\n"
            "Обычно отвечаем за 5–10 минут. Если задерживаемся — значит, разбираем сложный кейс, но ответим обязательно!\n\n"
            "Жмите на кнопку и задавайте свой вопрос: @Fe3riko"
        )
    elif text == "FAQ":
        await message.answer(
            "Часто задаваемые вопросы\n\n"
            "Доставка — по городу, возможен самовывоз.\n"
            "Оплата — банковский перевод или наличные при встрече.\n"
            "Работаем 24/7.\n\n"
            "Дополнительные вопросы: @Fe3riko"
        )
    elif text == "Акции":
        await message.answer(
            "Действующие акции\n\n"
            "Пригласите друга — получите оба скидку 10%.\n"
            "При заказе от 2000 руб. — случайный подарок.\n"
            "Ежедневное колесо фортуны — гарантированный приз.\n\n"
            "Подробности: @Fe3riko"
        )
    elif text == "Доставка":
        await message.answer(
            "Доставка\n\n"
            "Ближняя зона (до 1.5 км) — от 50 руб.\n"
            "Дальняя зона (более 1.5 км) — от 100 руб.\n"
            "Самовывоз — адрес уточняйте у менеджера.\n"
            "Доставка 24/7.\n\n"
            "Точную стоимость и время согласовывайте: @Fe3riko"
        )
    elif text == "Оплата":
        await message.answer(
            "Способы оплаты\n\n"
            "Банковский перевод\n"
            "Наличные при встрече\n\n"
            "Реквизиты и детали: @Fe3riko"
        )
    elif text == "Факт дня":
        facts = [
            "Первый прототип электронной сигареты был запатентован в 1965 году.",
            "Качественная жидкость не содержит диацетила и других вредных примесей.",
            "Мятные вкусы остаются самыми популярными в мире благодаря своей универсальности."
        ]
        await message.answer(f"Факт дня\n\n{random.choice(facts)}")
    elif text == "Крутить скидку":
        if user_id in user_wheel_used:
            await message.answer("Вы уже крутили сегодня. Завтра — снова!")
        else:
            prize = random.choice(PRIZES)
            user_wheel_used[user_id] = True
            await message.answer(
                f"Колесо фортуны\n\n"
                f"Вам выпал приз: {prize['prize']}!\n"
                f"Промокод: {prize['code']}\n\n"
                f"Предъявите при заказе: @Fe3riko"
            )
    elif text == "Новинки":
        subscribers.add(user_id)
        await message.answer("Вы подписались на уведомления о новинках!")
    elif text == "Реферал":
        code = str(user_id)[:6]
        referrals[code] = user_id
        await message.answer(
            f"Ваша реферальная ссылка:\n\n"
            f"https://t.me/amatil_bot?start={code}\n\n"
            f"Отправьте другу — и получите скидку 10% на следующий заказ!"
        )
    elif text == "История заказов":
        await message.answer("История ваших заказов появится здесь в ближайшее время.")
    elif any(phrase in text.lower() for phrase in SECRET_PHRASES):
        prize = random.choice(PRIZES)
        await message.answer(
            f"Секретная скидка AMATIL VAPE!\n\n"
            f"Приз: {prize['prize']}\n"
            f"Промокод: {prize['code']}\n\n"
            f"Предъявите при общении: @Fe3riko"
        )
    else:
        await message.answer("Используйте кнопки меню для навигации.")

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