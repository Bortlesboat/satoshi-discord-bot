"""Discord embed factory with Satoshi API branding."""

from datetime import datetime, timezone

import discord

BITCOIN_ORANGE = 0xF7931A
FOOTER_TEXT = "Powered by Satoshi API | bitcoinsapi.com"
LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Bitcoin.svg/240px-Bitcoin.svg.png"


def btc_embed(
    title: str,
    description: str | None = None,
    fields: dict[str, str] | None = None,
    inline: bool = True,
) -> discord.Embed:
    """Create a branded Bitcoin embed.

    Args:
        title: Embed title.
        description: Optional description text.
        fields: Dict of field name -> value to add.
        inline: Whether fields are inline (default True).
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=BITCOIN_ORANGE,
        timestamp=datetime.now(timezone.utc),
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=LOGO_URL)

    if fields:
        for name, value in fields.items():
            embed.add_field(name=name, value=str(value), inline=inline)

    return embed


def error_embed(message: str) -> discord.Embed:
    """Create an error embed."""
    return discord.Embed(
        title="Error",
        description=message,
        color=discord.Color.red(),
        timestamp=datetime.now(timezone.utc),
    ).set_footer(text=FOOTER_TEXT)


def format_btc(sats: float | int) -> str:
    """Format a satoshi amount as BTC."""
    return f"{sats / 1e8:.8f} BTC"


def format_number(n: int | float) -> str:
    """Format a number with commas."""
    if isinstance(n, float):
        return f"{n:,.2f}"
    return f"{n:,}"


def format_hashrate(h: float) -> str:
    """Format hashrate in human-readable units."""
    if h >= 1e18:
        return f"{h / 1e18:.2f} EH/s"
    if h >= 1e15:
        return f"{h / 1e15:.2f} PH/s"
    if h >= 1e12:
        return f"{h / 1e12:.2f} TH/s"
    return f"{h:.2f} H/s"


def format_bytes(b: int) -> str:
    """Format bytes in human-readable units."""
    if b >= 1e9:
        return f"{b / 1e9:.2f} GB"
    if b >= 1e6:
        return f"{b / 1e6:.2f} MB"
    if b >= 1e3:
        return f"{b / 1e3:.2f} KB"
    return f"{b} bytes"
