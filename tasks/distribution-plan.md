# Satoshi Bot Distribution Plan: 100 Servers in 90 Days

**Bot Invite Link:** https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&integration_type=0&scope=bot+applications.commands
**GitHub:** https://github.com/Bortlesboat/satoshi-discord-bot
**Powered by:** Satoshi API (bitcoinsapi.com)

---

## 1. Bot Directory Submissions (Day 1-3)

Submit to ALL of these. Each takes 10-30 minutes. Do them all in one sitting.

### Tier 1 (High Traffic -- Submit Day 1)

| Directory | URL | Monthly Visits | Notes |
|-----------|-----|---------------|-------|
| **top.gg** | https://top.gg/bot/new | ~18.6M | Largest directory. 1-2 week review. Bot MUST be online during review. |
| **discordbotlist.com** | https://discordbotlist.com/ | ~2.1M | Second largest. Has API for posting stats. |
| **discord.bots.gg** | https://discord.bots.gg/ | ~1M+ | Clean, developer-focused. Fast approval. |
| **discords.com** | https://discords.com/bots/ | ~500K | Combined bot + server directory. |

### Tier 2 (Medium Traffic -- Submit Day 2)

| Directory | URL | Notes |
|-----------|-----|-------|
| **botlist.me** | https://botlist.me/ | Good secondary listing. |
| **discordlist.gg** | https://discordlist.gg/ | Combined directory. |
| **discordextremelist.xyz** | https://discordextremelist.xyz/ | Smaller but active community. |
| **disforge.com** | https://disforge.com/bots | Has bot and server listings. |
| **bots.ondiscord.xyz** | https://bots.ondiscord.xyz/ | Supports BotBlock API. |
| **voidbots.net** | https://voidbots.net/ | Smaller, less competitive = easier visibility. |

### Tier 3 (Long Tail -- Submit Day 3)

| Directory | URL |
|-----------|-----|
| **yabl.xyz** | https://yabl.xyz/ |
| **radarcord.net** | https://radarcord.net/ |
| **omniplex.gg** | https://omniplex.gg/ |
| **disq.ink** | https://disq.ink/ |
| **vcodes.xyz** | https://vcodes.xyz |
| **cybralist.com** | https://cybralist.com/ |
| **discordservices.net** | https://discordservices.net/ |

### What You Need for Every Listing

Prepare these assets ONCE, reuse everywhere:

**Short Description (one line):**
> Real-time Bitcoin blockchain data -- price, fees, mempool, blocks, halving countdown, and more. Powered by a full Bitcoin node.

**Long Description (use for all listings):**
> Satoshi Bot brings live Bitcoin blockchain data directly to your Discord server. No account needed, no ads, completely free.
>
> 13 slash commands: /price (BTC price + 24h change), /convert (BTC/sats/USD converter), /fees (fee estimates by priority), /mempool (congestion + pending txs), /block (look up any block), /tip (chain tip), /halving (next halving countdown), /difficulty (difficulty + next adjustment), /hashrate (network hashrate), /supply (circulating supply + inflation rate), /network (node version + connections), /tx (transaction lookup), /help.
>
> Unlike gambling bots and tipping bots that use the word "crypto," Satoshi Bot is a pure data tool. Every response comes from a real Bitcoin full node via the Satoshi API (bitcoinsapi.com). No wallets, no tokens, no shilling -- just verified blockchain data formatted in clean embeds.
>
> Built for: Bitcoin communities, trading servers, node operators, educators, and anyone who wants instant Bitcoin data without leaving Discord.

**Tags/Categories (use on every platform):**
- bitcoin
- cryptocurrency
- crypto
- blockchain
- finance
- utility
- tools
- information
- price
- trading

**Required Assets:**
- Bot avatar: Bitcoin logo (already using Wikipedia Bitcoin SVG)
- Banner image: Create a 960x540 banner showing 2-3 embed screenshots side by side with the text "Satoshi Bot -- Bitcoin Data for Discord"
- Invite URL: `https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&integration_type=0&scope=bot+applications.commands`
- Support server: Create a small Discord server for bot support (top.gg requires this)
- Website: Link to bitcoinsapi.com or GitHub repo
- Prefix: `/` (slash commands)

### Post-Listing: Stat Posting

Integrate BotBlock API or individual directory APIs to auto-post server count. This keeps listings fresh and improves ranking.

```python
# Add to bot.py -- post guild count to top.gg every 30 minutes
# pip install topggpy
import topgg

# In SatoshiBot.__init__:
self.topgg_client = topgg.DBLClient(self, "YOUR_TOP_GG_TOKEN")
```

---

## 2. Target Discord Servers (Week 1-2)

### Tier 1: Large Bitcoin/Crypto Communities (10K+ members)

| # | Server Name | Est. Members | How to Get Bot Added | Why It Fits |
|---|-------------|-------------|---------------------|-------------|
| 1 | **r/CryptoCurrency Discord** | 76,000+ | Post in #suggestions or #bots channel. Mod team is accessible. | Largest crypto Discord, data-hungry traders. |
| 2 | **Bitcoin Community (discord.me/bitcoin)** | 50,000+ | DM mods or post in suggestions. Self-described "most active crypto Discord." | Bitcoin-focused, needs data tools. |
| 3 | **Cryptohub** | 54,000+ | Has bot channels. Post suggestion with screenshots. | Beginner-friendly, already has ChatGPT bot -- data bot complements. |
| 4 | **WallStreetBets Crypto** | 167,000+ | Post in suggestions. Large mod team. | Massive, price-obsessed audience. |
| 5 | **Axion Crypto Community** | 82,000+ | Contact mods via DM or suggestion channel. | Trading-focused, needs real-time data. |
| 6 | **Crypto Banter Hub** | 30,000+ | Suggestion channel or mod DM. | Active trading community tied to YouTube channel. |
| 7 | **TradingView Discord** | 20,000+ | Formal suggestion process. | Chart-focused traders who want on-chain data too. |

### Tier 2: Bitcoin-Specific Communities (1K-10K members)

| # | Server Name | Est. Members | How to Get Bot Added | Why It Fits |
|---|-------------|-------------|---------------------|-------------|
| 8 | **Bitcoin (Disboard tagged)** | 5,000-10,000 | Multiple Bitcoin servers on Disboard. Join top 5, post in suggestions. | Pure Bitcoin audience. |
| 9 | **Bitpam CryptoCurrency & Bitcoin** | 5,000+ | Suggestion channel. | Mixed BTC/crypto, educational. |
| 10 | **The Crypto Network** | 5,000+ | Mod contact. | General crypto with BTC focus. |
| 11 | **AltCryptoTalk** | 9,000+ | Suggestion/bot channel. | Traders who compare alts to BTC. |
| 12 | **Elite Crypto Signals** | 5,000+ | Contact admin. Trading signal servers love data bots. | Signal providers need real-time BTC data. |

### Tier 3: Node Operator / Developer Communities

| # | Server Name | Est. Members | How to Get Bot Added | Why It Fits |
|---|-------------|-------------|---------------------|-------------|
| 13 | **Core Lightning (Blockstream)** | 2,000+ | discord.gg/w27fMFESMN -- Dev community, DM maintainers. | Node operators, technical audience. Perfect for /difficulty /hashrate /mempool. |
| 14 | **Bitcoin Dev / Bitcoin Core** | 1,000-3,000 | Technical communities on Discord/Matrix. Find via bitcoin.org community links. | Developers who want quick chain state checks. |
| 15 | **Start9 (Embassy)** | 5,000+ | Node-in-a-box community. Suggestion channel. | Self-sovereign node runners. |
| 16 | **Umbrel** | 10,000+ | Node OS community. Active Discord. | Home node runners who want quick data. |
| 17 | **RaspiBlitz** | 2,000+ | DIY node community. | Technical, Bitcoin-only. |
| 18 | **Mempool.space** | 3,000+ | Community around the mempool explorer. | Users already care about fees/mempool data. |

### Tier 4: Bitcoin Education & Culture

| # | Server Name | Est. Members | How to Get Bot Added | Why It Fits |
|---|-------------|-------------|---------------------|-------------|
| 19 | **Jacob's Crypto Clan** | 23,000+ | Large YouTube-tied community. Post in suggestions. | Educational, new users love /halving and /supply. |
| 20 | **Bitcoin Magazine** | 5,000+ | Media community. Contact via Twitter DM or server suggestions. | News-focused, wants live data. |
| 21 | **Swan Bitcoin** | 3,000+ | DCA/stacking community. Suggestion channel. | Stackers who track price and supply. |
| 22 | **River Financial** | 2,000+ | Bitcoin-only exchange community. | Bitcoin-only audience. |
| 23 | **Unchained Capital** | 2,000+ | Multisig/custody community. | Security-minded Bitcoiners. |
| 24 | **Pleb Lab / Bitcoin Park** | 1,000+ | Austin Bitcoin community. DM organizers. | Builder community, appreciates open-source tools. |
| 25 | **Bitcoin Optech** | 1,000+ | Technical newsletter community. | Deep technical audience. |

### Discovery Method for Finding More Servers

1. Search **Disboard** (disboard.org/servers/tag/bitcoin) -- sort by member count, join top 20
2. Search **top.gg** (top.gg/discord/servers/tag/bitcoin) -- same approach
3. Search **Discord.me** (discord.me/servers/tag/bitcoin) -- different server pool
4. Search Discord's own Server Discovery for "bitcoin" -- largest verified servers
5. Check Twitter/X bios of Bitcoin influencers for Discord links

---

## 3. Outreach Templates

### Template A: Cold DM to Server Admin (Data-Focused)

> Hey [name] -- I built a free Discord bot called Satoshi Bot that pulls real-time Bitcoin data from a full node. Slash commands for price, fees, mempool stats, halving countdown, block lookup, etc.
>
> Thought [server name] might find it useful since your community is always discussing [price action / on-chain data / Bitcoin fundamentals].
>
> It's open source, lightweight (only needs Send Messages permission), and doesn't collect any user data. No ads, no tokens, no wallets -- just blockchain data.
>
> Here's the invite if you'd like to try it: https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&integration_type=0&scope=bot+applications.commands
>
> Happy to answer any questions. No pressure either way.

### Template B: Suggestion Channel Post (Community-Focused)

> **Bot Suggestion: Satoshi Bot -- Bitcoin Blockchain Data**
>
> Found this free, open-source bot that gives instant Bitcoin data via slash commands. Some commands that might be useful here:
>
> - `/price` -- BTC price + 24h change (great for quick checks without leaving Discord)
> - `/fees` -- Fee estimates so you know when to send transactions
> - `/mempool` -- See how congested the network is right now
> - `/halving` -- Countdown to the next halving
> - `/convert 100000 sats` -- Quick sats-to-USD conversion
>
> It pulls everything from a real Bitcoin full node, not just CoinGecko. Lightweight, only needs Send Messages permission.
>
> Invite: https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&integration_type=0&scope=bot+applications.commands
> GitHub: https://github.com/Bortlesboat/satoshi-discord-bot

### Template C: Technical Communities (Developer-Focused)

> Hey all -- I open-sourced a Discord bot that exposes Bitcoin node data through slash commands. Built on top of the Satoshi API (73+ endpoints wrapping Bitcoin Core RPC).
>
> Commands: /price, /fees, /mempool, /block [height], /tx [txid], /difficulty, /hashrate, /supply, /network, /halving, /convert, /tip
>
> Architecture: discord.py thin client -> Satoshi API (bitcoinsapi.com) -> Bitcoin Core full node. MIT licensed, self-hostable.
>
> If anyone wants to add it to the server: https://discord.com/oauth2/authorize?client_id=1479972638918049895&permissions=2048&integration_type=0&scope=bot+applications.commands
>
> GitHub: https://github.com/Bortlesboat/satoshi-discord-bot
>
> Feedback welcome -- especially if there are commands you'd want to see added.

---

## 4. Content Strategy

### Reddit Posts (Week 1-2)

| Subreddit | Post Type | Title | Timing |
|-----------|-----------|-------|--------|
| r/Bitcoin (5M+) | Show & Tell | "I built a free Discord bot that pulls live data from a Bitcoin full node -- 13 slash commands" | Week 1 |
| r/CryptoCurrency (9M+) | Project Share | "Open-source Discord bot for real-time Bitcoin data -- no tokens, no wallets, just blockchain data" | Week 1 |
| r/discordapp (1.5M+) | Bot Showcase | "Built a Bitcoin data bot with 13 slash commands -- free & open source" | Week 2 |
| r/selfhosted (500K+) | Self-Hosted Tool | "Self-hostable Bitcoin Discord bot backed by a full node API" | Week 2 |
| r/BitcoinBeginners (600K+) | Educational | "I made a free Discord bot that explains Bitcoin data in plain English -- halving countdown, supply stats, fee estimates" | Week 2 |
| r/node (small) | Tool Share | "Discord bot for node operators -- mempool, difficulty, hashrate, block lookup from your server" | Week 3 |
| r/lightningnetwork | Tool Share | "Free Discord bot for Bitcoin network stats -- useful for LN node operators" | Week 3 |

**Reddit Post Template (r/Bitcoin):**

> **Title:** I built a free Discord bot that pulls live data from a Bitcoin full node -- 13 slash commands
>
> Been working on a Bitcoin data API (Satoshi API) and just shipped a Discord bot on top of it. Figured the community might find it useful.
>
> What it does:
> - `/price` -- BTC price + 24h change
> - `/fees` -- Fee estimates (fast/medium/slow) -- know when to send
> - `/mempool` -- How congested is the network right now
> - `/halving` -- Next halving countdown
> - `/supply` -- Circulating supply + inflation rate
> - `/difficulty` -- Current difficulty + next adjustment estimate
> - `/convert 1000000 sats` -- Sats to USD instantly
> - `/block`, `/tx`, `/hashrate`, `/network`, `/tip`
>
> Everything comes from a real Bitcoin full node, not just price APIs. MIT licensed, open source.
>
> [Screenshot of /price and /halving embeds]
>
> GitHub: https://github.com/Bortlesboat/satoshi-discord-bot
> Add to your server: [invite link]
>
> Feedback welcome. What commands would you want to see added?

### Twitter/X Posts (Ongoing)

**Launch tweet:**
> Shipped Satoshi Bot -- a free Discord bot that brings real-time Bitcoin data to your server.
>
> 13 slash commands. Full node data. No tokens, no wallets, no ads.
>
> /price /fees /mempool /halving /supply /difficulty /hashrate /convert /block /tx /network /tip /help
>
> Add it free: [invite link]
> [Screenshot collage]

**Recurring content ideas (1-2x per week):**
- Screenshot of /halving with "X blocks until the next halving" when count hits milestones
- Screenshot of /fees during fee spikes: "Fees are spiking -- Satoshi Bot shows it live in Discord"
- Screenshot of /mempool during congestion events
- Screenshot of /difficulty before/after difficulty adjustments
- "Did you know?" threads about Bitcoin data the bot surfaces
- Tag Bitcoin influencers when the bot shows interesting data

**Hashtags:** #Bitcoin #BTC #Discord #OpenSource #BitcoinDev #BuildOnBitcoin

### Nostr Posts

Post the same content on Nostr using a client like Damus or Amethyst. Bitcoin maximalists are heavily on Nostr. Tag relevant npubs. Use the `t` tag for `bitcoin`, `discord`, `opensource`.

### Screenshot Strategy -- Best Commands for Screenshots

| Priority | Command | Why It Screenshots Well |
|----------|---------|----------------------|
| 1 | `/price` | Clean embed, everyone wants price, orange Bitcoin branding, 24h change is instantly relatable |
| 2 | `/halving` | Countdown creates urgency/interest, unique data point, conversation starter |
| 3 | `/fees` | Three-tier layout (fast/medium/slow) looks professional, immediately useful |
| 4 | `/convert 1000000 sats` | Visual "aha moment" -- people love seeing sats in USD |
| 5 | `/mempool` | Congestion gauge is visually interesting, shows technical depth |
| 6 | `/supply` | Inflation rate + % mined is a talking point |

**Screenshot Tips:**
- Use Discord dark mode (most users prefer it, screenshots look better)
- Show the slash command autocomplete dropdown in some screenshots (shows ease of use)
- Capture during interesting market conditions (fee spikes, price moves, near difficulty adjustment)
- Create a 2x2 or 3x1 grid collage for directory banners and social posts

### Viral Mechanics

Add to the bot's responses to encourage sharing:
- The "Powered by Satoshi API | bitcoinsapi.com" footer is already there (good)
- Consider adding a "Watching Bitcoin in X servers" presence status (already implemented)
- During notable events (halving milestones, ATH, fee spikes), the embed could include a subtle "Add Satoshi Bot to your server" link -- but keep it non-intrusive

---

## 5. Week-by-Week Timeline

### Week 1: Foundation (Day 1-7)

| Day | Action | Target |
|-----|--------|--------|
| Day 1 | Submit to top.gg, discordbotlist.com, discord.bots.gg, discords.com | 4 directory listings |
| Day 1 | Create bot support Discord server (required by top.gg) | 1 server |
| Day 1 | Take 6 high-quality screenshots (dark mode, interesting data) | Marketing assets |
| Day 1 | Create 960x540 banner image for directory listings | Marketing asset |
| Day 2 | Submit to Tier 2 directories (botlist.me, discordlist.gg, discordextremelist.xyz, disforge.com, bots.ondiscord.xyz, voidbots.net) | 6 more listings |
| Day 3 | Submit to Tier 3 directories (yabl.xyz, radarcord.net, omniplex.gg, disq.ink, vcodes.xyz, cybralist.com, discordservices.net) | 7 more listings |
| Day 3 | Post on r/Bitcoin and r/CryptoCurrency | 2 Reddit posts |
| Day 4 | Join 10 target Discord servers from Tier 1-2 list. Observe for 1-2 days before posting. | 10 servers joined |
| Day 5 | Post in suggestion channels of first 5 servers (Template B) | 5 outreach attempts |
| Day 6 | DM admins of 5 more servers (Template A) | 5 DM outreach attempts |
| Day 7 | Launch tweet on X. Post on Nostr. | Social presence |

**Week 1 Target: 5-10 servers + 17 directory listings pending**

### Week 2: First Wave Outreach (Day 8-14)

| Day | Action | Target |
|-----|--------|--------|
| Day 8-9 | Join 10 more target servers (Tier 2-3). Lurk, be helpful, understand culture. | 10 more servers joined |
| Day 10 | Post in suggestion channels of next 10 servers | 10 outreach attempts |
| Day 11 | Post on r/discordapp and r/selfhosted | 2 Reddit posts |
| Day 12 | DM admins of node operator communities (Start9, Umbrel, RaspiBlitz) using Template C | 3 technical outreach |
| Day 13 | Post on r/BitcoinBeginners | 1 Reddit post |
| Day 14 | Follow up on any directory listings that haven't been approved. Resubmit if needed. | Directory maintenance |

**Week 2 Target: 15-25 total servers**

### Week 3-4: Expand & Iterate (Day 15-28)

| Action | Details |
|--------|---------|
| Search Disboard for ALL "bitcoin" tagged servers | Join and pitch to every server with 500+ members |
| Search top.gg server directory for "crypto" and "trading" | Same approach |
| Post screenshot content on X 2x/week | /halving countdown, /fees during spikes |
| Respond to any Reddit comments/feedback | Community engagement |
| Check directory listings -- optimize descriptions based on what's converting | A/B test short descriptions |
| DM Bitcoin YouTubers/influencers who have Discord servers | Jacob Crypto Bury, Crypto Banter, etc. |
| Post on r/lightningnetwork and r/node | 2 more Reddit posts |
| Cross-post GitHub repo to Hacker News (Show HN) if momentum is building | High-leverage if it hits front page |

**Week 3-4 Target: 30-50 total servers**

### Month 2 (Day 29-60): Organic Growth + Feature-Driven Marketing

| Action | Details |
|--------|---------|
| Monitor which commands are most used -- double down on marketing those | Data-driven content |
| Add 2-3 new commands based on user feedback (Lightning stats? Address lookup?) | Feature-driven re-marketing |
| Post "update" threads on Reddit when new features ship | Re-engagement |
| Reach out to Bitcoin podcasters about the API + bot | Broader awareness |
| Submit to "awesome" lists on GitHub (awesome-bitcoin, awesome-discord-bots) | Long-tail discovery |
| Pitch to Bitcoin newsletter authors (Bitcoin Optech, Bitcoin Magazine) | Media coverage |
| Create a /stats command showing bot usage across servers | Social proof in the bot itself |
| Optimize top.gg listing based on analytics (views, invites, votes) | Conversion optimization |

**Month 2 Target: 50-75 total servers**

### Month 3 (Day 61-90): Scale & Sustain

| Action | Details |
|--------|---------|
| Run a "vote for Satoshi Bot" campaign on top.gg (incentivize with... nothing, it's free -- just ask) | Ranking boost |
| Partner with 2-3 Bitcoin education communities for "official bot" status | Sticky installs |
| If at 50+ servers, pitch to Discord's App Directory for featured placement | Major visibility |
| Write a blog post on bitcoinsapi.com: "How Satoshi Bot Processes X Commands Per Day" | Content marketing |
| Explore Telegram bot version to capture that market too | Platform expansion |
| Pitch "Bitcoin tools" roundup articles to crypto media | PR |

**Month 3 Target: 75-100+ total servers**

---

## 6. Competitive Edge Messaging

### Competitive Landscape

The "crypto" bot space on Discord is dominated by three types:
1. **Gambling/Casino bots** (24/7 Casino, Better Blackjack, Rocket Gambling) -- 80% of "crypto" tagged bots
2. **Tipping bots** (TIPBOT, Flippy, CryptoJar) -- send tokens between users
3. **Price alert bots** (CoinTrendz, CryptoBot) -- price-only, multi-coin, no on-chain data

**Satoshi Bot occupies a completely empty niche: pure Bitcoin blockchain data from a full node.**

No existing bot offers mempool stats, fee estimates, difficulty adjustments, halving countdown, block lookup, and transaction lookup together. The competitors that come closest (CoinTrendz, CryptoBot) only do price/charts and support thousands of coins without depth on any of them.

### Positioning Statement

> Satoshi Bot is the only Discord bot that gives you real Bitcoin blockchain data from a full node. Not a price ticker. Not a gambling bot. Not a tipping bot. Actual on-chain data -- fees, mempool, difficulty, supply, blocks -- formatted in clean embeds, delivered instantly via slash commands.

### One-Liner Pitches by Audience

**For server admins:**
> "Free Bitcoin data bot -- 13 commands, zero configuration, one permission needed. Your members get instant price, fees, mempool, and halving data without leaving Discord."

**For Bitcoin enthusiasts:**
> "Full node data in your Discord. Check fees before sending, watch the mempool, count down to the halving, look up any block or transaction -- all with slash commands."

**For traders:**
> "Real-time BTC price, fee estimates, and mempool congestion in one bot. Know the best time to move coins without leaving your trading server."

**For node operators:**
> "An open-source Discord bot backed by a real Bitcoin node. Hashrate, difficulty adjustments, network stats, block data -- the same RPC data you check on your node, but in Discord."

**For developers:**
> "MIT-licensed Discord bot built on the Satoshi API (73+ Bitcoin endpoints). Self-hostable, well-tested, clean architecture. Fork it, extend it, or just add it to your server."

### Key Differentiators (Use in All Marketing)

1. **Full node data, not just price** -- mempool, fees, difficulty, blocks, transactions
2. **Bitcoin-only** -- not diluted across 10,000 altcoins
3. **No wallets, no tokens, no gambling** -- pure data utility
4. **Open source** -- MIT licensed, self-hostable, auditable
5. **Lightweight** -- only needs Send Messages permission (2048)
6. **Clean embeds** -- Bitcoin orange branding, timestamp, source attribution
7. **Free forever** -- no premium tier, no paywalls on commands
8. **Backed by the Satoshi API** -- 73+ endpoints, production-grade

---

## Tracking & Metrics

### KPIs to Track Weekly

| Metric | Tool | Target (90 days) |
|--------|------|-----------------|
| Server count | Bot status / top.gg dashboard | 100+ |
| Directory listing views | top.gg analytics, discordbotlist analytics | 5,000+ |
| Directory votes | top.gg voting | 50+ |
| Reddit post upvotes | Reddit | 100+ combined |
| GitHub stars | GitHub | 25+ |
| Unique users (commands run) | Add logging to bot | 500+ |
| Most popular command | Command logging | Track for content strategy |

### Weekly Check-In Template

```
Week X Report:
- Servers: [count] (delta: +X)
- Top directories: [which are driving invites]
- Outreach sent: [count]
- Outreach converted: [count]
- Most used command this week: [command]
- Content posted: [list]
- Next week priority: [action]
```

---

## Quick-Start Checklist (Do These TODAY)

- [ ] Take 6 screenshots of best commands (dark mode Discord)
- [ ] Create banner image (960x540)
- [ ] Create bot support Discord server
- [ ] Submit to top.gg (https://top.gg/bot/new)
- [ ] Submit to discordbotlist.com
- [ ] Submit to discord.bots.gg
- [ ] Submit to discords.com
- [ ] Write and schedule r/Bitcoin post
- [ ] Write and schedule launch tweet
- [ ] Join first 5 target servers and observe culture
