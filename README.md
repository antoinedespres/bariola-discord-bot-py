# Bariola

Bariola is a small, funny Discord bot with a cat personality, built with [discord.py](https://github.com/Rapptz/discord.py). She answers questions, hands out compliments (and the occasional insult), shares cat facts, helps moderate a server, and replies in whichever language a server picks — English, French, or Korean.

Commands work both as classic prefix commands (`$ping`) and as native Discord slash commands (`/ping`) — use `/` in Discord to see the full up-to-date list with descriptions.

## Features

- **Personality**: `meow`, `question`, `feed`, `cute`, `notcute`, `fact`, `cuddle`, `randint`, `discord`
- **Utility**: `ping`, `vc`, `avatar`, `about`
- **Moderation** (admin-only): `warning` (auto-kicks after 3), `kick`, `ban`, `clear`, `say`
- **Per-server language**: `/language set <en|fr|ko>` (admin-only) — Bariola replies in that language on that server from then on
- Welcomes/says goodbye to members joining/leaving, in a rotating "status", and persists warnings and language settings across restarts via SQLite

## Local development

1. Create a Discord Application and Bot at the [Discord Developer Portal](https://discord.com/developers/applications). Copy the bot token, and invite the bot to a private test server with the `bot` and `applications.commands` OAuth2 scopes (the latter is required for slash commands).
2. Copy `.env.example` to `.env` and fill in `DISCORD_BOT_TOKEN`. Optionally set `DEV_GUILD_ID` to your test server's ID for fast slash-command sync during development.
3. `pip install -r requirements.txt`
4. `python bot.py`
5. In your test server, run the owner-only `sync` command (prefix-only, e.g. `$sync`) to push slash commands to your dev guild instantly. Use `$sync global` only when you want to ship the current command set to every server the bot is in (global syncs can take up to an hour to propagate).

## Deploying to a VPS

Bariola ships as a Docker image built and deployed automatically by GitHub Actions.

**One-time VPS setup:**
1. `mkdir -p ~/apps/bariola-discord-bot-py` on the VPS.
2. Copy `docker-compose.yml` into that directory.
3. `cp .env.example .env` in that directory and fill in `DISCORD_BOT_TOKEN`.
4. `docker login ghcr.io` once, using a GitHub personal access token with `read:packages`.
5. `docker compose pull && docker compose up -d`.

From then on, every push to `main` automatically bumps the version, builds and pushes a new image, and redeploys it on the VPS — no manual steps needed. Bariola's warning counts and per-server language settings live in a named Docker volume (`bariola-data`), so they survive every redeploy.

**Required GitHub repository secrets** (`Settings → Secrets and variables → Actions`):
- `VPS_HOST`, `VPS_SSH_PORT`, `VPS_SSH_USER`, `VPS_SSH_KEY` — a dedicated SSH deploy key for the VPS.

Also make sure `Settings → Actions → General → Workflow permissions` is set to "Read and write permissions", so the release workflow can push its version-bump commit/tag and publish to GHCR.

To view logs on the VPS: `docker compose -f ~/apps/bariola-discord-bot-py/docker-compose.yml logs -f`.

## Credits

Created by [Antoine Després](https://github.com/antoinedespres).
