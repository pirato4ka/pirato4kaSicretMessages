from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from app.filters.is_admin import IsAdmin
from app.states.admin_reply import AdminReplyState
from app.db.sqlite import connect
from app.db.repositories.appeals import AppealsRepo
from app.utils.formatters import format_user_answer


admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


@admin_router.callback_query(F.data.startswith("reply:"))
async def admin_reply_callback(callback: CallbackQuery, state: FSMContext):
    appeal_id = int(callback.data.split(":")[1])
    await state.update_data(appeal_id=appeal_id)
    await state.set_state(AdminReplyState.waiting_reply_text)

    await callback.message.answer(
        f"Введи ответ для обращения ID {appeal_id}.\n"
        "Отмена: /cancel"
    )
    await callback.answer()


@admin_router.message(Command("cancel"))
async def admin_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Операция отменена.")


@admin_router.message(AdminReplyState.waiting_reply_text, F.text)
async def admin_send_reply(message: Message, state: FSMContext, settings):
    data = await state.get_data()
    appeal_id = data.get("appeal_id")
    if not appeal_id:
        await state.clear()
        await message.answer("Не найден ID обращения. Начни заново.")
        return

    answer_text = message.text.strip()
    if not answer_text:
        await message.answer("Пустой ответ. Введи текст или /cancel")
        return

    async with connect(settings.DB_PATH) as db:
        repo = AppealsRepo(db)
        appeal = await repo.get(int(appeal_id))
        if not appeal:
            await state.clear()
            await message.answer("Обращение не найдено.")
            return

        await repo.mark_answered(
            appeal_id=int(appeal_id),
            admin_id=message.from_user.id,
            answer_text=answer_text,
        )

    # Отправляем ответ пользователю
    await message.bot.send_message(
        chat_id=appeal.user_id,
        text=format_user_answer(answer_text),
    )

    await message.answer(f"Ответ отправлен пользователю (обращение ID {appeal_id}).")
    await state.clear()