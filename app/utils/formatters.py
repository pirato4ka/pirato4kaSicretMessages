from app.db.repositories.appeals import Appeal


def format_admin_appeal(appeal_id: int, user_id: int, full_name: str | None, username: str | None, language: str | None, text: str) -> str:
    uname = f"@{username}" if username else "—"
    name = full_name or "—"
    lang = language or "—"
    return (
        f"<b>Новое обращение</b>\n"
        f"<b>ID:</b> <code>{appeal_id}</code>\n\n"
        f"<b>Пользователь:</b>\n"
        f"• <b>ID:</b> <code>{user_id}</code>\n"
        f"• <b>Имя:</b> {name}\n"
        f"• <b>Username:</b> {uname}\n"
        f"• <b>Язык:</b> {lang}\n\n"
        f"<b>Текст обращения:</b>\n"
        f"{text}"
    )


def format_user_ack() -> str:
    return (
        "<b>Ваше обращение отправлено!</b>\n"
        "Мы ответим вам в ближайшее время"
    )


def format_user_answer(answer_text: str) -> str:
    return (
        "<b>Ответ команды Черной занятости:</b>\n"
        f"{answer_text}"
    )