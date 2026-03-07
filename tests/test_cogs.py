"""Tests for cog command logic.

These test that given mocked API responses, each command produces
the correct embed with expected fields.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest

from embeds import BITCOIN_ORANGE


def make_interaction():
    """Create a mock Discord interaction."""
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()
    interaction.response.defer = AsyncMock()
    interaction.response.is_done.return_value = False
    interaction.followup = AsyncMock()
    interaction.followup.send = AsyncMock()
    return interaction


def make_bot(api_response):
    """Create a mock bot with a mocked API client."""
    bot = MagicMock()
    bot.api = AsyncMock()
    bot.api.get = AsyncMock(return_value=api_response)
    return bot


def get_sent_embed(interaction) -> discord.Embed:
    """Extract the embed sent via followup.send."""
    call_args = interaction.followup.send.call_args
    return call_args.kwargs.get("embed", call_args.args[0] if call_args.args else None)


# --- Price cog ---


@pytest.mark.asyncio
async def test_price_command():
    from cogs.price import PriceCog

    bot = make_bot({"USD": {"price": 67000, "change_24h_pct": 2.5}, "EUR": {"price": 62000}})
    cog = PriceCog(bot)
    interaction = make_interaction()

    await cog.price.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    assert embed.title == "Bitcoin Price"
    assert embed.color.value == BITCOIN_ORANGE
    field_names = [f.name for f in embed.fields]
    assert "USD" in field_names
    assert "24h Change" in field_names


@pytest.mark.asyncio
async def test_price_negative_change():
    from cogs.price import PriceCog

    bot = make_bot({"USD": {"price": 65000, "change_24h_pct": -3.2}})
    cog = PriceCog(bot)
    interaction = make_interaction()

    await cog.price.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    change_field = next(f for f in embed.fields if f.name == "24h Change")
    assert "\u2193" in change_field.value  # down arrow


# --- Fees cog ---


@pytest.mark.asyncio
async def test_fees_command():
    from cogs.fees import FeesCog

    bot = make_bot({
        "recommendation": "Low fees",
        "estimates": [
            {"blocks": 1, "fee_rate": 12, "label": "Fast"},
            {"blocks": 3, "fee_rate": 8, "label": "Medium"},
            {"blocks": 6, "fee_rate": 4, "label": "Slow"},
        ],
    })
    cog = FeesCog(bot)
    interaction = make_interaction()

    await cog.fees.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    assert embed.title == "Fee Estimates"
    field_names = [f.name for f in embed.fields]
    assert "Fast" in field_names


# --- Blocks cog ---


@pytest.mark.asyncio
async def test_block_command_with_height():
    from cogs.blocks import BlocksCog

    bot = make_bot({
        "height": 800000,
        "hash": "00000000000000000002a7c4c1e48d76c5a37902165a270156b7a8d72f8804bf",
        "tx_count": 3200,
        "size": 1500000,
        "weight": 3990000,
        "timestamp": 1690000000,
    })
    cog = BlocksCog(bot)
    interaction = make_interaction()

    await cog.block.callback(cog, interaction, height=800000)

    embed = get_sent_embed(interaction)
    assert "800,000" in embed.title
    bot.api.get.assert_called_once_with("/blocks/800000")


@pytest.mark.asyncio
async def test_block_command_latest():
    from cogs.blocks import BlocksCog

    bot = make_bot({"height": 881000, "hash": "abc", "tx_count": 2500, "size": 1200000, "weight": 3500000})
    cog = BlocksCog(bot)
    interaction = make_interaction()

    await cog.block.callback(cog, interaction, height=None)

    bot.api.get.assert_called_once_with("/blocks/latest")


@pytest.mark.asyncio
async def test_tip_command():
    from cogs.blocks import BlocksCog

    bot = make_bot({"height": 881000, "hash": "abc123def456", "timestamp": 1690000000, "tx_count": 2500})
    cog = BlocksCog(bot)
    interaction = make_interaction()

    await cog.tip.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    assert embed.title == "Chain Tip"


# --- Mempool cog ---


@pytest.mark.asyncio
async def test_mempool_command():
    from cogs.mempool import MempoolCog

    bot = make_bot({
        "tx_count": 45000,
        "vsize": 120000000,
        "total_fee_btc": 1.234,
        "congestion": {"level": "medium"},
    })
    cog = MempoolCog(bot)
    interaction = make_interaction()

    await cog.mempool.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    assert embed.title == "Mempool Status"
    field_names = [f.name for f in embed.fields]
    assert "Transactions" in field_names
    assert "Congestion" in field_names


# --- Mining cog ---


@pytest.mark.asyncio
async def test_halving_command():
    from cogs.mining import MiningCog

    bot = make_bot({
        "blocks_until_halving": 50000,
        "next_halving_height": 1050000,
        "halvings_completed": 4,
        "current_block_subsidy_btc": 3.125,
    })
    cog = MiningCog(bot)
    interaction = make_interaction()

    await cog.halving.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    assert embed.title == "Bitcoin Halving Countdown"
    field_names = [f.name for f in embed.fields]
    assert "Blocks Until Halving" in field_names


@pytest.mark.asyncio
async def test_difficulty_command():
    from cogs.mining import MiningCog

    bot = make_bot({
        "difficulty": 8.5e13,
        "progress_pct": 45.2,
        "estimated_adjustment_pct": 3.5,
        "blocks_until_retarget": 1100,
    })
    cog = MiningCog(bot)
    interaction = make_interaction()

    await cog.difficulty.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    assert embed.title == "Mining Difficulty"


# --- Network cog ---


@pytest.mark.asyncio
async def test_supply_command():
    from cogs.network import NetworkCog

    bot = make_bot({
        "circulating_supply": 19600000,
        "max_supply": 21000000,
        "percent_mined": 93.33,
        "annual_inflation_rate_pct": 1.7,
        "current_block_subsidy_btc": 3.125,
    })
    cog = NetworkCog(bot)
    interaction = make_interaction()

    await cog.supply.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    assert embed.title == "Bitcoin Supply"
    field_names = [f.name for f in embed.fields]
    assert "Circulating" in field_names
    assert "Max Supply" in field_names


@pytest.mark.asyncio
async def test_network_command():
    from cogs.network import NetworkCog

    bot = make_bot({
        "version": 270000,
        "subversion": "/Satoshi:27.0.0/",
        "connections": {"total": 125, "in": 100, "out": 25},
        "protocol_version": 70016,
    })
    cog = NetworkCog(bot)
    interaction = make_interaction()

    await cog.network.callback(cog, interaction)

    embed = get_sent_embed(interaction)
    assert embed.title == "Network Info"


@pytest.mark.asyncio
async def test_tx_command():
    from cogs.network import NetworkCog

    txid = "a" * 64
    bot = make_bot({
        "confirmations": 150,
        "fee_rate": 12.5,
        "fee": 2250,
        "input_count": 2,
        "output_count": 3,
        "vsize": 180,
        "is_segwit": True,
        "is_taproot": False,
    })
    cog = NetworkCog(bot)
    interaction = make_interaction()

    await cog.tx.callback(cog, interaction, txid=txid)

    embed = get_sent_embed(interaction)
    assert embed.title == "Transaction"
    field_names = [f.name for f in embed.fields]
    assert "Status" in field_names
    assert "Fee Rate" in field_names


@pytest.mark.asyncio
async def test_tx_invalid_txid():
    from cogs.network import NetworkCog

    bot = make_bot({})
    cog = NetworkCog(bot)
    interaction = make_interaction()

    await cog.tx.callback(cog, interaction, txid="not-a-valid-txid")

    embed = get_sent_embed(interaction)
    assert embed.title == "Error"
    # API should NOT have been called
    bot.api.get.assert_not_called()


@pytest.mark.asyncio
async def test_tx_unconfirmed():
    from cogs.network import NetworkCog

    txid = "b" * 64
    bot = make_bot({"confirmations": 0, "fee_rate": 25, "fee": 5000, "input_count": 1, "output_count": 2, "vsize": 200})
    cog = NetworkCog(bot)
    interaction = make_interaction()

    await cog.tx.callback(cog, interaction, txid=txid)

    embed = get_sent_embed(interaction)
    status_field = next(f for f in embed.fields if f.name == "Status")
    assert "Unconfirmed" in status_field.value
