import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Lokal .env mavjud bo‘lsa yuklaydi (Railwayda esa ignore)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN env variables orqali topilmadi!")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY env variables orqali topilmadi!")

if not CHANNEL_USERNAME:
    raise ValueError("❌ CHANNEL_USERNAME env variables orqali topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()