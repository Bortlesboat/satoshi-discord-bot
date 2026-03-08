# Cross-Promotion Review: Satoshi Discord Bot + Satoshi API Website

**Date:** 2026-03-07
**Reviewers:** Product Manager + Marketing Manager (joint review)
**Verdict:** Yes, cross-promote aggressively. These products have complementary audiences with near-zero overlap today.

---

## 1. Product Perspective: User Journey Mapping

### Who discovers each product today

| Product | Discovery channel | User profile | Intent |
|---------|------------------|-------------|--------|
| **Satoshi API** (bitcoinsapi.com) | Google search, GitHub, Hacker News, dev forums | Developer, builder, researcher | "I need a Bitcoin API for my project" |
| **Satoshi Bot** (Discord) | Bot directories, Reddit, Discord server suggestions | Server admin, community member, Bitcoin enthusiast | "I want Bitcoin data in my Discord" |

These audiences barely overlap today. The developer who finds the API via Google rarely thinks "I wonder if there's a Discord bot." The server admin who adds the bot rarely thinks "I should build something with this API." That is the opportunity.

### Funnel: Bot to API (non-developer becomes developer)

```
Discord user runs /price or /fees
  -> Sees "Powered by Satoshi API | bitcoinsapi.com" in footer
    -> Curiosity: "What is this API?"
      -> Visits bitcoinsapi.com
        -> Sees "From zero to Bitcoin data in 60 seconds" + curl example
          -> Tries it. Gets hooked. Gets API key.
```

**Current state:** The footer link exists but is passive. There is no call to action, no "build your own" nudge, no explanation of what the API offers beyond what the bot shows. The footer says "bitcoinsapi.com" but does not explain WHY a Discord user would care.

**Key insight:** The bot is a live demo of the API. Every `/price` response is proof the API works. But we never say that explicitly.

### Funnel: API to Bot (developer becomes advocate)

```
Developer finds Satoshi API
  -> Uses it in their project
    -> "I wish my Discord community had this data"
      -> Discovers bot exists (WHERE?)
        -> Adds bot to their server
          -> Server members discover bot -> some discover API
```

**Current state:** This funnel is completely broken. The website has zero mention of the Discord bot. The API README has zero mention. A developer who loves the API has no way to discover the bot exists unless they independently search Discord bot directories.

### The flywheel we should build

```
Website visitor -> Adds bot to server -> Bot users see API link
     ^                                         |
     |                                         v
     +---- Developer builds on API <--- Visits website
```

Every bot install seeds the API brand in a new community. Every API user who adds the bot creates a new discovery surface. The bot is the API's distribution layer for non-developers.

---

## 2. Marketing Perspective: Specific Changes

### A. Website (bitcoinsapi.com) -- Currently zero bot presence

**Problem:** The "Use Cases" section lists 6 use cases (Node Operators, Wallet Devs, AI Agents, Data/Analytics, Privacy, Educators) but does not mention Discord communities, the largest non-developer audience for Bitcoin data.

**Changes needed:**

1. **Add a "Discord Communities" use case card** alongside the existing 6. This is the single highest-impact change.

   Suggested copy:
   > **Discord Communities**
   >
   > Add real-time Bitcoin data to any Discord server. Price, fees, mempool, halving countdown -- 14 slash commands powered by the Satoshi API.
   >
   > [Add Satoshi Bot to Discord ->]

2. **Add bot to the bottom CTA section.** Currently it has 3 buttons: "Get Started", "Interactive Docs", "Self-Host (GitHub)". Add a 4th:

   > [Add to Discord](invite link)

   This captures the non-developer visitor who is not ready to write code but wants to USE the data.

3. **Add "Satoshi Bot" to the Roadmap section** under the "Now" items. It validates that the API has real consumers:

   > Done -- Discord Bot
   > 14 slash commands. Live in Discord servers. Powered by the API.

4. **Add bot to the site footer** alongside Status, Privacy, Terms, GitHub links:

   > Discord Bot | Support Server

5. **Update the API README.md** to mention the bot in a "Community" or "Ecosystem" section.

### B. Discord Bot -- Currently minimal API promotion

**Problem:** The footer text ("Powered by Satoshi API | bitcoinsapi.com") is good but passive. It does not explain what the API is or why a user would visit.

**Changes needed:**

1. **Upgrade the `/help` command.** Currently the last field has the invite link and disclaimer. Add an API section:

   Suggested addition:
   > **Build with the API**
   > The data behind this bot comes from the [Satoshi API](https://bitcoinsapi.com) -- a free Bitcoin REST API with 73+ endpoints. Build your own tools, dashboards, or bots.

2. **Add an `/api` or `/about` command** (very low effort). Single embed:

   > **Satoshi API**
   > This bot is powered by the Satoshi API -- a free, open-source REST API that turns a Bitcoin node into 73+ production-ready endpoints.
   >
   > Website: bitcoinsapi.com
   > Docs: bitcoinsapi.com/docs
   > GitHub: github.com/Bortlesboat/bitcoin-api
   > MCP Server: github.com/Bortlesboat/bitcoin-mcp
   >
   > **Satoshi Bot**
   > Add to your server: [Invite Link]
   > Support: discord.gg/EB6Jd66EsF
   > GitHub: github.com/Bortlesboat/satoshi-discord-bot

3. **Enrich the footer on high-engagement commands** (`/price`, `/halving`, `/fees`). These are the most-run commands and the best surfaces for promotion. Consider rotating footer text:

   - Default: `Powered by Satoshi API | bitcoinsapi.com`
   - Occasional: `Build your own tools at bitcoinsapi.com/docs`
   - Occasional: `73+ free Bitcoin API endpoints at bitcoinsapi.com`

   This keeps it fresh without being spammy.

4. **Support server improvements.** The support server (discord.gg/EB6Jd66EsF) should have:
   - A #resources channel with API links, docs link, GitHub links
   - Bot running in the server as a live demo
   - A pinned message in #general explaining the Satoshi ecosystem (API + Bot + MCP)

### C. Bot README (GitHub)

**Current state:** Good. Already links to bitcoinsapi.com and explains the architecture. Minor improvements:

1. Add a "Satoshi Ecosystem" section at the bottom:

   > ## Satoshi Ecosystem
   > | Product | Description | Link |
   > |---------|-------------|------|
   > | Satoshi API | 73+ endpoint Bitcoin REST API | bitcoinsapi.com |
   > | Satoshi Bot | Discord bot (this repo) | Invite link |
   > | Bitcoin MCP | MCP server for AI agents | github.com/Bortlesboat/bitcoin-mcp |

2. Add badges at the top (bot server count, API status, etc.) to build credibility.

### D. Bot Directory Listings

**Current state:** Short/long descriptions reference "Satoshi API (bitcoinsapi.com)" which is good.

**Improvement:** In the long description on top.gg and discordbotlist.com, add:

> Built on the Satoshi API (bitcoinsapi.com) -- a free, open-source Bitcoin REST API with 73+ endpoints. Developers can use the same API to build their own tools.

This turns every directory listing into a two-product advertisement.

---

## 3. Concrete Recommendations (Ranked by Impact/Effort)

| # | Change | Effort | Impact | Why |
|---|--------|--------|--------|-----|
| 1 | **Add "Discord Communities" use case to website** | 15 min | High | The website gets organic search traffic. Every visitor who is not a developer has no call to action today. This catches them. |
| 2 | **Add `/about` or `/api` command to bot** | 20 min | High | Gives every bot user a one-stop overview of the full ecosystem. Currently no way to learn about the API from inside Discord except a tiny footer. |
| 3 | **Add "Add to Discord" button in website bottom CTA** | 5 min | Medium-High | The bottom CTA is the last thing visitors see. A Discord button captures non-dev visitors who would otherwise bounce. |
| 4 | **Add "Build with the API" section to `/help`** | 10 min | Medium | `/help` is one of the first commands new users run. Prime real estate for API awareness. |
| 5 | **Add bot to website footer links** | 5 min | Medium | Low friction, always visible. Normalizes the bot as part of the product suite. |
| 6 | **Add "Satoshi Bot" to website Roadmap section** | 5 min | Medium | Social proof -- shows the API has real consumers. Validates the product. |
| 7 | **Update bot directory long descriptions** | 15 min | Medium | Every directory listing becomes a two-product ad. Free long-tail promotion. |
| 8 | **Add "Satoshi Ecosystem" section to bot README** | 10 min | Low-Medium | Developers who find the bot repo discover the full suite. |
| 9 | **Enrich support server with API resources** | 20 min | Low-Medium | Only matters once there is meaningful support server traffic. |
| 10 | **Rotating footer text on bot embeds** | 30 min | Low | Marginal gains. Current footer is fine. Only do this if other items are done. |

### Quick wins (do today, under 30 min total):

- Items 3, 5, 6: Website changes (15 min combined)
- Item 4: `/help` text update (10 min)

### Next sprint:

- Items 1, 2: Bigger changes but still under an hour each
- Item 7: Directory listing updates (15 min)

### Suggested copy for key touchpoints:

**Website "Discord Communities" use case card:**
```
Discord Communities

Add real-time Bitcoin data to any Discord server with Satoshi Bot.
14 slash commands: price, fees, mempool, halving, blocks, and more.
Free. No setup. Just invite and go.

[Add to Discord ->](invite link)
```

**Website bottom CTA button:**
```
[Add to Discord](invite link)
```
Style: btn-secondary to match the existing "Interactive Docs" and "Self-Host" buttons.

**Bot `/help` addition (new field before the disclaimer):**
```
**Powered by Satoshi API**
All data comes from [bitcoinsapi.com](https://bitcoinsapi.com) -- a free Bitcoin REST API with 73+ endpoints. Developers can build their own tools with the same data.
```

**Bot `/about` command embed:**
```
Title: About Satoshi Bot
Description: Real-time Bitcoin blockchain data, powered by a full node.

Fields:
- Bot: 14 slash commands | [Invite](link) | [GitHub](link)
- API: 73+ endpoints | [Website](bitcoinsapi.com) | [Docs](bitcoinsapi.com/docs)
- MCP: AI agent integration | [GitHub](link)
- Support: [Discord Server](discord.gg/EB6Jd66EsF)
- Contact: api@bitcoinsapi.com
```

---

## 4. What NOT to do

1. **Do not add intrusive "Try our API!" callouts in every bot response.** The current footer is the right level. Users will rebel against ads in a utility bot. Keep it classy -- one line footer, with richer info only in `/help` and `/about`.

2. **Do not gate bot features behind API key signup.** The bot should remain fully free and frictionless. The API upsell should be organic curiosity, not forced.

3. **Do not make the website feel like a Discord bot landing page.** The website's primary audience is developers. The Discord section should be ONE use case card and ONE CTA button, not a takeover.

4. **Do not cross-post bot server counts on the website** unless they are impressive (50+ servers). Showing "In 3 servers" would hurt credibility.

---

## 5. Success Metrics

| Metric | How to measure | Target (90 days) |
|--------|---------------|-------------------|
| Website -> Bot invite clicks | PostHog event on Discord CTA button | 50+ clicks |
| Bot -> Website referral traffic | PostHog referrer = discord (approximate) | 100+ visits |
| `/about` or `/api` command usage | Bot analytics (usage.db) | 5%+ of total commands |
| API key signups mentioning "Discord" | Email field correlation | 10+ signups |
| Directory listings mentioning API drive GitHub stars | GitHub star count | Incremental signal |

---

## Summary

The two products are currently islands. The bot has a passive footer link to the website; the website has zero knowledge that the bot exists. This is leaving growth on the table.

The highest-leverage move is making the website aware of the bot (use case card + CTA button + footer link). This captures non-developer visitors and gives the API social proof of real-world usage.

The second-highest leverage move is making the bot more aware of the API beyond the footer (an `/about` command + richer `/help` text). This creates a natural discovery path for curious users.

Combined, these changes take under 2 hours and create a self-reinforcing flywheel where each product drives traffic to the other.
