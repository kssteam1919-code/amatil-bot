```python
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
SECRET_PHRASE = "amatil секрет"

AVAILABLE_PRODUCTS = [
    {"name": "ANNIMA LOVE & ZOMBI", "price": 289, "taste": "Мятный коктейль с ледяным послевкусием"},
    {"name": "XROS 5", "price": 1089, "taste": "Компактный под-мод с регулируемым обдувом"},
    {"name": "Манго-маракуйя", "price": 350, "taste": "Тропический микс с кислинкой"},
    {"name": "Черничный взрыв", "price": 320, "taste": "Насыщенная черника с прохладой"},
    {"name": "Карамельный латте", "price": 299, "taste": "Сладкий кофейно-карамельный десерт"}
]

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
        [types.KeyboardButton(text="🎰 Подобрать вкус"), types.KeyboardButton(text="🧠 Факт дня")],
        [types.KeyboardButton(text="📋 История заказов")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        f"Добро пожаловать в AMATIL VAPE, {user_name}!\n\n"
        "Мы предлагаем оригинальные устройства и авторские жидкости по вашему городу.\n"
        "Быстро, качественно и с заботой о каждом клиенте.\n\n"
        "Ознакомьтесь с возможностями ниже:",
        reply_markup=keyboard
    )

@dp.message()
async def handle_all(message: types.Message):
    user_id = message.from_user.id

    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order = data["order"]
        total = data["total"]
        user = message.from_user
        name = user.full_name
        user_link = f"tg://user?id={user.id}"

        if user.username:
            client_info = f"{name} (@{user.username})"
        else:
            client_info = f"{name}\n🔗 Написать: {user_link}"

        if user_id not in user_orders:
            user_orders[user_id] = []
        user_orders[user_id].append({
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "items": order,
            "total": total
        })

        text = f"🛒 Новый заказ\n\n👤 Клиент: {client_info}\n🆔 ID: {user.id}\n\n"
        for item in order:
            text += f"• {item['name']} × {item['qty']} — {item['price'] * item['qty']} ₽\n"
        text += f"\n💰 Сумма заказа: {total} ₽"
        await bot.send_message(MY_ID, text)
        await message.answer(
            "Благодарим за заказ!\n\n"
            "В ближайшее время я свяжусь с вами для уточнения деталей.\n\n"
            "📲 Контакт для связи: @Fe3riko"
        )
        return

    if message.text == "💬 Отзывы":
        await message.answer(
            "💬 Отзывы наших клиентов\n\n"
            "Ознакомьтесь с реальными впечатлениями покупателей о продукции и обслуживании:\n"
            "👉 https://t.me/amatilrev\n\n"
            "Будем рады вашему отзыву — напишите @Fe3riko"
        )
    elif message.text == "📞 Поддержка":
        await message.answer(
            "📞 Служба поддержки\n\n"
            "По всем вопросам, включая подбор устройств и жидкостей, обращайтесь:\n"
            "👉 @Fe3riko\n\n"
            "Мы отвечаем оперативно и предоставляем профессиональную консультацию."
        )
    elif message.text == "❓ FAQ":
        await message.answer(
            "❓ Часто задаваемые вопросы\n\n"
            "🚗 Доставка — по городу, возможен самовывоз.\n"
            "💳 Оплата — банковский перевод или наличные при встрече.\n"
            "🛡 Гарантия — 14 дней на все устройства с момента получения.\n"
            "🧪 Жидкости — исключительно авторские составы, без химических примесей.\n"
            "🔄 Обмен/возврат — возможен в течение 7 дней при сохранении упаковки."
        )
    elif message.text == "🎁 Акции":
        await message.answer(
            "🎁 Действующие акции и специальные предложения\n\n"
            "👥 Приведи друга — получите оба скидку 25% на следующий заказ.\n"
            "🎁 При заказе от 2000 ₽ — случайный подарок (жижа или аксессуар).\n"
            "💎 Персональные условия для постоянных клиентов.\n\n"
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
            "Устройства с регулируемой мощностью позволяют точнее раскрывать вкус жидкости.",
            "Авторские жижи, как и крафтовое пиво, производятся малыми партиями с уникальной рецептурой.",
            "Мятные вкусы остаются самыми популярными в мире благодаря своей универсальности.",
            "Оригинальные испарители служат до трёх раз дольше реплик и обеспечивают чистую передачу вкуса."
        ]
        await message.answer(f"🧠 Факт дня\n\n{random.choice(facts)}")
    elif message.text == "🎰 Подобрать вкус":
        product = random.choice(AVAILABLE_PRODUCTS)
        await message.answer(
            "🎰 Рекомендация дня\n\n"
            f"Сегодня мы советуем обратить внимание на:\n"
            f"• {product['name']}\n"
            f"• Стоимость: {product['price']} ₽\n"
            f"• Профиль вкуса: {product['taste']}\n\n"
            "Перейдите в каталог, чтобы оформить заказ."
        )
    elif message.text == "📋 История заказов":
        if user_id in user_orders and user_orders[user_id]:
            text = "📋 История ваших заказов\n\n"
            for i, order in enumerate(user_orders[user_id][-5:], 1):
                items_text = ", ".join([f"{item['name']} × {item['qty']}" for item in order['items']])
                text += f"{i}. {order['date']}\n{items_text}\nСумма: {order['total']} ₽\n\n"
            text += "Для повторного заказа перейдите в каталог."
        else:
            text = "📋 У вас пока нет оформленных заказов.\n\nПерейдите в каталог, чтобы сделать первый."
        await message.answer(text)
    elif SECRET_PHRASE in message.text.lower():
        await message.answer(
            "🔮 Вы обнаружили секретную пасхалку AMATIL VAPE!\n\n"
            "В благодарность дарим персональный промокод на скидку 5%: SECRET5\n"
            "Предъявите его при общении с @Fe3riko"
        )
    else:
        await message.answer("Пожалуйста, используйте кнопки меню для навигации.")

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
```