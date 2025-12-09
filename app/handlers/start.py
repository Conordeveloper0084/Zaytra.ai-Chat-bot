from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    CallbackQuery
)
from aiogram.fsm.context import FSMContext

from app.bot import bot, CHANNEL_USERNAME
from app.db.users_db import user_exists, register_or_update_user
from app.keyboards.subscription import subscription_keyboard
from app.utils.subscription_check import is_user_subscribed
from app.states.registration import Registration

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):

    user_id = message.from_user.id

    # Kanalga obuna tekshiramiz
    subscribed = await is_user_subscribed(bot, user_id, CHANNEL_USERNAME)
    
    if not subscribed:
        await message.answer(
            "👋 Assalomu alaykum!\n\n"
            "Zaytra AI chatbotidan foydalanish uchun avval iltimos "
            f"{CHANNEL_USERNAME} kanaliga obuna bo‘ling.",
            reply_markup=subscription_keyboard()
        )
        return

    # Agar allaqachon ro‘yxatdan o‘tgan bo‘lsa
    if user_exists(user_id):
        await message.answer(
            "Siz allaqachon ro‘yxatdan o‘tgansiz ✅\n"
            "Endi biznes yoki SMM bo‘yicha savolingizni yozishingiz mumkin 😊"
        )
        return

    # Ro‘yxatdan o‘tish boshlanadi
    await state.set_state(Registration.waiting_for_full_name)
    await message.answer("Iltimos, to‘liq ismingizni yuboring ✍️")


@start_router.callback_query(F.data == "check_subscription")
async def callback_check_sub(callback: CallbackQuery, state: FSMContext):

    user_id = callback.from_user.id
    subscribed = await is_user_subscribed(bot, user_id, CHANNEL_USERNAME)

    if not subscribed:
        await callback.answer("Hali obuna bo‘lmagansiz ❌", show_alert=True)
        return

    await callback.message.answer(
        "Obuna tasdiqlandi! 🎉\n"
        "Endi to‘liq ismingizni yuboring."
    )
    await state.set_state(Registration.waiting_for_full_name)
    await callback.answer()


@start_router.message(Registration.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext):

    full_name = message.text.strip()
    await state.update_data(full_name=full_name)

    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Kontakt yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await state.set_state(Registration.waiting_for_contact)
    await message.answer(
        "Rahmat! Endi kontaktingizni yuboring 👇",
        reply_markup=contact_keyboard
    )


@start_router.message(Registration.waiting_for_contact, F.contact)
async def process_contact(message: Message, state: FSMContext):

    data = await state.get_data()
    full_name = data.get("full_name")
    phone = message.contact.phone_number
    user_id = message.from_user.id
    username = message.from_user.username or ""

    register_or_update_user(user_id, full_name, phone, username)

    await state.clear()
    await message.answer(
        "🎯 Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi!\n"
        "Endi savolingizni yozishingiz mumkin 🔥",
        reply_markup=ReplyKeyboardRemove()
    )