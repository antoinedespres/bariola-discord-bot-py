import os

import aiosqlite

import config

_connection: aiosqlite.Connection | None = None


async def init_db() -> None:
    global _connection

    db_dir = os.path.dirname(config.DB_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    _connection = await aiosqlite.connect(config.DB_PATH)
    await _connection.execute(
        """
        CREATE TABLE IF NOT EXISTS guild_settings (
            guild_id INTEGER PRIMARY KEY,
            language TEXT NOT NULL DEFAULT 'en'
        )
        """
    )
    await _connection.execute(
        """
        CREATE TABLE IF NOT EXISTS warnings (
            guild_id INTEGER NOT NULL,
            user_id  INTEGER NOT NULL,
            count    INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (guild_id, user_id)
        )
        """
    )
    await _connection.execute(
        """
        CREATE TABLE IF NOT EXISTS birthdays (
            guild_id INTEGER NOT NULL,
            user_id  INTEGER NOT NULL,
            day      INTEGER NOT NULL,
            month    INTEGER NOT NULL,
            PRIMARY KEY (guild_id, user_id)
        )
        """
    )
    await _connection.commit()


async def close_db() -> None:
    if _connection is not None:
        await _connection.close()


async def get_guild_language(guild_id: int | None) -> str:
    if guild_id is None:
        return "en"

    async with _connection.execute(
        "SELECT language FROM guild_settings WHERE guild_id = ?", (guild_id,)
    ) as cursor:
        row = await cursor.fetchone()

    return row[0] if row is not None else "en"


async def set_guild_language(guild_id: int, language: str) -> None:
    await _connection.execute(
        """
        INSERT INTO guild_settings (guild_id, language) VALUES (?, ?)
        ON CONFLICT (guild_id) DO UPDATE SET language = excluded.language
        """,
        (guild_id, language),
    )
    await _connection.commit()


async def get_warning_count(guild_id: int, user_id: int) -> int:
    async with _connection.execute(
        "SELECT count FROM warnings WHERE guild_id = ? AND user_id = ?",
        (guild_id, user_id),
    ) as cursor:
        row = await cursor.fetchone()

    return row[0] if row is not None else 0


async def increment_warning(guild_id: int, user_id: int) -> int:
    new_count = await get_warning_count(guild_id, user_id) + 1
    await _connection.execute(
        """
        INSERT INTO warnings (guild_id, user_id, count) VALUES (?, ?, ?)
        ON CONFLICT (guild_id, user_id) DO UPDATE SET count = excluded.count
        """,
        (guild_id, user_id, new_count),
    )
    await _connection.commit()
    return new_count


async def reset_warnings(guild_id: int, user_id: int) -> None:
    await _connection.execute(
        """
        INSERT INTO warnings (guild_id, user_id, count) VALUES (?, ?, 0)
        ON CONFLICT (guild_id, user_id) DO UPDATE SET count = 0
        """,
        (guild_id, user_id),
    )
    await _connection.commit()


async def set_birthday(guild_id: int, user_id: int, day: int, month: int) -> None:
    await _connection.execute(
        """
        INSERT INTO birthdays (guild_id, user_id, day, month) VALUES (?, ?, ?, ?)
        ON CONFLICT (guild_id, user_id) DO UPDATE SET day = excluded.day, month = excluded.month
        """,
        (guild_id, user_id, day, month),
    )
    await _connection.commit()


async def get_birthdays_on(day: int, month: int) -> list[tuple[int, int]]:
    async with _connection.execute(
        "SELECT guild_id, user_id FROM birthdays WHERE day = ? AND month = ?", (day, month)
    ) as cursor:
        return await cursor.fetchall()
