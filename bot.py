import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8534597622:AAGy2BFWxae892IghQylbkCoxjGdHvNrq0g"
ADMIN_ID = 8389699824
SITE_URL = "https://wonderful-sunshine-0fc294.netlify.app/"
VPN_CHANNEL = "https://t.me/amatilvpn"
REVIEWS_GROUP = "https://t.me/amatilrev"
SUPPORT = "https://t.me/Fe3riko"
PROMO_CODE = "AMATIL10"

# ===== ФАКТЫ ПРО ВЕЙПЫ =====
FACTS = [
    "💨 Первый вейп был изобретён в 1963 году. Его создатель — Херберт Гилберт, американский учёный.",
    "🔬 Никотин в жиже для вейпа может быть в двух формах: солевой и щелочной. Солевой усваивается быстрее и мягче.",
    "🌿 VG (растительный глицерин) отвечает за пар и мягкость, а PG (пропиленгликоль) — за «удар по горлу» и перенос вкуса.",
    "⚡ Чем ниже сопротивление испарителя, тем больше пара и тем быстрее садится аккумулятор.",
    "🍓 Большинство вкусов для жижи разрабатываются в лабораториях, где работают профессиональные химики-ароматисты.",
    "📅 Первый коммерческий вейп (Ruyan) появился в Китае в 2004 году. Его создал Хон Лик.",
    "🔋 Литий-ионные аккумуляторы в вейпах заряжаются так же, как в телефонах — они не «помнят» заряд.",
    "🧪 Ароматизаторы для жижи часто берутся из пищевой промышленности — те же, что используют в конфетах.",
    "💧 Жижа хранится до 2 лет, если держать её в тёмном прохладном месте и не открывать флакон.",
    "🌡️ При нагреве выше 250°C глицерин начинает распадаться на вредные вещества. Поэтому важно не «жечь» испаритель.",
    "🎨 Вкус жижи на 70% зависит от ароматизатора и на 30% — от соотношения VG/PG.",
    "⚙️ Обслуживаемые атомайзеры (RDA, RTA) позволяют менять спираль и вату самостоятельно — это дешевле, чем менять койлы.",
    "🍫 Вкус «табак» в вейпах — это не настоящий табак, а ароматизатор, имитирующий его запах.",
    "📱 Современные поды (например, XROS, Caliburn) заряжаются через Type-C и держат заряд до 2 дней.",
    "🚀 Скорость затяжки зависит от обдува: чем шире обдув, тем «свободнее» затяжка и больше пара."
]

# ===== ИНИЦИАЛИЗАЦИЯ =====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🛍 Каталог", web_app=WebAppInfo(url=SITE_URL)),
        InlineKeyboardButton(text="🛡 VPN", callback_data="menu_vpn")
    )
    builder.row(
        InlineKeyboardButton(text="⭐ Отзывы", callback_data="menu_reviews"),
        InlineKeyboardButton(text="💬 Поддержка", callback_data="menu_support")
    )
    builder.row(
        InlineKeyboardButton(text="❓ FAQ", callback_data="menu_faq"),
        InlineKeyboardButton(text="🎁 Акции", callback_data="menu_promo")
    )
    builder.row(
        InlineKeyboardButton(text="🚚 Доставка", callback_data="menu_delivery"),
        InlineKeyboardButton(text="💳 Оплата", callback_data="menu_payment")
    )
    builder.row(
        InlineKeyboardButton(text="🎲 Факт дня", callback_data="menu_fact"),
        InlineKeyboardButton(text="🎯 Реферал", callback_data="menu_referral")
    )
    return builder.as_markup()


# ===== КНОПКА НАЗАД =====
def back_button():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu"))
    return builder.as_markup()


# ===== /START =====
@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в <b>AMATIL VAPE</b> — магазин качественных вейпов и расходников в Великом Новгороде.\n\n"
        "🛍 <b>Открой каталог</b> — там все товары, цены и оформление заказа.\n"
        "🛡 Защити свой трафик — наш VPN-канал.\n"
        "💬 Есть вопросы — жми «Поддержка».\n\n"
        "Выбирай, что тебя интересует 👇"
    )
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")


# ===== ОБРАБОТЧИКИ КНОПОК =====
@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выбери, что тебя интересует 👇",
        reply_markup=main_menu()
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_vpn")
async def menu_vpn(callback: CallbackQuery):
    text = (
        "🛡 <b>AMATIL Secure — VPN</b>\n\n"
        "Быстрый и безопасный VPN:\n"
        "⚡ Скорость без тормозов\n"
        "🌍 Серверы в Европе, США и Азии\n"
        "🔓 Обход блокировок и белых списков\n"
        "🔒 Твои данные — только твои\n\n"
        "🎁 Первые 3 дня — бесплатно!\n\n"
        "Переходи в канал, чтобы узнать больше 👇"
    )
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🛡 Перейти в канал", url=VPN_CHANNEL))
    builder.row(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "menu_reviews")
async def menu_reviews(callback: CallbackQuery):
    text = (
        "⭐ <b>Отзывы наших клиентов</b>\n\n"
        "Мы гордимся тем, что наши клиенты возвращаются и рекомендуют нас друзьям.\n\n"
        "Хочешь почитать отзывы или оставить свой? Переходи в группу 👇"
    )
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⭐ Открыть отзывы", url=REVIEWS_GROUP))
    builder.row(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "menu_support")
async def menu_support(callback: CallbackQuery):
    text = (
        "💬 <b>Поддержка AMATIL VAPE</b>\n\n"
        "Есть вопрос по заказу, доставке или товару?\n\n"
        "Напиши нам напрямую — ответим быстро 👇"
    )
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💬 Написать @Fe3riko", url=SUPPORT))
    builder.row(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "menu_faq")
async def menu_faq(callback: CallbackQuery):
    text = (
        "❓ <b>Частые вопросы</b>\n\n"
        "<b>1. Как оформить заказ?</b>\n"
        "Открой каталог, добавь товары в корзину и нажми «Оформить». Мы свяжемся с тобой в течение 15 минут.\n\n"
        "<b>2. Есть ли доставка?</b>\n"
        "Да, по Великому Новгороду — от 200 ₽. От 3000 ₽ — бесплатно. Есть самовывоз.\n\n"
        "<b>3. Можно ли вернуть товар?</b>\n"
        "Да, в течение 14 дней, если товар не использован и упаковка сохранена.\n\n"
        "<b>4. Как оплатить?</b>\n"
        "Наличными, переводом на карту или через СБП.\n\n"
        "<b>5. Как проверить совместимость?</b>\n"
        "На сайте есть блок «Проверка совместимости» — выбираешь расходник и устройство, получаешь ответ."
    )
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "menu_promo")
async def menu_promo(callback: CallbackQuery):
    text = (
        "🎁 <b>Акции и промокоды</b>\n\n"
        f"🔥 <b>Промокод на первый заказ:</b>\n"
        f"<code>{PROMO_CODE}</code>\n\n"
        "Скидка 10% на первый заказ. Просто назови промокод при оформлении.\n\n"
        "Следи за новыми акциями в нашем канале 👇"
    )
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🛍 В каталог", web_app=WebAppInfo(url=SITE_URL)))
    builder.row(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "menu_delivery")
async def menu_delivery(callback: CallbackQuery):
    text = (
        "🚚 <b>Доставка</b>\n\n"
        "📍 <b>Самовывоз:</b>\n"
        "проспект Александра Корсунова, 49\n"
        "Ежедневно с 10:00 до 21:00\n\n"
        "🚗 <b>Курьером по городу:</b>\n"
        "от 200 ₽ — 1–2 часа\n"
        "от 3000 ₽ — бесплатно\n\n"
        "📦 <b>По области:</b>\n"
        "от 400 ₽ — 1–2 дня (СДЭК/Boxberry)"
    )
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "menu_payment")
async def menu_payment(callback: CallbackQuery):
    text = (
        "💳 <b>Способы оплаты</b>\n\n"
        "✅ Наличными при получении\n"
        "✅ Переводом на карту (Сбер, Тинькофф)\n"
        "✅ Через СБП (Система быстрых платежей)\n\n"
        "Реквизиты пришлём после подтверждения заказа."
    )
    await callback.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "menu_fact")
async def menu_fact(callback: CallbackQuery):
    fact = random.choice(FACTS)
    text = f"🎲 <b>Факт дня</b>\n\n{fact}"
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🎲 Ещё факт", callback_data="menu_fact"))
    builder.row(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "menu_referral")
async def menu_referral(callback: CallbackQuery):
    text = (
        "🎯 <b>Реферальная программа</b>\n\n"
        "Хочешь заработать на пригоне клиентов?\n\n"
        "Мы платим <b>процент с каждой продажи</b> тем, кто приводит к нам клиентов.\n\n"
        "Условия обсуждаются индивидуально:\n"
        "• сколько клиентов приведёшь — такой и процент\n"
        "• выплаты раз в неделю\n"
        "• прозрачная статистика\n\n"
        "Напиши администратору — обсудим детали 👇"
    )
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💬 Написать администратору", url=SUPPORT))
    builder.row(InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()


# ===== ЗАПУСК =====
async def main():
    print("Бот @amatilrev запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())