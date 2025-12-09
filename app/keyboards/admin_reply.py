from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_main_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Userlar")],
            [KeyboardButton(text="📢 Broadcast")],
            [KeyboardButton(text="🔧 Admin boshqaruvi")],
            [KeyboardButton(text="❌ Chiqish")],
        ],
        resize_keyboard=True
    )


def admin_users_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👥 Userlar soni")],
            [KeyboardButton(text="📋 Ro‘yxat")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True
    )


def admin_manage_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Admin qo‘shish")],
            [KeyboardButton(text="➖ Admin olib tashlash")],
            [KeyboardButton(text="📋 Adminlar ro‘yxati")],
            [KeyboardButton(text="⬅️ Orqaga")],
        ],
        resize_keyboard=True
    )