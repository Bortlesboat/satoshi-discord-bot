"""Tests for embed formatting."""

from embeds import (
    BITCOIN_ORANGE,
    FOOTER_TEXT,
    btc_embed,
    error_embed,
    format_btc,
    format_bytes,
    format_hashrate,
    format_number,
)


def test_btc_embed_branding():
    embed = btc_embed(title="Test")
    assert embed.title == "Test"
    assert embed.color.value == BITCOIN_ORANGE
    assert embed.footer.text == FOOTER_TEXT
    assert embed.timestamp is not None


def test_btc_embed_with_fields():
    fields = {"Price": "$67,000", "Change": "+2.5%"}
    embed = btc_embed(title="Price", fields=fields)
    assert len(embed.fields) == 2
    assert embed.fields[0].name == "Price"
    assert embed.fields[0].value == "$67,000"
    assert embed.fields[1].name == "Change"


def test_btc_embed_with_description():
    embed = btc_embed(title="Block", description="Some hash")
    assert embed.description == "Some hash"


def test_btc_embed_no_exceed_discord_limit():
    # Discord limit is 6000 chars total
    big_fields = {f"Field {i}": "x" * 100 for i in range(20)}
    embed = btc_embed(title="Big", fields=big_fields)
    total = len(embed.title or "")
    total += len(embed.description or "")
    for f in embed.fields:
        total += len(f.name) + len(f.value)
    assert total < 6000


def test_error_embed():
    embed = error_embed("Something went wrong")
    assert embed.title == "Error"
    assert embed.description == "Something went wrong"
    assert embed.color.value != BITCOIN_ORANGE  # Should be red


def test_format_btc():
    assert format_btc(100_000_000) == "1.00000000 BTC"
    assert format_btc(50_000) == "0.00050000 BTC"
    assert format_btc(1) == "0.00000001 BTC"


def test_format_number_int():
    assert format_number(1000) == "1,000"
    assert format_number(19_600_000) == "19,600,000"


def test_format_number_float():
    assert format_number(93.33) == "93.33"
    assert format_number(0.5) == "0.50"


def test_format_hashrate():
    assert "EH/s" in format_hashrate(6.5e18)
    assert "PH/s" in format_hashrate(1.2e15)
    assert "TH/s" in format_hashrate(5e12)


def test_format_bytes():
    assert "GB" in format_bytes(1_500_000_000)
    assert "MB" in format_bytes(1_500_000)
    assert "KB" in format_bytes(1_500)
    assert "bytes" in format_bytes(500)
