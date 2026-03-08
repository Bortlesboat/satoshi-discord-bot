# Social Media Posts — Ready to Post

## Reddit: r/Bitcoin

**Title:** I built a free Discord bot that pulls live data from a Bitcoin full node -- 13 slash commands

**Body:**

Been working on a Bitcoin data API (Satoshi API) and just shipped a Discord bot on top of it. Figured the community might find it useful.

What it does:
- `/price` -- BTC price + 24h change
- `/fees` -- Fee estimates (fast/medium/slow) -- know when to send
- `/mempool` -- How congested is the network right now
- `/halving` -- Next halving countdown
- `/supply` -- Circulating supply + inflation rate
- `/difficulty` -- Current difficulty + next adjustment estimate
- `/convert 1000000 sats` -- Sats to USD instantly
- `/block`, `/tx`, `/hashrate`, `/network`, `/tip`

Everything comes from a real Bitcoin full node, not just price APIs. MIT licensed, open source.

GitHub: https://github.com/Bortlesboat/satoshi-discord-bot
Add to your server: https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&scope=bot+applications.commands

Feedback welcome. What commands would you want to see added?

---

## Reddit: r/CryptoCurrency

**Title:** Open-source Discord bot for real-time Bitcoin data -- no tokens, no wallets, just blockchain data

**Body:**

Built a free Discord bot backed by a Bitcoin full node API. 13 slash commands covering price, fees, mempool, halving countdown, supply stats, difficulty, hashrate, block/tx lookup, and more.

Unlike the crypto gambling and tipping bots that dominate Discord, this is a pure data tool. No wallets, no tokens, no ads. Just verified blockchain data in clean embeds.

Open source, self-hostable, MIT licensed.

GitHub: https://github.com/Bortlesboat/satoshi-discord-bot
Add free: https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&scope=bot+applications.commands

---

## Reddit: r/discordapp

**Title:** Built a Bitcoin data bot with 13 slash commands -- free & open source

**Body:**

Made a Discord bot that brings real-time Bitcoin blockchain data to any server via slash commands. Price, fees, mempool stats, halving countdown, block lookup, transaction lookup, and more.

Only needs Send Messages permission (2048). Lightweight, no bloat.

GitHub: https://github.com/Bortlesboat/satoshi-discord-bot
Invite: https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&scope=bot+applications.commands

---

## Twitter/X Launch Tweet

Shipped Satoshi Bot -- a free Discord bot that brings real-time Bitcoin data to your server.

13 slash commands. Full node data. No tokens, no wallets, no ads.

/price /fees /mempool /halving /supply /difficulty /hashrate /convert /block /tx /network /tip /help

Add it free: https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&scope=bot+applications.commands

GitHub: https://github.com/Bortlesboat/satoshi-discord-bot

#Bitcoin #Discord #OpenSource

[Attach banner.png from assets/]

---

## Reddit: r/selfhosted

**Title:** Self-hostable Bitcoin Discord bot backed by a full node API

**Body:**

Open sourced a Discord bot that exposes Bitcoin node data through slash commands. Backed by the Satoshi API (77+ endpoints wrapping Bitcoin Core RPC).

Architecture: discord.py thin client -> Satoshi API -> Bitcoin Core full node

Self-host both the bot and the API, or just add the hosted bot to your server.

Commands: /price, /fees, /mempool, /block, /tx, /difficulty, /hashrate, /supply, /network, /halving, /convert, /tip, /help

MIT licensed. Python. Clean codebase.

GitHub: https://github.com/Bortlesboat/satoshi-discord-bot
API: https://bitcoinsapi.com
