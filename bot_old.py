import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import BOT_TOKEN, ADMIN_ID, VIP_CARD, VIP_PACKAGES

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


class AddAnime(StatesGroup):
    code = State()
    title = State()
    description = State()
    genre = State()
    poster = State()
    vip = State()


class AddEpisode(StatesGroup):
    code = State()
    episode = State()
    video = State()


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔎 Anime qidirish",
                    callback_data="search"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Profil",
                    callback_data="profile"
                ),
                InlineKeyboardButton(
                    text="📚 Tarix",
                    callback_data="history"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 VIP",
                    callback_data="vip"
                )
            ],
        ]
    )


def vip_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👑 1 oy — 30 000 so‘m",
                    callback_data="buy_30"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 3 oy — 70 000 so‘m",
                    callback_data="buy_90"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 6 oy — 120 000 so‘m",
                    callback_data="buy_180"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 1 yil — 200 000 so‘m",
                    callback_data="buy_365"
                )
            ],
        ]
    )


def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Anime qo‘shish",
                    callback_data="admin_anime"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎥 Qism/video qo‘shish",
                    callback_data="admin_episode"
                )
            ],
        ]
    )


@dp.message(Command("start"))
async def start_handler(message: Message):
    create_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🌌 <b>ANIMEVERSE UZ</b>\n\n"
        "🎬 Anime botiga xush kelibsiz!\n\n"
        "🔎 Anime kodini yuboring.\n"
        "👑 VIP bo‘limidan VIP olishingiz mumkin.\n"
        "📚 Ko‘rgan animelaringiz tarixda saqlanadi.\n\n"
        "👇 Menyudan foydalaning:",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "home")
async def home_callback(callback: CallbackQuery):
    await callback.message.answer(
        "🏠 <b>ANIMEVERSE UZ</b>",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(F.data == "search")
async def search_callback(callback: CallbackQuery):
    await callback.message.answer(
        "🔎 <b>ANIME QIDIRISH</b>\n\n"
        "Anime kodini yuboring.\n\n"
        "Masalan:\n"
        "<code>NARUTO</code>",
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = get_user(user_id)

    if not user:
        create_user(
            user_id,
            callback.from_user.username
        )
        user = get_user(user_id)

    xp = user[2] if len(user) > 2 else 0

    vip = "✅ Faol" if is_vip(user_id) else "❌ Yo‘q"

    text = (
        "👤 <b>PROFIL</b>\n\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"⭐ XP: <b>{xp}</b>\n"
        f"👑 VIP: <b>{vip}</b>"
    )

    if is_vip(user_id):
        until = get_vip_until(user_id)
        text += f"\n📅 Tugashi: <code>{until}</code>"

    await callback.message.answer(
        text,
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(F.data == "vip")
async def vip_callback(callback: CallbackQuery):
    user_id = callback.from_user.id

    if is_vip(user_id):
        until = get_vip_until(user_id)

        await callback.message.answer(
            "👑 <b>VIP FAOL</b>\n\n"
            f"📅 Tugash vaqti:\n"
            f"<code>{until}</code>",
            parse_mode="HTML"
        )
    else:
        await callback.message.answer(
            "👑 <b>ANIMEVERSE VIP</b>\n\n"
            "VIP paketlardan birini tanlang:",
            reply_markup=vip_menu(),
            parse_mode="HTML"
        )

    await callback.answer()


@dp.callback_query(F.data.startswith("buy_"))
async def buy_vip(callback: CallbackQuery):
    code = callback.data.replace("buy_", "")

    if code not in VIP_PACKAGES:
        await callback.answer(
            "❌ Paket topilmadi.",
            show_alert=True
        )
        return

    package, days, amount = VIP_PACKAGES[code]

    payment_id = create_payment(
        callback.from_user.id,
        package,
        days,
        amount
    )

    await callback.message.answer(
        "👑 <b>VIP TO‘LOV</b>\n\n"
        f"📦 Paket: <b>{package}</b>\n"
        f"💰 Narx: <b>{amount:,} so‘m</b>\n\n"
        "💳 HUMO karta:\n"
        f"<code>{VIP_CARD}</code>\n\n"
        "1️⃣ Kartaga to‘lov qiling.\n"
        "2️⃣ Chekni shu botga yuboring.\n"
        f"3️⃣ To‘lov ID: <code>#{payment_id}</code>",
        parse_mode="HTML"
    )

    await callback.answer()


@dp.message(F.photo)
async def receipt_handler(message: Message, bot: Bot):
    payment = get_pending_payment(
        message.from_user.id
    )

    if not payment:
        await message.answer(
            "❌ Sizda kutilayotgan VIP to‘lov yo‘q."
        )
        return

    payment_id = payment[0]
    package = payment[1]
    days = payment[2]
    amount = payment[3]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data=f"approve_{payment_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Rad etish",
                    callback_data=f"reject_{payment_id}"
                )
            ],
        ]
    )

    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=(
            "💳 <b>YANGI VIP TO‘LOV</b>\n\n"
            f"🆔 To‘lov: #{payment_id}\n"
            f"👤 User: <code>{message.from_user.id}</code>\n"
            f"📦 Paket: {package}\n"
            f"💰 Summa: {amount:,} so‘m"
        ),
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await message.answer(
        "✅ Chek adminga yuborildi.\n"
        "⏳ To‘lov tekshirilmoqda."
    )


@dp.callback_query(F.data.startswith("approve_"))
async def approve_payment(
    callback: CallbackQuery,
    bot: Bot
):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Admin emassiz.",
            show_alert=True
        )
        return

    payment_id = int(
        callback.data.replace(
            "approve_",
            ""
        )
    )

    payment = get_payment(payment_id)

    if not payment:
        await callback.answer(
            "❌ To‘lov topilmadi.",
            show_alert=True
        )
        return

    user_id = payment[1]
    days = payment[3]

    add_vip_days(
        user_id,
        days
    )

    set_payment_status(
        payment_id,
        "approved"
    )

    await bot.send_message(
        user_id,
        "🎉 <b>VIP FAOLLASHTIRILDI!</b>\n\n"
        f"📅 {days} kunlik VIP berildi.",
        parse_mode="HTML"
    )

    await callback.message.edit_caption(
        caption="✅ <b>TO‘LOV TASDIQLANDI</b>",
        parse_mode="HTML"
    )

    await callback.answer(
        "✅ VIP berildi."
    )


@dp.callback_query(F.data.startswith("reject_"))
async def reject_payment(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Admin emassiz.",
            show_alert=True
        )
        return

    payment_id = int(
        callback.data.replace(
            "reject_",
            ""
        )
    )

    payment = get_payment(payment_id)

    if not payment:
        await callback.answer(
            "❌ To‘lov topilmadi.",
            show_alert=True
        )
        return

    set_payment_status(
        payment_id,
        "rejected"
    )

    await callback.message.edit_caption(
        caption="❌ <b>TO‘LOV RAD ETILDI</b>",
        parse_mode="HTML"
    )

    await callback.answer(
        "❌ Rad etildi."
    )


@dp.message(Command("admin"))
async def admin_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer(
            "❌ Siz admin emassiz."
        )
        return

    await message.answer(
        "🛠 <b>ADMIN PANEL</b>\n\n"
        "👇 Tanlang:",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "admin_anime")
async def admin_anime(
    callback: CallbackQuery,
    state: FSMContext
):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Admin emassiz.",
            show_alert=True
        )
        return

    await state.set_state(
        AddAnime.code
    )

    await callback.message.answer(
        "➕ Anime kodini yuboring:"
    )

    await callback.answer()


@dp.message(AddAnime.code)
async def anime_code(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        code=message.text.strip()
    )

    await state.set_state(
        AddAnime.title
    )

    await message.answer(
        "🎬 Anime nomini yuboring:"
    )


@dp.message(AddAnime.title)
async def anime_title(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        title=message.text.strip()
    )

    await state.set_state(
        AddAnime.description
    )

    await message.answer(
        "📝 Tavsif yuboring.\n"
        "Kerak bo‘lmasa - yuboring."
    )


@dp.message(AddAnime.description)
async def anime_description(
    message: Message,
    state: FSMContext
):
    description = message.text.strip()

    if description == "-":
        description = ""

    await state.update_data(
        description=description
    )

    await state.set_state(
        AddAnime.genre
    )

    await message.answer(
        "🎭 Janrini yuboring:"
    )


@dp.message(AddAnime.genre)
async def anime_genre(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        genre=message.text.strip()
    )

    await state.set_state(
        AddAnime.poster
    )

    await message.answer(
        "🖼 Poster rasmini yuboring."
    )


@dp.message(AddAnime.poster, F.photo)
async def anime_poster(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        poster=message.photo[-1].file_id
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🆓 Bepul",
                    callback_data="free_anime"
                ),
                InlineKeyboardButton(
                    text="👑 VIP",
                    callback_data="vip_anime"
                ),
            ]
        ]
    )

    await state.set_state(
        AddAnime.vip
    )

    await message.answer(
        "Anime turini tanlang:",
        reply_markup=keyboard
    )


@dp.callback_query(
    F.data.in_(
        {"free_anime", "vip_anime"}
    )
)
async def save_anime(
    callback: CallbackQuery,
    state: FSMContext
):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Admin emassiz.",
            show_alert=True
        )
        return

    data = await state.get_data()

    vip = 1 if callback.data == "vip_anime" else 0

    add_anime(
        data["code"],
        data["title"],
        data["description"],
        data["genre"],
        data["poster"],
        vip
    )

    await callback.message.answer(
        "✅ <b>ANIME QO‘SHILDI!</b>\n\n"
        f"🎬 {data['title']}\n"
        f"🔢 Kod: <code>{data['code']}</code>\n"
        f"👑 VIP: {'Ha' if vip else 'Yo‘q'}",
        parse_mode="HTML"
    )

    await state.clear()
    await callback.answer()


@dp.callback_query(F.data == "admin_episode")
async def admin_episode(
    callback: CallbackQuery,
    state: FSMContext
):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer(
            "❌ Admin emassiz.",
            show_alert=True
        )
        return

    await state.set_state(
        AddEpisode.code
    )

    await callback.message.answer(
        "🎥 Anime kodini yuboring:"
    )

    await callback.answer()


@dp.message(AddEpisode.code)
async def episode_code(
    message: Message,
    state: FSMContext
):
    anime = get_anime(
        message.text.strip()
    )

    if not anime:
        await message.answer(
            "❌ Anime topilmadi."
        )
        return

    await state.update_data(
        anime_id=anime[0],
        title=anime[2]
    )

    await state.set_state(
        AddEpisode.episode
    )

    await message.answer(
        f"🎬 {anime[2]}\n\n"
        "📺 Qism raqamini yuboring:"
    )


@dp.message(AddEpisode.episode)
async def episode_number(
    message: Message,
    state: FSMContext
):
    try:
        number = int(
            message.text.strip()
        )
    except ValueError:
        await message.answer(
            "❌ Faqat raqam yuboring. Masalan: 1"
        )
        return

    await state.update_data(
        episode=number
    )

    await state.set_state(
        AddEpisode.video
    )

    await message.answer(
        "🎥 Endi videoni yuboring."
    )


@dp.message(AddEpisode.video, F.video)
async def episode_video(
    message: Message,
    state: FSMContext
):
    data = await state.get_data()

    add_episode(
        data["anime_id"],
        data["episode"],
        message.video.file_id
    )

    await message.answer(
        "✅ <b>VIDEO QO‘SHILDI!</b>\n\n"
        f"🎬 {data['title']}\n"
        f"📺 {data['episode']}-qism",
        parse_mode="HTML"
    )

    await state.clear()


@dp.callback_query(F.data.startswith("ep_"))
async def send_episode(callback: CallbackQuery):
    parts = callback.data.split("_")

    if len(parts) != 3:
        await callback.answer(
            "❌ Xato.",
            show_alert=True
        )
        return

    anime_id = int(parts[1])
    episode = int(parts[2])

    from db import connect

    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT code,title,description,genre,poster,is_vip FROM anime WHERE id=?",
        (anime_id,)
    )

    anime = cur.fetchone()

    con.close()

    if not anime:
        await callback.answer(
            "❌ Anime topilmadi.",
            show_alert=True
        )
        return

    if anime[5] and not is_vip(
        callback.from_user.id
    ):
        await callback.answer(
            "👑 Bu VIP anime.",
            show_alert=True
        )
        return

    video = get_episode(
        anime_id,
        episode
    )

    if not video:
        await callback.answer(
            "❌ Video topilmadi.",
            show_alert=True
        )
        return

    file_id = video[2]

    await callback.message.answer_video(
        video=file_id,
        caption=(
            f"🎬 <b>{anime[1]}</b>\n"
            f"📺 {episode}-qism"
        ),
        parse_mode="HTML"
    )

    save_history(
        callback.from_user.id,
        anime_id,
        episode
    )

    add_xp(
        callback.from_user.id,
        5
    )

    await callback.answer(
        "▶️ Yuborildi!"
    )


@dp.message()
async def search_anime(message: Message):
    if not message.text:
        return

    if message.text.startswith("/"):
        return

    code = message.text.strip()

    anime = get_anime(code)

    if not anime:
        await message.answer(
            "❌ Anime topilmadi.\n\n"
            "🔎 Kodni tekshirib qayta yuboring."
        )
        return

    anime_id = anime[0]
    title = anime[2]
    description = anime[3]
    genre = anime[4]
    poster = anime[5]
    vip = anime[6]

    if vip and not is_vip(
        message.from_user.id
    ):
        await message.answer(
            "👑 <b>VIP ANIME</b>\n\n"
            f"🎬 {title}\n\n"
            "Bu anime faqat VIP foydalanuvchilar uchun.",
            reply_markup=vip_menu(),
            parse_mode="HTML"
        )
        return

    from db import connect

    con = connect()
    cur = con.cursor()

    cur.execute(
        "SELECT episode,file_id FROM episodes WHERE anime_id=? ORDER BY episode",
        (anime_id,)
    )

    episodes = cur.fetchall()

    con.close()

    if not episodes:
        await message.answer(
            "🎬 Anime topildi, lekin qismlari hali qo‘shilmagan."
        )
        return

    buttons = []

    for ep in episodes:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"▶️ {ep[0]}-qism",
                    callback_data=f"ep_{anime_id}_{ep[0]}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="🏠 Bosh menyu",
                callback_data="home"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    text = (
        f"🎬 <b>{title}</b>\n\n"
        f"📝 {description}\n\n"
        f"🎭 {genre}\n\n"
        "📺 <b>QISMLAR:</b>"
    )

    if poster:
        try:
            await message.answer_photo(
                poster,
                caption=text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except Exception:
            await message.answer(
                text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
    else:
        await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )


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
