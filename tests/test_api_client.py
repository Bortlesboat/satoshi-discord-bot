"""Tests for the Satoshi API client."""

import pytest
import httpx
import respx

from api_client import (
    APIError,
    APIUnavailableError,
    CachedEntry,
    RateLimitError,
    SatoshiClient,
)


@pytest.fixture
def client():
    return SatoshiClient("https://bitcoinsapi.com", api_key="test-key")


@pytest.fixture
def mock_api():
    with respx.mock(base_url="https://bitcoinsapi.com") as m:
        yield m


# --- Happy path tests ---


@pytest.mark.asyncio
async def test_get_prices(client, mock_api):
    mock_api.get("/api/v1/prices").respond(200, json={
        "data": {"USD": {"price": 67000, "change_24h_pct": 2.5}},
        "meta": {"timestamp": "2026-03-07T12:00:00Z"},
    })
    data = await client.get("/prices")
    assert data["USD"]["price"] == 67000
    assert data["USD"]["change_24h_pct"] == 2.5
    await client.close()


@pytest.mark.asyncio
async def test_get_fees(client, mock_api):
    mock_api.get("/api/v1/fees/recommended").respond(200, json={
        "data": {
            "recommendation": "Low fees right now",
            "estimates": [
                {"blocks": 1, "fee_rate": 12, "label": "Fast"},
                {"blocks": 3, "fee_rate": 8, "label": "Medium"},
            ],
        },
    })
    data = await client.get("/fees/recommended")
    assert data["estimates"][0]["fee_rate"] == 12
    await client.close()


@pytest.mark.asyncio
async def test_get_block(client, mock_api):
    mock_api.get("/api/v1/blocks/800000").respond(200, json={
        "data": {"height": 800000, "hash": "abc123", "tx_count": 3200, "size": 1500000},
    })
    data = await client.get("/blocks/800000")
    assert data["height"] == 800000
    assert data["tx_count"] == 3200
    await client.close()


@pytest.mark.asyncio
async def test_get_mempool(client, mock_api):
    mock_api.get("/api/v1/mempool").respond(200, json={
        "data": {"tx_count": 45000, "vsize": 120000000, "total_fee_btc": 1.234},
    })
    data = await client.get("/mempool")
    assert data["tx_count"] == 45000
    await client.close()


@pytest.mark.asyncio
async def test_get_supply(client, mock_api):
    mock_api.get("/api/v1/supply").respond(200, json={
        "data": {
            "circulating_supply": 19600000,
            "max_supply": 21000000,
            "percent_mined": 93.33,
            "blocks_until_halving": 50000,
        },
    })
    data = await client.get("/supply")
    assert data["circulating_supply"] == 19600000
    assert data["blocks_until_halving"] == 50000
    await client.close()


# --- Caching tests ---


@pytest.mark.asyncio
async def test_cache_hit(client, mock_api):
    route = mock_api.get("/api/v1/prices").respond(200, json={
        "data": {"USD": {"price": 67000}},
    })
    await client.get("/prices")
    await client.get("/prices")  # should hit cache
    assert route.call_count == 1
    await client.close()


@pytest.mark.asyncio
async def test_cache_with_params(client, mock_api):
    route = mock_api.get("/api/v1/fees/recommended").respond(200, json={"data": {"fast": 10}})
    await client.get("/fees/recommended")
    await client.get("/fees/recommended")  # cache hit
    assert route.call_count == 1
    await client.close()


# --- Error handling tests ---


@pytest.mark.asyncio
async def test_rate_limit_error(client, mock_api):
    mock_api.get("/api/v1/prices").respond(429, headers={"Retry-After": "30"})
    with pytest.raises(RateLimitError) as exc_info:
        await client.get("/prices")
    assert exc_info.value.retry_after == 30.0
    await client.close()


@pytest.mark.asyncio
async def test_rate_limit_no_retry_after(client, mock_api):
    mock_api.get("/api/v1/prices").respond(429)
    with pytest.raises(RateLimitError) as exc_info:
        await client.get("/prices")
    assert exc_info.value.retry_after is None
    await client.close()


@pytest.mark.asyncio
async def test_server_error(client, mock_api):
    mock_api.get("/api/v1/prices").respond(500)
    with pytest.raises(APIUnavailableError):
        await client.get("/prices")
    await client.close()


@pytest.mark.asyncio
async def test_503_error(client, mock_api):
    mock_api.get("/api/v1/prices").respond(503)
    with pytest.raises(APIUnavailableError):
        await client.get("/prices")
    await client.close()


@pytest.mark.asyncio
async def test_404_error(client, mock_api):
    mock_api.get("/api/v1/blocks/999999999").respond(404, json={"detail": "Block not found"})
    with pytest.raises(APIError) as exc_info:
        await client.get("/blocks/999999999")
    assert exc_info.value.status_code == 404
    await client.close()


@pytest.mark.asyncio
async def test_bad_request(client, mock_api):
    mock_api.get("/api/v1/tx/invalid").respond(
        400, json={"detail": "Invalid txid"}, headers={"content-type": "application/json"}
    )
    with pytest.raises(APIError) as exc_info:
        await client.get("/tx/invalid")
    assert exc_info.value.status_code == 400
    await client.close()


@pytest.mark.asyncio
async def test_timeout_error(client, mock_api):
    mock_api.get("/api/v1/prices").mock(side_effect=httpx.TimeoutException("timeout"))
    with pytest.raises(APIUnavailableError):
        await client.get("/prices")
    await client.close()


@pytest.mark.asyncio
async def test_connection_error(client, mock_api):
    mock_api.get("/api/v1/prices").mock(side_effect=httpx.ConnectError("refused"))
    with pytest.raises(APIUnavailableError):
        await client.get("/prices")
    await client.close()


# --- TTL determination ---


def test_ttl_prices():
    client = SatoshiClient("https://example.com")
    assert client._get_ttl("/prices") == 30


def test_ttl_blocks():
    client = SatoshiClient("https://example.com")
    assert client._get_ttl("/blocks/800000") == 600


def test_ttl_default():
    client = SatoshiClient("https://example.com")
    assert client._get_ttl("/unknown/endpoint") == 60
