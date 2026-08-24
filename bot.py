import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)

from config import BOT_TOKEN


dp = Dispatcher()


# ==================================================
# 🌌 ANIMEVERSE MINI APP
# ==================================================

WEBAPP_URL = "https://animeverseuznu.github.io/animeverse/"


# ==================================================
# 🎨 ASOSIY PASTKI MENYU
# ==================================================

def main_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[

            [
                KeyboardButton(text="🌌 ANIMEVERSE APP")
            ],

            [
                KeyboardButton(text="🔥 TOP ANIME"),
                KeyboardButton(text="🆕 YANGILAR"),
            ],

            [
                KeyboardButton(text="🎭 JANRLAR"),
                KeyboardButton(text="🔎 QIDIRUV"),
            ],

            [
                KeyboardButton(text="📺 SERIAL"),
                KeyboardButton(text="🎞 FILMLAR"),
            ],

            [
                KeyboardButton(text="👑 VIP"),
                KeyboardButton(text="👤 PROFIL"),
            ],

        ],

        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="ANIMEVERSE 🌌",
    )


# ==================================================
# 🚀 START
# ==================================================

@dp.message(Command("start"))
async def start_handler(message: Message):

    await message.answer(
        "🌌 <b>ANIMEVERSE UZ</b>\n\n"
        "Anime olamiga xush kelibsiz! 🍿\n\n"
        "🎬 Anime tomosha qiling\n"
        "🔎 Sevimli animeingizni qidiring\n"
        "👑 VIP imkoniyatlardan foydalaning\n\n"
        "Pastki menyudan kerakli bo‘limni tanlang.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 🌌 MINI APP
# ==================================================

@dp.message(F.text == "🌌 ANIMEVERSE APP")
async def open_webapp(message: Message):

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🚀 MINI APP OCHISH",
                    web_app=WebAppInfo(
                        url=WEBAPP_URL
                    ),
                )
            ],
            [
                KeyboardButton(text="🔙 ORQAGA")
            ],
        ],
        resize_keyboard=True,
    )

    await message.answer(
        "🌌 <b>ANIMEVERSE MINI APP</b>\n\n"
        "⚡ Zamonaviy anime interfeysini ochish uchun "
        "pastdagi tugmani bosing.",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# ==================================================
# 🔥 TOP ANIME
# ==================================================

@dp.message(F.text == "🔥 TOP ANIME")
async def top_anime(message: Message):

    await message.answer(
        "🔥 <b>TOP ANIME</b>\n\n"
        "1️⃣ Solo Leveling\n"
        "2️⃣ One Piece\n"
        "3️⃣ Naruto\n"
        "4️⃣ Demon Slayer\n"
        "5️⃣ Jujutsu Kaisen\n\n"
        "🎬 Anime tanlash uchun Mini App'dan foydalaning.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 🆕 YANGILAR
# ==================================================

@dp.message(F.text == "🆕 YANGILAR")
async def new_anime(message: Message):

    await message.answer(
        "🆕 <b>YANGI ANIMELAR</b>\n\n"
        "✨ Yangi qismlar tez orada qo‘shiladi.\n\n"
        "🌌 To‘liq katalog uchun Mini App'ni oching.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 🎭 JANRLAR
# ==================================================

@dp.message(F.text == "🎭 JANRLAR")
async def genres(message: Message):

    await message.answer(
        "🎭 <b>JANRLAR</b>\n\n"
        "⚔️ Action\n"
        "❤️ Romance\n"
        "😂 Comedy\n"
        "👻 Horror\n"
        "🧙 Fantasy\n"
        "🚀 Sci-Fi\n"
        "🏫 School\n"
        "🥋 Martial Arts\n"
        "💀 Dark Fantasy\n\n"
        "🌌 Batafsil katalog Mini App'da.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 🔎 QIDIRUV
# ==================================================

@dp.message(F.text == "🔎 QIDIRUV")
async def search(message: Message):

    await message.answer(
        "🔎 <b>ANIME QIDIRUV</b>\n\n"
        "Anime nomini yuboring.\n\n"
        "Masalan:\n"
        "• Naruto\n"
        "• One Piece\n"
        "• Solo Leveling",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 📺 SERIAL
# ==================================================

@dp.message(F.text == "📺 SERIAL")
async def serial(message: Message):

    await message.answer(
        "📺 <b>SERIAL</b>\n\n"
        "🔥 Mashhur seriallar\n"
        "🆕 Yangi seriallar\n"
        "👑 VIP seriallar\n\n"
        "🌌 Mini App orqali katalogni ko‘ring.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 🎞 FILMLAR
# ==================================================

@dp.message(F.text == "🎞 FILMLAR")
async def movies(message: Message):

    await message.answer(
        "🎞 <b>FILMLAR</b>\n\n"
        "🍿 Anime filmlar\n"
        "🔥 Mashhur filmlar\n"
        "🆕 Yangi filmlar\n\n"
        "🌌 Mini App orqali tanlang.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 👑 VIP
# ==================================================

@dp.message(F.text == "👑 VIP")
async def vip(message: Message):

    await message.answer(
        "👑 <b>ANIMEVERSE VIP</b>\n\n"
        "⚡ VIP anime\n"
        "⚡ Reklamasiz tomosha\n"
        "⚡ Yangi qismlarga erta kirish\n"
        "⚡ Maxsus kontent\n\n"
        "💎 VIP tizimi tez orada ishga tushadi.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 👤 PROFIL
# ==================================================

@dp.message(F.text == "👤 PROFIL")
async def profile(message: Message):

    user = message.from_user

    name = user.first_name or "Anime Hunter"

    await message.answer(
        "👤 <b>PROFIL</b>\n\n"
        f"👋 Ism: <b>{name}</b>\n"
        f"🆔 ID: <code>{user.id}</code>\n\n"
        "⭐ XP: 0\n"
        "👑 VIP: Yo‘q\n"
        "🎬 Ko‘rilgan anime: 0",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# 🔙 ORQAGA
# ==================================================

@dp.message(F.text == "🔙 ORQAGA")
async def back(message: Message):

    await message.answer(
        "🌌 <b>ANIMEVERSE</b>\n\n"
        "Asosiy menyu.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# ❓ BOSHQA XABARLAR
# ==================================================

@dp.message()
async def other_message(message: Message):

    await message.answer(
        "🌌 <b>ANIMEVERSE</b>\n\n"
        "Pastki menyudan bo‘lim tanlang yoki "
        "Mini App'ni oching.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==================================================
# ▶️ BOTNI ISHGA TUSHIRISH
# ==================================================

async def main():

    bot = Bot(
        token=BOT_TOKEN
    )

    print("🌌 ANIMEVERSE UZ BOT ISHLADI!")

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
