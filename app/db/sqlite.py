import os
import aiosqlite


SCHEMA = """
CREATE TABLE IF NOT EXISTS appeals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    user_full_name TEXT,
    username TEXT,
    language_code TEXT,
    text TEXT NOT NULL,
    created_at TEXT NOT NULL,

    answered INTEGER NOT NULL DEFAULT 0,
    answered_at TEXT,
    admin_id INTEGER,
    answer_text TEXT
);
"""


async def init_db(db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    async with aiosqlite.connect(db_path) as db:
        await db.execute(SCHEMA)
        await db.commit()


def connect(db_path: str) -> aiosqlite.Connection:
    # В aiogram-хендлерах открываем соединение по месту (простая модель).
    # Для высокой нагрузки можно заменить на пул/единственный коннект в app-контексте.
    return aiosqlite.connect(db_path)