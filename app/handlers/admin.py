from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.bot import bot
from app.db.users_db import get_total_users, get_users_paginated
from app.db.admins_db import (
    is_admin,
    get_admins,
    add_admin,
    remove_admin
)
from app.keyboards.admin_menu import (
    admin_main_keyboard,
    admin_users_keyboard,
    admin_manage_keyboard,
)
from app.keyboards.pagination import users_page_keyboard
from app.states.admin_states import AdminState, BroadcastState

admin_router = Router()

USERS_PER_PAGE = 20


# =================== ADMIN PANEL =================== #

@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    user_id = message.from_user.id

    admins = get_admins()

    # Agar hali admin yo'q bo'lsa – birinchi /admin yozgan userni admin qilamiz
    if not admins:
        add_admin(user_id, message.from_user.username or "")
        await message.answer(
            "Siz birinchi admin sifatida qo'shildingiz ✅\n"
            "Endi admin paneldan foydalanishingiz mumkin.",
            reply_markup=admin_main_keyboard()
        )
        return

    if not is_admin(user_id):
        await message.answer("⛔ Siz admin emassiz!")
        return

    await message.answer(
        "👑 Admin panelga xush kelibsiz!",
        reply_markup=admin_main_keyboard()
    )

# ============== BACK TO MAIN MENU ============== #

@admin_router.callback_query(F.data == "admin_back")
async def back_admin_menu(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    await callback.message.edit_text(
        "👑 Admin panel",
        reply_markup=admin_main_keyboard()
    )
    await callback.answer()


# ============== USERS MANAGEMENT ============== #

@admin_router.callback_query(F.data == "admin_users")
async def users_main(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    await callback.message.edit_text(
        "📊 Userlar bo‘limi:",
        reply_markup=admin_users_keyboard()
    )
    await callback.answer()


@admin_router.callback_query(F.data == "admin_users_count")
async def users_count(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    count = get_total_users()
    await callback.message.answer(f"👥 Jami userlar: <b>{count}</b>")
    await callback.answer()


@admin_router.callback_query(F.data.startswith("admin_users_page:"))
async def users_page(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    _, page_str = callback.data.split(":")
    page = int(page_str)

    total = get_total_users()
    total_pages = (total + USERS_PER_PAGE - 1) // USERS_PER_PAGE

    users = get_users_paginated(page * USERS_PER_PAGE, USERS_PER_PAGE)

    if not users:
        return await callback.message.edit_text("Hali user yo‘q.")

    text = f"📋 Userlar ({page+1}/{total_pages}):\n\n"

    for index, user in enumerate(users, start=1):
        text += (
            f"{page*USERS_PER_PAGE + index}. <b>{user['full_name']}</b>\n"
            f"ID: <code>{user['telegram_id']}</code>\n"
            f"Tel: <code>{user['phone']}</code>\n"
            f"Link: <a href='tg://user?id={user['telegram_id']}'>Profil</a>\n\n"
        )

    await callback.message.edit_text(
        text,
        reply_markup=users_page_keyboard(page, total_pages),
        disable_web_page_preview=True
    )
    await callback.answer()


# ============== BROADCAST ============== #

@admin_router.callback_query(F.data == "admin_broadcast")
async def broadcast_init(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    await state.set_state(BroadcastState.waiting_for_broadcast_text)
    await callback.message.answer(
        "🔊 Broadcast tekstini yuboring.\n"
        "(HTML format: <b>Qalin</b>, linklar va h.k.)"
    )
    await callback.answer()


@admin_router.message(BroadcastState.waiting_for_broadcast_text)
async def broadcast_send(message: Message, state: FSMContext):
    admin_id = message.from_user.id

    if not is_admin(admin_id):
        await state.clear()
        return await message.answer("⛔ Ruxsat yo‘q!")

    text = message.html_text
    users = get_users_paginated(0, 10**9)  # barcha userlar

    success, fail = 0, 0

    await message.answer("📡 E'lon yuborilmoqda...")

    for u in users:
        try:
            await bot.send_message(u["telegram_id"], text)
            success += 1
        except:
            fail += 1

    await message.answer(
        f"📢 Broadcast yakunlandi!\n"
        f"✔ Yuborildi: {success}\n"
        f"❌ Xato: {fail}"
    )
    await state.clear()


# ============== ADMIN MANAGEMENT ============== #

@admin_router.callback_query(F.data == "admin_manage")
async def manage_admin(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    await callback.message.edit_text(
        "🔧 Admin boshqaruvi:",
        reply_markup=admin_manage_keyboard()
    )
    await callback.answer()


@admin_router.callback_query(F.data == "admin_list")
async def list_admins(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    admins = get_admins()

    if not admins:
        return await callback.message.answer("Hali admin yo‘q.")

    text = "📋 Adminlar:\n\n"
    for i, a in enumerate(admins, start=1):
        text += f"{i}. ID: <code>{a['telegram_id']}</code> | @{a.get('username', '-')}\n"

    await callback.message.answer(text)
    await callback.answer()


@admin_router.callback_query(F.data == "admin_add")
async def admin_add_init(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    await callback.message.answer("🆕 Admin Telegram ID sini yuboring:")
    await state.set_state(AdminState.waiting_for_new_admin_id)
    await callback.answer()


@admin_router.message(AdminState.waiting_for_new_admin_id)
async def admin_add_id(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await state.clear()
        return await message.answer("⛔ Ruxsat yo‘q!")

    try:
        admin_id = int(message.text)
    except:
        return await message.answer("❌ ID faqat raqamlardan iborat bo‘lishi kerak!")

    await state.update_data(admin_id=admin_id)
    await state.set_state(AdminState.waiting_for_new_admin_username)
    await message.answer("👤 Username yuboring (yoki '-' yozing):")


@admin_router.message(AdminState.waiting_for_new_admin_username)
async def admin_add_username(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await state.clear()
        return await message.answer("⛔ Ruxsat yo‘q!")

    data = await state.get_data()
    admin_id = data.get("admin_id")
    username = message.text.strip()

    if username.startswith("@"):
        username = username[1:]
    if username == "-":
        username = ""

    add_admin(admin_id, username)

    await state.clear()
    await message.answer(
        f"✔ Admin qo‘shildi!\n"
        f"ID: <code>{admin_id}</code>\n"
        f"Username: @{username or '-'}"
    )


@admin_router.callback_query(F.data == "admin_remove")
async def admin_remove_init(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return await callback.answer("⛔ Ruxsat yo‘q!", show_alert=True)

    await state.set_state(AdminState.waiting_for_remove_admin_id)
    await callback.message.answer("❌ O‘chirmoqchi bo‘lgan adminning ID sini yuboring:")
    await callback.answer()


@admin_router.message(AdminState.waiting_for_remove_admin_id)
async def admin_remove_do(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await state.clear()
        return await message.answer("⛔ Ruxsat yo‘q!")

    try:
        admin_id = int(message.text)
    except:
        return await message.answer("❌ ID faqat raqam bo‘lishi kerak!")

    removed = remove_admin(admin_id)
    await state.clear()

    if removed:
        await message.answer("🗑 Admin o‘chirildi!")
    else:
        await message.answer("❌ Admin topilmadi!")