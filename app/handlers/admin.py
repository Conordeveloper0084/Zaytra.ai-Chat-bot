from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot import bot
from app.db.users_db import get_total_users, get_users_paginated
from app.db.admins_db import (
    is_admin,
    get_admins,
    add_admin,
    remove_admin
)
from app.keyboards.admin_reply import (
    admin_main_kb,
    admin_users_kb,
    admin_manage_kb
)
from app.states.admin_states import AdminState, BroadcastState

admin_router = Router()

USERS_PER_PAGE = 20


# =================== ADMIN PANEL =================== #

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    user_id = message.from_user.id
    admins = get_admins()

    if not admins:
        add_admin(user_id, message.from_user.username or "")
        await message.answer(
            "Siz birinchi admin sifatida qo‘shildingiz 👑",
            reply_markup=admin_main_kb()
        )
        return

    if not is_admin(user_id):
        return await message.answer("⛔ Siz admin emassiz!")

    await state.clear()
    await message.answer(
        "👑 Admin panelga xush kelibsiz!",
        reply_markup=admin_main_kb()
    )


# 📌 Chiqish
@admin_router.message(F.text == "❌ Chiqish")
async def exit_admin(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Admin rejimdan chiqdingiz 👌", reply_markup=None)


# ============== USERS MANAGEMENT ============== #

@admin_router.message(F.text == "👤 Userlar")
async def users_main(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")
    
    await message.answer(
        "📊 Userlar bo‘limi:",
        reply_markup=admin_users_kb()
    )


@admin_router.message(F.text == "👥 Userlar soni")
async def users_count(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")

    count = get_total_users()
    await message.answer(f"👥 Jami userlar: {count}")


# 📋 Ro‘yxat (1-sahifa)
@admin_router.message(F.text == "📋 Ro‘yxat")
async def users_list(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")

    users = get_users_paginated(0, USERS_PER_PAGE)

    if not users:
        return await message.answer("Hali user yo‘q.")

    text = "📋 Userlar (1-sahifa):\n\n"
    for i, u in enumerate(users, start=1):
        username = u.get("username") or "not provided"
        text += (
            f"{i}. {u.get('full_name')}\n"
            f"ID: {u.get('telegram_id')}\n"
            f"Telefon: {u.get('phone')}\n"
            f"Username: {username}\n\n"
        )

    await message.answer(text)


# ============== BROADCAST ============== #

@admin_router.message(F.text == "📢 Broadcast")
async def broadcast_init(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")

    await state.set_state(BroadcastState.waiting_for_broadcast_text)
    await message.answer("🔊 E'lon matnini yuboring:")


@admin_router.message(BroadcastState.waiting_for_broadcast_text)
async def broadcast_send(message: Message, state: FSMContext):
    admin_id = message.from_user.id
    if not is_admin(admin_id):
        await state.clear()
        return await message.answer("⛔ Ruxsat yo‘q!")

    text = message.text
    users = get_users_paginated(0, 10**9)

    success = 0
    fail = 0

    await message.answer("📡 E'lon yuborilmoqda...")

    for u in users:
        try:
            await bot.send_message(u["telegram_id"], text)
            success += 1
        except:
            fail += 1

    await message.answer(
        f"📢 E'lon yakunlandi!\n"
        f"✔ Yuborildi: {success}\n"
        f"❌ Xato: {fail}"
    )
    await state.clear()


# ============== ADMIN MANAGEMENT ============== #

@admin_router.message(F.text == "🔧 Admin boshqaruvi")
async def manage_admin(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")

    await message.answer(
        "🔧 Admin boshqaruvi:",
        reply_markup=admin_manage_kb()
    )


@admin_router.message(F.text == "📋 Adminlar ro‘yxati")
async def list_admins(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")

    admins = get_admins()
    if not admins:
        return await message.answer("Hali admin yo‘q.")

    text = "📋 Adminlar:\n\n"
    for i, a in enumerate(admins, start=1):
        username = a.get("username") or "-"
        text += f"{i}. ID: {a['telegram_id']} | @{username}\n"

    await message.answer(text)


# ➕ Qo‘shish
@admin_router.message(F.text == "➕ Admin qo‘shish")
async def admin_add_ask_id(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")

    await state.set_state(AdminState.waiting_for_new_admin_id)
    await message.answer("🆕 Admin Telegram ID sini yuboring:")


@admin_router.message(AdminState.waiting_for_new_admin_id)
async def admin_add_id(message: Message, state: FSMContext):
    try:
        admin_id = int(message.text)
    except:
        return await message.answer("❌ ID faqat raqam bo‘lishi kerak!")

    await state.update_data(admin_id=admin_id)
    await state.set_state(AdminState.waiting_for_new_admin_username)
    await message.answer("👤 Username yuboring (yoki '-' yozing):")


@admin_router.message(AdminState.waiting_for_new_admin_username)
async def admin_add_username(message: Message, state: FSMContext):
    data = await state.get_data()
    admin_id = data.get("admin_id")
    username = message.text.replace("@", "").strip()
    
    if username == "-":
        username = ""

    add_admin(admin_id, username)

    await state.clear()
    await message.answer(f"✔ Admin qo‘shildi!\nID: {admin_id} | @{username or '-'}")


# ➖ O‘chirish
@admin_router.message(F.text == "➖ Admin olib tashlash")
async def admin_remove_init(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")

    await state.set_state(AdminState.waiting_for_remove_admin_id)
    await message.answer("❌ O‘chirmoqchi bo‘lgan admin ID sini yozing:")


@admin_router.message(AdminState.waiting_for_remove_admin_id)
async def admin_remove_do(message: Message, state: FSMContext):
    try:
        admin_id = int(message.text)
    except:
        return await message.answer("❌ ID faqat raqamlardan iborat bo‘ladi!")

    removed = remove_admin(admin_id)
    await state.clear()

    if removed:
        return await message.answer("🗑 Admin o‘chirildi!")
    return await message.answer("❌ Admin topilmadi!")


# Global BACK button
@admin_router.message(F.text == "⬅️ Orqaga")
async def admin_back(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q!")

    await message.answer("⬅️ Asosiy menyu", reply_markup=admin_main_kb())