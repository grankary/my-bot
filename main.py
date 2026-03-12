import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================== SOZLAMALAR ==================
TOKEN = "8794709341:AAGr6QoDr_WhyvG_mN_X1n_KXxIOsQZMxH4"
ADMIN_ID = 8167897562 # O'ZINGIZNING TELEGRAM ID

# ================== FATVO 2026 ==================
ZAKOT_NISOB = 100_000_000
ZAKOT_FOIZ = 0.025

FITR = {
    "Bug‘doy (2 kg)": 10_000,
    "Un (2 kg)": 12_000,
    "Arpa (4 kg)": 20_000,
    "Mayiz (2 kg)": 110_000,
    "Xurmo (4 kg)": 200_000,
}

FIDYA_BIR_KUN = 10_000

# ================== BOT ==================
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ================== STATES ==================
class StartState(StatesGroup):
    ism = State()

class ZakotState(StatesGroup):
    pul = State()
    savdo = State()
    oltin = State()
    kumush = State()
    qarz = State()

# ================== /START ==================
@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.answer("👋 Assalomu alaykum!\n\nIltimos, ismingizni kiriting:")
    await state.set_state(StartState.ism)

# ================== ISM QABUL QILISH ==================
@dp.message(StartState.ism)
async def ism_qabul(message: types.Message, state: FSMContext):
    ism = message.text.strip()
    user = message.from_user

    # Admin uchun xabar
    admin_text = (
        "🆕 YANGI FOYDALANUVCHI RO‘YXATDAN O‘TDI\n\n"
        f"📝 Ismi: {ism}\n"
        f"👤 Telegram: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'yo‘q'}\n"
        f"🆔 ID: {user.id}\n"
        f"🕒 Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        await bot.send_message(ADMIN_ID, admin_text)
    except:
        pass

    await state.clear()

    # Foydalanuvchiga menyu
    await message.answer(
        f"Xush kelibsiz, {ism} 😊\n\n"
        "🕌 Zakot • Fitr • Fidya bot\n\n"
        "Quyidagi buyruqlardan birini tanlang:\n\n"
        "/zakot – Zakot hisoblash\n"
        "/fitr – Fitr sadaqa miqdorlari\n"
        "/fidya – Fidya miqdori\n\n"
        "📌 2026-yil Fatvo markazi qaroriga asosan"
    )

# ================== /ZAKOT ==================
@dp.message(Command("zakot"))
async def zakot_start(message: types.Message, state: FSMContext):
    # Inline tugma bilan YouTube video
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎥 Zakot Video",
            url="https://youtu.be/8IPeMN6IVEg?si=z-HaW_D4xmLV2UoS"
        )]
    ])
    await message.answer(
        "💡 Zakot nima ekanligini tushunmaganlar uchun video quyidagi tugmadan ko‘ring:",
        reply_markup=keyboard
    )

    # Zakot uchun pulni so‘rash
    await message.answer("💰 Naqd va kartadagi pulingizni so‘mda kiriting:")
    await state.set_state(ZakotState.pul)

@dp.message(ZakotState.pul)
async def zakot_pul(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Iltimos, faqat raqam kiriting.")
        return
    await state.update_data(pul=float(message.text))
    await message.answer("📦 Savdo mollaringiz qiymati (so‘mda):")
    await state.set_state(ZakotState.savdo)

@dp.message(ZakotState.savdo)
async def zakot_savdo(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Faqat raqam kiriting.")
        return
    await state.update_data(savdo=float(message.text))
    await message.answer("🪙 Oltiningiz qiymati (so‘mda, bo‘lmasa 0):")
    await state.set_state(ZakotState.oltin)

@dp.message(ZakotState.oltin)
async def zakot_oltin(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Faqat raqam kiriting.")
        return
    await state.update_data(oltin=float(message.text))
    await message.answer("🥈 Kumushingiz qiymati (so‘mda, bo‘lmasa 0):")
    await state.set_state(ZakotState.kumush)

@dp.message(ZakotState.kumush)
async def zakot_kumush(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Faqat raqam kiriting.")
        return
    await state.update_data(kumush=float(message.text))
    await message.answer("💳 Qarzingiz (so‘mda):")
    await state.set_state(ZakotState.qarz)

@dp.message(ZakotState.qarz)
async def zakot_hisob(message: types.Message, state: FSMContext):
    if not message.text.isdig
it():
        await message.answer("❌ Faqat raqam kiriting.")
        return

    data = await state.get_data()
    qarz = float(message.text)

    jami = (
        data["pul"]
        + data["savdo"]
        + data["oltin"]
        + data["kumush"]
        - qarz
    )

    if jami >= ZAKOT_NISOB:
        zakot = jami * ZAKOT_FOIZ
        await message.answer(
            f"🧮 ZAKOT HISOBI\n\n"
            f"Jami mol-mulk: {jami:,.0f} so‘m\n"
            f"Zakot (2.5%): {zakot:,.0f} so‘m\n\n"
            "📌 Sizga zakot BERISH FARZ."
        )
    else:
        await message.answer(
            f"📌 Jami mol-mulk: {jami:,.0f} so‘m\n\n"
            "Zakot FARZ EMAS."
        )

    await state.clear()

# ================== /FITR ==================
@dp.message(Command("fitr"))
async def fitr(message: types.Message):
    text = "🌙 FITR SADAQA MIQDORLARI (2026):\n\n"
    for nom, summa in FITR.items():
        text += f"• {nom} — {summa:,} so‘m\n"
    await message.answer(text)

# ================== /FIDYA ==================
@dp.message(Command("fidya"))
async def fidya(message: types.Message):
    await message.answer(
        "☕ FIDYA MIQDORI\n\n"
        f"1 kun uchun fidya: {FIDYA_BIR_KUN:,} so‘m"
    )

# ================== RUN ==================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())