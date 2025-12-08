from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot import bot, CHANNEL_USERNAME
from app.ai.ai_client import generate_ai_response
from app.db.users_db import user_exists
from app.utils.subscription_check import is_user_subscribed
from app.keyboards.subscription import subscription_keyboard

chat_router = Router()


@chat_router.message()
async def chat_handler(message: Message, state: FSMContext):

    user_id = message.from_user.id
    text = message.text

    # Agar user biror state ichida bo'lsa → start handleriga qoldiramiz
    if await state.get_state() is not None:
        return

    # Kanal obunasi tekshirish
    subscribed = await is_user_subscribed(bot, user_id, CHANNEL_USERNAME)
    if not subscribed:
        await message.answer(
            "📌 Botdan foydalanish uchun avval kanalga obuna bo‘ling!",
            reply_markup=subscription_keyboard()
        )
        return

    # Ro‘yxatdan o‘tmagan bo‘lsa — registratsiya jarayoniga yo‘naltiramiz
    if not user_exists(user_id):
        await message.answer(
            "Ro‘yxatdan o‘tmagansiz ❗️\n"
            "Iltimos, /start buyrug‘ini yuboring."
        )
        return

    # AI ga so‘rov
    await message.chat.do("typing")

    try:
        response = await generate_ai_response(text)
        await message.answer(response)

    except Exception:
        await message.answer("⚠️ Javob generatsiyada xatolik. Qayta urinib ko‘ring.")