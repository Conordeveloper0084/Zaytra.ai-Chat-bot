from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    waiting_for_full_name = State()
    waiting_for_contact = State()