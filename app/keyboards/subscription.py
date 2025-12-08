from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@Conordevs_Blogs")


def subscription_keyboard() -> InlineKeyboardMarkup:
    channel_link = f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
    kb = [
        [
            InlineKeyboardButton(
                text="📣 Kanalga obuna bo‘lish",
                url=channel_link
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Obunani tekshirish",
                callback_data="check_subscription"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)