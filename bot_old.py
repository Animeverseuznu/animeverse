import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    VIP_CARD,
    VIP_PACKAGES,
)

from db import (
    init_db,
    create_user,
    get_user,
    add_xp,
    is_vip,
    get_vip_until,
    add_vip_days,
    add_anime,
    get_anime,
    add_episode,
    get_episode,
    save_history,
    create_payment,
    get_payment,
    set_payment_status,
    get_pending_payment,
)


dp = Dispatcher()


# =========================================================
# 🎨 PASTKI ASOSIY MENYU
# =========================================================

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
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
                KeyboardButton(text="🇯🇵 ANIME"),
                KeyboardButton(text="🇨🇳 DONGHUA"),
            ],
            [
                KeyboardButton(text="❤️ SEVIMLILAR"),
            ],
            [
                KeyboardButton(text="📚 DAVOM ETTIRISH"),
            ],
            [
                KeyboardButton(text="🎁 KUNLIK BONUS"),
                KeyboardButton(text="🏆 REYTING"),
            ],
            [
                KeyboardButton(text="👤 PROFIL"),
                KeyboardButton(text="⚙️ SOZLAMALAR"),
            ],
            [
                KeyboardButton(text="👑 VIP ZONA"),
            ],
            [
                KeyboardButton(text="💬 YORDAM"),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Menyudan bo‘lim tanlang..."
    )


# =========================================================
# 🎭 JANRLAR MENYUSI
# =========================================================

def genre_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⚔️ Action"),
                KeyboardButton(text="❤️ Romance"),
            ],
            [
                KeyboardButton(text="😂 Comedy"),
                KeyboardButton(text="👻 Horror"),
            ],
            [
                KeyboardButton(text="🧙 Fantasy"),
                KeyboardButton(text="🚀 Sci-Fi"),
            ],
            [
                KeyboardButton(text="🧠 Psychological"),
                KeyboardButton(text="🥷 Ninja"),
            ],
            [
                KeyboardButton(text="🏫 School"),
                KeyboardButton(text="🏆 Sport"),
            ],
            [
                KeyboardButton(text="🔙 BOSH MENU"),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


# =========================================================
# 👑 VIP MENYU
# =========================================================

def vip_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👑 VIP ANIMELAR"),
            ],
            [
                KeyboardButton(text="💳 VIP OLISH"),
                KeyboardButton(text="📅 VIP HOLATI"),
            ],
            [
                KeyboardButton(text="💎 VIP AFZALLIKLAR"),
            ],
            [
                KeyboardButton(text="🔙 BOSH MENU"),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


# =========================================================
# 🛠 ADMIN MENYU
# =========================================================

def admin_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ ANIME QO‘SHISH"),
            ],
            [
                KeyboardButton(text="🎥 QISM QO‘SHISH"),
            ],
            [
                KeyboardButton(text="💳 TO‘LOVLAR"),
            ],
            [
                KeyboardButton(text="📊 STATISTIKA"),
            ],
            [
                KeyboardButton(text="📢 XABAR YUBORISH"),
            ],
            [
                KeyboardButton(text="🔙 BOSH MENU"),
            ],
        ],
        resize_keyboard=True,
    )


# =========================================================
# 🏠 START
# =========================================================

@dp.message(Command("start"))
async def start_handler(message: Message):

    create_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🌌 <b>ANIMEVERSE UZ</b>\n\n"
        "✨ Anime olamiga xush kelibsiz!\n\n"
        "🔥 TOP animelar\n"
        "🆕 Yangi chiqishlar\n"
        "🎭 Janrlar\n"
        "👑 VIP zona\n"
        "🎁 Kunlik bonus\n"
        "🏆 XP va reyting tizimi\n\n"
        "👇 Pastki menyudan bo‘lim tanlang.",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🏠 BOSH MENU
# =========================================================

@dp.message(F.text == "🔙 BOSH MENU")
async def back_home(message: Message):

    await message.answer(
        "🏠 <b>ANIMEVERSE UZ</b>\n\n"
        "👇 Kerakli bo‘limni tanlang.",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 🔎 QIDIRUV
# =========================================================

@dp.message(F.text == "🔎 QIDIRUV")
async def search_button(message: Message):

    await message.answer(
        "🔎 <b>ANIME QIDIRUV</b>\n\n"
        "Anime kodini yuboring.\n\n"
        "Masalan:\n"
        "<code>NARUTO</code>\n"
        "<code>ONEPIECE</code>",
        parse_mode="HTML"
    )


# =========================================================
# 🎭 JANRLAR
# =========================================================

@dp.message(F.text == "🎭 JANRLAR")
async def genres(message: Message):

    await message.answer(
        "🎭 <b>ANIME JANRLARI</b>\n\n"
        "O‘zingizga yoqqan janrni tanlang:",
        reply_markup=genre_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 👤 PROFIL
# =========================================================

@dp.message(F.text == "👤 PROFIL")
async def profile(message: Message):

    user_id = message.from_user.id

    user = get_user(user_id)

    if not user:
        create_user(
            user_id,
            message.from_user.username
        )
        user = get_user(user_id)

    xp = 0

    if len(user) > 2:
        try:
            xp = int(user[2])
        except Exception:
            xp = 0

    level = (xp // 100) + 1
    next_xp = ((level) * 100) - xp

    vip_status = "❌ Faol emas"

    if is_vip(user_id):
        vip_status = "👑 FAOL"

    await message.answer(
        "👤 <b>PROFIL</b>\n\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"⭐ XP: <b>{xp}</b>\n"
        f"🏆 LEVEL: <b>{level}</b>\n"
        f"⚡ Keyingi level: <b>{next_xp} XP</b>\n"
        f"👑 VIP: <b>{vip_status}</b>\n\n"
        "━━━━━━━━━━━━━━\n"
        "🎖 <b>Anime Hunter</b>",
        parse_mode="HTML"
    )


# =========================================================
# 🏆 REYTING
# =========================================================

@dp.message(F.text == "🏆 REYTING")
async def rating(message: Message):

    await message.answer(
        "🏆 <b>ANIMEVERSE REYTING</b>\n\n"
        "🥇 1. AnimeMaster — 2 450 XP\n"
        "🥈 2. OtakuKing — 2 120 XP\n"
        "🥉 3. Senpai — 1 890 XP\n\n"
        "🔥 Siz ham anime ko‘rib XP yig‘ing!",
        parse_mode="HTML"
    )


# =========================================================
# 🎁 KUNLIK BONUS
# =========================================================

@dp.message(F.text == "🎁 KUNLIK BONUS")
async def daily_bonus(message: Message):

    add_xp(
        message.from_user.id,
        10
    )

    await message.answer(
        "🎁 <b>KUNLIK BONUS</b>\n\n"
        "⭐ Sizga +10 XP berildi!\n\n"
        "🔥 Ertaga yana kirib bonus oling.",
        parse_mode="HTML"
    )


# =========================================================
# 👑 VIP ZONA
# =========================================================

@dp.message(F.text == "👑 VIP ZONA")
async def vip_zone(message: Message):

    await message.answer(
        "👑 <b>ANIMEVERSE VIP ZONA</b>\n\n"
        "💎 VIP imkoniyatlari:\n\n"
        "🔥 Maxsus VIP animelar\n"
        "⚡ Eksklyuziv kontent\n"
        "🎬 Premium seriallar\n"
        "🏆 Maxsus status\n"
        "🎁 VIP bonuslar\n\n"
        "👇 Quyidagi menyudan foydalaning.",
        reply_markup=vip_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# 💎 VIP AFZALLIKLAR
# =========================================================

@dp.message(F.text == "💎 VIP AFZALLIKLAR")
async def vip_benefits(message: Message):

    await message.answer(
        "💎 <b>VIP AFZALLIKLARI</b>\n\n"
        "👑 VIP anime katalogi\n"
        "🎬 Maxsus seriallar\n"
        "⚡ Yangi kontentga erta kirish\n"
        "🎁 Qo‘shimcha bonuslar\n"
        "🏆 VIP profil belgisi",
        parse_mode="HTML"
    )


# =========================================================
# 📅 VIP HOLATI
# =========================================================

@dp.message(F.text == "📅 VIP HOLATI")
async def vip_status(message: Message):

    user_id = message.from_user.id

    if not is_vip(user_id):

        await message.answer(
            "❌ <b>VIP faol emas.</b>\n\n"
            "👑 VIP olish uchun VIP OLISH tugmasini bosing.",
            parse_mode="HTML"
        )

        return

    until = get_vip_until(user_id)

    await message.answer(
        "👑 <b>VIP FAOL</b>\n\n"
        f"📅 Tugash vaqti:\n"
        f"<code>{until}</code>",
        parse_mode="HTML"
    )


# =========================================================
# 💳 VIP OLISH
# =========================================================

@dp.message(F.text == "💳 VIP OLISH")
async def buy_vip_menu(message: Message):

    text = "👑 <b>VIP PAKETLAR</b>\n\n"

    for key, value in VIP_PACKAGES.items():

        package, days, amount = value

        text += (
            f"🔹 {package}\n"
            f"💰 {amount:,} so‘m\n\n"
        )

    text += (
        "📌 Paketni tanlash uchun quyidagi buyruqlardan "
        "foydalaning:\n\n"
        "<code>/vip30</code>\n"
        "<code>/vip90</code>\n"
        "<code>/vip180</code>\n"
        "<code>/vip365</code>"
    )

    await message.answer(
        text,
        parse_mode="HTML"
    )


# =========================================================
# 💳 VIP BUY COMMANDLAR
# =========================================================

async def create_vip_order(
    message: Message,
    code: str
):

    if code not in VIP_PACKAGES:

        await message.answer(
            "❌ Paket topilmadi."
        )

        return

    package, days, amount = VIP_PACKAGES[code]

    payment_id = create_payment(
        message.from_user.id,
        package,
        days,
        amount
    )

    await message.answer(
        "💳 <b>VIP TO‘LOV</b>\n\n"
        f"📦 Paket: <b>{package}</b>\n"
        f"💰 Summa: <b>{amount:,} so‘m</b>\n\n"
        f"💳 Karta:\n<code>{VIP_CARD}</code>\n\n"
        "1️⃣ Kartaga to‘lov qiling.\n"
        "2️⃣ Chekni shu botga yuboring.\n"
        f"3️⃣ To‘lov ID: <code>#{payment_id}</code>\n\n"
        "📸 Chekni rasm qilib yuboring.",
        parse_mode="HTML"
    )


@dp.message(Command("vip30"))
async def vip30(message: Message):
    await create_vip_order(message, "30")


@dp.message(Command("vip90"))
async def vip90(message: Message):
    await create_vip_order(message, "90")


@dp.message(Command("vip180"))
async def vip180(message: Message):
    await create_vip_order(message, "180")


@dp.message(Command("vip365"))
async def vip365(message: Message):
    await create_vip_order(message, "365")


# =========================================================
# 📸 VIP CHEK
# =========================================================

@dp.message(F.photo)
async def payment_receipt(
    message: Message,
    bot: Bot
):

    payment = get_pending_payment(
        message.from_user.id
    )

    if not payment:

        await message.answer(
            "❌ Sizda kutilayotgan VIP to‘lovi yo‘q."
        )

        return

    payment_id = payment[0]
    package = payment[1]
    days = payment[2]
    amount = payment[3]

    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=(
            "💳 <b>YANGI VIP TO‘LOV</b>\n\n"
            f"🆔 To‘lov: #{payment_id}\n"
            f"👤 User: <code>{message.from_user.id}</code>\n"
            f"📦 Paket: {package}\n"
            f"📅 Kun: {days}\n"
            f"💰 Summa: {amount:,} so‘m\n\n"
            "Admin tasdiqlashi kerak."
        ),
        parse_mode="HTML"
    )

    await message.answer(
        "✅ Chek adminga yuborildi.\n\n"
        "⏳ To‘lov tekshirilmoqda."
    )


# =========================================================
# 🎬 ANIME KODI
# =========================================================

@dp.message()
async def anime_search(message: Message):

    if not message.text:
        return

    text = message.text.strip()

    special_buttons = {
        "🔥 TOP ANIME",
        "🆕 YANGILAR",
        "🎭 JANRLAR",
        "🔎 QIDIRUV",
        "📺 SERIAL",
        "🎞 FILMLAR",
        "🇯🇵 ANIME",
        "🇨🇳 DONGHUA",
        "❤️ SEVIMLILAR",
        "📚 DAVOM ETTIRISH",
        "🎁 KUNLIK BONUS",
        "🏆 REYTING",
        "👤 PROFIL",
        "⚙️ SOZLAMALAR",
        "👑 VIP ZONA",
        "💬 YORDAM",
        "💳 VIP OLISH",
        "📅 VIP HOLATI",
        "💎 VIP AFZALLIKLAR",
        "🔙 BOSH MENU",
        "⚔️ Action",
        "❤️ Romance",
        "😂 Comedy",
        "👻 Horror",
        "🧙 Fantasy",
        "🚀 Sci-Fi",
        "🧠 Psychological",
        "🥷 Ninja",
        "🏫 School",
        "🏆 Sport",
    }

    if text in special_buttons:
        return

    if text.startswith("/"):
        return

    anime = get_anime(text)

    if not anime:

        await message.answer(
            "❌ Anime topilmadi.\n\n"
            "🔎 Kodni tekshirib qayta yuboring."
        )

        return

    anime_id = anime[0]

    title = anime[2]
    description = anime[3] or ""
    genre = anime[4] or ""
    poster = anime[5]
    vip_only = anime[6]

    if vip_only and not is_vip(
        message.from_user.id
    ):

        await message.answer(
            "👑 <b>VIP ANIME</b>\n\n"
            f"🎬 {title}\n\n"
            "Bu anime faqat VIP foydalanuvchilar uchun.",
            reply_markup=vip_keyboard(),
            parse_mode="HTML"
        )

        return

    # DBdan qismlar
    from db import connect

    con = connect()
    cur = con.cursor()

    cur.execute(
        """
        SELECT episode
        FROM episodes
        WHERE anime_id=?
        ORDER BY episode
        """,
        (anime_id,)
    )

    episodes = cur.fetchall()

    con.close()

    if not episodes:

        await message.answer(
            f"🎬 <b>{title}</b>\n\n"
            "❌ Hozircha qismlar qo‘shilmagan.",
            parse_mode="HTML"
        )

        return

    buttons = []

    row = []

    for item in episodes:

        ep = item[0]

        row.append(
            KeyboardButton(
                text=f"▶️ {ep}-qism"
            )
        )

        if len(row) == 3:

            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append(
        [
            KeyboardButton(
                text="🔙 BOSH MENU"
            )
        ]
    )

    episode_keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        is_persistent=True
    )

    await message.answer(
        f"🎬 <b>{title}</b>\n\n"
        f"📝 {description}\n\n"
        f"🎭 {genre}\n\n"
        f"📺 Qismlar: <b>{len(episodes)}</b>\n\n"
        "👇 Qismni tanlang.",
        reply_markup=episode_keyboard,
        parse_mode="HTML"
    )


# =========================================================
# ▶️ QISMNI YUBORISH
# =========================================================

@dp.message(F.text.regexp(r"^▶️ \d+-qism$"))
async def send_episode(message: Message):

    try:

        number = int(
            message.text
            .replace("▶️ ", "")
            .replace("-qism", "")
        )

    except Exception:

        return

    await message.answer(
        f"⏳ <b>{number}-qism</b> tayyorlanmoqda...",
        parse_mode="HTML"
    )

    # Anime IDni oxirgi qidiruvdan olish uchun
    # foydalanuvchining oxirgi anime kodini aniqlash
    # imkoniyati mavjud DBda bo‘lmagani sababli
    # hozircha foydalanuvchidan kod so‘raladi.

    await message.answer(
        "🔎 Avval anime kodini yuboring.\n\n"
        "Keyin kerakli qismni tanlang."
    )


# =========================================================
# 🔥 TOP
# =========================================================

@dp.message(F.text == "🔥 TOP ANIME")
async def top_anime(message: Message):

    await message.answer(
        "🔥 <b>TOP ANIMELAR</b>\n\n"
        "1️⃣ One Piece\n"
        "2️⃣ Naruto\n"
        "3️⃣ Attack on Titan\n"
        "4️⃣ Demon Slayer\n"
        "5️⃣ Solo Leveling\n\n"
        "🔎 Anime kodini yuborib ochishingiz mumkin.",
        parse_mode="HTML"
    )


# =========================================================
# 🆕 YANGILAR
# =========================================================

@dp.message(F.text == "🆕 YANGILAR")
async def new_anime(message: Message):

    await message.answer(
        "🆕 <b>YANGI ANIMELAR</b>\n\n"
        "Bu bo‘limga yangi qo‘shilgan animelar "
        "chiqariladi.",
        parse_mode="HTML"
    )


# =========================================================
# 📺 SERIAL
# =========================================================

@dp.message(F.text == "📺 SERIAL")
async def serials(message: Message):

    await message.answer(
        "📺 <b>SERIAL</b>\n\n"
        "Anime kodini yuboring yoki 🔎 QIDIRUV "
        "bo‘limidan foydalaning.",
        parse_mode="HTML"
    )


# =========================================================
# 🎞 FILMLAR
# =========================================================

@dp.message(F.text == "🎞 FILMLAR")
async def films(message: Message):

    await message.answer(
        "🎞 <b>ANIME FILMLAR</b>\n\n"
        "Anime film kodini yuboring.",
        parse_mode="HTML"
    )


# =========================================================
# 🇯🇵 ANIME
# =========================================================

@dp.message(F.text == "🇯🇵 ANIME")
async def japanese_anime(message: Message):

    await message.answer(
        "🇯🇵 <b>YAPON ANIMELARI</b>\n\n"
        "Kerakli anime kodini yuboring.",
        parse_mode="HTML"
    )


# =========================================================
# 🇨🇳 DONGHUA
# =========================================================

@dp.message(F.text == "🇨🇳 DONGHUA")
async def donghua(message: Message):

    await message.answer(
        "🇨🇳 <b>DONGHUA</b>\n\n"
        "Xitoy animatsiyalari bo‘limi.",
        parse_mode="HTML"
    )


# =========================================================
# ❤️ SEVIMLILAR
# =========================================================

@dp.message(F.text == "❤️ SEVIMLILAR")
async def favorites(message: Message):

    await message.answer(
        "❤️ <b>SEVIMLILAR</b>\n\n"
        "Siz saqlagan animelar shu yerda chiqadi."
    )


# =========================================================
# 📚 DAVOM ETTIRISH
# =========================================================

@dp.message(F.text == "📚 DAVOM ETTIRISH")
async def continue_watch(message: Message):

    await message.answer(
        "📚 <b>DAVOM ETTIRISH</b>\n\n"
        "Oxirgi ko‘rilgan animelar tarixi "
        "shu yerda chiqadi."
    )


# =========================================================
# ⚙️ SOZLAMALAR
# =========================================================

@dp.message(F.text == "⚙️ SOZLAMALAR")
async def settings(message: Message):

    await message.answer(
        "⚙️ <b>SOZLAMALAR</b>\n\n"
        "🔔 Bildirishnomalar: ON\n"
        "🌐 Til: O‘zbekcha\n\n"
        "Hozircha qo‘shimcha sozlamalar mavjud emas.",
        parse_mode="HTML"
    )


# =========================================================
# 💬 YORDAM
# =========================================================

@dp.message(F.text == "💬 YORDAM")
async def help_button(message: Message):

    await message.answer(
        "💬 <b>YORDAM</b>\n\n"
        "🔎 Anime topish uchun kodini yuboring.\n"
        "👑 VIP uchun VIP ZONA bo‘limiga kiring.\n"
        "🎁 Har kuni bonus olishni unutmang.\n\n"
        "Muammo bo‘lsa administratorga murojaat qiling.",
        parse_mode="HTML"
    )


# =========================================================
# 🛠 ADMIN
# =========================================================

@dp.message(Command("admin"))
async def admin_panel(message: Message):

    if message.from_user.id != ADMIN_ID:

        await message.answer(
            "❌ Siz admin emassiz."
        )

        return

    await message.answer(
        "🛠 <b>ANIMEVERSE ADMIN PANEL</b>\n\n"
        "Kerakli bo‘limni tanlang.",
        reply_markup=admin_keyboard(),
        parse_mode="HTML"
    )


# =========================================================
# ADMIN — ANIME QO‘SHISH
# =========================================================

@dp.message(F.text == "➕ ANIME QO‘SHISH")
async def admin_add_anime(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "➕ Anime qo‘shish funksiyasi uchun "
        "anime kodi, nomi va ma'lumotlari yuboriladi.\n\n"
        "Hozirgi DB strukturasi bilan xavfsiz "
        "qo‘shish uchun keyingi bosqichda FSM ulanadi."
    )


# =========================================================
# ADMIN — QISM
# =========================================================

@dp.message(F.text == "🎥 QISM QO‘SHISH")
async def admin_add_episode(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "🎥 <b>QISM QO‘SHISH</b>\n\n"
        "Avval anime kodini yuboring.",
        parse_mode="HTML"
    )


# =========================================================
# ADMIN — TO‘LOVLAR
# =========================================================

@dp.message(F.text == "💳 TO‘LOVLAR")
async def admin_payments(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "💳 <b>VIP TO‘LOVLAR</b>\n\n"
        "Yangi cheklar to‘g‘ridan-to‘g‘ri "
        "admin Telegram chatiga yuboriladi.",
        parse_mode="HTML"
    )


# =========================================================
# ADMIN — STATISTIKA
# =========================================================

@dp.message(F.text == "📊 STATISTIKA")
async def admin_stats(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📊 <b>ANIMEVERSE STATISTIKA</b>\n\n"
        "👥 Foydalanuvchilar: DB orqali\n"
        "🎬 Anime: DB orqali\n"
        "👑 VIP: DB orqali\n"
        "💳 To‘lovlar: DB orqali",
        parse_mode="HTML"
    )


# =========================================================
# ADMIN — XABAR
# =========================================================

@dp.message(F.text == "📢 XABAR YUBORISH")
async def admin_broadcast(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📢 Broadcast funksiyasi keyingi bosqichda "
        "qo‘shiladi."
    )


# =========================================================
# START BOT
# =========================================================

async def main():

    init_db()

    bot = Bot(
        token=BOT_TOKEN
    )

    print(
        "🌌 ANIMEVERSE UZ BOT ISHLADI!"
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
