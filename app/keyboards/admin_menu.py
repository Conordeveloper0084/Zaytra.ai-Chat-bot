from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_main_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="👤 Userlar",
                callback_data="admin_users"
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 Broadcast",
                callback_data="admin_broadcast"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔧 Admin boshqaruvi",
                callback_data="admin_manage"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def admin_users_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="👥 Userlar soni",
                callback_data="admin_users_count"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Userlar ro‘yxati",
                callback_data="admin_users_page:0"
            )
        ],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def admin_manage_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="➕ Admin qo‘shish",
                callback_data="admin_add"
            )
        ],
        [
            InlineKeyboardButton(
                text="➖ Admin olib tashlash",
                callback_data="admin_remove"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Adminlar ro‘yxati",
                callback_data="admin_list"
            )
        ],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)