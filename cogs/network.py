"""Network and supply commands."""

import discord
from discord import app_commands
from discord.ext import commands

from embeds import btc_embed, format_number


class NetworkCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="supply", description="Bitcoin circulating supply and inflation")
    async def supply(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/supply")

        fields = {}

        circ = data.get("circulating_supply", data.get("circulating_supply_btc", 0))
        if circ:
            fields["Circulating"] = f"{format_number(circ)} BTC"

        max_sup = data.get("max_supply", data.get("total_possible_btc", 0))
        if max_sup:
            fields["Max Supply"] = f"{format_number(max_sup)} BTC"

        if "percent_mined" in data:
            fields["Mined"] = f"{data['percent_mined']:.2f}%"

        if "annual_inflation_rate_pct" in data:
            fields["Annual Inflation"] = f"{data['annual_inflation_rate_pct']:.2f}%"

        if "current_block_subsidy_btc" in data:
            fields["Block Reward"] = f"{data['current_block_subsidy_btc']} BTC"

        embed = btc_embed(title="Bitcoin Supply", fields=fields)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="network", description="Bitcoin network info")
    async def network(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = await self.bot.api.get("/network")

        fields = {}

        if "version" in data:
            fields["Node Version"] = str(data["version"])
        if "subversion" in data:
            fields["User Agent"] = data["subversion"]
        conn_total = data.get("connections", 0)
        conn_in = data.get("connections_in", None)
        conn_out = data.get("connections_out", None)
        if isinstance(conn_total, dict):
            fields["Connections"] = f"{conn_total.get('total', '?')} (in: {conn_total.get('in', '?')}, out: {conn_total.get('out', '?')})"
        elif conn_in is not None and conn_out is not None:
            fields["Connections"] = f"{conn_total} (in: {conn_in}, out: {conn_out})"
        elif conn_total:
            fields["Connections"] = str(conn_total)
        if "protocol_version" in data:
            fields["Protocol"] = str(data["protocol_version"])

        embed = btc_embed(title="Network Info", fields=fields)
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="tx", description="Look up a Bitcoin transaction")
    @app_commands.describe(txid="Transaction ID (64-character hex)")
    async def tx(self, interaction: discord.Interaction, txid: str):
        await interaction.response.defer()

        txid = txid.strip()
        if len(txid) != 64 or not all(c in "0123456789abcdefABCDEF" for c in txid):
            from embeds import error_embed
            await interaction.followup.send(embed=error_embed("Invalid txid. Must be 64 hex characters."), ephemeral=True)
            return

        data = await self.bot.api.get(f"/tx/{txid}")

        fields = {}

        if "confirmations" in data:
            conf = data["confirmations"]
            if conf == 0:
                fields["Status"] = "\U0001f7e1 Unconfirmed"
            elif conf < 6:
                fields["Status"] = f"\U0001f7e0 {conf} confirmations"
            else:
                fields["Status"] = f"\U0001f7e2 {format_number(conf)} confirmations"

        if "fee_rate" in data:
            fields["Fee Rate"] = f"{data['fee_rate']} sat/vB"
        if "fee" in data:
            fields["Fee"] = f"{data['fee']} sats"

        if "input_count" in data:
            fields["Inputs"] = str(data["input_count"])
        if "output_count" in data:
            fields["Outputs"] = str(data["output_count"])

        if "vsize" in data:
            fields["vSize"] = f"{format_number(data['vsize'])} vB"

        flags = []
        if data.get("is_segwit"):
            flags.append("SegWit")
        if data.get("is_taproot"):
            flags.append("Taproot")
        if data.get("has_inscription"):
            flags.append("Inscription")
        if flags:
            fields["Flags"] = " | ".join(flags)

        embed = btc_embed(
            title="Transaction",
            description=f"`{txid[:16]}...{txid[-8:]}`",
            fields=fields,
        )
        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(NetworkCog(bot))
