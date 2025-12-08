from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

import logging

async def is_user_subscribed(bot: Bot, user_id: int, channel_username: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        logging.info(f"Subscription check: {user_id} → {member.status}")
        return member.status in ("creator", "administrator", "member", "restricted")
    except Exception as e:
        logging.error(f"Subscription check failed: {e}")
        return False

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