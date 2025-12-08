import json
from pathlib import Path

# JSON fayl manzili
DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"


def ensure_users_file():
    """Agar users.json mavjud bo'lmasa – yaratadi"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not USERS_FILE.exists():
        USERS_FILE.write_text(json.dumps({"users": []}, ensure_ascii=False, indent=2))


def load_users():
    """Hamma userlarni JSON fayldan o‘qib beradi"""
    ensure_users_file()
    try:
        data = json.loads(USERS_FILE.read_text(encoding="utf-8"))
        return data.get("users", [])
    except Exception:
        return []


def save_users(users):
    """Userlar ro‘yxatini JSON faylga saqlaydi"""
    ensure_users_file()
    USERS_FILE.write_text(json.dumps({"users": users}, ensure_ascii=False, indent=2))


def user_exists(telegram_id: int) -> bool:
    """User ro‘yxatdan o‘tganmi yoki yo‘q"""
    users = load_users()
    return any(u.get("telegram_id") == telegram_id for u in users)


def register_or_update_user(telegram_id: int, full_name: str, phone: str):
    """Yangi user qo‘shish yoki mavjudini yangilash"""
    users = load_users()

    for user in users:
        if user.get("telegram_id") == telegram_id:
            user["full_name"] = full_name
            user["phone"] = phone
            save_users(users)
            return

    users.append(
        {
            "telegram_id": telegram_id,
            "full_name": full_name,
            "phone": phone
        }
    )
    save_users(users)


def get_total_users() -> int:
    """Jami userlar soni"""
    return len(load_users())


def get_users_paginated(start: int, limit: int):
    """Userlar ro‘yxatini pagination bilan qaytarish"""
    users = load_users()
    return users[start:start + limit]