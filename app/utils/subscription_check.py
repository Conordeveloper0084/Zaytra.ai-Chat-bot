from aiogram import Bot

async def is_user_subscribed(bot: Bot, user_id: int, channel_username: str) -> bool:
    """
    User kanalga obuna bo‘lgan-bo‘lmaganini tekshiradi
    
    status bo‘lishi mumkin: creator, administrator, member, restricted
    left yoki kicked bo‘lsa → obuna emas
    """

    if not channel_username.startswith("@"):
        channel_username = "@" + channel_username

    try:
        member = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        return member.status in ("creator", "administrator", "member", "restricted")

    except Exception:
        # Kanal topilmasa yoki boshqa xatolik bo‘lsa ham → obuna emas
        return False