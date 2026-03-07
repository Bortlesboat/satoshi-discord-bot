"""Mempool commands."""

import discord
from discord import app_commands
from discord.ext import commands

from embeds import btc_embed, format_bytes, format_number


class MempoolCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mempool", description="Current mempool statistics")
    async def mempool(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/mempool")

        fields = {}

        # tx count: field may be 'tx_count' or 'size'
        tx_count = data.get("tx_count", data.get("size", 0))
        if tx_count:
            fields["Transactions"] = format_number(tx_count)

        if "bytes" in data:
            fields["Size"] = format_bytes(data["bytes"])
        elif "vsize" in data:
            fields["Virtual Size"] = format_bytes(data["vsize"])

        if "total_fee_btc" in data:
            fields["Total Fees"] = f"{data['total_fee_btc']:.4f} BTC"
        elif "total_fee" in data:
            fields["Total Fees"] = f"{data['total_fee']:.8f} BTC"

        if "congestion" in data:
            cong = data["congestion"]
            if isinstance(cong, dict):
                level = cong.get("level", "unknown")
            else:
                level = str(cong)
            emoji = {"low": "\U0001f7e2", "medium": "\U0001f7e1", "high": "\U0001f534"}.get(level.lower(), "\u26aa")
            fields["Congestion"] = f"{emoji} {level.title()}"

        if "next_block_min_fee" in data:
            fields["Next Block Min Fee"] = f"{data['next_block_min_fee']} sat/vB"

        embed = btc_embed(title="Mempool Status", fields=fields)
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(MempoolCog(bot))
