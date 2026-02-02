from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import aiosqlite


@dataclass
class Appeal:
    id: int
    user_id: int
    user_full_name: str | None
    username: str | None
    language_code: str | None
    text: str
    created_at: str
    answered: int
    answered_at: str | None
    admin_id: int | None
    answer_text: str | None


class AppealsRepo:
    def __init__(self, db: aiosqlite.Connection):
        self.db = db

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    async def create(
        self,
        user_id: int,
        user_full_name: str | None,
        username: str | None,
        language_code: str | None,
        text: str,
    ) -> int:
        created_at = self._now_iso()
        cursor = await self.db.execute(
            """
            INSERT INTO appeals (user_id, user_full_name, username, language_code, text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, user_full_name, username, language_code, text, created_at),
        )
        await self.db.commit()
        return int(cursor.lastrowid)

    async def get(self, appeal_id: int) -> Appeal | None:
        cursor = await self.db.execute(
            "SELECT id, user_id, user_full_name, username, language_code, text, created_at, "
            "answered, answered_at, admin_id, answer_text "
            "FROM appeals WHERE id = ?",
            (appeal_id,),
        )
        row = await cursor.fetchone()
        if not row:
            return None
        return Appeal(*row)

    async def mark_answered(self, appeal_id: int, admin_id: int, answer_text: str) -> None:
        answered_at = self._now_iso()
        await self.db.execute(
            """
            UPDATE appeals
            SET answered = 1, answered_at = ?, admin_id = ?, answer_text = ?
            WHERE id = ?
            """,
            (answered_at, admin_id, answer_text, appeal_id),
        )
        await self.db.commit()