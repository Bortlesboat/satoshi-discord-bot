"""Price commands."""

import discord
from discord import app_commands
from discord.ext import commands

from embeds import btc_embed, format_number


class PriceCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="price", description="Current Bitcoin price and 24h change")
    async def price(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/prices")

        # API returns currencies as plain numbers or nested dicts
        def get_price(key):
            val = data.get(key)
            if isinstance(val, dict):
                return val.get("price", 0)
            return val or 0

        usd_price = get_price("USD")
        change_24h = data.get("change_24h_pct", 0)
        if isinstance(data.get("USD"), dict):
            change_24h = data["USD"].get("change_24h_pct", change_24h)
        arrow = "\u2191" if change_24h >= 0 else "\u2193"

        fields = {"USD": f"${format_number(usd_price)}"}

        for currency in ["EUR", "GBP", "CAD", "AUD"]:
            p = get_price(currency)
            if p:
                fields[currency] = f"{format_number(p)}"

        fields["24h Change"] = f"{arrow} {change_24h:+.2f}%"

        embed = btc_embed(title="Bitcoin Price", fields=fields)
        embed.set_footer(text="Powered by Satoshi API | Not financial advice | bitcoinsapi.com")
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(PriceCog(bot))
