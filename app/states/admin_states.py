from aiogram.fsm.state import StatesGroup, State

class AdminState(StatesGroup):
    waiting_for_new_admin_id = State()
    waiting_for_new_admin_username = State()
    waiting_for_remove_admin_id = State()

class BroadcastState(StatesGroup):
    waiting_for_broadcast_text = State()