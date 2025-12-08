import json
from pathlib import Path

# JSON fayl manzili
DATA_DIR = Path("data")
ADMINS_FILE = DATA_DIR / "admins.json"


def ensure_admins_file():
    """Agar admins.json mavjud bo'lmasa – yaratadi"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not ADMINS_FILE.exists():
        ADMINS_FILE.write_text(json.dumps({"admins": []}, ensure_ascii=False, indent=2))


def load_admins():
    """Adminlar ro‘yxatini o‘qish"""
    ensure_admins_file()
    try:
        data = json.loads(ADMINS_FILE.read_text(encoding="utf-8"))
        return data.get("admins", [])
    except Exception:
        return []


def save_admins(admins):
    """Adminlar ro‘yxatini JSON faylga saqlash"""
    ensure_admins_file()
    ADMINS_FILE.write_text(json.dumps({"admins": admins}, ensure_ascii=False, indent=2))


def is_admin(telegram_id: int) -> bool:
    """User adminmi yoki yo‘q"""
    admins = load_admins()
    return any(a.get("telegram_id") == telegram_id for a in admins)


def add_admin(telegram_id: int, username: str = None):
    """Yangi admin qo‘shish"""
    admins = load_admins()
    if not is_admin(telegram_id):
        admins.append({
            "telegram_id": telegram_id,
            "username": username or ""
        })
        save_admins(admins)


def remove_admin(telegram_id: int) -> bool:
    """Adminni olib tashlash"""
    admins = load_admins()
    updated = [a for a in admins if a.get("telegram_id") != telegram_id]

    if len(updated) != len(admins):
        save_admins(updated)
        return True
    
    return False


def get_admins():
    """Barcha adminlar ro‘yxati"""
    return load_admins()