from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class IsAdmin(BaseFilter):
    async def __call__(self, event: Message | CallbackQuery, settings) -> bool:
        user_id = event.from_user.id
        return user_id in settings.admin_ids