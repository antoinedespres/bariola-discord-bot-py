import json
import os

import db

_LOCALES_DIR = os.path.join(os.path.dirname(__file__), "locales")
_FALLBACK_LANGUAGE = "en"

_locales: dict[str, dict[str, str]] = {}

for _filename in os.listdir(_LOCALES_DIR):
    if _filename.endswith(".json"):
        _language = _filename.removesuffix(".json")
        with open(os.path.join(_LOCALES_DIR, _filename), encoding="utf-8") as f:
            _locales[_language] = json.load(f)


async def t(key: str, guild_id: int | None, **kwargs) -> str:
    language = await db.get_guild_language(guild_id)

    template = _locales.get(language, {}).get(key)
    if template is None:
        template = _locales[_FALLBACK_LANGUAGE].get(key)
    if template is None:
        raise KeyError(f"Missing i18n key {key!r} in every locale (including fallback).")

    return template.format(**kwargs)


async def t_ctx(ctx, key: str, **kwargs) -> str:
    guild_id = ctx.guild.id if ctx.guild is not None else None
    return await t(key, guild_id, **kwargs)
