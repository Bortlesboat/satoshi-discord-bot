"""Satoshi Discord Bot — Bitcoin data at your fingertips."""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from api_client import APIError, APIUnavailableError, RateLimitError, SatoshiClient
from config import API_KEY, API_URL, BOT_TOKEN
from embeds import error_embed
from usage_log import log_command, log_error, log_guild_event

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("satoshi-bot")

COGS = [
    "cogs.price",
    "cogs.fees",
    "cogs.blocks",
    "cogs.mempool",
    "cogs.mining",
    "cogs.network",
    "cogs.tools",
]


class SatoshiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        self.api = SatoshiClient(API_URL, API_KEY)

    async def setup_hook(self):
        for cog in COGS:
            await self.load_extension(cog)
            log.info("Loaded cog: %s", cog)
        await self.tree.sync()
        log.info("Slash commands synced")

    async def close(self):
        await self.api.close()
        await super().close()

    async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command):
        guild_id = interaction.guild_id
        user_id = interaction.user.id
        log_command(command.name, guild_id, user_id)

    async def on_ready(self):
        log.info("Logged in as %s (ID: %s)", self.user, self.user.id)
        log.info("In %d guilds", len(self.guilds))
        n = len(self.guilds)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"Bitcoin in {n} server{'s' if n != 1 else ''}",
            )
        )

    async def on_guild_join(self, guild: discord.Guild):
        log.info("Joined guild: %s (ID: %s, members: %d)", guild.name, guild.id, guild.member_count or 0)
        log_guild_event(guild.id, guild.name, guild.member_count or 0, "join")
        n = len(self.guilds)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"Bitcoin in {n} server{'s' if n != 1 else ''}",
            )
        )

    async def on_guild_remove(self, guild: discord.Guild):
        log.info("Left guild: %s (ID: %s)", guild.name, guild.id)
        log_guild_event(guild.id, guild.name, guild.member_count or 0, "leave")
        n = len(self.guilds)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"Bitcoin in {n} server{'s' if n != 1 else ''}",
            )
        )


bot = SatoshiBot()


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Global error handler for all slash commands."""
    original = getattr(error, "original", error)
    cmd_name = interaction.command.name if interaction.command else "unknown"

    if isinstance(original, RateLimitError):
        msg = f"Rate limited. Try again in {original.retry_after:.0f}s." if original.retry_after else "Rate limited. Please wait a moment."
        log_error(cmd_name, interaction.guild_id, "rate_limit", msg)
    elif isinstance(original, APIUnavailableError):
        msg = "Satoshi API is temporarily unavailable. Try again shortly."
        log_error(cmd_name, interaction.guild_id, "api_unavailable", msg)
    elif isinstance(original, APIError):
        msg = str(original)
        log_error(cmd_name, interaction.guild_id, "api_error", msg)
    else:
        log.exception("Unhandled error in %s", cmd_name, exc_info=original)
        msg = "An unexpected error occurred."
        log_error(cmd_name, interaction.guild_id, "unhandled", str(original))

    embed = error_embed(msg)
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
