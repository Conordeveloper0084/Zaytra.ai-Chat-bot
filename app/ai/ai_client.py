import os
import asyncio
from openai import OpenAI

# OpenAI API kalitini o‘qiymiz
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY .env faylda topilmadi!")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Siz Zaytra AI nomli biznes va SMM bo‘yicha professional ekspert chatbotisiz. "
    "Siz foydalanuvchi savollariga o‘zbek tilida, aniqlik bilan, marketing strategiyasi, "
    "smm, kontent rejasi, o‘sish taktikasi, mijozlarni jalb qilish, brend boshqaruvi "
    "va biznes rivojlantirish bo‘yicha haqiqiy va foydali maslahatlar berasiz. "
    "Foydalanuvchi savoli mavzudan chetga chiqmasa, maksimal amaliy javob bering."
)


def _generate_ai_response_sync(user_text: str) -> str:
    """OpenAI blocking so‘rov — Thread ichida ishlatiladi"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
        max_tokens=500,
        temperature=0.75,
    )
    
    return response.choices[0].message.content.strip()


async def generate_ai_response(user_text: str) -> str:
    """Async wrapper — aiogramda ishlashi uchun"""
    return await asyncio.to_thread(_generate_ai_response_sync, user_text)