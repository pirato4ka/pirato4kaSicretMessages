from aiogram.fsm.state import State, StatesGroup


class AdminReplyState(StatesGroup):
    waiting_reply_text = State()