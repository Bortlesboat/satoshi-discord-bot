"""Utility commands (convert, help)."""

import discord
from discord import app_commands
from discord.ext import commands

from embeds import btc_embed, format_number


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
        embed.set_footer(text="Price via CoinGecko | Not financial advice | bitcoinsapi.com")
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
            name="\u200b",
            value=(
                "*Data is provided for informational purposes only. "
                "Not financial advice. Not guaranteed to be accurate or current.*\n\n"
                "[Add Satoshi Bot to your server](https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&scope=bot+applications.commands)"
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ToolsCog(bot))
