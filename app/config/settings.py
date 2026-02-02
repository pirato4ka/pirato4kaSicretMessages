from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_TOKEN: str
    ADMIN_IDS: str  # "1,2,3"
    DB_PATH: str = "data/bot.sqlite3"

    @property
    def admin_ids(self) -> List[int]:
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]