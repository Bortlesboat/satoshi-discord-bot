# Satoshi Bot

A Discord bot that brings real-time Bitcoin blockchain data to your server. Powered by the [Satoshi API](https://bitcoinsapi.com).

## Commands

| Command | Description |
|---------|-------------|
| `/price` | Current BTC price and 24h change |
| `/convert <amount> <unit>` | Convert between BTC, sats, and USD |
| `/fees` | Fee estimates (fast/medium/slow) |
| `/mempool` | Mempool statistics and congestion level |
| `/block [height]` | Look up a block by height (default: latest) |
| `/tip` | Current chain tip |
| `/halving` | Next halving countdown |
| `/difficulty` | Current difficulty and next adjustment estimate |
| `/hashrate` | Network hashrate |
| `/supply` | Circulating supply and inflation rate |
| `/network` | Node version and connection info |
| `/tx <txid>` | Transaction details and confirmation status |
| `/help` | List all commands |

## Add to Your Server

[Invite Satoshi Bot](https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&scope=bot+applications.commands)

## Self-Hosting

1. Clone this repo
2. Create a Discord application at [discord.com/developers](https://discord.com/developers/applications)
3. Copy `.env.example` to `.env` and fill in your bot token
4. Install dependencies and run:

```bash
pip install -r requirements.txt
python bot.py
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | Yes | Discord bot token |
| `API_URL` | No | Satoshi API URL (default: https://bitcoinsapi.com) |
| `API_KEY` | No | Satoshi API key for higher rate limits |

## Architecture

```
Discord User --> Slash Command --> Satoshi Bot (discord.py)
                                        |
                                  Satoshi API (bitcoinsapi.com)
                                        |
                                  Bot formats response --> Discord Embed
```

The bot is a thin client. All data comes from the [Satoshi API](https://bitcoinsapi.com), a self-hostable Bitcoin REST API with 77+ endpoints.

## Tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Disclaimer

Data is provided for informational purposes only. Not financial advice. Not guaranteed to be accurate or current.

## License

MIT
