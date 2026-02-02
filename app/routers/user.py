from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.filters.is_admin import IsAdmin
from app.db.sqlite import connect
from app.db.repositories.appeals import AppealsRepo
from app.keyboards.inline import admin_reply_kb
from app.utils.formatters import format_admin_appeal, format_user_ack


user_router = Router()


@user_router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "<b>Тебя приветствует команда Черной занятости!</b>\n"
        "Напиши анонимное обращение одним сообщением\n"
    )


@user_router.message(F.text, ~IsAdmin())
async def handle_appeal(message: Message, settings):
    text = message.text.strip()
    if not text:
        return

    async with connect(settings.DB_PATH) as db:
        repo = AppealsRepo(db)

        appeal_id = await repo.create(
            user_id=message.from_user.id,
            user_full_name=message.from_user.full_name,
            username=message.from_user.username,
            language_code=message.from_user.language_code,
            text=text,
        )

    await message.answer(format_user_ack())

    admin_text = format_admin_appeal(
        appeal_id=appeal_id,
        user_id=message.from_user.id,
        full_name=message.from_user.full_name,
        username=message.from_user.username,
        language=message.from_user.language_code,
        text=text,
    )

    for admin_id in settings.admin_ids:
        try:
            await message.bot.send_message(
                chat_id=admin_id,
                text=admin_text,
                reply_markup=admin_reply_kb(appeal_id),
            )
        except Exception:
            print(f"Failed to send message to admin {admin_id}")