"""Fee estimation commands."""

import discord
from discord import app_commands
from discord.ext import commands

from embeds import btc_embed


class FeesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="fees", description="Current Bitcoin fee estimates")
    async def fees(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/fees/recommended")

        fields = {}
        if "recommendation" in data:
            fields["Recommendation"] = data["recommendation"]
        if "estimates" in data:
            estimates = data["estimates"]
            if isinstance(estimates, dict):
                # API returns {"1": 2.257, "3": 1.082, ...}
                labels = {"1": "Fast (1 block)", "3": "Medium (3 blocks)", "6": "Slow (6 blocks)"}
                for target, rate in estimates.items():
                    label = labels.get(str(target), f"{target} blocks")
                    fields[label] = f"{rate} sat/vB"
            elif isinstance(estimates, list):
                for est in estimates:
                    target = est.get("blocks", "?")
                    rate = est.get("fee_rate", 0)
                    label = est.get("label", f"{target} blocks")
                    fields[label] = f"{rate} sat/vB"

        embed = btc_embed(title="Fee Estimates", fields=fields, inline=True)
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(FeesCog(bot))
