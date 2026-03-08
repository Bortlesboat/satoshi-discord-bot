"""Utility commands (convert, help)."""

import discord
from discord import app_commands
from discord.ext import commands

from embeds import btc_embed, format_number
from usage_log import get_command_counts, get_commands_since, get_total_commands, get_unique_guilds, get_unique_users


class ToolsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="convert", description="Convert between BTC, sats, and USD")
    @app_commands.describe(
        amount="Amount to convert",
        unit="Unit of the amount",
    )
    @app_commands.choices(unit=[
        app_commands.Choice(name="USD", value="usd"),
        app_commands.Choice(name="BTC", value="btc"),
        app_commands.Choice(name="sats", value="sats"),
    ])
    async def convert(self, interaction: discord.Interaction, amount: float, unit: app_commands.Choice[str]):
        await interaction.response.defer()
        price_data = await self.bot.api.get("/prices")
        usd_val = price_data.get("USD", 0)
        usd_price = usd_val.get("price", 0) if isinstance(usd_val, dict) else usd_val

        if usd_price <= 0:
            from embeds import error_embed
            await interaction.followup.send(embed=error_embed("Price data unavailable."))
            return

        if unit.value == "usd":
            btc = amount / usd_price
            sats = int(btc * 1e8)
            fields = {
                "USD": f"${format_number(amount)}",
                "BTC": f"{btc:.8f}",
                "Sats": format_number(sats),
            }
        elif unit.value == "btc":
            usd = amount * usd_price
            sats = int(amount * 1e8)
            fields = {
                "BTC": f"{amount:.8f}",
                "USD": f"${format_number(usd)}",
                "Sats": format_number(sats),
            }
        else:  # sats
            btc = amount / 1e8
            usd = btc * usd_price
            fields = {
                "Sats": format_number(int(amount)),
                "BTC": f"{btc:.8f}",
                "USD": f"${format_number(usd)}",
            }

        embed = btc_embed(title="Convert", fields=fields)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="help", description="List all Satoshi Bot commands")
    async def help(self, interaction: discord.Interaction):
        embed = btc_embed(
            title="Satoshi Bot Commands",
            description="Bitcoin data at your fingertips.",
        )

        embed.add_field(
            name="Market",
            value="`/price` — BTC price + 24h change\n`/convert` — BTC/USD/sats converter",
            inline=False,
        )
        embed.add_field(
            name="Network",
            value=(
                "`/fees` — Fee estimates\n"
                "`/mempool` — Mempool stats\n"
                "`/supply` — Circulating supply\n"
                "`/network` — Node & connection info"
            ),
            inline=False,
        )
        embed.add_field(
            name="Blocks & Mining",
            value=(
                "`/block [height]` — Block details\n"
                "`/tip` — Latest block\n"
                "`/halving` — Halving countdown\n"
                "`/difficulty` — Difficulty & next adjustment\n"
                "`/hashrate` — Network hashrate"
            ),
            inline=False,
        )
        embed.add_field(
            name="Data",
            value="`/tx <txid>` — Transaction lookup",
            inline=False,
        )
        embed.add_field(
            name="Powered by Satoshi API",
            value=(
                "All data comes from [bitcoinsapi.com](https://bitcoinsapi.com) — "
                "a free Bitcoin REST API with 73+ endpoints. "
                "Developers can build their own tools with the same data."
            ),
            inline=False,
        )
        embed.add_field(
            name="\u200b",
            value=(
                "*Data is provided for informational purposes only. "
                "Not financial advice. Not guaranteed to be accurate or current.*\n\n"
                "[Add Satoshi Bot to your server](https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&scope=bot+applications.commands)"
                " | [Support Server](https://discord.gg/EB6Jd66EsF)"
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="stats", description="Show Satoshi Bot usage statistics")
    async def stats(self, interaction: discord.Interaction):
        total = get_total_commands()
        guilds = get_unique_guilds()
        users = get_unique_users()
        today = get_commands_since(86400)
        week = get_commands_since(604800)
        counts = get_command_counts()

        top_cmds = "\n".join(f"`/{cmd}` — {cnt:,}" for cmd, cnt in list(counts.items())[:5])
        if not top_cmds:
            top_cmds = "No commands logged yet."

        embed = btc_embed(
            title="Satoshi Bot Stats",
            fields={
                "Total Commands": format_number(total),
                "Today / This Week": f"{format_number(today)} / {format_number(week)}",
                "Servers": format_number(len(self.bot.guilds)),
                "Unique Users": format_number(users),
            },
        )
        embed.add_field(name="Top Commands", value=top_cmds, inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ToolsCog(bot))
