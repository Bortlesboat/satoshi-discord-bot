"""Mining, halving, and difficulty commands."""

import discord
from discord import app_commands
from discord.ext import commands

from embeds import btc_embed, format_hashrate, format_number


class MiningCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="halving", description="Next Bitcoin halving countdown")
    async def halving(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/supply")

        fields = {}

        blocks_until = data.get("blocks_until_halving", data.get("blocks_until_next_halving", None))
        if blocks_until is not None:
            fields["Blocks Until Halving"] = format_number(blocks_until)
            # Rough estimate: 10 min/block
            days = blocks_until * 10 / 60 / 24
            if days > 365:
                fields["Estimated Time"] = f"~{days / 365:.1f} years"
            elif days > 30:
                fields["Estimated Time"] = f"~{days / 30:.1f} months"
            else:
                fields["Estimated Time"] = f"~{days:.0f} days"

        next_height = data.get("next_halving_height", None)
        if next_height:
            fields["Next Halving Height"] = format_number(next_height)

        halvings = data.get("halvings_completed", None)
        if halvings is not None:
            fields["Halvings Completed"] = str(halvings)

        subsidy = data.get("current_block_subsidy_btc", data.get("current_block_subsidy", None))
        if subsidy is not None:
            fields["Current Block Reward"] = f"{subsidy} BTC"

        embed = btc_embed(title="Bitcoin Halving Countdown", fields=fields)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="difficulty", description="Current mining difficulty and next adjustment")
    async def difficulty(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/network/difficulty")

        fields = {}

        if "difficulty" in data:
            diff = data["difficulty"]
            if diff >= 1e12:
                fields["Difficulty"] = f"{diff:.2e}"
            else:
                fields["Difficulty"] = format_number(diff)

        progress = data.get("progress_pct", data.get("progress_percent", None))
        if progress is not None:
            fields["Epoch Progress"] = f"{progress:.1f}%"

        adj_val = data.get("estimated_adjustment_pct", data.get("estimated_adjustment_percent", None))
        if adj_val is not None:
            adj = adj_val
            arrow = "\u2191" if adj >= 0 else "\u2193"
            fields["Est. Adjustment"] = f"{arrow} {adj:+.2f}%"

        if "estimated_retarget_date" in data:
            fields["Next Retarget"] = data["estimated_retarget_date"]
        elif "blocks_remaining" in data:
            fields["Blocks Until Retarget"] = format_number(data["blocks_remaining"])
        elif "blocks_until_retarget" in data:
            fields["Blocks Until Retarget"] = format_number(data["blocks_until_retarget"])

        embed = btc_embed(title="Mining Difficulty", fields=fields)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="hashrate", description="Current network hashrate")
    async def hashrate(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/mining")

        fields = {}

        hashrate = data.get("hashrate", data.get("networkhashps", None))
        if hashrate is not None:
            fields["Hashrate"] = format_hashrate(hashrate)
        elif "hashrate_eh" in data:
            fields["Hashrate"] = f"{data['hashrate_eh']:.2f} EH/s"

        if "difficulty" in data:
            fields["Difficulty"] = f"{data['difficulty']:.2e}"

        embed = btc_embed(title="Network Hashrate", fields=fields)
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(MiningCog(bot))
