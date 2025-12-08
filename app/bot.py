import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

# .env fayldan ma'lumotlarni yuklaymiz
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@Conordevs_Blogs")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN .env faylda topilmadi!")

# Bot obyektini yaratish
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

# Dispatcher — handlerlarni va eventlarni boshqaradi
dp = Dispatcher()