from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def users_page_keyboard(page: int, total_pages: int) -> InlineKeyboardMarkup:
    kb = []

    nav_row = []

    if page > 0:
        nav_row.append(
            InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data=f"admin_users_page:{page-1}"
            )
        )
    if page < total_pages - 1:
        nav_row.append(
            InlineKeyboardButton(
                text="Keyingi ➡️",
                callback_data=f"admin_users_page:{page+1}"
            )
        )

    if nav_row:
        kb.append(nav_row)

    kb.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_users")])

    return InlineKeyboardMarkup(inline_keyboard=kb)