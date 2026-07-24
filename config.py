import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
BOT_PREFIX = os.environ.get("BOT_PREFIX", "$")
DEV_GUILD_ID = os.environ.get("DEV_GUILD_ID")
DB_PATH = os.environ.get("DB_PATH", "data/bariola.db")

if not BOT_TOKEN:
    raise RuntimeError(
        "DISCORD_BOT_TOKEN is not set — copy .env.example to .env and fill it in."
    )
