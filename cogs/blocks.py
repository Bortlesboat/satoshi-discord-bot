"""Block commands."""

import discord
from discord import app_commands
from discord.ext import commands

from embeds import btc_embed, format_bytes, format_number


class BlocksCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="block", description="Look up a Bitcoin block by height")
    @app_commands.describe(height="Block height (omit for latest)")
    async def block(self, interaction: discord.Interaction, height: int | None = None):
        await interaction.response.defer()

        if height is not None:
            data = await self.bot.api.get(f"/blocks/{height}")
        else:
            data = await self.bot.api.get("/blocks/latest")

        block_height = data.get("height", height or "?")
        fields = {
            "Height": format_number(block_height),
            "Transactions": format_number(data.get("tx_count", data.get("nTx", 0))),
            "Size": format_bytes(data.get("size", 0)),
            "Weight": format_number(data.get("weight", 0)),
        }
        if "timestamp" in data:
            fields["Time"] = f"<t:{data['timestamp']}:R>"
        if "fee_stats" in data:
            fs = data["fee_stats"]
            if "median_fee_rate" in fs:
                fields["Median Fee"] = f"{fs['median_fee_rate']} sat/vB"
        elif "median_fee_rate" in data:
            fields["Median Fee"] = f"{data['median_fee_rate']} sat/vB"

        embed = btc_embed(
            title=f"Block {format_number(block_height)}",
            fields=fields,
        )
        if "hash" in data:
            embed.description = f"`{data['hash']}`"

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="tip", description="Current chain tip (latest block height and hash)")
    async def tip(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/blocks/latest")

        fields = {
            "Height": format_number(data.get("height", 0)),
        }
        if "hash" in data:
            fields["Hash"] = f"`{data['hash'][:16]}...`"
        if "timestamp" in data:
            fields["Time"] = f"<t:{data['timestamp']}:R>"
        if "tx_count" in data or "nTx" in data:
            fields["Transactions"] = format_number(data.get("tx_count", data.get("nTx", 0)))

        embed = btc_embed(title="Chain Tip", fields=fields)
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(BlocksCog(bot))
